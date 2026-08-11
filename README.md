# 🏙️ Bengaluru Real Estate – Six Sigma DMAIC Dashboard

An interactive **Streamlit dashboard** for analysing the **Bagaluru Micro-Market real estate data (December 2022 – November 2025)** using the **Six Sigma DMAIC framework**, a **SimPy-powered Digital Twin simulator**, **AI recommendations**, and **SPC control charts**.

---

## 🚀 Live Demo

👉 [**Open Bengaluru Real Estate – Six Sigma DMAIC Dashboard**](https://bengaluru-real-estate-dashboard-o7kf7xxnbspwwowyvnose6.streamlit.app/)

## 🚀 Features

### 📊 Market Overview

- **KPI Cards**
  - Total Units
  - Units Sold
  - Units Unsold
  - Sigma Level
- **Projects At-Risk**
- **Absorption Rate by Project**
  - Horizontal bar chart
  - 70% target line
- **Sold vs Unsold Split**
  - Donut chart
- **Price vs Absorption**
  - Interactive bubble chart
- **By-Segment Breakdown**
  - Luxury
  - Mid
  - Plots

---

## 🏗️ Builder Deep Dive

- Filter by individual developer / builder
- Project-level absorption table
- Colour-coded health tags:
  - 🟢 Healthy
  - 🟡 Moderate
  - 🔴 At Risk
- Unit-mix analysis (sold vs unsold by unit type)
- Price sensitivity scatter plot
- Construction stage vs absorption comparison

---

## 🤖 Digital Twin Simulator (SimPy)

A SimPy-powered Digital Twin simulator for evaluating future sales and interventions.

- Select any project
- Simulate future sales over **6–24 months**
- Set a base monthly sales rate using real absorption data
- Apply a mid-simulation intervention at any chosen month
- Example interventions:
  - Price cut
  - Subvention scheme
- Side-by-side comparison:
  - Baseline trajectory
  - Intervention trajectory
- Sellout prediction:
  - Estimated month when inventory reaches zero

---

## 🧠 AI Recommendations Engine

Automatically learns from **top-performing (healthy) projects**.

### Detects Issues

- High price
- Construction delay
- Low unit-mix fit
- Slow absorption

### Recommendation Priority

- 🔴 **HIGH**
- 🟡 **MEDIUM**
- 🟢 **LOW**

### Batch Scan

One-click analysis of **all At-Risk projects** with prioritised recommendations per project.

---

## 📈 SPC Control Chart

- **Individual (I) Control Chart** for monthly absorption rates
- **Moving Range (MR) chart**
- UCL / LCL / Centre-line calculated using standard SPC formulas
- Flags out-of-control points with red markers
- Forecast extension using linear regression

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| **Streamlit** | Web dashboard framework |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical computing |
| **Plotly** | Interactive charts |
| **SimPy** | Discrete-event simulation (Digital Twin) |
| **Scikit-learn** | Linear regression for SPC forecast |
| **OpenPyXL** | Excel file support |

---

## 📁 Project Structure

```text
Bengaluru-Real-Estate-Dashboard/
│
├── app/
│   └── streamlit_app.py       # Main Streamlit application
│
├── data/
│   └── Bagaluru - Micro Market Analysis(1).xlsx
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

Clone or download this repository.

```bash
git clone https://github.com/sadiya211/Bengaluru-Real-Estate-Dashboard.git
cd Bengaluru-Real-Estate-Dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app/streamlit_app.py
```

If Streamlit is not recognised, use:

```bash
python -m streamlit run app/streamlit_app.py
```

Open your browser at:

```text
http://localhost:8501
```

---

## 📊 Data

The dashboard uses embedded project data for **18 residential projects** in the **Bagaluru Micro-Market, Bengaluru**, covering:

**December 2022 – November 2025**

### 🔑 Key Data Fields

| Field | Description |
|---|---|
| `project` | Project name |
| `developer` | Builder / developer name |
| `developer_tier` | Category: Established / Luxury-New / New |
| `segment` | Luxury / Mid / Plots |
| `total_units` | Total units launched |
| `absorbed_units` | Units sold to date |
| `unsold_units` | Unsold inventory |
| `pct_sold` | Absorption percentage |
| `price_sqft` | Price per square foot (Rs.) |
| `delay_months` | Construction delay in months |
| `construction_stage` | Stage of construction (0–5) |

---

## 📐 Six Sigma DMAIC Framework

The dashboard is structured around the **DMAIC methodology**:

| Phase | What the Dashboard Does |
|---|---|
| **Define** | Identifies at-risk projects (less than 70% sold) as defects |
| **Measure** | Calculates DPMO and Sigma Level from absorption data |
| **Analyse** | Bubble charts, deep-dive comparisons, segment breakdowns |
| **Improve** | Digital Twin simulation of interventions |
| **Control** | SPC control charts to monitor ongoing absorption |

---

## 🧮 Sigma Level Formula

### DPMO

```text
DPMO = (Unsold Units / Total Units) × 1,000,000
```

### Sigma

```text
Sigma = 0.8406 + √(29.37 - 2.221 × ln(DPMO))
```

### 🎯 Target

```text
Sigma ≥ 4.0
```

Equivalent to:

```text
Less than 30% unsold
```

---

## 🔄 DMAIC Application

### 1. Define

Identifies at-risk projects with **less than 70% sold** and treats them as defects.

### 2. Measure

Calculates:

- Total units
- Sold units
- Unsold units
- Absorption percentage
- DPMO
- Sigma Level

### 3. Analyse

Uses:

- Bubble charts
- Builder comparisons
- Segment breakdowns
- Unit-mix analysis
- Price sensitivity
- Construction stage
- Construction delays
- Project-level absorption

### 4. Improve

Uses the Digital Twin Simulator to evaluate interventions such as:

- Price cuts
- Subvention schemes

### 5. Control

Uses SPC control charts to monitor:

- Monthly absorption
- UCL
- LCL
- Centre line
- Out-of-control points
- Forecasted absorption trend

---

## 🎯 Project Objective

The dashboard combines **real estate analytics, Six Sigma methodology, simulation, AI recommendations, and statistical process control** to identify underperforming residential projects and evaluate potential strategies for improving inventory absorption.
