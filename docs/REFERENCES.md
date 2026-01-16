# References

## Academic Citations

This document provides comprehensive references for the methodologies, algorithms, statistical techniques, and clinical concepts used in the SEER Breast Cancer clustering analysis.

---

## Clustering Algorithms

### DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

1. **Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996).** "A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise." *Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD-96)*, 226-231.
   - **Original DBSCAN paper** introducing the algorithm and theoretical foundations

2. **Schubert, E., Sander, J., Ester, M., Kriegel, H.-P., & Xu, X. (2017).** "DBSCAN Revisited, Revisited: Why and How You Should (Still) Use DBSCAN." *ACM Transactions on Database Systems*, 42(3), 1-21.
   - Modern perspective on DBSCAN applications and best practices

3. **Sander, J., Ester, M., Kriegel, H.-P., & Xu, X. (1998).** "Density-Based Clustering in Spatial Databases: The Algorithm GDBSCAN and Its Applications." *Data Mining and Knowledge Discovery*, 2(2), 169-194.
   - Extensions and generalizations of DBSCAN

### K-Means Clustering

4. **MacQueen, J. (1967).** "Some Methods for Classification and Analysis of Multivariate Observations." *Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability*, 1(14), 281-297.
   - **Original k-means algorithm** introduction

5. **Lloyd, S. P. (1982).** "Least Squares Quantization in PCM." *IEEE Transactions on Information Theory*, 28(2), 129-137.
   - Lloyd's algorithm for k-means (originally from 1957 Bell Labs report)

6. **Arthur, D., & Vassilvitskii, S. (2007).** "k-means++: The Advantages of Careful Seeding." *Proceedings of the Eighteenth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA)*, 1027-1035.
   - **k-means++ initialization** method for improved convergence

7. **Hamerly, G., & Elkan, C. (2004).** "Learning the K in K-Means." *Advances in Neural Information Processing Systems (NIPS)*, 17, 281-288.
   - Methods for selecting optimal k

### Gaussian Mixture Models (GMM)

8. **Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977).** "Maximum Likelihood from Incomplete Data via the EM Algorithm." *Journal of the Royal Statistical Society, Series B*, 39(1), 1-38.
   - **Expectation-Maximization (EM) algorithm** foundational paper

9. **McLachlan, G., & Peel, D. (2000).** *Finite Mixture Models.* Wiley Series in Probability and Statistics. John Wiley & Sons.
   - Comprehensive textbook on mixture models

10. **Reynolds, D. A. (2009).** "Gaussian Mixture Models." *Encyclopedia of Biometrics*, 741-746. Springer.
    - Practical overview of GMM applications

### Agglomerative Hierarchical Clustering

11. **Ward, J. H., Jr. (1963).** "Hierarchical Grouping to Optimize an Objective Function." *Journal of the American Statistical Association*, 58(301), 236-244.
    - **Ward's linkage method** original publication

12. **Murtagh, F., & Contreras, P. (2012).** "Algorithms for Hierarchical Clustering: An Overview." *Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery*, 2(1), 86-97.
    - Modern review of hierarchical clustering algorithms

13. **Mullner, D. (2013).** "fastcluster: Fast Hierarchical, Agglomerative Clustering Routines for R and Python." *Journal of Statistical Software*, 53(9), 1-18.
    - Efficient implementations of hierarchical clustering

---

## Clustering Validation Metrics

### Internal Validation

14. **Rousseeuw, P. J. (1987).** "Silhouettes: A Graphical Aid to the Interpretation and Validation of Cluster Analysis." *Journal of Computational and Applied Mathematics*, 20, 53-65.
    - **Silhouette Score** original paper

15. **Davies, D. L., & Bouldin, D. W. (1979).** "A Cluster Separation Measure." *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 1(2), 224-227.
    - **Davies-Bouldin Index** for cluster validation

16. **Caliński, T., & Harabasz, J. (1974).** "A Dendrite Method for Cluster Analysis." *Communications in Statistics - Theory and Methods*, 3(1), 1-27.
    - **Calinski-Harabasz Index** (Variance Ratio Criterion)

