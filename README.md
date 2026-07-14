<<<<<<< HEAD
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
=======
# 🏗️ Bengaluru Real Estate — Unified Analytics Dashboard

> **AI-Powered Six Sigma DMAIC + Geospatial Decision Support System for Bengaluru Real Estate**  
> Bagaluru Micro-Market · 25 Bengaluru Zones · Dec 2022 – Nov 2025

---

## 📌 Overview

This is a unified **Streamlit** dashboard that combines **two powerful analytical frameworks** into a single application for Bengaluru real estate analysis:

**🏙️ Six Sigma DMAIC Module** — Applies quality management methodology to residential real estate sales, identifying unsold inventory as "defects" and using ML models, SimPy simulation, and SPC control charts to find root causes and recommend corrective actions.

**🗺️ AI Map Decision Support System** — An intelligent geospatial platform that scores **25 Bengaluru micro-markets** on construction and investment suitability using a Random Forest ML model trained on 10 infrastructure and market variables.

Together the dashboard covers **18 project phases** across **9 developers** (10,000+ units) and **25 city zones** with interactive maps, radar charts, price analytics, and live simulations.

---

## ✨ Features

### 🏙️ Module 1 — Six Sigma DMAIC

#### 📊 Page 1 — Market Overview
- **5 KPI cards**: Total Units Launched, Units Sold, Units Unsold, Sigma Level (σ), At-Risk Projects
- **Absorption Rate Bar Chart** — per project, colour-coded: 🔴 <70% / 🟡 70–95% / 🟢 ≥95%
- **Donut Chart** — overall sold vs unsold split with centre annotation
- **Bubble Scatter Plot** — Price vs Absorption Rate (bubble size = total units, colour = status)
- **Six Sigma Level** — computed from DPMO (Defects Per Million Opportunities)
- **Builder Filter** — sidebar dropdown switches all charts between full market and single developer view

#### 🏢 Page 2 — Builder Deep Dive
- Per-developer KPIs: total units, sold %, unsold count, avg construction delay
- **Stacked Bar Chart** — sold vs unsold units per project (green / red)
- **Gradient Boosting Forecast vs Actual** — compares ML-predicted absorption against real performance
- Expandable **at-risk project cards** with ML defect probability and root cause details

#### 🤖 Page 3 — Digital Twin Simulator (SimPy)
- Select any project → configure base monthly sales rate and simulation duration (6–24 months)
- **Poisson-based event simulation** (`env.timeout(1)` = 1 month, SimPy discrete-event engine)
- **Segmented buyer model**: Budget buyers, Premium buyers, Normal buyers (weighted by price sensitivity, construction stage progress, and seasonal demand index)
- **Mid-simulation intervention**: inject a policy change (price cut, subvention scheme) at any chosen month
- **Charts**: Cumulative sales line, monthly sales bars, inventory remaining, segmented demand area chart
- Side-by-side baseline vs intervention curves with revenue recovery estimate in ₹ Crores

#### 💡 Page 4 — AI Recommendations Engine
- Recommendations **benchmarked from sold-out projects** (≥95% absorbed)
- Rule-based + ML engine covering 6 issue signals:
  - 💰 High price (>₹9,500/sqft) — price reduction + subvention scheme
  - 🏗️ Construction delay (>6 months) — fast-track guidance with specific benchmarks
  - 📐 Large unit size (>2,000 sqft) — floor plan redesign suggestion
  - ✈️ Luxury segment mismatch — NRI investor repositioning strategy
  - 📸 Early construction stage — virtual tours & live webcam trust-building
  - ⭐ Weak developer brand — CRISIL rating + bank home loan tie-up
- **Estimated recoverable units** per recommendation
- **Mini Digital Twin** preview — with vs without intervention impact

#### 📈 Page 5 — SPC Control Chart
- **Individual-Moving Range (I-MR) Chart** — correct Six Sigma standard (d2 = 1.128)
- **UCL/LCL** control limits using Moving Range σ; Out-of-Control detection (>3σ) 🔴
- **Runs Rules** (Western Electric): 8-consecutive-point violations, 6-point trend violations 🟡
- **Moving Range (MR) Chart** with D4 constant UCL
- **6-Month Forecast** (Dec 2025 – May 2026) using linear trend + seasonal correction with confidence bands
- OOC event table listing each violation month, value, and corrective action

