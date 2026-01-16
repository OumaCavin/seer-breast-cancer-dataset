# SEER Breast Cancer DBSCAN Clustering Analysis

## Project Overview

This project presents a comprehensive unsupervised learning analysis of the SEER (Surveillance, Epidemiology, and End Results) Breast Cancer dataset, focusing on identifying clinically meaningful patient subgroups through advanced clustering methodologies.

## Executive Summary

**Objective:** To apply density-based clustering (DBSCAN) and comparative algorithms to discover latent patient phenotypes in breast cancer populations, with validation through both statistical metrics and clinical outcomes (survival analysis).

**Dataset:** SEER Breast Cancer Dataset
- **Source:** National Cancer Institute SEER Program
- **Scope:** Female breast cancer cases with complete staging and survival data
- **Features:** 16 clinical and demographic variables
- **Sample Size:** Post-preprocessing cohort suitable for cluster analysis

**Methodology:**
- **Primary Algorithm:** DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
- **Comparative Algorithms:** K-Means, Gaussian Mixture Models (GMM), Agglomerative Hierarchical Clustering
- **Validation:** 18 comprehensive metrics spanning internal validity, external validity, and clinical relevance

## Key Findings

### Clustering Performance
The analysis reveals distinct patient subgroups characterized by:
- **Risk Stratification:** Clusters show statistically significant differences in survival outcomes (Kruskal-Wallis p < 0.05)
- **Clinical Coherence:** High purity and homogeneity scores indicate alignment with known cancer staging systems
- **Noise Detection:** DBSCAN successfully identifies outlier cases that don't fit standard patterns

### Algorithm Comparison
Comparative analysis of four clustering approaches demonstrates:
- **DBSCAN:** Superior performance in handling irregular cluster shapes and identifying outliers in heterogeneous cancer populations
- **K-Means:** Efficient for spherical clusters but limited in capturing complex clinical patterns
- **GMM:** Provides probabilistic cluster assignments useful for uncertainty quantification
- **Agglomerative:** Offers hierarchical structure but computationally intensive for large datasets

## Project Structure

```
seer_breast_cancer_data/
├── SEER_DBSCAN_Clustering_Analysis.ipynb  # Main analysis notebook
├── output_v2/                              # Analysis outputs
│   ├── metrics/                           # Comprehensive metrics
│   ├── visualizations/                    # Figures and plots
│   └── models/                            # Saved clustering models
├── docs/                                  # Project documentation
│   ├── README.md                          # This file
│   ├── METHODOLOGY.md                     # Detailed methods
│   ├── DATA_DICTIONARY.md                 # Variable definitions
│   ├── HYPERPARAMETER_TUNING.md           # Tuning process
│   └── REFERENCES.md                      # Academic citations
└── scripts/                               # Processing pipelines
    ├── dbscan_optimized.py               # DBSCAN implementation
    └── clustering_metrics_comparison.py   # Metrics calculation
```

## Getting Started

### Prerequisites
```bash
# Core Dependencies
- Python 3.8+
- Jupyter Notebook
- scikit-learn >= 1.0
- pandas >= 1.3
- numpy >= 1.21
- matplotlib >= 3.4
- seaborn >= 0.11
- scipy >= 1.7
```

### Running the Analysis
1. **Open Main Notebook:**
   ```bash
   jupyter notebook SEER_DBSCAN_Clustering_Analysis.ipynb
   ```

2. **Execute Cells Sequentially:**
   - Data loading and preprocessing
   - Algorithm theory and implementation
   - Comprehensive algorithm comparison
   - Clinical validation and interpretation

3. **Review Outputs:**
   - Visualizations saved to `output_v2/visualizations/`
   - Metrics exported to `output_v2/metrics/`

## Academic Context

**Degree Program:** Master of Science in Public Health Data Science

**Learning Outcomes Demonstrated:**
- Advanced unsupervised machine learning techniques
- Public health data analysis and interpretation
- Statistical validation and hypothesis testing
- Reproducible research practices
- Scientific communication and visualization

**Applications:**
- Precision medicine and personalized treatment strategies
- Healthcare resource allocation optimization
- Cancer epidemiology research
- Clinical decision support systems

## Results Interpretation

### Clinical Implications
The identified clusters represent distinct patient populations with:
- **Differential Survival Patterns:** Enabling risk-stratified screening and treatment protocols
- **Feature Importance:** Highlighting key prognostic factors (stage, grade, tumor size)
- **Outlier Detection:** Identifying atypical cases requiring specialized clinical attention

### Public Health Relevance
- **Population Health Management:** Targeted interventions for high-risk clusters
- **Health Equity:** Examining demographic disparities across clusters
- **Resource Optimization:** Allocating healthcare resources based on cluster characteristics

## Future Directions

1. **External Validation:** Apply clustering model to independent breast cancer cohorts
2. **Temporal Analysis:** Incorporate longitudinal data for trajectory-based clustering
3. **Feature Engineering:** Develop composite clinical risk scores from cluster characteristics
4. **Integration:** Combine with genomic data for multi-omics clustering approaches

## Contact and Contribution

This project represents academic coursework for a Master's in Public Health Data Science program. For questions regarding methodology or findings, please refer to the comprehensive documentation in the `docs/` directory.

## License

This analysis uses publicly available SEER data. Please review SEER data use agreements and cite appropriately in derivative works.

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Author:** Cavin Otieno  
**Purpose:** Master's Project Portfolio - Public Health Data Science
