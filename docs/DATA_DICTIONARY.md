# Data Dictionary

## Overview

This document provides comprehensive definitions for all variables in the SEER Breast Cancer dataset used in this clustering analysis. Understanding these clinical and demographic features is essential for interpreting cluster characteristics and clinical implications.

## Dataset Information

- **Source:** SEER (Surveillance, Epidemiology, and End Results) Program
- **Population:** Female breast cancer patients
- **Registry:** Multi-state SEER registries
- **Data Type:** De-identified patient records

## Variable Definitions

### 1. Demographic Variables

#### Age at Diagnosis
- **Variable Name:** `Age`
- **Type:** Continuous (numeric)
- **Unit:** Years
- **Range:** Typically 18-100+
- **Description:** Patient's age at the time of breast cancer diagnosis
- **Clinical Significance:** 
  - Age is a critical prognostic factor in breast cancer
  - Younger patients (<40) may have more aggressive disease
  - Older patients (>70) may have comorbidities affecting treatment
- **Missing Data:** Minimal (<1%)
- **Preprocessing:** Standardized using z-score normalization

#### Race
- **Variable Name:** `Race`
- **Type:** Categorical (nominal)
- **Categories:**
  - White
  - Black/African American
  - Asian/Pacific Islander
  - American Indian/Alaska Native
  - Other/Unknown
- **Description:** Self-reported or registry-recorded race/ethnicity
- **Clinical Significance:**
  - Racial disparities exist in breast cancer incidence and outcomes
  - Certain subtypes more prevalent in specific populations
  - Social determinants of health affect screening and treatment access
- **Encoding:** One-hot encoding for clustering
- **Missing Data:** Coded as "Unknown" category

#### Marital Status
- **Variable Name:** `Marital_Status`
- **Type:** Categorical (nominal)
- **Categories:**
  - Married (including domestic partner)
  - Single (never married)
  - Divorced
  - Widowed
  - Separated
  - Unknown
- **Description:** Patient's marital status at diagnosis
- **Clinical Significance:**
  - Married patients often have better outcomes (social support hypothesis)
  - Reflects potential caregiver availability
  - May influence treatment decisions and compliance
- **Encoding:** One-hot encoding
- **Missing Data:** <5%

### 2. Tumor Characteristics