---

### 🗺️ Module 2 — AI Map Decision Support System

#### 🏠 Page 1 — Home Dashboard
- **5 KPI cards**: Areas Covered, Average Price/sqft, Highest Growth Area, AI Top-Pick, High-Risk Zones
- **Top 5 areas** leaderboard by ML suitability score
- Feature guide explaining all 10 ML input variables

#### 📍 Page 2 — Interactive Map (Folium)
- **Folium map** (Leaflet.js) centred on Bengaluru — CartoDB dark base tiles
- **25 area markers** — colour-coded by ML score: 🟢 ≥75 / 🟡 50–74 / 🔴 <50
- **Click popups** showing: Score, Price/sqft, Road connectivity, Flood risk, Metro distance
- **13 Metro station markers** — Purple Line, Green Line, Yellow Line differentiated
- **Sidebar filters**: Flood Risk, Minimum AI Score slider, Market Segment
- Filterable data table below the map

#### 🤖 Page 3 — AI Suitability Analyzer
- **Radar/Spider Chart** — 6-axis polygon (Metro, Hospitals, Schools, Roads, Infrastructure, Population Growth)
- **AI Score Badge** — 🟢 Highly Suitable / 🟡 Moderate / 🔴 Less Suitable
- **Score Breakdown Table** — factor-by-factor contribution to the final score
- **AI Recommendation Box** — green success / yellow warning / red error with bullet-point analysis

#### 📊 Page 4 — Price Analytics (3 tabs)
- **Tab 1 — Price Overview**: Horizontal bar chart (Price/sqft by area), RdYlGn colour scale
- **Tab 2 — Trend Analysis**: Scatter (Flood Risk vs Price) + Bar chart (YoY price trend % by area)
- **Tab 3 — Correlation**: Heatmap showing statistical correlations between all numeric variables

#### 📋 Page 5 — Area Comparison
- Select 2–3 areas for side-by-side comparison
- **Metrics table** with all 10+ attributes compared
- **Radar comparison chart** — both areas on the same spider chart in different colours
- Score badges for instant visual comparison

#### 📈 Page 6 — DMAIC Charts
- **Pareto Chart** — 80/20 analysis of unsold inventory across all 25 areas
- **RF Feature Importance** — explainable AI showing which variables drive the suitability score
- **What-If Scenario Analyzer** — live ML prediction updates as you adjust sliders
- **SPC I-Chart** — applied to area-level price trend data

#### 🌡️ Page 7 — Heatmap View
- **Plotly Scattermapbox** — bubble size = population growth, colour = AI suitability score
- Hover cards: area name, score, price, trend, segment
- **Rankings leaderboard table** — areas sorted by AI score with full metrics

---


## 🗂️ Project Structure

```text
Bengaluru-Real-Estate-Dashboard/
│
├── app/
│   └── streamlit_app.py          # Unified Streamlit application (~2,150 lines)
│
├── data/
│   ├── Bagaluru - Micro Market Analysis(1).xlsx   # DMAIC dataset
│   └── bengaluru_realestate_dataset.xlsx          # AI Map dataset
│
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
>>>>>>> 5545aa9 (Updated Streamlit dashboard)
```

---

<<<<<<< HEAD
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
=======
## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sadiya211/Bengaluru-real-Estate-Dashboard.git
   cd Bengaluru-real-Estate-Dashboard
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   streamlit run app/streamlit_app.py
   ```

5. Open your browser at **`http://localhost:8501`**

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `pandas` | Data manipulation |
| `numpy` | Numerical computing |
| `plotly` | Interactive charts (bar, scatter, pie, radar, heatmap, mapbox) |
| `folium` | Interactive Leaflet.js maps |
| `streamlit-folium` | Folium map rendering inside Streamlit |
| `simpy` | Discrete-event simulation (Digital Twin) |
| `scikit-learn` | Random Forest + Gradient Boosting ML models |
| `openpyxl` | Excel data file reading |

---

