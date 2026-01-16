# Methodology

## Overview

This document provides a comprehensive explanation of the analytical methodology employed in the SEER Breast Cancer clustering analysis, including algorithmic theory, preprocessing steps, validation strategies, and statistical testing procedures.

## 1. Data Acquisition and Preprocessing

### 1.1 Data Source
- **Dataset:** SEER Breast Cancer Dataset
- **Repository:** National Cancer Institute SEER Program
- **Inclusion Criteria:** Female breast cancer cases with complete staging, demographic, and survival information
- **Temporal Scope:** Multi-year SEER registry data

### 1.2 Data Preprocessing Pipeline

#### Missing Data Handling
```
Strategy: Multiple Imputation and Case Deletion
- Categorical Variables: Mode imputation for <5% missingness
- Continuous Variables: Median imputation or KNN imputation
- Critical Variables: Complete case analysis for survival and staging
```

#### Feature Engineering
1. **Survival Time Calculation:**
   - Computed from diagnosis to death/last contact
   - Censoring indicator for survival analysis

2. **Categorical Encoding:**
   - One-Hot Encoding: Nominal variables (race, marital status)
   - Ordinal Encoding: Ordered categories (grade, stage)
   - Label Encoding: Binary variables (ER/PR status)

3. **Feature Scaling:**
   - **Method:** StandardScaler (z-score normalization)
   - **Formula:** `z = (x - μ) / σ`
   - **Rationale:** Essential for distance-based clustering algorithms (DBSCAN, K-Means)

#### Dimensionality Assessment
- **Original Features:** 16 clinical/demographic variables
- **Dimensionality Reduction:** Not applied in primary analysis to preserve clinical interpretability
- **Multicollinearity Check:** VIF (Variance Inflation Factor) < 10 for all features

## 2. Clustering Algorithms: Theory and Implementation

### 2.1 DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

#### Mathematical Foundation

**Core Concepts:**

1. **ε-neighborhood:** For a point p, the ε-neighborhood is defined as:
   ```
   Nε(p) = {q ∈ D | dist(p, q) ≤ ε}
   ```
   where D is the dataset and dist() is the Euclidean distance metric.

2. **Core Points:** A point p is a core point if:
   ```
   |Nε(p)| ≥ MinPts
   ```
   where MinPts is the minimum number of points required to form a dense region.

3. **Directly Density-Reachable:** Point q is directly density-reachable from p if:
   - q ∈ Nε(p)
   - p is a core point

4. **Density-Reachable:** Point q is density-reachable from p if there exists a chain:
   ```
   p = p₁, p₂, ..., pₙ = q
   ```
   where pᵢ₊₁ is directly density-reachable from pᵢ.

5. **Density-Connected:** Points p and q are density-connected if there exists a point o such that both p and q are density-reachable from o.

**Algorithm Steps:**
```
1. For each unvisited point p in dataset:
   a. Mark p as visited
   b. Find Nε(p)
   c. If |Nε(p)| < MinPts:
      - Mark p as noise (temporary)
   d. Else:
      - Create new cluster C
      - Add p to C
      - For each point q in Nε(p):
         i. If q is unvisited:
            - Mark q as visited
            - Find Nε(q)
            - If |Nε(q)| ≥ MinPts:
              - Add Nε(q) to neighborhood queue
         ii. If q not in any cluster:
            - Add q to C
2. Return clusters and noise points
```

**Advantages:**
- Discovers clusters of arbitrary shape
- Robust to outliers (explicitly identifies noise)
- Does not require pre-specifying number of clusters
- Effective for datasets with varying density

**Limitations:**
- Sensitive to hyperparameters (ε, MinPts)
- Struggles with clusters of varying densities
- Computational complexity: O(n log n) with spatial indexing, O(n²) without

**Clinical Application:**
In cancer data, DBSCAN excels at:
- Identifying rare patient phenotypes (small, dense clusters)
- Detecting outlier cases requiring specialized treatment
- Handling heterogeneous patient populations

### 2.2 K-Means Clustering

#### Mathematical Foundation

**Objective Function:**
Minimize within-cluster sum of squares (WCSS):
```
J = Σᵢ₌₁ᵏ Σₓ∈Cᵢ ||x - μᵢ||²
```
where:
- k = number of clusters
- Cᵢ = cluster i
- μᵢ = centroid of cluster i
- x = data point