17. **Dunn, J. C. (1974).** "Well-Separated Clusters and Optimal Fuzzy Partitions." *Journal of Cybernetics*, 4(1), 95-104.
    - **Dunn Index** for cluster validity

### External Validation

18. **Hubert, L., & Arabie, P. (1985).** "Comparing Partitions." *Journal of Classification*, 2(1), 193-218.
    - **Adjusted Rand Index (ARI)** for partition comparison

19. **Strehl, A., & Ghosh, J. (2002).** "Cluster Ensembles—A Knowledge Reuse Framework for Combining Multiple Partitions." *Journal of Machine Learning Research*, 3, 583-617.
    - **Normalized Mutual Information (NMI)** and ensemble methods

20. **Manning, C. D., Raghavan, P., & Schütze, H. (2008).** *Introduction to Information Retrieval.* Cambridge University Press.
    - **Purity** and other information retrieval metrics applied to clustering

### Model Selection

21. **Tibshirani, R., Walther, G., & Hastie, T. (2001).** "Estimating the Number of Clusters in a Data Set via the Gap Statistic." *Journal of the Royal Statistical Society: Series B (Statistical Methodology)*, 63(2), 411-423.
    - **Gap Statistic** for determining optimal k

22. **Schwarz, G. (1978).** "Estimating the Dimension of a Model." *The Annals of Statistics*, 6(2), 461-464.
    - **Bayesian Information Criterion (BIC)**

23. **Akaike, H. (1974).** "A New Look at the Statistical Model Identification." *IEEE Transactions on Automatic Control*, 19(6), 716-723.
    - **Akaike Information Criterion (AIC)**

---

## Statistical Methods

### Survival Analysis

24. **Kaplan, E. L., & Meier, P. (1958).** "Nonparametric Estimation from Incomplete Observations." *Journal of the American Statistical Association*, 53(282), 457-481.
    - **Kaplan-Meier estimator** for survival curves

25. **Mantel, N. (1966).** "Evaluation of Survival Data and Two New Rank Order Statistics Arising in Its Consideration." *Cancer Chemotherapy Reports*, 50(3), 163-170.
    - **Log-rank test** for comparing survival curves

26. **Cox, D. R. (1972).** "Regression Models and Life-Tables." *Journal of the Royal Statistical Society, Series B*, 34(2), 187-220.
    - **Cox proportional hazards model**

27. **Kruskal, W. H., & Wallis, W. A. (1952).** "Use of Ranks in One-Criterion Variance Analysis." *Journal of the American Statistical Association*, 47(260), 583-621.
    - **Kruskal-Wallis H-test** for non-parametric group comparisons

### Hypothesis Testing

28. **Dunn, O. J. (1964).** "Multiple Comparisons Using Rank Sums." *Technometrics*, 6(3), 241-252.
    - **Dunn's test** for post-hoc pairwise comparisons

29. **Tukey, J. W. (1949).** "Comparing Individual Means in the Analysis of Variance." *Biometrics*, 5(2), 99-114.
    - **Tukey's HSD test** for multiple comparisons

30. **Pearson, K. (1900).** "On the Criterion that a Given System of Deviations from the Probable in the Case of a Correlated System of Variables is Such that it Can be Reasonably Supposed to have Arisen from Random Sampling." *Philosophical Magazine*, 50(302), 157-175.
    - **Chi-square test** for categorical data

### Effect Size and Power

31. **Cohen, J. (1988).** *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
    - **Cohen's d** and power analysis methods

32. **Cramér, H. (1946).** *Mathematical Methods of Statistics.* Princeton University Press.
    - **Cramér's V** for categorical association strength

---

## Machine Learning and Data Science

### General Machine Learning

33. **Hastie, T., Tibshirani, R., & Friedman, J. (2009).** *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer.
    - Comprehensive reference for statistical learning methods

34. **Bishop, C. M. (2006).** *Pattern Recognition and Machine Learning.* Springer.
    - Fundamental machine learning textbook