## 📊 Datasets

### DMAIC Dataset — Bagaluru Micro-Market (18 Projects)

| Developer | Projects Covered | Tier |
|---|---|---|
| Brigade | El Dorado (Diora, Cobalt, Beryl), Aurum | Established |
| Godrej | Ananda III (H-K, P, M, L) | Established |
| Kalyani | Living Tree T1-T6, T3/T4 | Established |
| Puravankara | Provident Ecopolitan, Ecopolitan V | Established |
| Adarsh | Palm Acres III | Luxury/New |
| Kumar | Plumeria | Luxury/New |
| MJR | North Park | New |
| NVG | Rakshak | New |
| Sri Sai Dev | Dev Enclave | Small |

**Time period**: December 2022 – November 2025 (35 months of monthly absorption data)

### Map Dataset — 25 Bengaluru Zones

Whitefield, Electronic City, Koramangala, Indiranagar, HSR Layout, Sarjapur Road, Bagaluru, Hebbal, Yelahanka, Bannerghatta Road, JP Nagar, Malleswaram, Marathahalli, Bellandur, Panathur, Devanahalli, Kengeri, Rajajinagar, Jayanagar, BTM Layout, Thanisandra, Hennur, Kadugodi, Horamavu, Bommasandra

**10 features per area**: avg price/sqft, YoY trend, metro distance, hospital distance, school distance, highway distance, flood risk, road connectivity, infrastructure score, population growth, unsold %

---

## 🧠 Six Sigma DMAIC Framework Applied

| Phase | What was done |
|---|---|
| **Define** | Problem: ~10.5% unsold inventory across Bagaluru micro-market; defect = project with <70% absorption |
| **Measure** | DPMO calculation, Sigma Level (σ), SPC control charts, absorption rates per project |
| **Analyse** | Root cause identification — price, delay, unit size, segment mismatch, brand trust deficit |
| **Improve** | AI recommendations engine with estimated recoverable units; Digital Twin intervention modelling |
| **Control** | SPC I-MR Chart with real-time OOC detection, Runs Rules, and 6-month forward forecast |
>>>>>>> 5545aa9 (Updated Streamlit dashboard)

---

## 🤖 Machine Learning Models

<<<<<<< HEAD
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
=======
| Model | Algorithm | Purpose | Output |
|---|---|---|---|
| RF Classifier | Random Forest (200 trees, depth 5) | Classify projects as Defect / Healthy | P(defect) 0–1 |
| GB Regressor | Gradient Boosting (200 trees, depth 3, LR=0.05) | Predict expected % sold | Absorption % |
| RF Regressor | Random Forest (300 trees, depth 6) | Score 25 areas on construction suitability | Score 0–100 |

All models use **data augmentation** (10–15× Gaussian noise replication) to prevent overfitting on small datasets.

---

## 🔬 Technical Highlights

- **SimPy Digital Twin** with segmented buyer model (Budget / Premium / Normal buyers weighted by price sensitivity, construction stage, and seasonal demand index)
- **Proper I-MR Chart** implementation using d2 = 1.128 constant for correct Moving Range σ estimation
- **ML augmentation**: 10–15× data augmentation with Gaussian noise to train all three ML models on small datasets (18 projects / 25 areas)
- **Explainable AI**: Random Forest feature importance chart reveals which variables drive suitability scores
- **Runs Rule detection**: 8-consecutive-points same side of centre line + 6-point trending runs
- **Live What-If Analyzer**: real-time ML prediction updates as sidebar sliders are adjusted
>>>>>>> 5545aa9 (Updated Streamlit dashboard)

---

## 📄 License

<<<<<<< HEAD
This project is developed for academic and educational purposes.

---


=======
This project is open-source and available under the [MIT License](LICENSE).

---

## 🙋 Author

Built as a Six Sigma + AI analytics project for Bengaluru residential real estate micro-market analysis.  
Data source: Bagaluru Micro Market Analysis (proprietary field research) + 25-zone infrastructure dataset.

---

*Built with ❤️ using Streamlit · SimPy · Plotly · Folium · scikit-learn*
>>>>>>> 5545aa9 (Updated Streamlit dashboard)
