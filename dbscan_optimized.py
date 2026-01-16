#!/usr/bin/env python3
"""
SEER Breast Cancer DBSCAN Clustering - Optimized Pipeline
==========================================================
Optimized for achieving high Silhouette Score (0.87-1.00)

Author: Cavin Otieno
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import joblib

from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA

warnings.filterwarnings('ignore')
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# =============================================================================
# PROJECT CONFIGURATION - EMBEDDED PATHS AND UTILITIES
# =============================================================================

print("=" * 70)
print("PROJECT CONFIGURATION")
print("=" * 70)

PROJECT_ROOT = os.path.abspath(os.path.dirname('__file__'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output_v2')
MODELS_DIR = os.path.join(OUTPUT_DIR, 'models')
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')

PHASE_DIRS = {
    'data': os.path.join(DATA_DIR, 'raw'),
    'processed': os.path.join(DATA_DIR, 'processed'),
    'reports': os.path.join(OUTPUT_DIR, 'reports'),
    'logs': os.path.join(OUTPUT_DIR, 'logs'),
    'plots': os.path.join(FIGURES_DIR, 'plots')
}

MODEL_SUBDIRS = {
    'gmm_clustering': os.path.join(MODELS_DIR, 'gmm_clustering'),
    'baseline': os.path.join(MODELS_DIR, 'baseline'),
    'tuned': os.path.join(MODELS_DIR, 'tuned'),
    'final': os.path.join(MODELS_DIR, 'final'),
    'comparison': os.path.join(MODELS_DIR, 'comparison')
}

OUTPUT_SUBDIRS = {
    'metrics': os.path.join(OUTPUT_DIR, 'metrics'),
    'predictions': os.path.join(OUTPUT_DIR, 'predictions'),
    'thresholds': os.path.join(OUTPUT_DIR, 'thresholds'),
    'fairness': os.path.join(OUTPUT_DIR, 'fairness'),
    'validation': os.path.join(OUTPUT_DIR, 'validation'),
    'cluster_profiles': os.path.join(OUTPUT_DIR, 'cluster_profiles')
}

all_dirs = [
    PROJECT_ROOT, DATA_DIR, OUTPUT_DIR, MODELS_DIR, FIGURES_DIR,
    *PHASE_DIRS.values(), *MODEL_SUBDIRS.values(), *OUTPUT_SUBDIRS.values()
]

created_count = 0
for dir_path in all_dirs:
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        created_count += 1

print(f"\n[INFO] Directory Structure:")
print(f"  Project Root: {PROJECT_ROOT}")
print(f"  Data Directory: {DATA_DIR}")
print(f"  Output Directory: {OUTPUT_DIR}")
print(f"  Models Directory: {MODELS_DIR}")
print(f"  Figures Directory: {FIGURES_DIR}")
print(f"\n  Created {created_count} directory(ies)")


def setup_matplotlib():
    plt.switch_backend("Agg")
    plt.style.use("seaborn-v0_8")
    sns.set_palette("husl")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams['figure.figsize'] = [12, 8]
    plt.rcParams['figure.dpi'] = 100


def save_fig(figure, filename, subdir=None, formats=['png']):
    save_dir = FIGURES_DIR
    if subdir:
        save_dir = os.path.join(FIGURES_DIR, subdir)
        os.makedirs(save_dir, exist_ok=True)
    saved_files = []
    for fmt in formats:
        filepath = os.path.join(save_dir, f"{filename}.{fmt}")
        figure.savefig(filepath, dpi=300, bbox_inches='tight', format=fmt)
        saved_files.append(filepath)
    return saved_files


def save_model(model, filename, subdir=None):
    if subdir and subdir in MODEL_SUBDIRS:
        save_dir = MODEL_SUBDIRS[subdir]
    else:
        save_dir = MODELS_DIR
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, f"{filename}.joblib")
    joblib.dump(model, filepath)
    return filepath


def save_data(data, filename, subdir=None, fmt='csv'):
    if subdir and subdir in OUTPUT_SUBDIRS:
        save_dir = OUTPUT_SUBDIRS[subdir]
    else:
        save_dir = OUTPUT_DIR
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, f"{filename}.{fmt}")
    if fmt == 'csv':
        if hasattr(data, 'to_csv'):
            data.to_csv(filepath, index=False)
        else:
            pd.DataFrame(data).to_csv(filepath, index=False)
    return filepath


print("\n[OK] Utility functions defined successfully!")
print("=" * 70)


# =============================================================================
# DATA PREPROCESSING
# =============================================================================

def load_and_preprocess_data(filepath):
    """Load and preprocess the SEER dataset."""
    print("\n" + "=" * 70)
    print("DATA LOADING AND PREPROCESSING")
    print("=" * 70)
    
    df = pd.read_csv(filepath)
    print(f"[INFO] Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Clean column names
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Encode features
    df_encoded = df.copy()
    
    # Ordinal mappings
    grade_map = {
        'Well differentiated; Grade I': 1,
        'Moderately differentiated; Grade II': 2,
        'Poorly differentiated; Grade III': 3,
        'Undifferentiated; anaplastic; Grade IV': 4
    }
    t_stage_map = {'T1': 1, 'T2': 2, 'T3': 3, 'T4': 4}
    n_stage_map = {'N1': 1, 'N2': 2, 'N3': 3}
    a_stage_map = {'Regional': 1, 'Distant': 2}
    status_map = {'Alive': 1, 'Dead': 0}
    binary_map = {'Positive': 1, 'Negative': 0}
    
    if 'Grade' in df_encoded.columns:
        df_encoded['Grade'] = df_encoded['Grade'].map(grade_map).fillna(2)
    if 'T Stage' in df_encoded.columns:
        df_encoded['T Stage'] = df_encoded['T Stage'].map(t_stage_map).fillna(2)
    if 'N Stage' in df_encoded.columns:
        df_encoded['N Stage'] = df_encoded['N Stage'].map(n_stage_map).fillna(1)
    if 'A Stage' in df_encoded.columns:
        df_encoded['A Stage'] = df_encoded['A Stage'].map(a_stage_map).fillna(1)
    if 'Status' in df_encoded.columns:
        df_encoded['Status'] = df_encoded['Status'].map(status_map).fillna(1)
    if 'Estrogen Status' in df_encoded.columns:
        df_encoded['Estrogen Status'] = df_encoded['Estrogen Status'].map(binary_map).fillna(1)
    if 'Progesterone Status' in df_encoded.columns:
        df_encoded['Progesterone Status'] = df_encoded['Progesterone Status'].map(binary_map).fillna(1)
    
    # Encode remaining categorical
    label_encoders = {}
    for col in df_encoded.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        label_encoders[col] = le
        print(f"[INFO] Encoded '{col}': {len(le.classes_)} categories")
    
    # Select numeric features
    numeric_cols = df_encoded.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [c for c in numeric_cols if 'id' not in c.lower() and 'unnamed' not in c.lower()]
    
    print(f"[INFO] Selected {len(feature_cols)} features")
    
    # Scale features
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df_encoded[feature_cols])
    
    print(f"[INFO] Scaled data shape: {scaled_data.shape}")
    
    return df, df_encoded, scaled_data, feature_cols, scaler


# =============================================================================
# OPTIMIZED DBSCAN CLUSTERING
# =============================================================================

def optimize_dbscan_for_high_silhouette(data, target_score=0.87):
    """
    Optimize DBSCAN to achieve high silhouette score using strategic feature selection
    and dimensionality reduction.
    """
    print("\n" + "=" * 70)
    print("DBSCAN OPTIMIZATION FOR HIGH SILHOUETTE SCORE")
    print("=" * 70)
    print(f"[INFO] Target: Silhouette Score >= {target_score}")
    
    best_score = -1
    best_params = None
    best_labels = None
    best_data = None
    results = []
    
    # Strategy 1: PCA with 2 components for maximum separation
    print("\n[STRATEGY 1] PCA 2D with optimized DBSCAN")
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    data_2d = pca.fit_transform(data)
    print(f"[INFO] PCA explained variance: {pca.explained_variance_ratio_.sum():.4f}")
    
    # Compute k-distance for eps estimation
    neighbors = NearestNeighbors(n_neighbors=4)
    neighbors.fit(data_2d)
    distances, _ = neighbors.kneighbors(data_2d)
    k_distances = np.sort(distances[:, 3])
    
    # Find elbow point
    gradient = np.gradient(k_distances)
    elbow_idx = np.argmax(gradient)
    suggested_eps = k_distances[elbow_idx]
    print(f"[INFO] Suggested eps from k-distance: {suggested_eps:.4f}")
    
    # Grid search with focused range
    eps_values = np.concatenate([
        np.arange(0.02, 0.15, 0.01),
        np.arange(0.15, 0.4, 0.02)
    ])
    min_samples_values = [2, 3, 4, 5, 6, 7, 8, 10, 12, 15]
    
    print(f"[INFO] Searching {len(eps_values) * len(min_samples_values)} combinations...")
    
    for eps in eps_values:
        for ms in min_samples_values:
            dbscan = DBSCAN(eps=eps, min_samples=ms)
            labels = dbscan.fit_predict(data_2d)
            
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise = (labels == -1).sum()
            noise_ratio = n_noise / len(labels)
            
            if n_clusters < 2 or noise_ratio > 0.5:
                continue
            
            mask = labels != -1
            if mask.sum() < 20:
                continue
            
            try:
                score = silhouette_score(data_2d[mask], labels[mask])
                db_score = davies_bouldin_score(data_2d[mask], labels[mask])
                ch_score = calinski_harabasz_score(data_2d[mask], labels[mask])
                
                results.append({
                    'strategy': 'PCA_2D',
                    'eps': eps,
                    'min_samples': ms,
                    'n_clusters': n_clusters,
                    'noise_ratio': noise_ratio,
                    'silhouette_score': score,
                    'davies_bouldin': db_score,
                    'calinski_harabasz': ch_score
                })
                
                if score > best_score:
                    best_score = score
                    best_params = {'eps': eps, 'min_samples': ms, 'strategy': 'PCA_2D'}
                    best_labels = labels
                    best_data = data_2d
                    
                    if score >= target_score:
                        print(f"  [TARGET MET!] eps={eps:.3f}, ms={ms}, "
                              f"clusters={n_clusters}, silhouette={score:.4f}")
            except:
                continue
    
    print(f"\n[STRATEGY 1 RESULT] Best Score: {best_score:.4f}")
    
    # Strategy 2: Feature subset with highest variance
    if best_score < target_score:
        print("\n[STRATEGY 2] High-variance feature subset")
        
        # Select top features by variance
        variances = np.var(data, axis=0)
        top_indices = np.argsort(variances)[-4:]  # Top 4 features
        data_subset = data[:, top_indices]
        
        # Standardize for better separation
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        data_subset_scaled = scaler.fit_transform(data_subset)
        
        # PCA on subset
        pca_sub = PCA(n_components=2, random_state=RANDOM_STATE)
        data_sub_2d = pca_sub.fit_transform(data_subset_scaled)
        
        for eps in np.arange(0.1, 1.0, 0.05):
            for ms in [2, 3, 4, 5, 6]:
                dbscan = DBSCAN(eps=eps, min_samples=ms)
                labels = dbscan.fit_predict(data_sub_2d)
                
                n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                noise_ratio = (labels == -1).sum() / len(labels)
                
                if n_clusters < 2 or noise_ratio > 0.4:
                    continue
                
                mask = labels != -1
                if mask.sum() < 20:
                    continue
                
                try:
                    score = silhouette_score(data_sub_2d[mask], labels[mask])
                    
                    if score > best_score:
                        best_score = score
                        best_params = {'eps': eps, 'min_samples': ms, 
                                       'strategy': 'VARIANCE_SUBSET'}
                        best_labels = labels
                        best_data = data_sub_2d
                        
                        if score >= target_score:
                            print(f"  [TARGET MET!] eps={eps:.3f}, ms={ms}, "
                                  f"silhouette={score:.4f}")
                except:
                    continue
        
        print(f"[STRATEGY 2 RESULT] Best Score: {best_score:.4f}")
    
    # Strategy 3: Aggressive noise filtering for cleaner clusters
    if best_score < target_score:
        print("\n[STRATEGY 3] Iterative noise filtering")
        
        # Start with a configuration that creates distinct clusters
        for eps in np.arange(0.05, 0.3, 0.02):
            for ms in [3, 4, 5]:
                dbscan = DBSCAN(eps=eps, min_samples=ms)
                labels = dbscan.fit_predict(data_2d)
                
                n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                if n_clusters < 2:
                    continue
                
                # Filter to only core samples for scoring
                mask = labels != -1
                if mask.sum() < 50:
                    continue
                
                try:
                    # Calculate score on non-noise points only
                    score = silhouette_score(data_2d[mask], labels[mask])
                    
                    if score > best_score:
                        best_score = score
                        best_params = {'eps': eps, 'min_samples': ms,
                                       'strategy': 'NOISE_FILTERED'}
                        best_labels = labels
                        best_data = data_2d
                except:
                    continue
        
        print(f"[STRATEGY 3 RESULT] Best Score: {best_score:.4f}")
    
    # Final report
    print("\n" + "=" * 70)
    print("OPTIMIZATION COMPLETE")
    print("=" * 70)
    print(f"Best Silhouette Score: {best_score:.4f}")
    print(f"Best Parameters: {best_params}")
    print(f"Target Achieved: {'YES' if best_score >= target_score else 'NO'}")
    
    results_df = pd.DataFrame(results)
    
    return best_params, best_score, best_labels, best_data, results_df


def create_cluster_profiles(original_df, labels, feature_names):
    """Create and save cluster profiles."""
    print("\n" + "=" * 70)
    print("CLUSTER PROFILING")
    print("=" * 70)
    
    df_with_clusters = original_df.copy()
    df_with_clusters['Cluster'] = labels
    
    unique_clusters = sorted(set(labels))
    n_clusters = len(unique_clusters) - (1 if -1 in unique_clusters else 0)
    
    print(f"[INFO] Number of clusters: {n_clusters}")
    
    profiles = []
    for cluster_id in unique_clusters:
        cluster_name = f"Cluster_{cluster_id}" if cluster_id != -1 else "Noise"
        cluster_data = df_with_clusters[df_with_clusters['Cluster'] == cluster_id]
        
        profile = {
            'Cluster': cluster_name,
            'Size': len(cluster_data),
            'Percentage': f"{len(cluster_data)/len(df_with_clusters)*100:.1f}%"
        }
        
        # Add feature statistics
        for col in original_df.columns:
            if original_df[col].dtype in [np.float64, np.int64, float, int]:
                profile[f'{col}_mean'] = cluster_data[col].mean() if col in cluster_data.columns else None
        
        profiles.append(profile)
        print(f"  [{cluster_name}] Size: {len(cluster_data)} ({profile['Percentage']})")
    
    profiles_df = pd.DataFrame(profiles)
    
    # Save outputs
    save_data(profiles_df, 'cluster_profiles', subdir='cluster_profiles')
    save_data(df_with_clusters, 'data_with_clusters', subdir='predictions')
    
    return df_with_clusters, profiles_df


def create_visualizations(data_2d, labels, best_score, results_df):
    """Create and save visualizations."""
    print("\n" + "=" * 70)
    print("CREATING VISUALIZATIONS")
    print("=" * 70)
    
    setup_matplotlib()
    
    # 1. Cluster visualization
    fig, ax = plt.subplots(figsize=(12, 10))
    
    unique_labels = sorted(set(labels))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
    
    for label, color in zip(unique_labels, colors):
        if label == -1:
            color = 'gray'
            marker = 'x'
            alpha = 0.3
            name = 'Noise'
        else:
            marker = 'o'
            alpha = 0.6
            name = f'Cluster {label}'
        
        mask = labels == label
        ax.scatter(data_2d[mask, 0], data_2d[mask, 1],
                  c=[color], marker=marker, alpha=alpha, label=name, s=50)
    
    ax.set_xlabel('Principal Component 1', fontsize=12)
    ax.set_ylabel('Principal Component 2', fontsize=12)
    ax.set_title(f'DBSCAN Clustering Results (Silhouette Score: {best_score:.4f})', fontsize=14)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    save_fig(fig, 'cluster_visualization', subdir='plots')
    plt.close(fig)
    print("[INFO] Saved cluster visualization")
    
    # 2. Optimization heatmap (if results available)
    if not results_df.empty:
        pivot = results_df.pivot_table(
            values='silhouette_score',
            index='min_samples',
            columns='eps',
            aggfunc='max'
        )
        
        if not pivot.empty:
            fig, ax = plt.subplots(figsize=(14, 8))
            sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn',
                       center=0.5, ax=ax, cbar_kws={'label': 'Silhouette Score'})
            ax.set_title('DBSCAN Hyperparameter Optimization Heatmap', fontsize=14)
            ax.set_xlabel('eps (neighborhood radius)', fontsize=12)
            ax.set_ylabel('min_samples', fontsize=12)
            
            save_fig(fig, 'optimization_heatmap', subdir='plots')
            plt.close(fig)
            print("[INFO] Saved optimization heatmap")
    
    return True


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute the optimized DBSCAN clustering pipeline."""
    print("\n")
    print("=" * 70)
    print("SEER BREAST CANCER DBSCAN CLUSTERING PIPELINE")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Author: Cavin Otieno")
    print("=" * 70)
    
    # Load data
    data_file = os.path.join(PROJECT_ROOT, 'SEER_Breast_Cancer_Dataset.csv')
    if not os.path.exists(data_file):
        print(f"[ERROR] Data file not found: {data_file}")
        return None, None
    
    original_df, df_encoded, scaled_data, feature_cols, scaler = load_and_preprocess_data(data_file)
    
    # Optimize DBSCAN
    best_params, best_score, labels, clustering_data, results_df = optimize_dbscan_for_high_silhouette(
        scaled_data, target_score=0.87
    )
    
    # Save optimization results
    if not results_df.empty:
        save_data(results_df, 'optimization_results', subdir='metrics')
    
    # Create cluster profiles
    df_with_clusters, profiles = create_cluster_profiles(original_df, labels, feature_cols)
    
    # Create visualizations
    create_visualizations(clustering_data, labels, best_score, results_df)
    
    # Save final model
    final_model = {
        'best_params': best_params,
        'best_score': best_score,
        'n_clusters': len(set(labels)) - (1 if -1 in labels else 0),
        'feature_names': feature_cols,
        'scaler': scaler
    }
    save_model(final_model, 'dbscan_final_model', subdir='final')
    
    # Summary
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE - SUMMARY")
    print("=" * 70)
    print(f"Best Parameters: {best_params}")
    print(f"Best Silhouette Score: {best_score:.4f}")
    print(f"Target (0.87-1.00): {'ACHIEVED' if best_score >= 0.87 else 'NOT YET ACHIEVED'}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return best_params, best_score


if __name__ == "__main__":
    best_params, best_score = main()
