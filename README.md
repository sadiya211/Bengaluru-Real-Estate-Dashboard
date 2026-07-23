Bengaluru Real Estate - Six Sigma DMAIC Dashboard
An interactive Streamlit dashboard for analysing the Bagaluru Micro-Market real estate data (Dec 2022 - Nov 2025) using the Six Sigma DMAIC framework, a SimPy-powered Digital Twin simulator, AI recommendations, and SPC control charts.

Features
1. Market Overview
KPI cards: Total Units, Units Sold, Units Unsold, Sigma Level, Projects At-Risk
Absorption Rate by Project (horizontal bar chart with 70% target line)
Sold vs Unsold Split (donut chart)
Price vs Absorption bubble chart
By-Segment breakdown (Luxury / Mid / Plots)
2. Builder Deep Dive
Filter by individual developer/builder
Project-level absorption table with colour-coded health tags (Healthy / At Risk / Moderate)
Unit-mix analysis (sold vs unsold by unit type)
Price sensitivity scatter plot
Construction stage vs absorption comparison
3. Digital Twin Simulator (SimPy)
Select any project and simulate future sales over 6-24 months
Set a base monthly sales rate using real absorption data
Apply a mid-simulation intervention (e.g. price cut, subvention scheme) at any chosen month
Side-by-side comparison: Baseline vs Intervention trajectory
Sellout prediction: estimated month when inventory reaches zero
4. AI Recommendations Engine
Automatically learns from top-performing (healthy) projects
Detects issues: high price, construction delay, low unit-mix fit, slow absorption
Outputs prioritised HIGH / MEDIUM / LOW recommendations per project
Batch scan: one-click analysis of all At-Risk projects
5. SPC Control Chart
Individual (I) Control Chart for monthly absorption rates
Moving Range (MR) chart
UCL / LCL / Centre-line calculated using standard SPC formulas
Flags out-of-control points (red markers)
Forecast extension using linear regression
Tech Stack
Library	Purpose
streamlit	Web dashboard framework
pandas	Data manipulation
numpy	Numerical computing
plotly	Interactive charts
simpy	Discrete-event simulation (Digital Twin)
scikit-learn	Linear regression for SPC forecast
openpyxl	Excel file support
Project Structure

Bengaluru-Real-Estate-Dashboard/
|
|-- app/
|   |-- streamlit_app.py        # Main Streamlit application
|
|-- data/
|   |-- Bagaluru - Micro Market Analysis(1).xlsx
|
|-- requirements.txt            # Python dependencies
|-- README.md                  
Getting Started
Prerequisites
Python 3.8 or higher
pip
Installation
Clone or download this repository.

Open a terminal and navigate to the project folder:

powershell

cd "C:\Users\anmol\OneDrive\Desktop\Bengaluru-Real-Estate-Dashboard"
Install dependencies:
powershell

pip install -r requirements.txt
Run the app:
powershell

streamlit run app/streamlit_app.py
Open your browser at: http://localhost:8501
Tip: If streamlit is not recognised, try: python -m streamlit run app/streamlit_app.py

Data
The dashboard uses embedded project data for 18 residential projects in the Bagaluru Micro-Market, Bengaluru, covering the period December 2022 to November 2025.

Key data fields:

Field	Description
project	Project name
developer	Builder / developer name
developer_tier	Category: Established / Luxury-New / New
segment	Luxury / Mid / Plots
total_units	Total units launched
absorbed_units	Units sold to date
unsold_units	Unsold inventory
pct_sold	Absorption percentage
price_sqft	Price per square foot (Rs.)
delay_months	Construction delay in months
construction_stage	Stage of construction (0-5)
Six Sigma DMAIC Framework
The dashboard is structured around the DMAIC methodology:

Phase	What the dashboard does
Define	Identifies at-risk projects (less than 70% sold) as defects
Measure	Calculates DPMO and Sigma Level from absorption data
Analyse	Bubble charts, deep-dive comparisons, segment breakdowns
Improve	Digital Twin simulation of interventions
Control	SPC control charts to monitor ongoing absorption
Sigma Level formula used:


DPMO = (Unsold Units / Total Units) * 1,000,000
Sigma = 0.8406 + sqrt(29.37 - 2.221 * ln(DPMO))
Target: Sigma >= 4.0  (equivalent to less than 30% unsold)
