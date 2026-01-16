# SEER Breast Cancer Dataset

A curated dataset of breast cancer patients from the Surveillance, Epidemiology, and End Results (SEER) Program of the National Cancer Institute (NCI).

## Dataset Overview

This dataset was obtained from the 2017 November update of the SEER Program, which provides population-based cancer statistics for the United States.

## Features

| Column | Description |
|--------|-------------|
| Age | Patient age at diagnosis |
| Race | Patient race/ethnicity |
| Marital Status | Patient marital status |
| T Stage | Primary tumor stage (T1-T4) |
| N Stage | Regional lymph node involvement (N0-N3) |
| 6th Stage | AJCC 6th edition cancer stage |
| Grade | Tumor differentiation grade |
| A Stage | Regional or Distant stage |
| Tumor Size | Tumor size in millimeters |
| Estrogen Status | Estrogen receptor status (Positive/Negative) |
| Progesterone Status | Progesterone receptor status (Positive/Negative) |
| Regional Node Examined | Number of regional lymph nodes examined |
| Regional Node Positive | Number of positive regional lymph nodes |
| Survival Months | Patient survival time in months |
| Status | Patient vital status (Alive/Dead) |

## Data Source

- **Source:** SEER Program, National Cancer Institute
- **Update:** November 2017
- **Format:** CSV

## Usage

```python
import pandas as pd

# Load the dataset
df = pd.read_csv('SEER_Breast_Cancer_Dataset.csv')

# Display basic info
print(df.info())
print(df.head())
```

## License

This dataset is provided for research and educational purposes. Please cite the SEER Program when using this data.

## Author

Curated by Cavin Otieno
