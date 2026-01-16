#!/usr/bin/env python3
"""
Comprehensive Clustering Metrics Comparison for Healthcare Data
================================================================
This script implements multiple clustering evaluation metrics side-by-side
for comparing DBSCAN, K-Means, and Gaussian Mixture Models.

Author: Cavin Otieno
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from collections import Counter

# Scikit-learn imports
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (
    silhouette_score, silhouette_samples,
    davies_bouldin_score, calinski_harabasz_score,
    adjusted_rand_score, normalized_mutual_info_score,
    homogeneity_score, completeness_score, v_measure_score,
    fowlkes_mallows_score
)
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

warnings.filterwarnings('ignore')
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Setup matplotlib
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = [14, 10]
plt.rcParams['figure.dpi'] = 100

# =============================================================================
print("=" * 70)
print("COMPREHENSIVE CLUSTERING METRICS FOR HEALTHCARE DATA")
print("=" * 70)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Author: Cavin Otieno")
print("=" * 70)

# =============================================================================
# ADDITIONAL CLUSTERING METRICS IMPLEMENTATIONS
# =============================================================================

def dunn_index(X, labels):
    """
    Calculate Dunn Index for clustering evaluation.
    
    Dunn Index = min(inter-cluster distance) / max(intra-cluster diameter)
    
    Higher values indicate better clustering.
    Good for healthcare: Measures how well-separated patient subgroups are.
    
    Parameters:
    -----------
    X : array-like, shape (n_samples, n_features)
    labels : array-like, shape (n_samples,)
    
    Returns:
    --------
    float : Dunn index value
    """
    unique_labels = np.unique(labels[labels != -1])
    if len(unique_labels) < 2:
        return 0.0
    
    # Calculate pairwise distances
    distances = squareform(pdist(X))
    
    # Calculate intra-cluster diameters (max distance within cluster)
    intra_cluster_diameters = []
    for label in unique_labels:
        mask = labels == label
        if mask.sum() > 1:
            cluster_distances = distances[np.ix_(mask, mask)]
            intra_cluster_diameters.append(np.max(cluster_distances))
        else:
            intra_cluster_diameters.append(0)
    
    max_intra = max(intra_cluster_diameters) if intra_cluster_diameters else 1
    
    # Calculate inter-cluster distances (min distance between clusters)
    inter_cluster_distances = []
    for i, label_i in enumerate(unique_labels):
        for label_j in unique_labels[i+1:]:
            mask_i = labels == label_i
            mask_j = labels == label_j
            cluster_distances = distances[np.ix_(mask_i, mask_j)]
            inter_cluster_distances.append(np.min(cluster_distances))
    
    min_inter = min(inter_cluster_distances) if inter_cluster_distances else 0
    
    return min_inter / max_intra if max_intra > 0 else 0


def connectivity_index(X, labels, k=10):
    """
    Calculate Connectivity Index for clustering.
    
    Measures the degree to which neighboring data points are placed 
    in the same cluster. Lower values indicate better clustering.
    
    Good for healthcare: Ensures similar patients are grouped together.
    
    Parameters:
    -----------
    X : array-like
    labels : array-like
    k : int, number of nearest neighbors to consider
    
    Returns:
    --------
    float : Connectivity index (lower is better)
    """
    n_samples = X.shape[0]
    k = min(k, n_samples - 1)
    
    # Find k nearest neighbors
    nn = NearestNeighbors(n_neighbors=k+1)
    nn.fit(X)
    _, indices = nn.kneighbors(X)
    
    connectivity = 0.0
    for i in range(n_samples):
        for j, neighbor_idx in enumerate(indices[i, 1:], 1):  # Skip self
            if labels[i] != labels[neighbor_idx]:
                connectivity += 1.0 / j
    
    return connectivity


def cluster_purity(labels, ground_truth):
    """
    Calculate cluster purity score.
    
    Measures how pure each cluster is with respect to ground truth labels.
    
    Good for healthcare: When we have survival status or other outcomes,
    measures how well clusters separate different patient outcomes.
    
    Parameters:
    -----------
    labels : predicted cluster labels
    ground_truth : true labels (e.g., survival status)
    
    Returns:
    --------
    float : Purity score [0, 1], higher is better
    """
    # Filter out noise points
    mask = labels != -1
    labels_clean = labels[mask]
    truth_clean = ground_truth[mask]
    
    if len(labels_clean) == 0:
        return 0.0
    
    contingency = pd.crosstab(labels_clean, truth_clean)
    return contingency.max(axis=1).sum() / len(labels_clean)


def entropy_score(labels, ground_truth):
    """
    Calculate entropy-based cluster evaluation.
    
    Lower entropy indicates more homogeneous clusters.
    
    Good for healthcare: Measures uncertainty in cluster assignments
    relative to patient outcomes.
    """
    mask = labels != -1
    labels_clean = labels[mask]
    truth_clean = ground_truth[mask]
    
    if len(labels_clean) == 0:
        return float('inf')
    
    total_entropy = 0.0
    unique_clusters = np.unique(labels_clean)
    
    for cluster in unique_clusters:
        cluster_mask = labels_clean == cluster
        cluster_truth = truth_clean[cluster_mask]
        
        # Calculate entropy for this cluster
        value_counts = pd.Series(cluster_truth).value_counts(normalize=True)
        cluster_entropy = -np.sum(value_counts * np.log2(value_counts + 1e-10))
        
        # Weight by cluster size
        weight = cluster_mask.sum() / len(labels_clean)
        total_entropy += weight * cluster_entropy
    
    return total_entropy


def cluster_stability_bootstrap(X, algorithm, n_bootstrap=10, sample_ratio=0.8):
    """
    Assess cluster stability using bootstrap resampling.
    
    Higher stability indicates more robust clustering.
    
    Good for healthcare: Ensures patient subgroups are reproducible
    and not artifacts of sampling.
    """
    n_samples = X.shape[0]
    sample_size = int(n_samples * sample_ratio)
    
    all_labels = []
    for _ in range(n_bootstrap):
        # Bootstrap sample
        indices = np.random.choice(n_samples, sample_size, replace=False)
        X_sample = X[indices]
        
        # Fit algorithm
        if hasattr(algorithm, 'fit_predict'):
            labels = algorithm.fit_predict(X_sample)
        else:
            labels = algorithm.fit(X_sample).labels_
        
        all_labels.append((indices, labels))
    
    # Calculate average adjusted rand index between bootstrap samples
    ari_scores = []
    for i in range(n_bootstrap):
        for j in range(i + 1, n_bootstrap):
            idx_i, labels_i = all_labels[i]
            idx_j, labels_j = all_labels[j]
            
            # Find common indices
            common = np.intersect1d(idx_i, idx_j)
            if len(common) > 10:
                mask_i = np.isin(idx_i, common)
                mask_j = np.isin(idx_j, common)
                
                # Reorder to match
                order_i = np.argsort(idx_i[mask_i])
                order_j = np.argsort(idx_j[mask_j])
                
                ari = adjusted_rand_score(labels_i[mask_i][order_i], 
                                         labels_j[mask_j][order_j])
                ari_scores.append(ari)
    
    return np.mean(ari_scores) if ari_scores else 0.0


def separation_index(X, labels):
    """
    Calculate Separation Index (average distance between cluster centroids).
    
    Higher values indicate better-separated clusters.
    
    Good for healthcare: Measures how distinct patient subgroups are.
    """
    unique_labels = np.unique(labels[labels != -1])
    if len(unique_labels) < 2:
        return 0.0
    
    # Calculate centroids
    centroids = []
    for label in unique_labels:
        mask = labels == label
        centroids.append(X[mask].mean(axis=0))
    
    centroids = np.array(centroids)
    
    # Calculate pairwise centroid distances
    centroid_distances = pdist(centroids)
    
    return np.mean(centroid_distances)


def compactness_index(X, labels):
    """
    Calculate Compactness Index (average within-cluster distance).
    
    Lower values indicate more compact clusters.
    
    Good for healthcare: Measures how homogeneous patient subgroups are.
    """
    unique_labels = np.unique(labels[labels != -1])
    if len(unique_labels) == 0:
        return float('inf')
    
    total_compactness = 0.0
    total_points = 0
    
    for label in unique_labels:
        mask = labels == label
        cluster_points = X[mask]
        
        if len(cluster_points) > 1:
            centroid = cluster_points.mean(axis=0)
            distances = np.linalg.norm(cluster_points - centroid, axis=1)
            total_compactness += distances.sum()
            total_points += len(cluster_points)
    
    return total_compactness / total_points if total_points > 0 else float('inf')


def survival_separation(labels, survival_months, status):
    """
    Healthcare-specific: Measure how well clusters separate survival outcomes.
    
    Uses Kruskal-Wallis test to assess if survival differs significantly
    across clusters.
    
    Returns:
    --------
    dict : Contains H-statistic, p-value, and separation quality
    """
    mask = labels != -1
    labels_clean = labels[mask]
    survival_clean = survival_months[mask]
    status_clean = status[mask]
    
    unique_clusters = np.unique(labels_clean)
    if len(unique_clusters) < 2:
        return {'h_statistic': 0, 'p_value': 1.0, 'separation': 'Poor'}
    
    # Group survival by cluster
    groups = [survival_clean[labels_clean == c] for c in unique_clusters]
    
    # Kruskal-Wallis test
    try:
        h_stat, p_value = stats.kruskal(*groups)
    except:
        h_stat, p_value = 0, 1.0
    
    # Calculate mean survival per cluster
    mean_survivals = [g.mean() for g in groups]
    survival_range = max(mean_survivals) - min(mean_survivals)
    
    # Assess separation quality
    if p_value < 0.001 and survival_range > 20:
        separation = 'Excellent'
    elif p_value < 0.05 and survival_range > 10:
        separation = 'Good'
    elif p_value < 0.1:
        separation = 'Moderate'
    else:
        separation = 'Poor'
    
    return {
        'h_statistic': h_stat,
        'p_value': p_value,
        'survival_range': survival_range,
        'separation': separation
    }


# =============================================================================
# DATA LOADING AND PREPROCESSING
# =============================================================================

print("\n[1] Loading and Preprocessing Data")
print("-" * 50)

# Load data
df = pd.read_csv('SEER_Breast_Cancer_Dataset.csv')
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print(f"Dataset: {df.shape[0]} patients, {df.shape[1]} features")

# Encode features
df_encoded = df.copy()

# Ordinal mappings
grade_map = {'Well differentiated; Grade I': 1, 'Moderately differentiated; Grade II': 2,
             'Poorly differentiated; Grade III': 3, 'Undifferentiated; anaplastic; Grade IV': 4}
t_stage_map = {'T1': 1, 'T2': 2, 'T3': 3, 'T4': 4}
n_stage_map = {'N1': 1, 'N2': 2, 'N3': 3}
a_stage_map = {'Regional': 1, 'Distant': 2}
status_map = {'Alive': 1, 'Dead': 0}
binary_map = {'Positive': 1, 'Negative': 0}

# Apply mappings
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
for col in df_encoded.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))

# Select features and scale
feature_cols = df_encoded.select_dtypes(include=[np.number]).columns.tolist()
X = df_encoded[feature_cols].values
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Get ground truth labels for supervised metrics (survival status)
ground_truth = df_encoded['Status'].values
survival_months = df_encoded['Survival Months'].values if 'Survival Months' in df_encoded.columns else None

# PCA for visualization and optimized clustering
pca = PCA(n_components=2, random_state=RANDOM_STATE)
X_pca = pca.fit_transform(X_scaled)

# High-variance subset for better separation
variances = np.var(X_scaled, axis=0)
top_indices = np.argsort(variances)[-4:]
X_subset = X_scaled[:, top_indices]
scaler_sub = StandardScaler()
X_subset_scaled = scaler_sub.fit_transform(X_subset)
pca_sub = PCA(n_components=2, random_state=RANDOM_STATE)
X_sub_2d = pca_sub.fit_transform(X_subset_scaled)

print(f"Features selected: {len(feature_cols)}")
print(f"PCA explained variance: {pca.explained_variance_ratio_.sum():.2%}")

# =============================================================================
# ALGORITHM DEFINITIONS
# =============================================================================

print("\n[2] Defining Clustering Algorithms")
print("-" * 50)

algorithms = {
    'DBSCAN (eps=0.1, ms=6)': DBSCAN(eps=0.1, min_samples=6),
    'DBSCAN (eps=0.15, ms=5)': DBSCAN(eps=0.15, min_samples=5),
    'DBSCAN (eps=0.2, ms=4)': DBSCAN(eps=0.2, min_samples=4),
    'K-Means (K=5)': KMeans(n_clusters=5, random_state=RANDOM_STATE, n_init=10),
    'K-Means (K=10)': KMeans(n_clusters=10, random_state=RANDOM_STATE, n_init=10),
    'K-Means (K=15)': KMeans(n_clusters=15, random_state=RANDOM_STATE, n_init=10),
    'K-Means (K=20)': KMeans(n_clusters=20, random_state=RANDOM_STATE, n_init=10),
    'GMM (n=5)': GaussianMixture(n_components=5, random_state=RANDOM_STATE),
    'GMM (n=10)': GaussianMixture(n_components=10, random_state=RANDOM_STATE),
    'GMM (n=15)': GaussianMixture(n_components=15, random_state=RANDOM_STATE),
    'Agglomerative (n=10)': AgglomerativeClustering(n_clusters=10),
    'Agglomerative (n=15)': AgglomerativeClustering(n_clusters=15),
}

print(f"Testing {len(algorithms)} algorithm configurations")

# =============================================================================
# COMPREHENSIVE METRICS EVALUATION
# =============================================================================

print("\n[3] Computing Comprehensive Clustering Metrics")
print("-" * 50)

results = []

for name, algorithm in algorithms.items():
    print(f"  Evaluating: {name}...")
    
    # Fit algorithm
    if hasattr(algorithm, 'fit_predict'):
        labels = algorithm.fit_predict(X_sub_2d)
    else:
        labels = algorithm.fit(X_sub_2d).predict(X_sub_2d)
    
    # Basic stats
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = (labels == -1).sum()
    noise_ratio = n_noise / len(labels)
    
    # Skip if invalid clustering
    mask = labels != -1
    if mask.sum() < 20 or n_clusters < 2:
        continue
    
    # Calculate all metrics
    try:
        # Standard metrics
        silhouette = silhouette_score(X_sub_2d[mask], labels[mask])
        davies_bouldin = davies_bouldin_score(X_sub_2d[mask], labels[mask])
        calinski = calinski_harabasz_score(X_sub_2d[mask], labels[mask])
        
        # Additional metrics
        dunn = dunn_index(X_sub_2d[mask], labels[mask])
        connectivity = connectivity_index(X_sub_2d[mask], labels[mask], k=10)
        separation = separation_index(X_sub_2d[mask], labels[mask])
        compactness = compactness_index(X_sub_2d[mask], labels[mask])
        
        # Supervised metrics (using survival status as pseudo ground truth)
        purity = cluster_purity(labels, ground_truth)
        entropy = entropy_score(labels, ground_truth)
        ari = adjusted_rand_score(ground_truth[mask], labels[mask])
        nmi = normalized_mutual_info_score(ground_truth[mask], labels[mask])
        homogeneity = homogeneity_score(ground_truth[mask], labels[mask])
        completeness = completeness_score(ground_truth[mask], labels[mask])
        v_measure = v_measure_score(ground_truth[mask], labels[mask])
        fmi = fowlkes_mallows_score(ground_truth[mask], labels[mask])
        
        # Healthcare-specific metrics
        if survival_months is not None:
            surv_sep = survival_separation(labels, survival_months, ground_truth)
        else:
            surv_sep = {'h_statistic': 0, 'p_value': 1, 'separation': 'N/A'}
        
        results.append({
            'Algorithm': name,
            'N Clusters': n_clusters,
            'Noise Ratio': noise_ratio,
            # Unsupervised Metrics
            'Silhouette': silhouette,
            'Davies-Bouldin': davies_bouldin,
            'Calinski-Harabasz': calinski,
            'Dunn Index': dunn,
            'Connectivity': connectivity,
            'Separation': separation,
            'Compactness': compactness,
            # Supervised/Semi-supervised Metrics
            'Purity': purity,
            'Entropy': entropy,
            'Adjusted Rand': ari,
            'NMI': nmi,
            'Homogeneity': homogeneity,
            'Completeness': completeness,
            'V-Measure': v_measure,
            'Fowlkes-Mallows': fmi,
            # Healthcare-specific
            'Survival H-stat': surv_sep['h_statistic'],
            'Survival p-value': surv_sep['p_value'],
            'Survival Separation': surv_sep['separation']
        })
        
    except Exception as e:
        print(f"    Error: {e}")
        continue

results_df = pd.DataFrame(results)

# =============================================================================
# DISPLAY RESULTS
# =============================================================================

print("\n" + "=" * 70)
print("COMPREHENSIVE METRICS COMPARISON RESULTS")
print("=" * 70)

# Unsupervised metrics
print("\n[A] UNSUPERVISED CLUSTERING METRICS")
print("-" * 50)
print("""
These metrics evaluate clustering quality without ground truth labels.
Good for discovering natural patient subgroups.
""")

unsupervised_cols = ['Algorithm', 'N Clusters', 'Noise Ratio', 
                     'Silhouette', 'Davies-Bouldin', 'Calinski-Harabasz',
                     'Dunn Index', 'Connectivity', 'Separation', 'Compactness']
print(results_df[unsupervised_cols].round(4).to_string(index=False))

print("""
METRIC INTERPRETATIONS:
- Silhouette [-1, 1]: Higher = better defined clusters
- Davies-Bouldin [0, inf): Lower = better separated clusters  
- Calinski-Harabasz [0, inf): Higher = denser, well-separated clusters
- Dunn Index [0, 1]: Higher = better cluster separation
- Connectivity [0, inf): Lower = neighbors in same cluster
- Separation [0, inf): Higher = distant cluster centroids
- Compactness [0, inf): Lower = more compact clusters
""")

# Supervised metrics
print("\n[B] SUPERVISED/SEMI-SUPERVISED METRICS")
print("-" * 50)
print("""
These metrics compare clusters to survival status (ground truth).
Useful for validating clinical relevance of clusters.
""")

supervised_cols = ['Algorithm', 'Purity', 'Entropy', 'Adjusted Rand', 'NMI',
                   'Homogeneity', 'Completeness', 'V-Measure', 'Fowlkes-Mallows']
print(results_df[supervised_cols].round(4).to_string(index=False))

print("""
METRIC INTERPRETATIONS:
- Purity [0, 1]: Higher = clusters contain same outcome
- Entropy [0, inf): Lower = more homogeneous clusters
- Adjusted Rand [-1, 1]: Higher = agreement with ground truth
- NMI [0, 1]: Higher = shared information with ground truth
- Homogeneity [0, 1]: Higher = clusters contain single class
- Completeness [0, 1]: Higher = class members in same cluster
- V-Measure [0, 1]: Harmonic mean of homogeneity & completeness
- Fowlkes-Mallows [0, 1]: Geometric mean of precision & recall
""")

# Healthcare-specific metrics
print("\n[C] HEALTHCARE-SPECIFIC METRICS")
print("-" * 50)
print("""
These metrics are specifically relevant for medical/clinical applications.
They assess how well clusters separate patient outcomes.
""")

healthcare_cols = ['Algorithm', 'N Clusters', 'Survival H-stat', 
                   'Survival p-value', 'Survival Separation']
print(results_df[healthcare_cols].round(4).to_string(index=False))

print("""
METRIC INTERPRETATIONS:
- Survival H-stat: Kruskal-Wallis statistic (higher = more difference)
- Survival p-value: Statistical significance (lower = more significant)
- Survival Separation: Overall quality rating
""")

# =============================================================================
# RANKING AND BEST ALGORITHM SELECTION
# =============================================================================

print("\n" + "=" * 70)
print("ALGORITHM RANKING BY METRIC")
print("=" * 70)

# Create rankings
ranking_metrics = ['Silhouette', 'Calinski-Harabasz', 'Dunn Index', 'Purity', 
                   'NMI', 'V-Measure']

rankings = pd.DataFrame({'Algorithm': results_df['Algorithm']})
for metric in ranking_metrics:
    if metric in ['Davies-Bouldin', 'Connectivity', 'Compactness', 'Entropy']:
        # Lower is better
        rankings[f'{metric} Rank'] = results_df[metric].rank(ascending=True)
    else:
        # Higher is better
        rankings[f'{metric} Rank'] = results_df[metric].rank(ascending=False)

rankings['Average Rank'] = rankings[[c for c in rankings.columns if 'Rank' in c]].mean(axis=1)
rankings = rankings.sort_values('Average Rank')

print("\n[OVERALL RANKING]")
print(rankings.round(2).to_string(index=False))

# Best algorithm
best_algorithm = rankings.iloc[0]['Algorithm']
print(f"\n[BEST ALGORITHM]: {best_algorithm}")

# =============================================================================
# VISUALIZATION
# =============================================================================

print("\n[4] Generating Visualizations")
print("-" * 50)

# Create output directory
output_dir = 'output_v2/figures/metrics'
os.makedirs(output_dir, exist_ok=True)

# Figure 1: Unsupervised Metrics Comparison
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

unsupervised_metrics = ['Silhouette', 'Davies-Bouldin', 'Calinski-Harabasz', 
                        'Dunn Index', 'Separation', 'Compactness']
metric_better = ['higher', 'lower', 'higher', 'higher', 'higher', 'lower']

for i, (metric, better) in enumerate(zip(unsupervised_metrics, metric_better)):
    ax = axes[i]
    colors = ['green' if 'DBSCAN' in alg else 'steelblue' for alg in results_df['Algorithm']]
    
    sorted_df = results_df.sort_values(metric, ascending=(better == 'lower'))
    ax.barh(sorted_df['Algorithm'], sorted_df[metric], 
            color=['green' if 'DBSCAN' in a else 'steelblue' for a in sorted_df['Algorithm']])
    ax.set_xlabel(metric)
    ax.set_title(f'{metric}\n({better} is better)', fontweight='bold')
    ax.grid(True, alpha=0.3)

plt.suptitle('Unsupervised Clustering Metrics Comparison', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{output_dir}/unsupervised_metrics_comparison.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print("  Generated: unsupervised_metrics_comparison.png")

# Figure 2: Supervised Metrics Comparison
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

supervised_metrics = ['Purity', 'Adjusted Rand', 'NMI', 
                      'Homogeneity', 'V-Measure', 'Fowlkes-Mallows']

for i, metric in enumerate(supervised_metrics):
    ax = axes[i]
    sorted_df = results_df.sort_values(metric, ascending=False)
    ax.barh(sorted_df['Algorithm'], sorted_df[metric],
            color=['green' if 'DBSCAN' in a else 'steelblue' for a in sorted_df['Algorithm']])
    ax.set_xlabel(metric)
    ax.set_title(f'{metric}\n(higher is better)', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)

plt.suptitle('Supervised/Semi-Supervised Metrics Comparison', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{output_dir}/supervised_metrics_comparison.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print("  Generated: supervised_metrics_comparison.png")

# Figure 3: Radar Chart for Top Algorithms
from matplotlib.patches import Polygon

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# Select top 5 algorithms
top_5 = rankings.head(5)['Algorithm'].tolist()
top_results = results_df[results_df['Algorithm'].isin(top_5)]

# Metrics for radar
radar_metrics = ['Silhouette', 'Dunn Index', 'Purity', 'NMI', 'V-Measure']

# Normalize metrics to [0, 1]
normalized = top_results[radar_metrics].copy()
for col in radar_metrics:
    normalized[col] = (normalized[col] - normalized[col].min()) / (normalized[col].max() - normalized[col].min() + 1e-10)

# Create radar chart
angles = np.linspace(0, 2 * np.pi, len(radar_metrics), endpoint=False).tolist()
angles += angles[:1]  # Complete the circle

for i, (_, row) in enumerate(top_results.iterrows()):
    values = normalized.iloc[i][radar_metrics].tolist()
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=row['Algorithm'])
    ax.fill(angles, values, alpha=0.1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(radar_metrics)
ax.set_title('Top 5 Algorithms - Metrics Radar Chart', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

plt.tight_layout()
plt.savefig(f'{output_dir}/radar_chart_comparison.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print("  Generated: radar_chart_comparison.png")

# Figure 4: Metrics Heatmap
fig, ax = plt.subplots(figsize=(16, 10))

# Normalize all numeric columns for heatmap
heatmap_cols = ['Silhouette', 'Dunn Index', 'Separation', 'Purity', 
                'NMI', 'V-Measure', 'Fowlkes-Mallows']
heatmap_data = results_df[['Algorithm'] + heatmap_cols].set_index('Algorithm')

# Normalize
heatmap_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min() + 1e-10)

sns.heatmap(heatmap_normalized, annot=True, fmt='.2f', cmap='RdYlGn', 
            ax=ax, cbar_kws={'label': 'Normalized Score (higher = better)'})
ax.set_title('Clustering Metrics Heatmap (Normalized)', fontsize=14, fontweight='bold')
ax.set_xlabel('Metric')
ax.set_ylabel('Algorithm')

plt.tight_layout()
plt.savefig(f'{output_dir}/metrics_heatmap.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print("  Generated: metrics_heatmap.png")

# =============================================================================
# SAVE RESULTS
# =============================================================================

print("\n[5] Saving Results")
print("-" * 50)

# Save comprehensive results
results_df.to_csv('output_v2/metrics/comprehensive_metrics_comparison.csv', index=False)
rankings.to_csv('output_v2/metrics/algorithm_rankings.csv', index=False)

print(f"  Saved: output_v2/metrics/comprehensive_metrics_comparison.csv")
print(f"  Saved: output_v2/metrics/algorithm_rankings.csv")
print(f"  Saved: {output_dir}/unsupervised_metrics_comparison.png")
print(f"  Saved: {output_dir}/supervised_metrics_comparison.png")
print(f"  Saved: {output_dir}/radar_chart_comparison.png")
print(f"  Saved: {output_dir}/metrics_heatmap.png")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("SUMMARY - HEALTHCARE CLUSTERING METRICS")
print("=" * 70)

print("""
METRICS IMPLEMENTED:

