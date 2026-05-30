# 🏗️ Six Sigma DMAIC — Bengaluru Real Estate Market Optimization
> **Applying Six Sigma methodology with Machine Learning & Digital Twin simulation to reduce unsold inventory and stabilize pricing in the Bagaluru micro-market, Bengaluru.**
---
## 📌 Project Overview
This project applies the **Six Sigma DMAIC framework** (Define → Measure → Analyze → Improve → Control) to the Bengaluru real estate sector, specifically the **Bagaluru Micro-Market** (Dec 2022 – Nov 2025).
The Bagaluru corridor (near BIAL, NH-44) saw rapid project launches leading to inventory pile-up, pricing inconsistency, and demand-supply mismatch. This project uses data analytics, machine learning, and discrete-event simulation (Digital Twin) to identify root causes and recommend corrective actions.
---
## 🎯 Problem Statement
|
 Metric 
|
 Baseline 
|
 Target 
|
|
--------
|
----------
|
--------
|
|
 Process Sigma Level 
|
 ~2.5σ 
|
 ≥ 4σ 
|
|
 Unsold Inventory Rate 
|
 ~16.7% (1,741 units) 
|
 < 10% 
|
|
 DPMO 
|
 ~167,000 
|
 < 6,210 
|
|
 At-Risk Projects (<70% sold) 
|
 6 out of 18 
|
 0 
|
**CTQ (Critical to Quality):** Percentage of units sold per project ≥ 70% (threshold) / ≥ 95% (target).
**Defect Definition:** Any residential project with less than 70% unit absorption.
---
## 🏗️ DMAIC Framework Applied
### 📋 Define
- Project charter, SIPOC diagram, stakeholder mapping
- CTQ: % units sold per project
- Dataset: 18 residential projects, 10,283 total units launched
### 📏 Measure
- Baseline Sigma = **2.5σ** | DPMO = **167,000**
- Total units: **10,283** | Sold: **8,542** (83%) | Unsold: **1,741** (17%)
- 6 out of 18 projects identified as "At-Risk" (<70% absorption)
- I-MR Statistical Process Control chart established on monthly absorption data (Jan 2023 baseline)
### 🔍 Analyze
- **Pareto Analysis**: Top 3 root causes account for ~80% of unsold units:
  1. 🔴 **High Price (>₹9,500/sqft)** — affects projects like Adarsh Palm Acres III (₹17,285/sqft, only 11% sold) and Kumar Plumeria (₹10,500/sqft, 17% sold)
  2. 🔴 **Construction Delays** — North Park (19-month delay, 79% sold), Godrej Ananda III (9-month delay)
  3. 🟡 **Post-Saturation Launch** — projects launched in late 2024/2025 into an already saturated market
- **Random Forest Feature Importance**: Price/sqft → Developer Brand → Months on Market → Delay Months
- **Correlation Heatmap**: Strong negative correlation between price/sqft and % sold (r = -0.72)
### ⚙️ Improve
- Gradient Boosting What-If simulator: projects interventions like price cuts, subvention schemes, CRISIL ratings
- **Digital Twin (SimPy)**: Discrete-event simulation of monthly sales processes with Poisson buyer arrival model
- Monte Carlo scenario analysis with mid-simulation policy injection
- Recommendations engine trained on patterns from 100%-sold projects (Brigade El Dorado, Provident Ecopolitan)
### 📊 Control
- **SPC I-MR Control Chart**: Monthly absorption monitored against Jan–Dec 2023 baseline
  - UCL: ~590 units/month | CL: ~217 units/month | LCL: ~0
  - Western Electric Rules applied (OOC, 2-of-3, trend, run rules)
- Streamlit real-time dashboard with automated sigma drift alerts
---
## 🗂️ Dataset
**Source:** Bagaluru Micro-Market Analysis (`Bagaluru - Micro Market Analysis(1).xlsx`)
|
 Attribute 
|
 Details 
|
|
-----------
|
---------
|
|
 Projects 
|
 18 residential project phases 
|
|
 Developers 