35. **Murphy, K. P. (2012).** *Machine Learning: A Probabilistic Perspective.* MIT Press.
    - Probabilistic approaches to machine learning

### Feature Scaling and Preprocessing

36. **Milligan, G. W., & Cooper, M. C. (1988).** "A Study of Standardization of Variables in Cluster Analysis." *Journal of Classification*, 5(2), 181-204.
    - Impact of standardization on clustering results

37. **Van der Maaten, L., & Hinton, G. (2008).** "Visualizing Data using t-SNE." *Journal of Machine Learning Research*, 9, 2579-2605.
    - **t-SNE** for high-dimensional data visualization (supplementary analysis)

### Validation and Cross-Validation

38. **Efron, B., & Tibshirani, R. J. (1994).** *An Introduction to the Bootstrap.* Chapman & Hall/CRC.
    - **Bootstrap methods** for uncertainty quantification

39. **Kohavi, R. (1995).** "A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection." *Proceedings of the 14th International Joint Conference on Artificial Intelligence (IJCAI)*, 2, 1137-1143.
    - Cross-validation methodologies

---

## Cancer Epidemiology and Clinical Context

### SEER Program

40. **National Cancer Institute. (2021).** *Surveillance, Epidemiology, and End Results (SEER) Program.* [https://seer.cancer.gov/](https://seer.cancer.gov/)
    - Official SEER program website and data documentation

41. **Duggan, M. A., Anderson, W. F., Altekruse, S., Penberthy, L., & Sherman, M. E. (2016).** "The Surveillance, Epidemiology, and End Results (SEER) Program and Pathology: Toward Strengthening the Critical Relationship." *The American Journal of Surgical Pathology*, 40(12), e94-e102.
    - SEER data quality and pathology integration

### Breast Cancer Staging and Classification

42. **American Joint Committee on Cancer (AJCC). (2017).** *AJCC Cancer Staging Manual* (8th ed.). Springer.
    - **TNM staging system** official guidelines

43. **Giuliano, A. E., Connolly, J. L., Edge, S. B., et al. (2017).** "Breast Cancer—Major Changes in the American Joint Committee on Cancer Eighth Edition Cancer Staging Manual." *CA: A Cancer Journal for Clinicians*, 67(4), 290-303.
    - Updates to breast cancer staging

44. **Elston, C. W., & Ellis, I. O. (1991).** "Pathological Prognostic Factors in Breast Cancer. I. The Value of Histological Grade in Breast Cancer: Experience from a Large Study with Long-term Follow-up." *Histopathology*, 19(5), 403-410.
    - **Nottingham Histologic Score** for tumor grading

### Breast Cancer Biology and Subtypes

45. **Perou, C. M., Sørlie, T., Eisen, M. B., et al. (2000).** "Molecular Portraits of Human Breast Tumours." *Nature*, 406(6797), 747-752.
    - **Intrinsic subtypes** of breast cancer (molecular classification)

46. **Prat, A., & Perou, C. M. (2011).** "Deconstructing the Molecular Portraits of Breast Cancer." *Molecular Oncology*, 5(1), 5-23.
    - Modern understanding of breast cancer subtypes

47. **Goldhirsch, A., Winer, E. P., Coates, A. S., et al. (2013).** "Personalizing the Treatment of Women with Early Breast Cancer: Highlights of the St Gallen International Expert Consensus on the Primary Therapy of Early Breast Cancer 2013." *Annals of Oncology*, 24(9), 2206-2223.
    - **Clinical treatment guidelines** based on subtypes

### Biomarkers

48. **Hammond, M. E. H., Hayes, D. F., Dowsett, M., et al. (2010).** "American Society of Clinical Oncology/College of American Pathologists Guideline Recommendations for Immunohistochemical Testing of Estrogen and Progesterone Receptors in Breast Cancer." *Journal of Clinical Oncology*, 28(16), 2784-2795.
    - **ASCO/CAP guidelines** for ER/PR testing

49. **Wolff, A. C., Hammond, M. E. H., Allison, K. H., et al. (2018).** "Human Epidermal Growth Factor Receptor 2 Testing in Breast Cancer: American Society of Clinical Oncology/College of American Pathologists Clinical Practice Guideline Focused Update." *Journal of Clinical Oncology*, 36(20), 2105-2122.
    - **HER2 testing guidelines** (relevant for triple-negative classification)

### Prognosis and Outcomes

50. **DeSantis, C. E., Ma, J., Gaudet, M. M., et al. (2019).** "Breast Cancer Statistics, 2019." *CA: A Cancer Journal for Clinicians*, 69(6), 438-451.
    - Contemporary breast cancer incidence, mortality, and survival statistics

51. **Howlader, N., Altekruse, S. F., Li, C. I., et al. (2014).** "US Incidence of Breast Cancer Subtypes Defined by Joint Hormone Receptor and HER2 Status." *Journal of the National Cancer Institute*, 106(5), dju055.
    - **Subtype-specific outcomes** from SEER data

### Health Disparities

52. **DeSantis, C. E., Fedewa, S. A., Goding Sauer, A., et al. (2016).** "Breast Cancer Statistics, 2015: Convergence of Incidence Rates Between Black and White Women." *CA: A Cancer Journal for Clinicians*, 66(1), 31-42.
    - **Racial disparities** in breast cancer outcomes

53. **Silber, J. H., Rosenbaum, P. R., Clark, A. S., et al. (2013).** "Characteristics Associated with Differences in Survival Among Black and White Women with Breast Cancer." *JAMA*, 310(4), 389-397.
    - Analysis of survival differences by race

---

## Public Health Data Science

### Precision Medicine and Personalized Treatment

54. **Collins, F. S., & Varmus, H. (2015).** "A New Initiative on Precision Medicine." *New England Journal of Medicine*, 372(9), 793-795.
    - **Precision Medicine Initiative** overview

55. **Ashley, E. A. (2016).** "Towards Precision Medicine." *Nature Reviews Genetics*, 17(9), 507-522.
    - Application of data science to personalized healthcare

### Clinical Decision Support

56. **Obermeyer, Z., & Emanuel, E. J. (2016).** "Predicting the Future—Big Data, Machine Learning, and Clinical Medicine." *New England Journal of Medicine*, 375(13), 1216-1219.
    - Machine learning in clinical decision-making

57. **Rajkomar, A., Dean, J., & Kohane, I. (2019).** "Machine Learning in Medicine." *New England Journal of Medicine*, 380(14), 1347-1358.
    - Contemporary review of ML applications in healthcare

### Population Health Management

58. **Kindig, D., & Stoddart, G. (2003).** "What Is Population Health?" *American Journal of Public Health*, 93(3), 380-383.
    - Definition and scope of population health

59. **Institute of Medicine. (2012).** *For the Public's Health: Investing in a Healthier Future.* The National Academies Press.
    - Public health infrastructure and data systems

---

## Software and Tools

### Python Libraries

60. **Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011).** "Scikit-learn: Machine Learning in Python." *Journal of Machine Learning Research*, 12, 2825-2830.
    - **scikit-learn** library documentation (clustering algorithms)

