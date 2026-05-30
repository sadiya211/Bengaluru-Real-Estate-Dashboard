# 🏗️ Six Sigma DMAIC – Bengaluru Real Estate Market Optimization

**AI-Driven Six Sigma Dashboard with Machine Learning & Digital Twin Simulation for Bengaluru Real Estate Analysis**

> Applying the Six Sigma DMAIC framework, Machine Learning, Statistical Process Control (SPC), and Digital Twin Simulation to optimize inventory absorption and stabilize pricing in Bengaluru's Bagaluru Micro-Market.

---

## 📌 Project Overview

This project applies the **Six Sigma DMAIC (Define–Measure–Analyze–Improve–Control)** methodology to Bengaluru's real estate sector, specifically the **Bagaluru Micro-Market**.

The dashboard analyzes residential projects launched between **December 2022 and November 2025**, identifies root causes of unsold inventory, predicts project health using Machine Learning, and evaluates improvement strategies through Digital Twin Simulation.

---

## 🎯 Problem Statement

| Metric                | Baseline | Target  |
| --------------------- | -------- | ------- |
| Process Sigma Level   | ~2.5σ    | ≥ 4σ    |
| Unsold Inventory Rate | ~16.9%   | < 10%   |
| DPMO                  | ~167,000 | < 6,210 |
| At-Risk Projects      | 6 of 18  | 0       |

### Critical-to-Quality (CTQ)

A project is considered healthy when:

* Absorption Rate ≥ 70%
* Target Performance ≥ 95%

### Defect Definition

Any residential project with:

```text
Absorption Rate < 70%
```

---

## 🏗️ DMAIC Framework

### 📋 Define

* Defined project charter and stakeholder requirements
* Identified CTQ metric as percentage of units sold
* Analyzed 18 residential projects across Bagaluru

### 📏 Measure

* Total Units: 10,283
* Sold Units: 8,542
* Unsold Units: 1,741
* Absorption Rate: 83.1%
* Sigma Level: ~2.5σ

Implemented SPC I-MR control charts to establish baseline process performance.

### 🔍 Analyze

#### 🔴 High Pricing

Projects above ₹9,500/sqft show significantly lower absorption.

#### 🔴 Construction Delays

Delayed projects experience slower inventory movement.

#### 🟡 Post-Saturation Launches

Projects launched during saturated market periods face lower demand.

Machine Learning analysis revealed the strongest performance drivers:

1. Price per sqft
2. Developer Brand
3. Months on Market
4. Delay Months

### ⚙️ Improve

Implemented:

* AI Recommendation Engine
* What-If Simulator
* Digital Twin Simulation
* Monte Carlo Analysis
* Gradient Boosting Forecast Models

### 📊 Control

Used:

* I-Chart
* MR-Chart
* Western Electric Rules
* Real-Time Dashboard Monitoring
* Sigma Drift Alerts

---

## 📂 Dataset

### Source

Bagaluru Micro-Market Analysis Dataset

### Dataset Summary

| Attribute   | Details             |
| ----------- | ------------------- |
| Projects    | 18                  |
| Developers  | 9                   |
| Period      | Dec 2022 – Nov 2025 |
| Total Units | 10,283              |
| Segments    | Luxury, Mid, Plots  |

### Key Features

* price_sqft
* total_units
* absorbed_units
* delay_months
* construction_stage
* bhk_range
* unit_size

---

## 🤖 Machine Learning Models

### Random Forest Classifier

**Purpose:** Identify At-Risk Projects

Features Used:

* Price/sqft
* Unit Size
* Delay Months
* Brand Score
* Construction Stage
* Months on Market

### Gradient Boosting Regressor

**Purpose:** Forecast Future Absorption Rates

Outputs:

* Predicted Absorption
* Recovery Potential
* What-If Scenario Evaluation

---

## 🌐 Digital Twin Simulation

A SimPy-based virtual model replicates the real estate sales process.

### Buyer Segments

🏠 Budget Buyers

🏢 Premium Buyers

📊 Normal Buyers

### Simulation Features

* Monthly Sales Forecasting
* Demand Variation Modeling
* Intervention Testing
* Price Cut Analysis
* Marketing Campaign Impact

---

## 📊 Dashboard Features

### Market Overview

* KPI Cards
* Absorption Analysis
* Sold vs Unsold Split
* Price vs Absorption Analysis

### Builder Deep Dive

* Developer Performance
* At-Risk Project Detection
* Comparative Analysis

### AI Recommendation Engine

* Root Cause Analysis
* Recovery Strategies
* Risk Alerts

### Digital Twin Simulator

* Scenario Testing
* Demand Simulation
* Recovery Forecasts

### SPC Control Charts

* Individual Control Chart
* Moving Range Chart
* Violation Detection

---

## 📁 Project Structure

```text
Bengaluru-Real-Estate-Dashboard
│
├── app
│   └── streamlit_app.py
│
├── data
│   └── Bagaluru_Micro_Market_Analysis.xlsx
│
├── screenshots
│   ├── absorption_rate_by_project.png
│   ├── sold_vs_unsold_split.png
│   ├── price_vs_absorption.png
│   ├── individual_control_chart.png
│   ├── moving_range_chart_forecast.png
│   └── digital_twin_simulation.png
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🏆 Key Results

| Metric           | Value  |
| ---------------- | ------ |
| Total Units      | 10,283 |
| Units Sold       | 8,542  |
| Units Unsold     | 1,741  |
| Absorption Rate  | 83.1%  |
| Sigma Level      | ~2.5σ  |
| At-Risk Projects | 6      |

### Biggest Recovery Opportunity

**Adarsh Palm Acres III**

Potential recovery through pricing intervention.

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* Scikit-Learn
* SimPy
* OpenPyXL
* Git & GitHub

---

## 🌍 Sustainable Development Goals (SDGs)

* SDG 11 – Sustainable Cities & Communities
* SDG 8 – Decent Work & Economic Growth
* SDG 9 – Industry, Innovation & Infrastructure
* SDG 1 – No Poverty

---

## ▶️ Run Locally

```bash
git clone https://github.com/sadiya211/Bengaluru-Real-Estate-Dashboard.git

cd Bengaluru-Real-Estate-Dashboard

pip install -r requirements.txt

streamlit run app/streamlit_app.py
```

---

## 👥 Team Members

* Shaik Sadiya Anmol
* Veekshitha P
* Jeevana Sai S
* T Vaishnavi

---

## 📄 License

This project is developed for academic and educational purposes.

---