|
 Adarsh, Brigade, Godrej, Kalyani, Kumar, MJR, NVG, Puravankara, Sri Sai Dev 
|
|
 Segments 
|
 Luxury, Mid, Plots 
|
|
 Location Types 
|
 Highway Corridor, Mid Bagaluru, Inner Bagaluru 
|
|
 Time Period 
|
 Dec 2022 – Nov 2025 (35 months of monthly absorption data) 
|
|
 Key Features 
|
 price_sqft, total_units, absorbed_units, delay_months, construction_stage, BHK range, unit size 
|
**Defect label:** `is_defect = 1` if `pct_sold < 70%`
---
## 🤖 Machine Learning Models
### Random Forest Classifier
- **Task:** Classify projects as "At-Risk" or "Healthy"
- **Features:** Price/sqft, Avg Unit Size, BHK Min, Delay Months, Developer Brand Score, Construction Stage, Months on Market, Total Units
- **Training:** Data augmented 10× with Gaussian noise (RandomState=42); 200 trees, max_depth=5
- **Validation:** Cross-validation (min(5, class_size) folds)
### Gradient Boosting Regressor
- **Task:** Predict % units sold for What-If scenario simulation
- **Config:** 200 estimators, max_depth=3, learning_rate=0.05, subsample=0.8
- **Output:** Before/After % sold under interventions + units recoverable estimate
### Key Findings
- Projects priced **< ₹8,000/sqft** show near-100% absorption
- **Established developer brand** (Brigade, Godrej, Puravankara) is second strongest predictor of success
- Construction stage at Interior/Finishing/Ready correlates with faster clearance
---
## 🌐 Digital Twin (SimPy Simulation)
The Digital Twin creates a **virtual replica of the real estate sales process**:
```python
env = simpy.Environment()   # simulation clock
env.timeout(1)              # advances 1 month
Poisson(rate)               # stochastic monthly buyer arrivals
```
**Three buyer segments modeled:**
- 🏠 **Budget Buyers** — price-sensitive; rate ↑ as price ↓
- 🏢 **Premium Buyers** — stage-sensitive; rate ↑ as construction nears completion  
- 📊 **Normal Buyers** — demand-index driven; follows seasonal market cycles
**Intervention injection:** At any month N, inject a policy change (price cut, subvention scheme, marketing push) and observe how the absorption curve shifts.
---
## 📊 Streamlit Dashboard
### Run Locally
```bash
pip install streamlit pandas numpy plotly scikit-learn simpy
streamlit run streamlit_app.py
```
### Dashboard Pages
|
 Page 
|
 DMAIC Phase 
|
 Description 
|
|
------
|
------------
|
-------------
|
|
 📊 Market Overview 
|
 Measure 
|
 KPI cards, absorption bar chart, sold vs unsold donut, price vs absorption bubble 
|
|
 🏢 Builder Deep Dive 
|
 Measure 
|
 Per-developer stacked bar, project table with status, at-risk expanders 
|
|
 🤖 Digital Twin Simulator 
|
 Improve 
|
 SimPy sales simulation, intervention modeling, event log 
|
|
 💡 AI Recommendations 
|
 Improve 
|
 Pattern-learned recommendations from 100%-sold projects 
|
|
 📈 SPC Control Chart 
|
 Control 
|
 I-MR chart, Western Electric signal detection, violation table 
|
### Alternative Dashboard
```bash
streamlit run dashboard.py
```
Includes additional tabs: Root Cause Analysis (Pareto), ML Feature Importance, What-If Simulator, Sold vs Unsold Reasons, Digital Twin with Monte Carlo.
---
## 📁 Project Structure
```
six sigmas/
│
├── streamlit_app.py              # Main Streamlit dashboard (builder-focused)
├── dashboard.py                  # Extended dashboard (7 tabs, full DMAIC)
├── project.ipynb                 # Jupyter notebook — full analysis pipeline
├── Untitled5.ipynb               # Supporting analysis notebook
├── Untitled7 (1).ipynb           # Supporting analysis notebook
│
├── Bagaluru - Micro Market       # Primary dataset (Excel)
│   Analysis(1).xlsx
│
├── ieee_paper.tex                # IEEE-format research paper (LaTeX)
├── poster.html                   # Academic conference poster (HTML)
├── six sigma.pptx                # Project presentation
├── Puravankara_PPT_Template.pptx # Case study template
├── Presentation_Explanation_     # Slide-by-slide guide (Word)
│   Guide.docx
│
├── generate_presentation_doc.py  # Script to auto-generate presentation doc
├── six_sigma_implementation_     # Implementation plan
│   plan.md
└── README.md                     # This file
```
---
## 🔑 Key Results
|
 Metric 
