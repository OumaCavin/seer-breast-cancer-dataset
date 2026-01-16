#!/usr/bin/env python3
"""
SEER Breast Cancer Dataset - Variable Definitions and Clinical Context
=======================================================================
Understanding the clinical meaning of each variable is essential for
appropriate analysis and interpretation of breast cancer health data.

Author: Cavin Otieno
"""

import pandas as pd
import os

# =============================================================================
print("=" * 70)
print("VARIABLE DEFINITIONS AND CLINICAL CONTEXT")
print("=" * 70)
print("""
Understanding the clinical meaning of each variable is essential for
appropriate analysis and interpretation of SEER Breast Cancer Dataset health data.
The following provides detailed definitions and clinical reference ranges.
""")

# =============================================================================
# COMPREHENSIVE VARIABLE DESCRIPTIONS DICTIONARY
# =============================================================================

variable_descriptions = {
    
    # =========================================================================
    # DEMOGRAPHIC VARIABLES
    # =========================================================================
    
    'Age': {
        'Description': 'Age of patient at diagnosis in years',
        'Data Type': 'Continuous (Numeric)',
        'Clinical Relevance': 'Age is one of the strongest risk factors for breast cancer. '
                             'Risk increases with age, with most cases diagnosed after age 50. '
                             'Younger patients (<40) often have more aggressive tumors.',
        'Reference Range': '30-90 years (typical dataset range)',
        'Clinical Categories': {
            'Young': '<40 years - Higher likelihood of aggressive subtypes, BRCA mutations',
            'Middle-aged': '40-65 years - Peak incidence period for breast cancer',
            'Elderly': '>65 years - Higher comorbidity considerations, treatment tolerance'
        },
        'Prognostic Impact': 'Moderate - Younger age often associated with worse prognosis'
    },
    
    'Race': {
        'Description': 'Self-reported racial/ethnic background of patient',
        'Data Type': 'Categorical (Nominal)',
        'Clinical Relevance': 'Racial disparities exist in breast cancer incidence, '
                             'stage at diagnosis, access to care, and survival outcomes. '
                             'African American women have higher mortality rates despite lower incidence.',
        'Categories': {
            'White': 'Caucasian/European ancestry',
            'Black': 'African American/African ancestry',
            'Other': 'American Indian/AK Native, Asian/Pacific Islander'
        },
        'Health Disparities': 'Black women have 40% higher mortality rate; '
                             'Asian women have lowest incidence rates',
        'Prognostic Impact': 'Significant - Due to biological and socioeconomic factors'
    },
    
    'Marital Status': {
        'Description': 'Legal marital status of patient at time of diagnosis',
        'Data Type': 'Categorical (Nominal)',
        'Clinical Relevance': 'Social support systems affect treatment adherence, '
                             'psychological outcomes, and survival. Married patients '
                             'often have better outcomes due to caregiver support.',
        'Categories': {
            'Married': 'Including common law marriages',
            'Single': 'Never married',
            'Divorced': 'Previously married, legally dissolved',
            'Widowed': 'Spouse deceased',
            'Separated': 'Living apart from spouse'
        },
        'Psychosocial Factor': 'Strong predictor of treatment compliance and quality of life',
        'Prognostic Impact': 'Moderate - Married patients show improved survival'
    },
    
    # =========================================================================
    # TUMOR STAGING VARIABLES (TNM CLASSIFICATION)
    # =========================================================================
    
    'T Stage': {
        'Description': 'Primary Tumor Size and Extent (T in TNM staging)',
        'Data Type': 'Categorical (Ordinal)',
        'Clinical Relevance': 'Describes the size and local extent of the primary tumor. '
                             'Larger tumors generally indicate more advanced disease and '
                             'may require more aggressive treatment approaches.',
        'Categories': {
            'T1': 'Tumor <= 20mm in greatest dimension',
            'T2': 'Tumor > 20mm but <= 50mm',
            'T3': 'Tumor > 50mm',
            'T4': 'Tumor of any size with direct extension to chest wall/skin'
        },
        'Staging Details': {
            'T1a': '<= 5mm', 'T1b': '>5mm to 10mm', 'T1c': '>10mm to 20mm',
            'T4a': 'Extension to chest wall',
            'T4b': 'Skin ulceration, satellite nodules, or edema',
            'T4c': 'Both T4a and T4b',
            'T4d': 'Inflammatory carcinoma'
        },
        'Treatment Implications': 'Determines surgical approach and neoadjuvant therapy need',
        'Prognostic Impact': 'High - Direct correlation with survival outcomes'
    },
    
    'N Stage': {
        'Description': 'Regional Lymph Node Involvement (N in TNM staging)',
        'Data Type': 'Categorical (Ordinal)',
        'Clinical Relevance': 'Indicates spread to regional lymph nodes. Nodal involvement '
                             'is one of the most important prognostic factors in breast cancer.',
        'Categories': {
            'N1': '1-3 axillary lymph nodes involved',
            'N2': '4-9 axillary lymph nodes involved',
            'N3': '10+ axillary nodes OR infraclavicular/supraclavicular nodes'
        },
        'Clinical Subcategories': {
            'N1mi': 'Micrometastases (>0.2mm to 2mm)',
            'N1a': '1-3 axillary nodes with metastases >2mm',
            'N2a': '4-9 axillary nodes',
            'N2b': 'Internal mammary nodes without axillary involvement',
            'N3a': '10+ axillary nodes or infraclavicular nodes',
            'N3b': 'Clinically detected internal mammary nodes with axillary nodes',
            'N3c': 'Supraclavicular lymph nodes'
        },
        'Treatment Implications': 'Determines need for axillary dissection and radiation field',
        'Prognostic Impact': 'Very High - Most significant prognostic factor'
    },
    
    '6th Stage': {
        'Description': 'AJCC 6th Edition Overall Stage Grouping',
        'Data Type': 'Categorical (Ordinal)',
        'Clinical Relevance': 'Combines T, N, and M staging into overall disease stage. '
                             'Used for treatment planning and prognosis estimation.',
        'Categories': {
            'IIA': 'T0-1/N1 or T2/N0 - Localized with limited spread',
            'IIB': 'T2/N1 or T3/N0 - Moderate local advancement',
            'IIIA': 'T0-2/N2 or T3/N1-2 - Locally advanced',
            'IIIB': 'T4/N0-2 - Chest wall/skin involvement',
            'IIIC': 'Any T/N3 - Extensive nodal involvement'
        },
        'Stage Grouping Survival (5-year)': {
            'Stage I': '~100%',
            'Stage IIA': '~93%',
            'Stage IIB': '~72%',
            'Stage IIIA': '~54%',
            'Stage IIIB': '~41%',
            'Stage IIIC': '~49%'
        },
        'Prognostic Impact': 'Very High - Primary determinant of treatment approach'
    },
    
    'A Stage': {
        'Description': 'Summary Stage indicating Regional vs Distant disease',
        'Data Type': 'Categorical (Binary)',
        'Clinical Relevance': 'Simplified staging indicating whether cancer has spread '
                             'beyond regional lymph nodes to distant sites.',
        'Categories': {
            'Regional': 'Cancer confined to breast and regional lymph nodes',
            'Distant': 'Cancer has metastasized to distant organs (bone, liver, lung, brain)'
        },
        'Treatment Implications': {
            'Regional': 'Curative intent treatment - surgery, radiation, systemic therapy',
            'Distant': 'Palliative intent - focus on quality of life and disease control'
        },
        'Prognostic Impact': 'Very High - Distant disease dramatically reduces survival'
    },
    
    # =========================================================================
    # TUMOR CHARACTERISTICS
    # =========================================================================
    
    'Tumor Size': {
        'Description': 'Largest dimension of primary tumor in millimeters',
        'Data Type': 'Continuous (Numeric)',
        'Clinical Relevance': 'Direct measurement of tumor burden. Correlates with '
                             'likelihood of lymph node involvement and distant metastasis.',
        'Reference Ranges': {
            'Small': '<= 20mm - Generally favorable prognosis',
            'Intermediate': '21-50mm - Moderate risk',
            'Large': '> 50mm - Higher risk, may need neoadjuvant therapy'
        },
        'Surgical Considerations': {
            'Breast-conserving': 'Usually feasible for tumors <40-50mm relative to breast size',
            'Mastectomy': 'Often required for larger tumors or multicentric disease'
        },
        'Prognostic Impact': 'High - Larger tumors associated with worse outcomes'
    },
    
    'Grade': {
        'Description': 'Histological grade indicating tumor differentiation and aggressiveness',
        'Data Type': 'Categorical (Ordinal)',
        'Clinical Relevance': 'Reflects how much tumor cells differ from normal cells. '
                             'Higher grades indicate more aggressive, faster-growing cancers.',
        'Categories': {
            'Well differentiated; Grade I': 'Low grade - Slow growing, resembles normal tissue',
            'Moderately differentiated; Grade II': 'Intermediate grade - Moderate growth rate',
            'Poorly differentiated; Grade III': 'High grade - Fast growing, aggressive',
            'Undifferentiated; anaplastic; Grade IV': 'Very high grade - Highly aggressive'
        },
        'Nottingham Grading System Components': {
            'Tubule Formation': 'Percentage of tumor forming tubular structures',
            'Nuclear Pleomorphism': 'Variation in nuclear size and shape',
            'Mitotic Count': 'Number of dividing cells per high-power field'
        },
        'Treatment Implications': 'High grade tumors often benefit more from chemotherapy',
        'Prognostic Impact': 'High - Independent predictor of recurrence and survival'
    },
    
    # =========================================================================
    # HORMONE RECEPTOR STATUS
    # =========================================================================
    
    'Estrogen Status': {
        'Description': 'Estrogen Receptor (ER) expression status of tumor',
        'Data Type': 'Categorical (Binary)',
        'Clinical Relevance': 'ER-positive tumors grow in response to estrogen and can be '
                             'treated with hormone therapy. Approximately 70-80% of breast '
                             'cancers are ER-positive.',
        'Categories': {
            'Positive': 'ER expression >= 1% of tumor cells by IHC',
            'Negative': 'ER expression < 1% of tumor cells'
        },
        'Testing Method': 'Immunohistochemistry (IHC) on tumor tissue',
        'Treatment Implications': {
            'ER-Positive': 'Eligible for endocrine therapy (tamoxifen, aromatase inhibitors)',
            'ER-Negative': 'Chemotherapy primary systemic treatment option'
        },
        'Breast Cancer Subtypes': {
            'Luminal A': 'ER+/PR+/HER2-, Grade 1-2 - Best prognosis',
            'Luminal B': 'ER+/PR+/- HER2+/-, Grade 2-3 - Intermediate prognosis'
        },
        'Prognostic Impact': 'Very High - ER+ cancers have better overall prognosis'
    },
    
    'Progesterone Status': {
        'Description': 'Progesterone Receptor (PR) expression status of tumor',
        'Data Type': 'Categorical (Binary)',
        'Clinical Relevance': 'PR expression is regulated by estrogen receptor and indicates '
                             'a functional ER pathway. PR positivity adds prognostic information '
                             'beyond ER status alone.',
        'Categories': {
            'Positive': 'PR expression >= 1% of tumor cells by IHC',
            'Negative': 'PR expression < 1% of tumor cells'
        },
        'Clinical Significance': {
            'ER+/PR+': 'Best response to endocrine therapy',
            'ER+/PR-': 'May have less robust response to hormonal treatment',
            'ER-/PR+': 'Rare, considered biologically similar to ER+ tumors'
        },
        'Treatment Response': 'PR+ tumors show 10-15% better response to tamoxifen',
        'Prognostic Impact': 'Moderate - Adds incremental prognostic value to ER status'
    },
    
    # =========================================================================
    # LYMPH NODE ASSESSMENT
    # =========================================================================
    
    'Regional Node Examined': {
        'Description': 'Number of regional lymph nodes pathologically examined',
        'Data Type': 'Continuous (Numeric/Count)',
        'Clinical Relevance': 'Quality metric for surgical staging. Adequate lymph node '
                             'sampling is critical for accurate staging and treatment planning.',
        'Reference Standards': {
            'Sentinel Node Biopsy': '1-5 nodes typically examined',
            'Axillary Dissection': 'Minimum 10 nodes recommended for adequate staging',
            'Optimal Assessment': '15-20+ nodes for comprehensive evaluation'
        },
        'Quality Implications': 'Fewer nodes examined may lead to stage migration and '
                               'under-treatment of occult nodal disease',
        'Prognostic Impact': 'Indirect - Affects accuracy of staging'
    },
    
    'Reginol Node Positive': {
        'Description': 'Number of regional lymph nodes with metastatic cancer',
        'Data Type': 'Continuous (Numeric/Count)',
        'Clinical Relevance': 'Strongest prognostic factor in breast cancer. Number of '
                             'positive nodes directly correlates with recurrence risk.',
        'Prognostic Categories': {
            '0 nodes': 'Node-negative - Best prognosis',
            '1-3 nodes': 'Low nodal burden - Moderate risk',
            '4-9 nodes': 'Intermediate nodal burden - High risk',
            '10+ nodes': 'High nodal burden - Very high risk'
        },
        'Treatment Implications': {
            '0 nodes': 'May avoid chemotherapy in favorable subtypes',
            '1-3 nodes': 'Often requires adjuvant chemotherapy',
            '4+ nodes': 'Definitely requires aggressive systemic therapy'
        },
        'Nodal Ratio': 'Positive nodes / Examined nodes - Alternative prognostic metric',
        'Prognostic Impact': 'Very High - Primary determinant of adjuvant therapy'
    },
    
    # =========================================================================
    # OUTCOME VARIABLES
    # =========================================================================
    
    'Survival Months': {
        'Description': 'Survival time from diagnosis in months',
        'Data Type': 'Continuous (Numeric)',
        'Clinical Relevance': 'Primary outcome measure for cancer studies. Represents '
                             'time from diagnosis to death or last follow-up.',
        'Survival Metrics': {
            'Overall Survival (OS)': 'Time to death from any cause',
            'Disease-Specific Survival': 'Time to death from breast cancer',
            'Disease-Free Survival': 'Time to recurrence or death'
        },
        'Benchmark Survival Rates': {
            'Stage I': '5-year survival ~99%',
            'Stage II': '5-year survival ~86%',
            'Stage III': '5-year survival ~57%',
            'Stage IV': '5-year survival ~29%'
        },
        'Censoring': 'Patients alive at last follow-up are censored observations',
        'Analysis Methods': 'Kaplan-Meier curves, Cox proportional hazards regression'
    },
    
    'Status': {
        'Description': 'Vital status at last follow-up',
        'Data Type': 'Categorical (Binary)',
        'Clinical Relevance': 'Primary endpoint indicating patient survival outcome. '
                             'Essential for survival analysis and prognostic modeling.',
        'Categories': {
            'Alive': 'Patient alive at last contact date',
            'Dead': 'Patient deceased (may be cancer-related or other cause)'
        },
        'Event Definition': {
            'Overall Survival': 'Death from any cause',
            'Cancer-Specific': 'Death attributed to breast cancer'
        },
        'Prognostic Impact': 'Outcome variable - Used to assess other factors'
    }
}