#### T Stage (Tumor Size)
- **Variable Name:** `T_Stage`
- **Type:** Ordinal categorical
- **Categories (TNM Staging):**
  - **T0:** No evidence of primary tumor
  - **Tis:** Carcinoma in situ (DCIS, LCIS, Paget's disease)
  - **T1:** Tumor ≤ 20 mm
    - T1mi: ≤1 mm
    - T1a: >1 mm, ≤5 mm
    - T1b: >5 mm, ≤10 mm
    - T1c: >10 mm, ≤20 mm
  - **T2:** Tumor >20 mm, ≤50 mm
  - **T3:** Tumor >50 mm
  - **T4:** Any size with chest wall/skin extension
    - T4a: Chest wall extension
    - T4b: Skin ulceration/nodules
    - T4c: Both T4a and T4b
    - T4d: Inflammatory breast cancer
- **Description:** Extent of primary tumor based on size and local invasion
- **Clinical Significance:**
  - Primary determinant of cancer stage
  - Larger tumors associated with worse prognosis
  - Guides surgical approach (lumpectomy vs. mastectomy)
- **Encoding:** Ordinal encoding (0-4 for main categories)
- **Missing Data:** <2% (tumors with unknown size)

#### N Stage (Regional Lymph Nodes)
- **Variable Name:** `N_Stage`
- **Type:** Ordinal categorical
- **Categories (TNM Staging):**
  - **N0:** No regional lymph node metastasis
  - **N1:** Metastasis in 1-3 axillary lymph nodes
  - **N2:** Metastasis in 4-9 axillary lymph nodes OR positive internal mammary nodes
  - **N3:** Metastasis in ≥10 axillary lymph nodes OR infraclavicular nodes OR supraclavicular nodes
- **Description:** Extent of regional lymph node involvement
- **Clinical Significance:**
  - Critical prognostic indicator
  - Determines need for adjuvant therapy
  - Higher N stage indicates increased metastatic potential
- **Encoding:** Ordinal encoding (0-3)
- **Missing Data:** <3% (nodes not examined or assessment inadequate)

#### M Stage (Distant Metastasis)
- **Variable Name:** `M_Stage`
- **Type:** Binary categorical
- **Categories:**
  - **M0:** No distant metastasis
  - **M1:** Distant metastasis present
- **Description:** Presence of distant organ metastasis at diagnosis
- **Clinical Significance:**
  - Distinguishes localized/regional from metastatic disease
  - M1 indicates Stage IV cancer (incurable but treatable)
  - Dramatically affects treatment goals (curative vs. palliative)
- **Encoding:** Binary (0/1)
- **Missing Data:** Minimal (<1%)

#### Overall Stage Group
- **Variable Name:** `Stage`
- **Type:** Ordinal categorical
- **Categories (AJCC Staging):**
  - **Stage 0:** Tis, N0, M0 (in situ)
  - **Stage I:** Small tumor, no nodes (T1, N0, M0)
  - **Stage II:** Larger tumor or limited node involvement
    - IIA: T0-1N1M0 or T2N0M0
    - IIB: T2N1M0 or T3N0M0
  - **Stage III:** Advanced local/regional disease
    - IIIA: T0-2N2M0 or T3N1-2M0
    - IIIB: T4N0-2M0
    - IIIC: Any T, N3, M0
  - **Stage IV:** Distant metastasis (any T, any N, M1)
- **Description:** Composite staging based on TNM classification
- **Clinical Significance:**
  - Primary determinant of prognosis and treatment
  - 5-year survival: Stage I (~99%), Stage II (~93%), Stage III (~72%), Stage IV (~22%)
  - Guides treatment intensity and clinical trial eligibility
- **Encoding:** Ordinal encoding (0-4)
- **Missing Data:** <1% (incomplete staging workup)

#### Histologic Grade
- **Variable Name:** `Grade`
- **Type:** Ordinal categorical
- **Categories:**
  - **Grade 1 (Well differentiated):** Cells closely resemble normal breast tissue
  - **Grade 2 (Moderately differentiated):** Intermediate appearance
  - **Grade 3 (Poorly differentiated):** Cells look very abnormal, rapidly dividing
  - **Grade 4 (Undifferentiated):** Extremely abnormal (rare in breast cancer)
  - **Grade X:** Cannot be assessed
- **Description:** Degree of tumor cell differentiation (how abnormal cells appear)
- **Grading System:** Nottingham Histologic Score
  - Based on: Tubule formation, nuclear pleomorphism, mitotic count
  - Score 3-5 = Grade 1, 6-7 = Grade 2, 8-9 = Grade 3
- **Clinical Significance:**
  - Higher grade = more aggressive tumor biology
  - Independent prognostic factor
  - Influences chemotherapy decisions
- **Encoding:** Ordinal encoding (1-3, excluding Grade X)
- **Missing Data:** ~5% (small biopsies, technical issues)

#### Tumor Size (Continuous)
- **Variable Name:** `Tumor_Size`
- **Type:** Continuous (numeric)
- **Unit:** Millimeters (mm)
- **Range:** 1-999 mm (typically <200 mm)
- **Description:** Maximum diameter of primary tumor on pathology
- **Clinical Significance:**
  - Continuous measure complementing T stage
  - Used in online prognostic calculators (e.g., Adjuvant! Online)
  - Threshold effects at 10mm, 20mm, 50mm
- **Preprocessing:** Log transformation to reduce skewness, then standardized
- **Missing Data:** ~3% (diffuse tumors, no surgery)

#### Number of Positive Lymph Nodes
- **Variable Name:** `Positive_Nodes`
- **Type:** Count (discrete numeric)
- **Unit:** Number of nodes
- **Range:** 0-90+ (most patients 0-10)
- **Description:** Count of regional lymph nodes with metastatic cancer
- **Clinical Significance:**
  - Continuous measure complementing N stage
  - Strong prognostic indicator (more nodes = worse prognosis)
  - Determines adjuvant chemotherapy regimen intensity
- **Preprocessing:** Square root transformation, then standardized
- **Missing Data:** <2% (nodes not examined)

#### Number of Lymph Nodes Examined
- **Variable Name:** `Examined_Nodes`
- **Type:** Count (discrete numeric)
- **Unit:** Number of nodes
- **Range:** 0-90+
- **Description:** Total number of lymph nodes surgically removed and examined
- **Clinical Significance:**
  - Adequacy of staging (recommended ≥10 nodes for axillary dissection)
  - Affects accuracy of N stage classification
  - Quality metric for surgical/pathology workup
- **Preprocessing:** Standardized
- **Missing Data:** <1%

### 3. Biomarker Variables

#### Estrogen Receptor (ER) Status
- **Variable Name:** `ER_Status`
- **Type:** Categorical (ordinal/binary)
- **Categories:**
  - **Positive:** ≥1% tumor cells with nuclear staining (Allred score ≥3)
  - **Negative:** <1% tumor cells staining
  - **Borderline:** 1-10% (rare, usually re-classified)
  - **Unknown/Not tested**
- **Assay:** Immunohistochemistry (IHC)
- **Description:** Presence of estrogen receptors on tumor cells
- **Clinical Significance:**
  - ER+ tumors (~70% of cases) respond to hormone therapy (tamoxifen, aromatase inhibitors)
  - ER- tumors require chemotherapy-based treatment
  - Major determinant of treatment strategy
- **Encoding:** Binary (Positive=1, Negative=0)
- **Missing Data:** <5% (older cases pre-routine testing)

#### Progesterone Receptor (PR) Status
- **Variable Name:** `PR_Status`
- **Type:** Categorical (ordinal/binary)
- **Categories:**
  - **Positive:** ≥1% tumor cells with nuclear staining
  - **Negative:** <1% tumor cells staining
  - **Borderline:** 1-10%
  - **Unknown/Not tested**
- **Assay:** Immunohistochemistry (IHC)
- **Description:** Presence of progesterone receptors on tumor cells
- **Clinical Significance:**
  - Provides additional information beyond ER status
  - ER+/PR+ tumors have best prognosis and hormone therapy response
  - ER+/PR- may indicate less responsive disease
  - ER-/PR+ is rare (<3% of cases)
- **Encoding:** Binary (Positive=1, Negative=0)
- **Missing Data:** <5%

### 4. Treatment Variables

#### Surgery Type
- **Variable Name:** `Surgery`
- **Type:** Categorical (nominal)
- **Categories:**
  - **Breast-Conserving Surgery (BCS):** Lumpectomy, partial mastectomy, quadrantectomy
  - **Mastectomy:** Total mastectomy, modified radical mastectomy
  - **No Surgery:** Inoperable, patient refused, palliative care
  - **Surgery NOS (Not Otherwise Specified)**
- **Description:** Primary surgical procedure performed
- **Clinical Significance:**
  - BCS requires adjuvant radiation therapy
  - Mastectomy may be followed by reconstruction
  - Surgical choice based on tumor size, patient preference
- **Encoding:** One-hot encoding
- **Missing Data:** <1%

#### Radiation Therapy
- **Variable Name:** `Radiation`
- **Type:** Binary categorical
- **Categories:**
  - **Yes:** Received radiation therapy
  - **No/Unknown:** No radiation or unknown
- **Description:** Receipt of external beam radiation therapy
- **Clinical Significance:**
  - Standard after BCS to reduce local recurrence
  - May be used after mastectomy (high-risk features)
  - Omission in appropriate cases may indicate comorbidities/frailty
- **Encoding:** Binary (Yes=1, No=0)
- **Missing Data:** ~10% (unknown status in older records)

#### Chemotherapy
- **Variable Name:** `Chemotherapy`
- **Type:** Binary categorical (in SEER, often inferred)
- **Categories:**
  - **Yes:** Received chemotherapy
  - **No/Unknown:** No chemotherapy or unknown
- **Description:** Receipt of systemic chemotherapy
- **Note:** SEER does not consistently record chemotherapy; may be underreported
- **Clinical Significance:**
  - Recommended for high-risk disease (node-positive, high grade, large tumors)
  - Triple-negative and HER2+ tumors typically receive chemotherapy
  - Absence may indicate low-risk disease or patient choice
- **Encoding:** Binary (Yes=1, No=0)
- **Missing Data:** Significant (~30% unknown in older SEER data)

### 5. Outcome Variables

#### Survival Time (Months)
- **Variable Name:** `Survival_Months`
- **Type:** Continuous (numeric)
- **Unit:** Months
- **Range:** 0-300+ months
- **Description:** Time from diagnosis to death or last contact
- **Calculation:** 
  - For deceased: (Date of death - Date of diagnosis)
  - For alive: (Date of last contact - Date of diagnosis)
- **Clinical Significance:**
  - Primary endpoint for survival analysis
  - Used in Kaplan-Meier curves and Cox models
  - Assesses long-term cancer outcomes
- **Preprocessing:** Not transformed (used in survival models)
- **Missing Data:** Minimal (<1%)

#### Vital Status
- **Variable Name:** `Vital_Status`
- **Type:** Binary categorical
- **Categories:**
  - **Alive:** Patient alive at last contact
  - **Dead:** Patient deceased
- **Description:** Vital status at end of follow-up
- **Clinical Significance:**
  - Censoring indicator for survival analysis
  - Alive patients are "right-censored" (event not yet observed)
  - Dead patients have observed survival time
- **Encoding:** Binary (Alive=0, Dead=1)
- **Missing Data:** <1% (lost to follow-up coded as last known status)

#### Cause of Death
- **Variable Name:** `COD` (Cause of Death)
- **Type:** Categorical
- **Categories:**
  - **Breast Cancer:** Death attributable to breast cancer
  - **Other Cancer:** Death from other malignancy
  - **Non-Cancer:** Death from cardiovascular, infection, accident, etc.
  - **Unknown**
  - **Not Applicable:** Patient alive
- **Description:** Underlying cause of death for deceased patients
- **Clinical Significance:**
  - Distinguishes cancer-specific vs. overall survival
  - Important for elderly patients with competing risks
  - Breast cancer-specific survival is more sensitive endpoint
- **Encoding:** Multi-category encoding
- **Missing Data:** ~10% among deceased (death certificate unavailable)

## Data Quality and Preprocessing

### Completeness
- **Overall Missingness:** <5% for most variables
- **High Missingness:** Chemotherapy (~30%), PR status (~5%)
- **Handling:** Multiple imputation for analysis, complete case for survival endpoints

### Validity
- **Range Checks:** Automated validation for out-of-range values
- **Consistency Checks:** TNM staging logic validated
- **Clinical Review:** Outliers manually reviewed

### Transformations Applied

1. **Continuous Variables:**
   - Age: Standardized (z-score)
   - Tumor Size: Log-transform → Standardized
   - Positive Nodes: Square root transform → Standardized
   - Examined Nodes: Standardized

2. **Categorical Variables:**
   - Ordinal (Stage, Grade, T, N): Ordinal encoding
   - Nominal (Race, Marital Status): One-hot encoding
   - Binary (ER, PR, M stage): Binary encoding (0/1)

3. **Survival Variables:**
   - Survival Months: No transformation (time variable)
   - Vital Status: Event indicator (0=censored, 1=event)

## Feature Engineering

### Derived Variables
- **Lymph Node Ratio:** Positive_Nodes / Examined_Nodes
- **Hormone Receptor Status:** Combined ER/PR (HR+: ER+ or PR+, HR-: both negative)
- **Risk Category:** Composite based on Stage + Grade

### Interaction Terms
- Age × Stage (age-stage interaction)
- ER Status × Grade (biology-grade interaction)

## Clinical Context

### Breast Cancer Subtypes (Biological)
While not directly in dataset, clustering may recapitulate:
- **Luminal A:** ER+, PR+, HER2-, low grade (best prognosis)
- **Luminal B:** ER+, HER2+ or high grade (intermediate prognosis)
- **HER2-enriched:** ER-, PR-, HER2+ (requires targeted therapy)
- **Triple-Negative (Basal-like):** ER-, PR-, HER2- (worst prognosis, limited treatment options)

### Staging and Prognosis
**5-Year Relative Survival Rates (SEER Data):**
- Localized (confined to breast): 99%
- Regional (spread to lymph nodes): 86%
- Distant (metastatic): 29%
- All stages combined: 90%

## References

- **AJCC Cancer Staging Manual (8th Edition):** TNM staging definitions
- **SEER Program Coding and Staging Manual:** Variable specifications
- **WHO Classification of Tumours of the Breast:** Histologic grading
- **ASCO/CAP Guidelines:** ER/PR testing methodology

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Author:** Cavin Otieno  
**Purpose:** Variable definitions for SEER Breast Cancer clustering analysis
