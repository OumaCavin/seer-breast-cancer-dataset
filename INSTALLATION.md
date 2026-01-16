# Installation Guide

## Prerequisites

### Python Version
- **Required:** Python 3.12.3 (or compatible 3.12.x version)
- Check your version: `python3 --version`

### System Dependencies (Ubuntu/Debian)

Before installing Python packages, you may need system dependencies:

```bash
# Update package list
sudo apt update

# Install Python development headers (required for some packages)
sudo apt install python3.12-dev

# Install build tools (required for packages with C extensions)
sudo apt install build-essential

# Install Jupyter (alternative method if pip fails)
sudo apt install jupyter-core jupyter-notebook
```

### System Dependencies (Windows)

- Install Python 3.12.x from [python.org](https://www.python.org/downloads/)
- Ensure "Add Python to PATH" is checked during installation
- Install Visual Studio Build Tools if needed for C extensions

### System Dependencies (macOS)

```bash
# Install Xcode command line tools
xcode-select --install

# If using Homebrew:
brew install python@3.12
```

---

## Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/OumaCavin/seer-breast-cancer-dataset.git
cd seer-breast-cancer-dataset
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 3: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 4: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
# Check Jupyter is installed
jupyter --version

# Check Python packages
python -c "import numpy, pandas, sklearn, matplotlib, seaborn; print('All core packages installed successfully!')"
```

### Step 6: Launch Notebook

```bash
jupyter notebook SEER_DBSCAN_Clustering_Analysis.ipynb
```

---

## Troubleshooting

### Error: "jupyter: command not found"

**Solution 1:** Install via pip
```bash
pip install jupyter notebook
```

**Solution 2:** Install via apt (Ubuntu/Debian)
```bash
sudo apt install jupyter-core jupyter-notebook
```

**Solution 3:** Use Python module directly
```bash
python -m notebook SEER_DBSCAN_Clustering_Analysis.ipynb
```

### Error: "Python.h: No such file or directory"

This occurs when installing packages with C extensions (like hdbscan).

**Solution (Ubuntu/Debian):**
```bash
sudo apt install python3.12-dev build-essential
```

**Solution (macOS):**
```bash
xcode-select --install
```

**Note:** The hdbscan package is **optional** and not required for the main analysis. The notebook uses scikit-learn's DBSCAN which doesn't require compilation.

### Error: "ModuleNotFoundError: No module named 'xxx'"

**Solution:** Install the missing package
```bash
pip install xxx
```

### Error: Building wheel failed

**Solution:** Try installing pre-built wheels
```bash
pip install --only-binary :all: package_name
```

### Error: Permission denied

**Solution:** Use virtual environment (recommended) or user install
```bash
pip install --user -r requirements.txt
```

---

## Alternative Installation (Conda)

If pip installation fails, try using Conda:

```bash
# Create conda environment
conda create -n seer-analysis python=3.12
conda activate seer-analysis

# Install packages
conda install numpy pandas scipy scikit-learn matplotlib seaborn jupyter notebook statsmodels

# Install remaining packages via pip
pip install lifelines plotly tqdm openpyxl ipywidgets
```

---

## Package Overview

### Core Packages (Required)
| Package | Purpose |
|---------|---------|
| numpy | Numerical computing |
| pandas | Data manipulation |
| scipy | Scientific computing |
| scikit-learn | Machine learning (DBSCAN, K-Means, GMM, etc.) |
| matplotlib | Visualization |
| seaborn | Statistical visualization |
| jupyter/notebook | Interactive notebook environment |

### Analysis Packages (Required)
| Package | Purpose |
|---------|---------|
| statsmodels | Statistical analysis |
| lifelines | Survival analysis (Kaplan-Meier, log-rank) |
| plotly | Interactive visualizations |

### Utility Packages
| Package | Purpose |
|---------|---------|
| tqdm | Progress bars |
| joblib | Parallel processing |
| openpyxl | Excel file support |

### Optional Packages
| Package | Purpose | Note |
|---------|---------|------|
| hdbscan | Hierarchical DBSCAN | Requires C compiler, not essential |

---

## Verification Script

Create and run this script to verify your installation:

```python
#!/usr/bin/env python3
"""Verify SEER Breast Cancer Analysis Installation"""

import sys

def check_package(name, import_name=None):
    if import_name is None:
        import_name = name
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"  [OK] {name}: {version}")
        return True
    except ImportError:
        print(f"  [FAIL] {name}: NOT INSTALLED")
        return False

print(f"Python version: {sys.version}")
print("\nChecking required packages...")

packages = [
    ('numpy', 'numpy'),
    ('pandas', 'pandas'),
    ('scipy', 'scipy'),
    ('scikit-learn', 'sklearn'),
    ('matplotlib', 'matplotlib'),
    ('seaborn', 'seaborn'),
    ('jupyter', 'jupyter'),
    ('notebook', 'notebook'),
    ('statsmodels', 'statsmodels'),
    ('lifelines', 'lifelines'),
    ('plotly', 'plotly'),
]

all_ok = True
for name, import_name in packages:
    if not check_package(name, import_name):
        all_ok = False

if all_ok:
    print("\n[SUCCESS] All required packages are installed!")
    print("You can now run: jupyter notebook SEER_DBSCAN_Clustering_Analysis.ipynb")
else:
    print("\n[WARNING] Some packages are missing. Run: pip install -r requirements.txt")
```

Save as `verify_installation.py` and run:
```bash
python verify_installation.py
```

---

## Quick Start (After Installation)

```bash
# Navigate to project
cd seer-breast-cancer-dataset

# Activate environment
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Launch notebook
jupyter notebook SEER_DBSCAN_Clustering_Analysis.ipynb

# In Jupyter: Kernel → Restart & Run All
```

---

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Ensure Python 3.12.x is installed
3. Use a virtual environment
4. Check the `docs/` folder for methodology details

---

**Author:** Cavin Otieno  
**Repository:** https://github.com/OumaCavin/seer-breast-cancer-dataset