# =============================================================================
# DISPLAY VARIABLE DEFINITIONS
# =============================================================================

def display_variable_info(var_name):
    """Display detailed information about a specific variable."""
    if var_name in variable_descriptions:
        info = variable_descriptions[var_name]
        print(f"\n{'='*60}")
        print(f"VARIABLE: {var_name}")
        print('='*60)
        for key, value in info.items():
            if isinstance(value, dict):
                print(f"\n  {key}:")
                for sub_key, sub_value in value.items():
                    print(f"    - {sub_key}: {sub_value}")
            else:
                print(f"\n  {key}: {value}")
    else:
        print(f"Variable '{var_name}' not found in descriptions.")


def display_all_variables():
    """Display summary of all variables."""
    print("\n" + "=" * 70)
    print("VARIABLE SUMMARY TABLE")
    print("=" * 70)
    
    summary_data = []
    for var_name, info in variable_descriptions.items():
        summary_data.append({
            'Variable': var_name,
            'Type': info.get('Data Type', 'N/A'),
            'Prognostic Impact': info.get('Prognostic Impact', 'N/A'),
            'Description': info.get('Description', 'N/A')[:50] + '...'
        })
    
    df = pd.DataFrame(summary_data)
    print(df.to_string(index=False))
    return df


def get_clinical_context_report():
    """Generate a comprehensive clinical context report."""
    report = """
================================================================================
SEER BREAST CANCER DATASET - CLINICAL CONTEXT REPORT
================================================================================

OVERVIEW
--------
The SEER (Surveillance, Epidemiology, and End Results) Breast Cancer Dataset
contains population-based cancer registry data from the National Cancer 
Institute. This dataset is essential for understanding breast cancer 
epidemiology, treatment patterns, and survival outcomes.

VARIABLE CATEGORIES
-------------------

1. DEMOGRAPHIC VARIABLES
   - Age: Patient age at diagnosis
   - Race: Self-reported racial background
   - Marital Status: Social support indicator

2. TUMOR STAGING (TNM SYSTEM)
   - T Stage: Primary tumor size and extent
   - N Stage: Regional lymph node involvement
   - 6th Stage: AJCC overall stage grouping
   - A Stage: Regional vs Distant disease summary

3. TUMOR CHARACTERISTICS
   - Tumor Size: Primary tumor measurement (mm)
   - Grade: Histological differentiation level

4. BIOMARKERS
   - Estrogen Status: ER expression (hormone sensitivity)
   - Progesterone Status: PR expression (hormone sensitivity)

5. LYMPH NODE ASSESSMENT
   - Regional Node Examined: Nodes sampled for staging
   - Regional Node Positive: Nodes with metastatic disease

6. OUTCOME VARIABLES
   - Survival Months: Follow-up duration
   - Status: Vital status (Alive/Dead)

CLINICAL SIGNIFICANCE FOR CLUSTERING
------------------------------------

For DBSCAN clustering analysis, key considerations include:

1. PROGNOSTIC GROUPING:
   - Variables with high prognostic impact (N Stage, Grade, ER Status)
     can help identify clinically meaningful patient subgroups

2. TREATMENT RESPONSE:
   - Hormone receptor status defines treatment eligibility
   - Stage determines treatment intensity

3. SURVIVAL PATTERNS:
   - Combining clinical and pathological features reveals
     distinct survival profiles within the population

4. HEALTH DISPARITIES:
   - Demographic variables may reveal disparities in
     outcomes across population subgroups

RECOMMENDED ANALYSIS APPROACH
-----------------------------

1. Use ordinal encoding for staging variables (T, N, Grade)
2. Binary encoding for receptor status (ER, PR)
3. Consider interaction between variables (e.g., ER+/Grade I vs ER-/Grade III)
4. Validate clusters against survival outcomes
5. Profile clusters for clinical interpretability

================================================================================
Report Generated by: Cavin Otieno
================================================================================
"""
    return report


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Display all variable summaries
    summary_df = display_all_variables()
    
    # Show detailed info for key prognostic variables
    print("\n\n" + "=" * 70)
    print("KEY PROGNOSTIC VARIABLES - DETAILED VIEW")
    print("=" * 70)
    
    key_variables = ['N Stage', 'Grade', 'Estrogen Status', 'Survival Months']
    for var in key_variables:
        display_variable_info(var)
    
    # Generate clinical context report
    print(get_clinical_context_report())
    
    # Save variable descriptions to CSV
    output_dir = os.path.join(os.path.dirname('__file__'), 'output_v2', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert to DataFrame for export
    export_data = []
    for var_name, info in variable_descriptions.items():
        row = {'Variable': var_name}
        for key, value in info.items():
            if isinstance(value, dict):
                row[key] = str(value)
            else:
                row[key] = value
        export_data.append(row)
    
    export_df = pd.DataFrame(export_data)
    export_path = os.path.join(output_dir, 'variable_definitions.csv')
    export_df.to_csv(export_path, index=False)
    print(f"\n[INFO] Variable definitions saved to: {export_path}")
    
    print("\n" + "=" * 70)
    print("[OK] Variable definitions and clinical context loaded successfully!")
    print("=" * 70)