|
 Value 
|
|
--------
|
-------
|
|
 Total Units Launched 
|
 10,283 
|
|
 Units Sold 
|
 8,542 (83.1%) 
|
|
 Units Unsold 
|
 1,741 (16.9%) 
|
|
 Process Sigma 
|
 ~2.5σ 
|
|
 At-Risk Projects 
|
 6 / 18 
|
|
 Top Root Cause 
|
 High price (>₹9.5k/sqft) 
|
|
 Biggest Recovery Potential 
|
 Adarsh Palm Acres III (174 units via price cut) 
|
|
 SPC OOC Events Detected 
|
 Multiple (Jul-23, Nov-23, Dec-24 — positive demand spikes) 
|
---
## 🏆 Notable Project Benchmarks
|
 Project 
|
 Developer 
|
 % Sold 
|
 Why It Succeeded 
|
|
---------
|
-----------
|
--------
|
-----------------
|
|
 Brigade El Dorado (Cobalt) 
|
 Brigade 
|
 100% 
|
 Established brand, ₹8,860/sqft, launched Q2 2024 
|
|
 Provident Ecopolitan 
|
 Puravankara 
|
 96.2% 
|
 Affordable ₹6,342/sqft, 956 units, strong brand 
|
|
 Kalyani Living Tree T1-T6 
|
 Kalyani 
|
 80.1% 
|
 Mid-price ₹7,490/sqft, 1,686 units (large scale) 
|
|
 Adarsh Palm Acres III 
|
 Adarsh 
|
 11.2% 
|
 Luxury at ₹17,285/sqft — overshoots market 
|
|
 Kumar Plumeria 
|
 Kumar 
|
 17.0% 
|
 ₹10,500/sqft + new brand + early stage 
|
---
## 🛠️ Tech Stack
|
 Tool 
|
 Purpose 
|
|
------
|
---------
|
|
 Python 3.10+ 
|
 Core language 
|
|
 Pandas / NumPy 
|
 Data wrangling 
|
|
 Plotly / Plotly Express 
|
 Interactive charts 
|
|
 Scikit-learn 
|
 Random Forest, Gradient Boosting, CV 
|
|
 SimPy 
|
 Discrete-event Digital Twin simulation 
|
|
 Streamlit 
|
 Web dashboard 
|
|
 LaTeX 
|
 IEEE paper 
|
---
## 🌍 SDG Alignment
- 🟥 **SDG 11** — Sustainable Cities & Communities (affordable housing access)
- 🟧 **SDG 8** — Decent Work & Economic Growth (real estate market efficiency)
- 🟦 **SDG 9** — Industry, Innovation & Infrastructure (data-driven construction)
- 🟥 **SDG 1** — No Poverty (reducing housing cost barriers)
---
## 📄 Research Paper
An IEEE-format paper is included (`ieee_paper.tex`) covering:
- Literature review of Six Sigma in real estate
- DMAIC methodology applied to micro-market data
- ML model architecture and validation
- Digital Twin design and SimPy implementation
- SPC control chart methodology (I-MR)
- Results, discussion, and future work
---
## 👤 Author
**Anmol Sharma**  
B.Tech, Computer Science & Engineering (AI & ML)  
Dayananda Sagar University, Bengaluru  
---
## 📜 License
This project is for academic and educational purposes.  
Dataset sourced from publicly available Bagaluru micro-market real estate records.
---
> *"In God we trust; all others must bring data."* — W. Edwards Deming