61. **McKinney, W. (2010).** "Data Structures for Statistical Computing in Python." *Proceedings of the 9th Python in Science Conference*, 56-61.
    - **pandas** library for data manipulation

62. **Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020).** "Array Programming with NumPy." *Nature*, 585(7825), 357-362.
    - **NumPy** library for numerical computing

63. **Hunter, J. D. (2007).** "Matplotlib: A 2D Graphics Environment." *Computing in Science & Engineering*, 9(3), 90-95.
    - **matplotlib** library for data visualization

64. **Waskom, M. L. (2021).** "seaborn: Statistical Data Visualization." *Journal of Open Source Software*, 6(60), 3021.
    - **seaborn** library for statistical graphics

65. **Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020).** "SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python." *Nature Methods*, 17(3), 261-272.
    - **SciPy** library for scientific computing (hierarchical clustering)

### Reproducible Research

66. **Kluyver, T., Ragan-Kelley, B., Pérez, F., et al. (2016).** "Jupyter Notebooks—A Publishing Format for Reproducible Computational Workflows." *Positioning and Power in Academic Publishing: Players, Agents and Agendas*, 87-90. IOS Press.
    - **Jupyter Notebook** for reproducible data science

67. **Rule, A., Birmingham, A., Zuniga, C., et al. (2019).** "Ten Simple Rules for Writing and Sharing Computational Analyses in Jupyter Notebooks." *PLOS Computational Biology*, 15(7), e1007007.
    - Best practices for computational notebooks