**Algorithm (Lloyd's Algorithm):**
```
1. Initialize: Randomly select k centroids μ₁, μ₂, ..., μₖ
2. Repeat until convergence:
   a. Assignment Step:
      - For each point x:
        C(x) = argminⱼ ||x - μⱼ||²
   b. Update Step:
      - For each cluster j:
        μⱼ = (1/|Cⱼ|) Σₓ∈Cⱼ x
3. Return clusters C₁, C₂, ..., Cₖ
```

**Advantages:**
- Computationally efficient: O(nkt) where t = iterations
- Simple to implement and interpret
- Works well with spherical, evenly-sized clusters
- Scales to large datasets

**Limitations:**
- Requires pre-specifying k (number of clusters)
- Assumes spherical clusters with similar variance
- Sensitive to initialization (k-means++)
- Affected by outliers

**Clinical Application:**
Suitable for:
- Well-defined risk categories (low, medium, high)
- Balanced patient populations
- Situations requiring fast, interpretable groupings

### 2.3 Gaussian Mixture Models (GMM)

#### Mathematical Foundation

**Probabilistic Model:**
Assumes data generated from mixture of k Gaussian distributions:
```
p(x) = Σᵢ₌₁ᵏ πᵢ 𝒩(x | μᵢ, Σᵢ)
```
where:
- πᵢ = mixing coefficient (prior probability of cluster i)
- 𝒩(x | μᵢ, Σᵢ) = Gaussian distribution with mean μᵢ and covariance Σᵢ
- Σᵢ₌₁ᵏ πᵢ = 1

**Expectation-Maximization (EM) Algorithm:**
```
Initialize: μᵢ, Σᵢ, πᵢ for i = 1, ..., k

Repeat until convergence:
  E-Step: Compute responsibilities
    γ(zₙₖ) = [πₖ 𝒩(xₙ | μₖ, Σₖ)] / [Σⱼ πⱼ 𝒩(xₙ | μⱼ, Σⱼ)]
  
  M-Step: Update parameters
    Nₖ = Σₙ γ(zₙₖ)
    μₖ = (1/Nₖ) Σₙ γ(zₙₖ) xₙ
    Σₖ = (1/Nₖ) Σₙ γ(zₙₖ)(xₙ - μₖ)(xₙ - μₖ)ᵀ
    πₖ = Nₖ / N
```

**Advantages:**
- Provides soft cluster assignments (probabilities)
- Models cluster covariance structure
- Principled probabilistic framework
- Can handle elliptical clusters

**Limitations:**
- Sensitive to initialization
- Computationally expensive
- Risk of overfitting with full covariance matrices
- Requires specifying k

**Clinical Application:**
Valuable for:
- Uncertainty quantification in patient stratification
- Patients with mixed phenotypes
- Probabilistic treatment assignment

### 2.4 Agglomerative Hierarchical Clustering

#### Mathematical Foundation

**Linkage Criteria:**

1. **Single Linkage (Minimum):**
   ```
   d(C₁, C₂) = min{d(x, y) : x ∈ C₁, y ∈ C₂}
   ```

2. **Complete Linkage (Maximum):**
   ```
   d(C₁, C₂) = max{d(x, y) : x ∈ C₁, y ∈ C₂}
   ```

3. **Average Linkage:**
   ```
   d(C₁, C₂) = (1/|C₁||C₂|) Σₓ∈C₁ Σᵧ∈C₂ d(x, y)
   ```

4. **Ward's Method:** Minimize increase in total within-cluster variance:
   ```
   d(C₁, C₂) = √[(2|C₁||C₂|)/(|C₁|+|C₂|)] ||μ₁ - μ₂||²
   ```

**Algorithm:**
```
1. Initialize: Each point is its own cluster
2. Repeat until k clusters remain:
   a. Find two closest clusters Cᵢ, Cⱼ using linkage criterion
   b. Merge Cᵢ and Cⱼ
   c. Update distance matrix
3. Return dendrogram and final clusters
```

**Advantages:**
- Produces hierarchical structure (dendrogram)
- No need to pre-specify k
- Deterministic results
- Captures multi-scale clustering

**Limitations:**
- Computationally expensive: O(n²log n) to O(n³)
- Sensitive to noise and outliers
- Cannot undo merge decisions
- Memory intensive for large datasets

**Clinical Application:**
Useful for:
- Exploring hierarchical disease subtypes
- Visualizing patient similarity relationships
- Identifying optimal granularity for risk groups

## 3. Hyperparameter Tuning

### 3.1 DBSCAN Hyperparameters

**ε (epsilon) - Neighborhood radius:**
- **Optimization Method:** k-distance graph (elbow method)
- **Procedure:**
  1. Compute k-nearest neighbor distances for each point
  2. Sort distances in ascending order
  3. Plot sorted k-distances
  4. Select ε at "elbow" (sharp bend in curve)
- **Selected Value:** Determined empirically from k-distance plot
- **Rationale:** Balances cluster cohesion with noise detection

**MinPts - Minimum cluster size:**
- **Heuristic:** MinPts ≥ D + 1 (where D = dimensionality)
- **Common Range:** 2 × D for high-dimensional data
- **Selected Value:** Tuned through silhouette score validation
- **Rationale:** Ensures statistical significance of clusters

### 3.2 K-Means Hyperparameters

**k - Number of clusters:**
- **Optimization Methods:**
  1. Elbow method (WCSS vs. k)
  2. Silhouette analysis
  3. Gap statistic
  4. Clinical interpretability
- **Range Evaluated:** k ∈ [2, 10]
- **Selected Value:** Balancing statistical metrics with clinical utility

**Initialization:**
- **Method:** k-means++ (smart centroid initialization)
- **Rationale:** Reduces sensitivity to random initialization

### 3.3 GMM Hyperparameters

**Number of Components:**
- **Optimization:** Bayesian Information Criterion (BIC) and Akaike Information Criterion (AIC)
- **Formula (BIC):** `BIC = -2 log L + k log n`
  - L = likelihood
  - k = number of parameters
  - n = sample size

**Covariance Type:**
- **Options:** 'full', 'tied', 'diag', 'spherical'
- **Selected:** 'full' for flexibility, 'diag' for efficiency
- **Rationale:** Balance between model complexity and overfitting

### 3.4 Agglomerative Hyperparameters

**Linkage Method:**
- **Evaluated:** Single, Complete, Average, Ward
- **Selected:** Ward's method for balanced, compact clusters
- **Rationale:** Minimizes within-cluster variance (aligns with k-means objective)

**Number of Clusters:**
- **Method:** Dendrogram analysis and cophenetic correlation
- **Tool:** Cutting dendrogram at optimal height

## 4. Validation Metrics

### 4.1 Internal Validation Metrics

**Silhouette Score:**
```
s(i) = [b(i) - a(i)] / max{a(i), b(i)}
```
- a(i) = average distance to points in same cluster
- b(i) = average distance to points in nearest cluster
- Range: [-1, 1], higher is better

**Davies-Bouldin Index:**
```
DB = (1/k) Σᵢ₌₁ᵏ maxⱼ≠ᵢ [(σᵢ + σⱼ) / d(cᵢ, cⱼ)]
```
- σᵢ = average distance of points to centroid in cluster i
- d(cᵢ, cⱼ) = distance between centroids
- Lower values indicate better clustering

**Calinski-Harabasz Index:**
```
CH = [SSB / (k-1)] / [SSW / (n-k)]
```
- SSB = between-cluster dispersion
- SSW = within-cluster dispersion
- Higher values indicate better-defined clusters

### 4.2 External Validation Metrics

**Adjusted Rand Index (ARI):**
- Measures agreement with ground truth labels
- Adjusted for chance
- Range: [-1, 1], 1 = perfect agreement

**Normalized Mutual Information (NMI):**
- Information-theoretic measure
- Range: [0, 1], 1 = perfect correlation

**Purity:**
```
Purity = (1/n) Σₖ max_j |Cₖ ∩ Tⱼ|
```
- Fraction of correctly assigned points
- Range: [0, 1], higher is better

### 4.3 Clinical Validation Metrics

**Kruskal-Wallis H-test for Survival:**
- **Null Hypothesis:** No difference in survival distributions across clusters
- **Test Statistic:**
  ```
  H = (12/[n(n+1)]) Σᵢ (Rᵢ²/nᵢ) - 3(n+1)
  ```
- **Interpretation:** p < 0.05 indicates significant survival differences

**Log-Rank Test:**
- Compares survival curves between clusters
- Evaluates clinical relevance of cluster assignments

**Feature Importance Analysis:**
- Identifies variables driving cluster separation
- Methods: Random Forest feature importance, SHAP values

## 5. Statistical Analysis

### 5.1 Hypothesis Testing
- **Chi-Square Tests:** For categorical variable distributions across clusters
- **ANOVA/Kruskal-Wallis:** For continuous variable differences
- **Post-hoc Tests:** Tukey HSD or Dunn's test for pairwise comparisons

### 5.2 Effect Size Estimation
- **Cohen's d:** For magnitude of differences between clusters
- **Cramér's V:** For categorical associations

### 5.3 Confidence Intervals
- Bootstrap resampling (1000 iterations) for metric uncertainty quantification

## 6. Reproducibility

### 6.1 Random Seed Control
- All stochastic processes use fixed random seeds
- Seeds documented in code cells

### 6.2 Version Control
- Package versions recorded
- Environment specification provided

### 6.3 Code Documentation
- Inline comments for complex operations
- Markdown cells explaining analytical choices

## References

See `REFERENCES.md` for complete bibliography of methodological sources.

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Author:** Cavin Otieno