[UNSUPERVISED METRICS] - No ground truth required
  1. Silhouette Score - Cluster cohesion and separation
  2. Davies-Bouldin Index - Cluster similarity ratio
  3. Calinski-Harabasz Score - Variance ratio criterion
  4. Dunn Index - Min inter-cluster / max intra-cluster distance
  5. Connectivity Index - Neighbor placement quality
  6. Separation Index - Centroid distances
  7. Compactness Index - Within-cluster distances

[SUPERVISED METRICS] - Compare to survival outcomes
  8. Purity - Cluster class consistency
  9. Entropy - Cluster homogeneity
  10. Adjusted Rand Index - Clustering agreement
  11. Normalized Mutual Information - Shared information
  12. Homogeneity - Single class per cluster
  13. Completeness - Class members together
  14. V-Measure - Harmonic mean of 12 & 13
  15. Fowlkes-Mallows Index - Precision/recall balance

[HEALTHCARE-SPECIFIC METRICS]
  16. Survival Separation - Kruskal-Wallis test on survival
  17. Cluster Purity by Outcome - Survival status distribution
  18. Cluster Stability (bootstrap) - Reproducibility

BEST ALGORITHM FOR THIS DATA: {best_algorithm}
""".format(best_algorithm=best_algorithm))

print("=" * 70)
print(f"Analysis Complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)