---

## Methodological Reviews

68. **Jain, A. K., Murty, M. N., & Flynn, P. J. (1999).** "Data Clustering: A Review." *ACM Computing Surveys*, 31(3), 264-323.
    - Comprehensive review of clustering methods

69. **Xu, R., & Wunsch, D. (2005).** "Survey of Clustering Algorithms." *IEEE Transactions on Neural Networks*, 16(3), 645-678.
    - Survey of clustering algorithms and applications

70. **Von Luxburg, U. (2007).** "A Tutorial on Spectral Clustering." *Statistics and Computing*, 17(4), 395-416.
    - Spectral clustering methods (alternative approach)

71. **Rodriguez, M. Z., Comin, C. H., Casanova, D., et al. (2019).** "Clustering Algorithms: A Comparative Approach." *PLOS ONE*, 14(1), e0210236.
    - Modern comparative analysis of clustering algorithms

---

## Data Ethics and Privacy

72. **National Institutes of Health. (2018).** "NIH Data Sharing Policy and Implementation Guidance."
    - Data sharing and ethical considerations for research

73. **Gaye, A., Marcon, Y., Isaeva, J., et al. (2014).** "DataSHIELD: Taking the Analysis to the Data, not the Data to the Analysis." *International Journal of Epidemiology*, 43(6), 1929-1944.
    - Privacy-preserving data analysis methods

---

## Online Resources and Databases

74. **SEER*Stat Software.** National Cancer Institute. [https://seer.cancer.gov/seerstat/](https://seer.cancer.gov/seerstat/)
    - Official SEER data extraction and analysis software

75. **Breast Cancer Risk Assessment Tool.** National Cancer Institute. [https://bcrisktool.cancer.gov/](https://bcrisktool.cancer.gov/)
    - Clinical risk calculator (Gail model)

76. **Adjuvant! Online.** [https://www.adjuvantonline.com/](https://www.adjuvantonline.com/)
    - Treatment benefit calculator for breast cancer (now replaced by PREDICT tools)

---

## Additional Reading

### Textbooks

77. **Aggarwal, C. C., & Reddy, C. K. (Eds.). (2013).** *Data Clustering: Algorithms and Applications.* Chapman and Hall/CRC.
    - Comprehensive clustering textbook

78. **Kaufman, L., & Rousseeuw, P. J. (1990).** *Finding Groups in Data: An Introduction to Cluster Analysis.* John Wiley & Sons.
    - Classic clustering text with emphasis on validation

79. **Kleinbaum, D. G., & Klein, M. (2012).** *Survival Analysis: A Self-Learning Text* (3rd ed.). Springer.
    - Textbook on survival analysis methods

80. **Vittinghoff, E., Glidden, D. V., Shiboski, S. C., & McCulloch, C. E. (2012).** *Regression Methods in Biostatistics: Linear, Logistic, Survival, and Repeated Measures Models* (2nd ed.). Springer.
    - Biostatistical methods for clinical research

---

## Citation Style

All references follow the AMA (American Medical Association) citation style, commonly used in public health and medical research.

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Compiled by:** Cavin Otieno  
**Purpose:** Comprehensive bibliography for SEER Breast Cancer clustering analysis

**Note:** While DOIs and URLs are available for most references, they have been omitted here for brevity. Complete citations with DOIs can be provided upon request for manuscript preparation.
