#!/usr/bin/env python3
"""
SEER Breast Cancer DBSCAN Clustering Pipeline
==============================================
A comprehensive, reproducible pipeline for identifying meaningful health 
subpopulations using DBSCAN clustering with systematic hyperparameter optimization.

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
from itertools import product

# Scikit-learn imports
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# =============================================================================
# PROJECT CONFIGURATION - EMBEDDED PATHS AND UTILITIES
# =============================================================================

print("=" * 70)
print("PROJECT CONFIGURATION")
print("=" * 70)

# Define project root directory (current working directory)
PROJECT_ROOT = os.path.abspath(os.path.dirname('__file__'))

# Define main directory paths
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output_v2')
MODELS_DIR = os.path.join(OUTPUT_DIR, 'models')
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')

# Define phase-specific subdirectories
PHASE_DIRS = {
    'data': os.path.join(DATA_DIR, 'raw'),
    'processed': os.path.join(DATA_DIR, 'processed'),
    'reports': os.path.join(OUTPUT_DIR, 'reports'),
    'logs': os.path.join(OUTPUT_DIR, 'logs'),
    'plots': os.path.join(FIGURES_DIR, 'plots')
}

# Define model subdirectories
MODEL_SUBDIRS = {
    'gmm_clustering': os.path.join(MODELS_DIR, 'gmm_clustering'),
    'baseline': os.path.join(MODELS_DIR, 'baseline'),
    'tuned': os.path.join(MODELS_DIR, 'tuned'),
    'final': os.path.join(MODELS_DIR, 'final'),
    'comparison': os.path.join(MODELS_DIR, 'comparison')
}

# Define output subdirectories
OUTPUT_SUBDIRS = {
    'metrics': os.path.join(OUTPUT_DIR, 'metrics'),
    'predictions': os.path.join(OUTPUT_DIR, 'predictions'),
    'thresholds': os.path.join(OUTPUT_DIR, 'thresholds'),
    'fairness': os.path.join(OUTPUT_DIR, 'fairness'),
    'validation': os.path.join(OUTPUT_DIR, 'validation'),
    'cluster_profiles': os.path.join(OUTPUT_DIR, 'cluster_profiles')
}

# Create all directories if they don't exist
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


def setup_matplotlib_for_plotting():
    """Setup matplotlib and seaborn for plotting with proper configuration."""
    plt.switch_backend("Agg")
    plt.style.use("seaborn-v0_8")
    sns.set_palette("husl")
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "WenQuanYi Zen Hei", 
                                        "PingFang SC", "Arial Unicode MS", 
                                        "Hiragino Sans GB", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams['figure.figsize'] = [12, 8]
    plt.rcParams['figure.dpi'] = 100


def save_fig(figure, filename, subdir=None, formats=['png', 'pdf', 'svg']):
    """Save a matplotlib figure in multiple formats."""
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
    """Save a trained model using joblib."""
    if subdir and subdir in MODEL_SUBDIRS:
        save_dir = MODEL_SUBDIRS[subdir]
    else:
        save_dir = MODELS_DIR
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, f"{filename}.joblib")
    joblib.dump(model, filepath)
    return filepath


def save_data(data, filename, subdir=None, fmt='csv'):
    """Save data (DataFrame or array) to file."""
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
# DATA LOADING AND PREPROCESSING
# =============================================================================

class DataPreprocessor:
    """Comprehensive data preprocessing for DBSCAN clustering."""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.label_encoders = {}
        self.scaler = None
        self.feature_names = None
        
    def load_data(self, filepath):
        """Load the SEER breast cancer dataset."""
        print("\n" + "=" * 70)
        print("DATA LOADING")
        print("=" * 70)
        
        df = pd.read_csv(filepath)
        print(f"[INFO] Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"[INFO] Columns: {list(df.columns)}")
        return df
    
    def clean_data(self, df):
        """Clean and prepare data for clustering."""
        print("\n" + "=" * 70)
        print("DATA CLEANING")
        print("=" * 70)
        
        df_clean = df.copy()
        
        # Clean column names (remove extra spaces)
        df_clean.columns = df_clean.columns.str.strip()
        
        # Drop unnamed columns if any
        df_clean = df_clean.loc[:, ~df_clean.columns.str.contains('^Unnamed')]
        
        # Handle missing values
        initial_rows = len(df_clean)
        df_clean = df_clean.dropna()
        print(f"[INFO] Removed {initial_rows - len(df_clean)} rows with missing values")
        print(f"[INFO] Remaining rows: {len(df_clean)}")
        
        return df_clean
    
    def encode_features(self, df):
        """Encode categorical features."""
        print("\n" + "=" * 70)
        print("FEATURE ENCODING")
        print("=" * 70)
        
        df_encoded = df.copy()
        
        # Define ordinal mappings for cancer staging
        grade_mapping = {
            'Well differentiated; Grade I': 1,
            'Moderately differentiated; Grade II': 2,
            'Poorly differentiated; Grade III': 3,
            'Undifferentiated; anaplastic; Grade IV': 4
        }
        
        t_stage_mapping = {'T1': 1, 'T2': 2, 'T3': 3, 'T4': 4}
        n_stage_mapping = {'N1': 1, 'N2': 2, 'N3': 3}
        a_stage_mapping = {'Regional': 1, 'Distant': 2}
        status_mapping = {'Alive': 1, 'Dead': 0}
        estrogen_mapping = {'Positive': 1, 'Negative': 0}
        progesterone_mapping = {'Positive': 1, 'Negative': 0}
        
        # Apply ordinal mappings
        if 'Grade' in df_encoded.columns:
            df_encoded['Grade'] = df_encoded['Grade'].map(grade_mapping).fillna(2)
        if 'T Stage' in df_encoded.columns:
            df_encoded['T Stage'] = df_encoded['T Stage'].map(t_stage_mapping).fillna(2)
        if 'N Stage' in df_encoded.columns:
            df_encoded['N Stage'] = df_encoded['N Stage'].map(n_stage_mapping).fillna(1)
        if 'A Stage' in df_encoded.columns:
            df_encoded['A Stage'] = df_encoded['A Stage'].map(a_stage_mapping).fillna(1)
        if 'Status' in df_encoded.columns:
            df_encoded['Status'] = df_encoded['Status'].map(status_mapping).fillna(1)
        if 'Estrogen Status' in df_encoded.columns:
            df_encoded['Estrogen Status'] = df_encoded['Estrogen Status'].map(estrogen_mapping).fillna(1)
        if 'Progesterone Status' in df_encoded.columns:
            df_encoded['Progesterone Status'] = df_encoded['Progesterone Status'].map(progesterone_mapping).fillna(1)
        
        # Encode remaining categorical columns
        categorical_cols = df_encoded.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            self.label_encoders[col] = le
            print(f"[INFO] Encoded '{col}': {len(le.classes_)} categories")
        
        print(f"[INFO] Final encoded shape: {df_encoded.shape}")
        return df_encoded
    
    def select_features(self, df):
        """Select optimal features for clustering."""
        print("\n" + "=" * 70)
        print("FEATURE SELECTION")
        print("=" * 70)
        
        # Select numeric features for clustering
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Exclude ID-like columns if any
        exclude_patterns = ['id', 'index', 'unnamed']
        feature_cols = [col for col in numeric_cols 
                       if not any(p in col.lower() for p in exclude_patterns)]
        
        self.feature_names = feature_cols
        print(f"[INFO] Selected {len(feature_cols)} features: {feature_cols}")
        
        return df[feature_cols]
    
    def scale_features(self, df):
        """Scale features using MinMaxScaler for DBSCAN."""
        print("\n" + "=" * 70)
        print("FEATURE SCALING")
        print("=" * 70)
        
        self.scaler = MinMaxScaler()
        scaled_data = self.scaler.fit_transform(df)
        
        print(f"[INFO] Scaled features to [0, 1] range")
        print(f"[INFO] Scaled data shape: {scaled_data.shape}")
        
        return scaled_data, df.columns.tolist()
    
    def reduce_dimensions(self, data, n_components=2, method='pca'):
        """Reduce dimensionality for better DBSCAN performance."""
        print("\n" + "=" * 70)
        print(f"DIMENSIONALITY REDUCTION ({method.upper()})")
        print("=" * 70)
        
        if method == 'pca':
            reducer = PCA(n_components=n_components, random_state=self.random_state)
            reduced_data = reducer.fit_transform(data)
            explained_var = reducer.explained_variance_ratio_.sum()
            print(f"[INFO] PCA explained variance: {explained_var:.4f}")
        elif method == 'tsne':
            reducer = TSNE(n_components=n_components, random_state=self.random_state,
                          perplexity=30, n_iter=1000)
            reduced_data = reducer.fit_transform(data)
            print(f"[INFO] t-SNE reduction complete")
        else:
            reduced_data = data
            
        print(f"[INFO] Reduced from {data.shape[1]} to {reduced_data.shape[1]} dimensions")
        
        return reduced_data


# =============================================================================
# DBSCAN HYPERPARAMETER OPTIMIZATION
# =============================================================================

class DBSCANOptimizer:
    """Systematic hyperparameter optimization for DBSCAN clustering."""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.optimization_results = []
        self.best_model = None
        self.best_params = None
        self.best_score = -1
        
    def compute_k_distance(self, data, k=5):
        """Compute k-distance graph for eps estimation."""
        print("\n[INFO] Computing k-distance graph...")
        neighbors = NearestNeighbors(n_neighbors=k)
        neighbors.fit(data)
        distances, _ = neighbors.kneighbors(data)
        k_distances = np.sort(distances[:, k-1])
        return k_distances
    
    def plot_k_distance(self, k_distances, k=5):
        """Plot k-distance graph to help determine eps."""
        setup_matplotlib_for_plotting()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(range(len(k_distances)), k_distances, 'b-', linewidth=1)
        ax.set_xlabel('Points sorted by distance', fontsize=12)
        ax.set_ylabel(f'{k}-NN Distance', fontsize=12)
        ax.set_title(f'K-Distance Graph (k={k}) for Epsilon Estimation', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # Add elbow point estimation
        gradient = np.gradient(k_distances)
        elbow_idx = np.argmax(gradient)
        elbow_eps = k_distances[elbow_idx]
        ax.axhline(y=elbow_eps, color='r', linestyle='--', 
                   label=f'Suggested eps: {elbow_eps:.4f}')
        ax.legend()
        
        save_fig(fig, 'k_distance_graph', subdir='plots')
        plt.close(fig)
        
        print(f"[INFO] Suggested eps from k-distance: {elbow_eps:.4f}")
        return elbow_eps
    
    def grid_search(self, data, eps_range, min_samples_range, target_silhouette=0.87):
        """Perform grid search for optimal DBSCAN parameters."""
        print("\n" + "=" * 70)
        print("DBSCAN HYPERPARAMETER OPTIMIZATION")
        print("=" * 70)
        print(f"[INFO] Target Silhouette Score: >= {target_silhouette}")
        print(f"[INFO] eps range: {eps_range[0]:.2f} to {eps_range[-1]:.2f}")
        print(f"[INFO] min_samples range: {min_samples_range[0]} to {min_samples_range[-1]}")
        
        total_combinations = len(eps_range) * len(min_samples_range)
        print(f"[INFO] Total combinations to evaluate: {total_combinations}")
        print("-" * 70)
        
        self.optimization_results = []
        best_score = -1
        iteration = 0
        
        for eps in eps_range:
            for min_samples in min_samples_range:
                iteration += 1
                
                # Fit DBSCAN
                dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
                labels = dbscan.fit_predict(data)
                
                # Calculate metrics
                n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                n_noise = (labels == -1).sum()
                noise_ratio = n_noise / len(labels)
                
                # Skip if all noise or single cluster
                if n_clusters < 2:
                    continue
                
                # Calculate clustering metrics (excluding noise points)
                mask = labels != -1
                if mask.sum() < 10:  # Need at least 10 non-noise points
                    continue
                    
                try:
                    silhouette = silhouette_score(data[mask], labels[mask])
                    davies_bouldin = davies_bouldin_score(data[mask], labels[mask])
                    calinski = calinski_harabasz_score(data[mask], labels[mask])
                except:
                    continue
                
                result = {
                    'eps': eps,
                    'min_samples': min_samples,
                    'n_clusters': n_clusters,
                    'n_noise': n_noise,
                    'noise_ratio': noise_ratio,
                    'silhouette_score': silhouette,
                    'davies_bouldin_index': davies_bouldin,
                    'calinski_harabasz_score': calinski
                }
                self.optimization_results.append(result)
                
                # Check if this is the best model
                if silhouette > best_score and noise_ratio < 0.3:
                    best_score = silhouette
                    self.best_score = silhouette
                    self.best_params = {'eps': eps, 'min_samples': min_samples}
                    self.best_model = dbscan
                    
                # Progress update
                if iteration % 20 == 0 or silhouette >= target_silhouette:
                    status = "TARGET MET!" if silhouette >= target_silhouette else ""
                    print(f"  [{iteration}/{total_combinations}] eps={eps:.3f}, "
                          f"min_samples={min_samples}, clusters={n_clusters}, "
                          f"silhouette={silhouette:.4f} {status}")
        
        print("-" * 70)
        print(f"\n[RESULT] Best Silhouette Score: {self.best_score:.4f}")
        print(f"[RESULT] Best Parameters: {self.best_params}")
        
        return pd.DataFrame(self.optimization_results)
    
    def advanced_optimization(self, data, initial_eps=0.1, target_silhouette=0.87):
        """Advanced optimization with adaptive search for high silhouette scores."""
        print("\n" + "=" * 70)
        print("ADVANCED OPTIMIZATION FOR HIGH SILHOUETTE SCORE")
        print("=" * 70)
        
        # Strategy 1: Fine-grained search around estimated eps
        k_distances = self.compute_k_distance(data, k=5)
        suggested_eps = self.plot_k_distance(k_distances, k=5)
        
        # Strategy 2: Multiple search phases
        best_overall_score = -1
        best_overall_params = None
        best_overall_labels = None
        
        # Phase 1: Coarse search
        print("\n[PHASE 1] Coarse Grid Search")
        eps_coarse = np.arange(0.05, 0.8, 0.05)
        min_samples_coarse = [3, 5, 7, 10, 15, 20, 25, 30]
        
        results_df = self.grid_search(data, eps_coarse, min_samples_coarse, target_silhouette)
        
        if self.best_score >= target_silhouette:
            print(f"\n[SUCCESS] Target achieved in Phase 1!")
            best_overall_score = self.best_score
            best_overall_params = self.best_params
        
        # Phase 2: Fine search around best parameters
        if self.best_params and self.best_score < target_silhouette:
            print("\n[PHASE 2] Fine-grained Search")
            eps_center = self.best_params['eps']
            ms_center = self.best_params['min_samples']
            
            eps_fine = np.arange(max(0.01, eps_center - 0.1), 
                                 eps_center + 0.1, 0.01)
            min_samples_fine = list(range(max(2, ms_center - 5), 
                                          ms_center + 6, 1))
            
            results_fine = self.grid_search(data, eps_fine, min_samples_fine, target_silhouette)
            results_df = pd.concat([results_df, results_fine], ignore_index=True)
        
        # Phase 3: Ultra-fine search if still not meeting target
        if self.best_score < target_silhouette and self.best_params:
            print("\n[PHASE 3] Ultra-fine Search with Feature Engineering")
            
            # Try with fewer dimensions (more separation)
            pca = PCA(n_components=2, random_state=self.random_state)
            data_2d = pca.fit_transform(data)
            
            eps_ultra = np.arange(0.01, 0.5, 0.01)
            min_samples_ultra = [2, 3, 4, 5, 6, 7, 8]
            
            for eps in eps_ultra:
                for ms in min_samples_ultra:
                    dbscan = DBSCAN(eps=eps, min_samples=ms)
                    labels = dbscan.fit_predict(data_2d)
                    
                    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                    if n_clusters < 2:
                        continue
                    
                    mask = labels != -1
                    if mask.sum() < 10:
                        continue
                    
                    try:
                        score = silhouette_score(data_2d[mask], labels[mask])
                        noise_ratio = (labels == -1).sum() / len(labels)
                        
                        if score > best_overall_score and noise_ratio < 0.3:
                            best_overall_score = score
                            best_overall_params = {'eps': eps, 'min_samples': ms, 
                                                   'method': 'pca_2d'}
                            best_overall_labels = labels
                            self.best_score = score
                            self.best_params = best_overall_params
                            
                            if score >= target_silhouette:
                                print(f"  [TARGET MET] eps={eps:.3f}, ms={ms}, "
                                      f"silhouette={score:.4f}")
                    except:
                        continue
        
        return results_df, self.best_params, self.best_score
    
    def plot_optimization_heatmap(self, results_df):
        """Plot optimization results as a heatmap."""
        setup_matplotlib_for_plotting()
        
        if results_df.empty:
            print("[WARNING] No valid results to plot")
            return
        
        # Create pivot table for heatmap
        pivot = results_df.pivot_table(
            values='silhouette_score',
            index='min_samples',
            columns='eps',
            aggfunc='max'
        )
        
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn', 
                    center=0.5, ax=ax, cbar_kws={'label': 'Silhouette Score'})
        ax.set_title('DBSCAN Hyperparameter Optimization Heatmap', fontsize=14)
        ax.set_xlabel('eps (neighborhood radius)', fontsize=12)
        ax.set_ylabel('min_samples (minimum points)', fontsize=12)
        
        save_fig(fig, 'optimization_heatmap', subdir='plots')
        plt.close(fig)
        
        print("[INFO] Saved optimization heatmap")


# =============================================================================
# CLUSTER ANALYSIS AND INTERPRETATION
# =============================================================================

class ClusterAnalyzer:
    """Analyze and interpret clustering results."""
    
    def __init__(self):
        self.cluster_profiles = None
        
    def fit_final_model(self, data, params):
        """Fit the final DBSCAN model with optimal parameters."""
        print("\n" + "=" * 70)
        print("FINAL MODEL FITTING")
        print("=" * 70)
        
        eps = params.get('eps', 0.1)
        min_samples = params.get('min_samples', 5)
        
        # Check if we need to use PCA-reduced data
        if params.get('method') == 'pca_2d':
            pca = PCA(n_components=2, random_state=42)
            data_for_clustering = pca.fit_transform(data)
            print(f"[INFO] Using PCA-reduced data (2D)")
        else:
            data_for_clustering = data
        
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(data_for_clustering)
        
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = (labels == -1).sum()
        
        print(f"[INFO] Parameters: eps={eps}, min_samples={min_samples}")
        print(f"[INFO] Number of clusters: {n_clusters}")
        print(f"[INFO] Noise points: {n_noise} ({n_noise/len(labels)*100:.1f}%)")
        
        # Calculate final metrics
        mask = labels != -1
        if mask.sum() >= 10 and n_clusters >= 2:
            silhouette = silhouette_score(data_for_clustering[mask], labels[mask])
            davies_bouldin = davies_bouldin_score(data_for_clustering[mask], labels[mask])
            calinski = calinski_harabasz_score(data_for_clustering[mask], labels[mask])
            
            print(f"\n[METRICS]")
            print(f"  Silhouette Score: {silhouette:.4f}")
            print(f"  Davies-Bouldin Index: {davies_bouldin:.4f}")
            print(f"  Calinski-Harabasz Score: {calinski:.2f}")
        
        return labels, data_for_clustering
    
    def create_cluster_profiles(self, original_df, labels, feature_names):
        """Create detailed profiles for each cluster."""
        print("\n" + "=" * 70)
        print("CLUSTER PROFILING")
        print("=" * 70)
        
        df_with_clusters = original_df.copy()
        df_with_clusters['Cluster'] = labels
        
        # Calculate statistics for each cluster
        profiles = []
        unique_clusters = sorted(set(labels))
        
        for cluster_id in unique_clusters:
            cluster_name = f"Cluster_{cluster_id}" if cluster_id != -1 else "Noise"
            cluster_data = df_with_clusters[df_with_clusters['Cluster'] == cluster_id]
            
            profile = {'Cluster': cluster_name, 'Size': len(cluster_data)}
            
            # Calculate mean for numeric columns
            for col in feature_names:
                if col in cluster_data.columns:
                    profile[f'{col}_mean'] = cluster_data[col].mean()
                    profile[f'{col}_std'] = cluster_data[col].std()
            
            profiles.append(profile)
            
            print(f"\n[{cluster_name}] Size: {len(cluster_data)} "
                  f"({len(cluster_data)/len(df_with_clusters)*100:.1f}%)")
        
        self.cluster_profiles = pd.DataFrame(profiles)
        
        # Save profiles
        save_data(self.cluster_profiles, 'cluster_profiles', subdir='cluster_profiles')
        save_data(df_with_clusters, 'data_with_clusters', subdir='predictions')
        
        return df_with_clusters, self.cluster_profiles
    
    def plot_clusters(self, data, labels, title="DBSCAN Clustering Results"):
        """Visualize clusters in 2D."""
        setup_matplotlib_for_plotting()
        
        # Reduce to 2D if necessary
        if data.shape[1] > 2:
            pca = PCA(n_components=2, random_state=42)
            data_2d = pca.fit_transform(data)
        else:
            data_2d = data
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        unique_labels = set(labels)
        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
        
        for label, color in zip(sorted(unique_labels), colors):
            if label == -1:
                # Noise points in gray
                color = 'gray'
                marker = 'x'
                alpha = 0.3
                label_name = 'Noise'
            else:
                marker = 'o'
                alpha = 0.6
                label_name = f'Cluster {label}'
            
            mask = labels == label
            ax.scatter(data_2d[mask, 0], data_2d[mask, 1],
                      c=[color], marker=marker, alpha=alpha,
                      label=label_name, s=50)
        
        ax.set_xlabel('Component 1', fontsize=12)
        ax.set_ylabel('Component 2', fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        save_fig(fig, 'cluster_visualization', subdir='plots')
        plt.close(fig)
        
        print("[INFO] Saved cluster visualization")
    
    def plot_feature_distribution(self, df_with_clusters, feature_names):
        """Plot feature distributions across clusters."""
        setup_matplotlib_for_plotting()
        
        n_features = min(len(feature_names), 6)  # Plot top 6 features
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, feature in enumerate(feature_names[:n_features]):
            if feature not in df_with_clusters.columns:
                continue
            ax = axes[i]
            
            for cluster_id in sorted(df_with_clusters['Cluster'].unique()):
                if cluster_id == -1:
                    continue
                cluster_data = df_with_clusters[df_with_clusters['Cluster'] == cluster_id]
                ax.hist(cluster_data[feature], alpha=0.5, 
                       label=f'Cluster {cluster_id}', bins=20)
            
            ax.set_xlabel(feature, fontsize=10)
            ax.set_ylabel('Count', fontsize=10)
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        
        plt.suptitle('Feature Distributions Across Clusters', fontsize=14)
        plt.tight_layout()
        
        save_fig(fig, 'feature_distributions', subdir='plots')
        plt.close(fig)
        
        print("[INFO] Saved feature distribution plots")


# =============================================================================
# MAIN PIPELINE EXECUTION
# =============================================================================

def main():
    """Execute the complete DBSCAN clustering pipeline."""
    print("\n")
    print("=" * 70)
    print("SEER BREAST CANCER DBSCAN CLUSTERING PIPELINE")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Author: Cavin Otieno")
    print("=" * 70)
    
    # Initialize components
    preprocessor = DataPreprocessor(random_state=RANDOM_STATE)
    optimizer = DBSCANOptimizer(random_state=RANDOM_STATE)
    analyzer = ClusterAnalyzer()
    
    # Step 1: Load Data
    data_file = os.path.join(PROJECT_ROOT, 'SEER_Breast_Cancer_Dataset.csv')
    if not os.path.exists(data_file):
        print(f"[ERROR] Data file not found: {data_file}")
        return
    
    df = preprocessor.load_data(data_file)
    
    # Step 2: Clean and Preprocess
    df_clean = preprocessor.clean_data(df)
    df_encoded = preprocessor.encode_features(df_clean)
    df_features = preprocessor.select_features(df_encoded)
    
    # Step 3: Scale Features
    scaled_data, feature_names = preprocessor.scale_features(df_features)
    
    # Step 4: Dimensionality Reduction
    reduced_data = preprocessor.reduce_dimensions(scaled_data, n_components=3, method='pca')
    
    # Step 5: Hyperparameter Optimization
    results_df, best_params, best_score = optimizer.advanced_optimization(
        reduced_data, 
        target_silhouette=0.87
    )
    
    # Save optimization results
    if not results_df.empty:
        save_data(results_df, 'optimization_results', subdir='metrics')
        optimizer.plot_optimization_heatmap(results_df)
    
    # Step 6: Fit Final Model
    if best_params:
        labels, clustering_data = analyzer.fit_final_model(reduced_data, best_params)
        
        # Step 7: Analyze Clusters
        df_with_clusters, profiles = analyzer.create_cluster_profiles(
            df_clean, labels, feature_names
        )
        
        # Step 8: Visualizations
        analyzer.plot_clusters(clustering_data, labels, 
                              title=f"DBSCAN Clusters (Silhouette: {best_score:.4f})")
        analyzer.plot_feature_distribution(df_with_clusters, feature_names)
        
        # Save final model
        final_model_info = {
            'best_params': best_params,
            'best_score': best_score,
            'n_clusters': len(set(labels)) - (1 if -1 in labels else 0),
            'feature_names': feature_names
        }
        save_model(final_model_info, 'dbscan_final_model', subdir='final')
    
    # Summary Report
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE - SUMMARY")
    print("=" * 70)
    print(f"Best Parameters: {best_params}")
    print(f"Best Silhouette Score: {best_score:.4f}")
    print(f"Target Score (0.87-1.00): {'ACHIEVED' if best_score >= 0.87 else 'NOT ACHIEVED'}")
    print(f"\nOutput Directory: {OUTPUT_DIR}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return best_params, best_score


if __name__ == "__main__":
    best_params, best_score = main()
