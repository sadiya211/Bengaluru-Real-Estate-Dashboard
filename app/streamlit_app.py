"""
╔══════════════════════════════════════════════════════════════════════════╗
║  BENGALURU REAL ESTATE — UNIFIED DASHBOARD                              ║
║  Six Sigma DMAIC + AI Map Decision Support System                       ║
║  Builder Selector · Digital Twin Simulator · Recommendations            ║
║  Interactive Map · ML Suitability Scorer · Price Analytics              ║
║                                                                          ║
║  Run:  streamlit run streamlit_app.py                                   ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, RandomForestRegressor
import simpy
import warnings
warnings.filterwarnings('ignore')

# ── Try importing folium ──────────────────────────────────────────────────
try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_OK = True
except ImportError:
    FOLIUM_OK = False

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bengaluru Real Estate — Unified Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS  (merged from both files)
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}

/* ── DMAIC styles ───────────────────────────────────────────── */
.metric-card {
    background: white; border-radius: 12px; padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 12px;
    border-left: 5px solid #2E75B6;
}
.metric-card.red  { border-left-color: #E24B4A; }
.metric-card.green{ border-left-color: #16A34A; }
.metric-card.amber{ border-left-color: #EF9F27; }
.metric-val  { font-size: 2rem; font-weight: 700; color: #1e2d5a; }
.metric-label{ font-size: 0.82rem; color: #64748b; margin-top: 2px; }
.section-head {
    background: linear-gradient(135deg, #1e2d5a 0%, #2E75B6 100%);
    color: white; padding: 12px 20px; border-radius: 10px;
    font-size: 1.1rem; font-weight: 600; margin: 18px 0 12px 0;
}
.rec-box {
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 10px; padding: 14px 18px; margin: 8px 0;
}
.rec-box.warn {
    background: #fefce8; border-color: #fde68a;
}
.rec-box.info {
    background: #eff6ff; border-color: #bfdbfe;
}
.twin-box {
    background: #1e293b; color: #38bdf8;
    border-radius: 12px; padding: 18px;
    font-family: 'Courier New', monospace; font-size: 0.85rem;
}
.tag-sold   { background:#dcfce7; color:#166534; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
.tag-unsold { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
.tag-mid    { background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
h2 { color: #1e2d5a !important; }
.stSelectbox label { font-weight: 600; color: #334155; }

/* ── Global white background ────────────────────────────────── */
.main { background: #ffffff !important; }
.block-container { background: #ffffff !important; }

/* ── Map / AI KPI cards — light theme ───────────────────────── */
.kpi{background:linear-gradient(135deg,#f0f4ff,#e8eeff);border:1px solid #c7d2fe;
     border-radius:14px;padding:18px 22px;text-align:center;
     box-shadow:0 4px 20px rgba(99,102,241,0.1);transition:transform .2s;}
.kpi:hover{transform:translateY(-3px);box-shadow:0 8px 28px rgba(99,102,241,0.18);}
.kpi-t{font-size:11px;font-weight:600;color:#6366f1;letter-spacing:1.1px;text-transform:uppercase;margin-bottom:6px;}
.kpi-v{font-size:28px;font-weight:700;color:#1e2d5a;}
.kpi-s{font-size:11px;color:#64748b;margin-top:3px;}
.good{color:#16a34a!important;} .bad{color:#dc2626!important;} .warn{color:#d97706!important;}

/* ── Section header ─────────────────────────────────────────── */
.sec{font-size:16px;font-weight:700;color:#1e2d5a;border-left:4px solid #6366f1;
     padding-left:12px;margin:22px 0 14px;}

/* ── Area cards — light theme ───────────────────────────────── */
.area-card{background:linear-gradient(135deg,#f8faff,#eef2ff);border:1px solid #c7d2fe;
           border-radius:12px;padding:16px;margin:6px 0;color:#1e2d5a;}
.area-card b { color: #1e2d5a !important; }
.area-card span { color: #475569 !important; }

/* ── Score badges (keep colored) ───────────────────────────── */
.score-badge{display:inline-block;border-radius:50px;padding:6px 18px;
             font-weight:700;font-size:18px;color:#fff;}
.s-high{background:linear-gradient(90deg,#15803d,#22c55e);}
.s-med {background:linear-gradient(90deg,#b45309,#f59e0b);}
.s-low {background:linear-gradient(90deg,#991b1b,#ef4444);}

/* ── Sidebar — soft white/indigo ────────────────────────────── */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#f8faff,#eef2ff) !important;
    border-right:1px solid #c7d2fe;}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #1e2d5a !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #1e2d5a !important; }
.stRadio>div{gap:6px;}
hr{border-color:#c7d2fe;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# DATASET — BAGALURU MICRO-MARKET PROJECTS
# ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.DataFrame({
        'project': [
            'Adarsh Palm Acres III', 'Aurum@Brigade El Dorado',
            'Brigade El Dorado (Diora)', 'Brigade El Dorado (Cobalt)',
            'Brigade El Dorado (Beryl)', 'Emerald & Luminaire',
            'Godrej Ananda III (H-K)', 'Godrej Ananda III (P)',
            'Godrej Ananda III (M)', 'Godrej Ananda III (L)',
            'Kalyani Living Tree T1-T6', 'Kalyani Living Tree T3/T4',
            'Kumar Plumeria', 'North Park',
            'NVG Rakshak', 'Provident Ecopolitan',
            'Provident Ecopolitan V', 'Sri Sai Dev Enclave',
        ],
        'developer': [
            'Adarsh', 'Brigade', 'Brigade', 'Brigade', 'Brigade', 'Brigade',
            'Godrej', 'Godrej', 'Godrej', 'Godrej',
            'Kalyani', 'Kalyani', 'Kumar', 'MJR', 'NVG',
            'Puravankara', 'Puravankara', 'Sri Sai Dev',
        ],
        'developer_tier': [
            'Luxury/New', 'Established', 'Established', 'Established', 'Established', 'Established',
            'Established', 'Established', 'Established', 'Established',
            'Established', 'Established', 'Luxury/New', 'New', 'New',
            'Established', 'Established', 'Small',
        ],
        'segment': [
            'Luxury', 'Mid', 'Mid', 'Mid', 'Mid', 'Mid',
            'Mid', 'Mid', 'Mid', 'Mid',
            'Mid', 'Mid', 'Luxury', 'Mid', 'Mid',
            'Mid', 'Mid', 'Plots',
        ],
        'launch_year': [2025,2023,2024,2024,2024,2023,2023,2023,2024,2024,2024,2025,2025,2024,2024,2023,2024,2023],
        'total_units': [196,635,525,948,800,250,1163,349,349,349,1686,500,100,354,390,956,581,152],
        'absorbed_units': [22,635,525,948,800,250,1162,290,225,194,1350,33,17,278,166,920,576,151],
        'price_sqft': [17285,5265,8600,8860,9345,4800,7537,7537,7775,7775,7490,7700,10500,7625,7850,6342,8581,3950],
        'unit_size_min': [3500,938,521,536,521,938,750,1092,1092,1092,576,1314,2600,430,530,650,539,820],
        'bhk_min': [4,2,1,1,1,2,1,2,2,2,1,2,4,1,1,1,1,0],
        'bhk_max': [5,3,3,0,2,3,3,3,3,3,3,0,5,3,3,3,4,0],
        'delay_months': [0,12,0,0,0,0,9,0,0,0,0,0,0,19,0,0,0,5],
        'construction_stage': [
            'Excavation', 'Excavation & Plinth', 'Slab GF', 'Excavation & Plinth',
            'Slab GF', 'Finishing', 'Interior', 'Interior', 'Interior', 'Interior',
            'Excavation & Plinth', 'Excavation & Plinth', 'Excavation & Plinth',
            'Slab 11', 'Slab 1', 'Slab 6', 'Excavation & Plinth', 'Ready',
        ],
        'location_type': [
            'Inner Bagaluru', 'Highway Corridor', 'Highway Corridor', 'Highway Corridor',
            'Highway Corridor', 'Highway Corridor', 'Highway Corridor', 'Highway Corridor',
            'Highway Corridor', 'Highway Corridor', 'Mid Bagaluru', 'Mid Bagaluru',
            'Inner Bagaluru', 'Mid Bagaluru', 'Mid Bagaluru',
            'Highway Corridor', 'Highway Corridor', 'Highway Corridor',
        ],
    })
    df['pct_sold']    = (df['absorbed_units'] / df['total_units'] * 100).round(2)
    df['unsold_units'] = df['total_units'] - df['absorbed_units']
    df['is_defect']   = (df['pct_sold'] < 70).astype(int)
    df['status']      = df['pct_sold'].apply(
        lambda x: '✅ Healthy' if x >= 95 else ('⚠️ At Risk' if x < 70 else '🔶 Moderate')
    )
    return df

# Monthly absorption data
MONTHS = [
    'Jan-23','Feb-23','Mar-23','Apr-23','May-23','Jun-23',
    'Jul-23','Aug-23','Sep-23','Oct-23','Nov-23','Dec-23',
    'Jan-24','Feb-24','Mar-24','Apr-24','May-24','Jun-24',
    'Jul-24','Aug-24','Sep-24','Oct-24','Nov-24','Dec-24',
    'Jan-25','Feb-25','Mar-25','Apr-25','May-25','Jun-25',
    'Jul-25','Aug-25','Sep-25','Oct-25','Nov-25',
]
ABSORPTION = np.array([
    54,38,29,24,37,22,324,424,401,127,587,462,
    294,480,286,129,197,166,134,193,194,475,400,766,
    336,306,269,236,196,180,215,217,143,77,124,
], dtype=float)

df = load_data()

# ─────────────────────────────────────────────────────────────────
# DATASET — 25 BENGALURU AREAS (Map Dashboard)
# ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_areas():
    data = {
        "area": [
            "Whitefield","Electronic City","Koramangala","Indiranagar","HSR Layout",
            "Sarjapur Road","Bagaluru","Hebbal","Yelahanka","Bannerghatta Road",
            "JP Nagar","Malleswaram","Marathahalli","Bellandur","Panathur",
            "Devanahalli","Kengeri","Rajajinagar","Jayanagar","BTM Layout",
            "Thanisandra","Hennur","Kadugodi","Horamavu","Bommasandra",
        ],
        "lat": [
            12.9698,12.8456,12.9352,12.9784,12.9116,
            12.8726,13.1100,13.0350,13.1007,12.8606,
            12.9077,13.0031,12.9591,12.9276,12.9392,
            13.2046,12.9072,13.0009,12.9255,12.9165,
            13.0621,13.0468,12.9823,13.0239,12.8073,
        ],
        "lng": [
            77.7499,77.6603,77.6245,77.6408,77.6472,
            77.6833,77.6101,77.5972,77.5945,77.5969,
            77.5831,77.5637,77.7014,77.6784,77.7012,
            77.7122,77.4823,77.5569,77.5832,77.6101,
            77.6309,77.6501,77.7553,77.6498,77.6781,
        ],
        "avg_price_sqft": [
            8200,6500,9800,12500,9200,
            7800,7000,10500,6800,7200,
            8800,11000,8000,8500,8100,
            5500,4800,9500,10200,7600,
            7100,6900,7500,6600,5200,
        ],
        "price_trend_yoy": [
            14,11,8,6,10,
            13,18,9,12,7,
            8,5,11,12,13,
            22,7,6,5,9,
            16,14,10,9,8,
        ],
        "metro_dist_km": [
            1.2,6.5,3.1,0.4,4.2,
            7.8,15.0,2.1,5.8,8.5,
            4.1,0.8,2.6,6.9,5.5,
            18.0,3.4,0.6,1.5,3.8,
            3.1,4.6,8.4,5.1,11.0,
        ],
        "hospital_dist_km": [
            1.5,2.8,0.8,0.5,1.2,
            3.1,4.5,1.0,2.0,1.8,
            1.1,0.4,1.3,2.5,2.2,
            6.0,2.5,0.6,0.7,1.4,
            2.0,1.8,3.5,2.1,4.8,
        ],
        "school_dist_km": [
            0.8,1.5,0.5,0.4,0.6,
            1.2,2.8,0.9,1.1,0.9,
            0.6,0.3,0.7,1.8,1.5,
            4.5,1.8,0.4,0.4,0.7,
            1.2,1.0,2.1,1.1,3.2,
        ],
        "mall_dist_km": [
            0.5,3.0,1.2,2.1,3.5,
            4.2,12.0,4.5,7.0,2.8,
            3.2,1.5,0.8,3.0,2.5,
            15.0,5.5,1.2,1.8,2.6,
            4.0,5.5,8.0,4.2,8.0,
        ],
        "highway_dist_km": [
            2.5,1.8,5.5,6.0,5.0,
            3.2,1.5,2.0,1.8,4.5,
            6.5,7.0,3.5,4.0,4.5,
            0.8,3.0,5.0,6.5,5.5,
            2.2,2.8,3.0,3.5,1.2,
        ],
        "park_dist_km": [
            1.0,2.5,0.6,0.3,0.8,
            2.1,3.5,1.2,1.5,0.7,
            0.5,0.2,1.1,1.5,1.8,
            5.0,2.0,0.5,0.3,0.9,
            1.5,1.2,2.8,1.0,4.0,
        ],
        "flood_risk": [
            "Low","Low","Low","Low","Low",
            "Medium","Low","Medium","Low","Low",
            "Low","Low","Medium","High","High",
            "Low","Low","Low","Low","Low",
            "Low","Medium","Medium","Medium","Low",
        ],
        "road_connectivity": [
            9,8,9,10,9,
            7,6,8,7,7,
            8,10,9,7,8,
            5,6,9,9,8,
            7,7,7,7,6,
        ],
        "infrastructure_score": [
            8,7,9,10,9,
            7,5,8,6,7,
            8,10,8,7,7,
            4,5,9,9,8,
            6,6,6,6,5,
        ],
        "population_growth": [
            8,7,5,4,6,
            9,12,7,9,6,
            5,3,7,8,9,
            15,5,4,3,6,
            11,10,8,7,6,
        ],
        "segment": [
            "Premium","Mid","Luxury","Luxury","Premium",
            "Premium","Mid","Luxury","Mid","Mid",
            "Premium","Luxury","Premium","Premium","Premium",
            "Budget","Budget","Premium","Luxury","Mid",
            "Mid","Mid","Mid","Mid","Budget",
        ],
        "total_projects": [12,9,7,5,8,10,6,4,7,6,8,3,9,7,6,5,4,5,4,9,7,8,6,7,5],
        "unsold_pct": [
            15,22,8,5,12,
            18,32,10,25,20,
            11,6,14,19,16,
            38,28,9,7,17,
            21,24,18,22,35,
        ],
    }
    adf = pd.DataFrame(data)
    flood_map = {"Low": 0, "Medium": 1, "High": 2}
    adf["flood_num"] = adf["flood_risk"].map(flood_map)
    return adf

# ─────────────────────────────────────────────────────────────────────────
# METRO STATIONS
# ─────────────────────────────────────────────────────────────────────────
METRO_STATIONS = [
    {"name": "Majestic",        "lat": 12.9767, "lng": 77.5713, "line": "Both"},
    {"name": "MG Road",         "lat": 12.9747, "lng": 77.6097, "line": "Purple"},
    {"name": "Indiranagar",     "lat": 12.9784, "lng": 77.6408, "line": "Purple"},
    {"name": "Whitefield",      "lat": 12.9698, "lng": 77.7499, "line": "Purple"},
    {"name": "Baiyappanahalli", "lat": 12.9988, "lng": 77.6490, "line": "Purple"},
    {"name": "Hebbal",          "lat": 13.0350, "lng": 77.5972, "line": "Green"},
    {"name": "Yelahanka",       "lat": 13.1007, "lng": 77.5945, "line": "Green"},
    {"name": "Rajajinagar",     "lat": 13.0009, "lng": 77.5569, "line": "Green"},
    {"name": "Malleswaram",     "lat": 13.0031, "lng": 77.5637, "line": "Green"},
    {"name": "Nagasandra",      "lat": 13.0445, "lng": 77.5148, "line": "Green"},
    {"name": "Silk Board",      "lat": 12.9176, "lng": 77.6233, "line": "Yellow"},
    {"name": "Bommasandra",     "lat": 12.8073, "lng": 77.6781, "line": "Yellow"},
    {"name": "Kengeri",         "lat": 12.9072, "lng": 77.4823, "line": "Purple"},
]

areas_df = load_areas()

# ─────────────────────────────────────────────────────────────────────────
# ML MODEL — MAP SUITABILITY SCORER
# ─────────────────────────────────────────────────────────────────────────
@st.cache_resource
def train_map_model(adf):
    """Train a Random Forest to predict Construction Suitability Score (0–100)."""
    def rule_score(row):
        s = 50.0
        if row["avg_price_sqft"] < 5000:    s += 5
        elif row["avg_price_sqft"] < 8000:  s += 15
        elif row["avg_price_sqft"] < 11000: s += 8
        else:                               s -= 10
        if row["metro_dist_km"] < 1:   s += 15
        elif row["metro_dist_km"] < 3: s += 10
        elif row["metro_dist_km"] < 6: s += 4
        else:                          s -= 5
        s += [-0, -12, -25][row["flood_num"]]
        s += (row["road_connectivity"] - 5) * 1.5
        s += (row["infrastructure_score"] - 5) * 1.5
        s += min(row["population_growth"] * 0.8, 12)
        if row["hospital_dist_km"] < 1:   s += 8
        elif row["hospital_dist_km"] < 3: s += 4
        s -= row["unsold_pct"] * 0.3
        return float(np.clip(s, 0, 100))

    rng = np.random.RandomState(42)
    adf = adf.copy()
    adf["suitability"] = adf.apply(rule_score, axis=1)

    FEAT = ["avg_price_sqft","metro_dist_km","hospital_dist_km","school_dist_km",
            "highway_dist_km","flood_num","road_connectivity","infrastructure_score",
            "population_growth","unsold_pct"]

    X = adf[FEAT].values
    y = adf["suitability"].values
    X_aug = np.vstack([X + rng.normal(0, 0.01, X.shape) * X.std(0) for _ in range(15)] + [X])
    y_aug = np.tile(y, 16)

    rf = RandomForestRegressor(n_estimators=300, max_depth=6, random_state=42)
    rf.fit(X_aug, y_aug)
    return rf, FEAT, adf

map_rf_model, MAP_FEAT_COLS, areas_df = train_map_model(areas_df)

def predict_area_score(row_dict):
    x = np.array([[row_dict[f] for f in MAP_FEAT_COLS]])
    return float(np.clip(map_rf_model.predict(x)[0], 0, 100))

def score_label(s):
    if s >= 75: return "🟢 Highly Suitable",  "s-high"
    if s >= 50: return "🟡 Moderate",          "s-med"
    return              "🔴 Less Suitable",     "s-low"

# ─────────────────────────────────────────────────────────────────
# ML MODELS — DMAIC (cached)
# ─────────────────────────────────────────────────────────────────
@st.cache_resource
def train_dmaic_models():
    FEATURES = ['price_sqft','unit_size_min','bhk_min','delay_months']
    X = df[FEATURES].fillna(0).values
    y_cls = df['is_defect'].values
    y_reg = df['pct_sold'].values
    rng = np.random.RandomState(42)
    X_aug = np.vstack([X + rng.normal(0,0.05,X.shape)*X.std(0) for _ in range(9)] + [X])
    y_cls_aug = np.tile(y_cls, 10)
    y_reg_aug = np.tile(y_reg, 10)
    rf = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)
    rf.fit(X_aug, y_cls_aug)
    gb = GradientBoostingRegressor(n_estimators=200, max_depth=3, learning_rate=0.05, random_state=42)
    gb.fit(X_aug, y_reg_aug)
    return rf, gb, FEATURES

rf_model, gb_model, FEAT_COLS = train_dmaic_models()

# ─────────────────────────────────────────────────────────────────
# DIGITAL TWIN SIMULATOR (SimPy)
# ─────────────────────────────────────────────────────────────────
def run_digital_twin(total_units, monthly_rate, months=12, intervention=None):
    """
    SimPy Digital Twin: simulates monthly sales events for a project.
    intervention: dict with keys 'month', 'new_rate' to model a policy change mid-simulation.
    Returns DataFrame of (month, sold_this_month, cumulative_sold, inventory_remaining).
    """
    env = simpy.Environment()
    results = []
    state = {
        'cumulative': 0,
        'remaining': total_units,
        'rate': monthly_rate,
    }

    def sales_process(env, state):
        for month in range(1, months + 1):
            yield env.timeout(1)
            if intervention and month == intervention['month']:
                state['rate'] = intervention['new_rate']
            sold = min(
                int(np.random.poisson(state['rate'])),
                state['remaining']
            )
            state['cumulative'] += sold
            state['remaining']  -= sold
            results.append({
                'Month': month,
                'Sold This Month': sold,
                'Cumulative Sold': state['cumulative'],
                'Remaining': state['remaining'],
                'Rate Used': state['rate'],
                'Intervention': month == (intervention['month'] if intervention else -1)
            })
            if state['remaining'] <= 0:
                break

    env.process(sales_process(env, state))
    env.run()
    return pd.DataFrame(results)


def run_digital_twin_segmented(total_units, base_rate, months=12,
                               budget_weight=0.4, premium_weight=0.3, normal_weight=0.3,
                               price_start=9000, price_change=0, stage_start=0, stage_inc=0.2,
                               demand_index=1.0):
    env = simpy.Environment()
    results = []
    price, stage = price_start, stage_start
    remaining, cumulative = total_units, 0

    def sales_process(env):
        nonlocal price, stage, remaining, cumulative
        for month in range(1, months+1):
            yield env.timeout(1)
            price *= (1 + price_change/100)
            stage = min(5, stage + stage_inc)
            demand = demand_index * (1 + 0.1*np.sin(month/3))

            budget = max(0, 12000 - price)/12000
            premium = stage / 5
            normal = demand / 1.0

            eff_rate = base_rate * (budget_weight*budget +
                                    premium_weight*premium +
                                    normal_weight*normal)

            sold = min(int(np.random.poisson(eff_rate)), remaining)
            remaining -= sold; cumulative += sold
            results.append({
                "Month": month, "Price": int(price), "Stage": round(stage,1),
                "Demand Index": round(demand,2), "Sold": sold,
                "Cumulative": cumulative, "Remaining": remaining,
                "Rate": eff_rate
            })
            if remaining <= 0: break

    env.process(sales_process(env))
    env.run()
    return pd.DataFrame(results)


# ─────────────────────────────────────────────────────────────────
# RECOMMENDATIONS ENGINE
# ─────────────────────────────────────────────────────────────────
def get_recommendations(project_row, data_df):
    """Generate smart recommendations by learning from sold-out projects."""
    recs  = []
    issues = []

    healthy = data_df[data_df['pct_sold'] >= 95]
    avg_healthy_price = healthy['price_sqft'].mean()
    avg_healthy_size  = healthy['unit_size_min'].mean()

    price  = project_row['price_sqft']
    delay  = project_row['delay_months']
    size   = project_row['unit_size_min']
    stage  = project_row['construction_stage']
    pct    = project_row['pct_sold']
    seg    = project_row['segment']

    if price > 9500:
        issues.append(f"🔴 Price ₹{price:,}/sqft is above the ₹9,500 market threshold")
        rec_price = round(avg_healthy_price * 0.95)
        recs.append({
            'icon': '💰', 'priority': 'HIGH',
            'title': f'Reduce launch price to ₹{rec_price:,}/sqft',
            'detail': f'Healthy projects in Bagaluru average ₹{int(avg_healthy_price):,}/sqft. '
                      f'A price cut to ₹{rec_price:,} (−{((price-rec_price)/price*100):.0f}%) '
                      f'could unlock buyers in the ₹7,000–9,000 sweet spot. '
                      f'Learn from Brigade El Dorado (100% sold at ₹8,600–9,345/sqft).',
            'recovered_units': int((project_row['unsold_units']) * 0.45),
            'type': 'rec'
        })
        recs.append({
            'icon': '🏦', 'priority': 'HIGH',
            'title': 'Offer subvention scheme (builder pays EMI for 24 months)',
            'detail': 'Subvention removes the biggest buyer barrier — paying rent + EMI. '
                      'Puravankara used this successfully for Provident Ecopolitan (96% sold). '
                      'Cost to builder: ~2% of project value. Return: faster cash flow.',
            'recovered_units': int(project_row['unsold_units'] * 0.25),
            'type': 'rec'
        })

    if delay > 6:
        issues.append(f"🔴 Construction delay of {delay} months destroys buyer trust")
        recs.append({
            'icon': '🏗️', 'priority': 'HIGH',
            'title': f'Fast-track construction — reduce delay from {delay} to <6 months',
            'detail': f'Every extra month of delay costs approximately 1–2% additional unsold units. '
                      f'North Park (19-month delay) has 21.5% units stuck. Godrej projects with 9-month '
                      f'delay are at 55–83% sold. Expedite by hiring additional contractors and '
                      f'running parallel construction tracks. Consider offering possession guarantee.',
            'recovered_units': int(project_row['unsold_units'] * 0.35),
            'type': 'rec'
        })

    if size > 2000:
        issues.append(f"🔴 Unit size {size} sqft targets niche HNI buyers only")
        recs.append({
            'icon': '📐', 'priority': 'MEDIUM',
            'title': 'Split or redesign units to 1,000–1,500 sqft range',
            'detail': f'Bagaluru buyer profile is mid-segment families needing 2–3 BHK in 750–1,400 sqft. '
                      f'Units at {size} sqft price out 80%+ of potential buyers. '
                      f'Consider redesigning floor plans to offer sub-1,500 sqft options. '
                      f'Brigade El Dorado (521–1,382 sqft) sold 100%. Godrej (750–1,630 sqft) is at 83–99%.',
            'recovered_units': int(project_row['unsold_units'] * 0.20),
            'type': 'rec'
        })

    if seg == 'Luxury' and pct < 70:
        issues.append(f"🔴 Luxury segment mismatch — Bagaluru is a mid-market corridor")
        recs.append({
            'icon': '✈️', 'priority': 'MEDIUM',
            'title': 'Reposition for NRI/investor buyers with rental guarantee',
            'detail': 'Luxury villas in peripheral markets need a different buyer profile. '
                      'Target NRI investors via Gulf/UK/US real estate expos. '
                      'Offer 3-year rental guarantee (5–6% yield) to make it an investment play. '
                      'Partner with NoBroker/PropTiger for NRI-specific listings.',
            'recovered_units': int(project_row['unsold_units'] * 0.30),
            'type': 'rec'
        })

    early_stages = ['Excavation', 'Excavation & Plinth', 'Slab 1', 'Slab GF']
    if stage in early_stages:
        issues.append(f"🟡 Construction at early stage ({stage}) — buyers can't see progress")
        recs.append({
            'icon': '📸', 'priority': 'MEDIUM',
            'title': 'Launch virtual tours and live construction webcam',
            'detail': 'Buyers at early stage projects need confidence. Install live webcam feed '
                      'on project website. Create 3D virtual walkthroughs of sample units. '
                      'Host monthly progress updates on WhatsApp/email to registered leads. '
                      'NVG Rakshak improved trust by sharing weekly construction updates.',
            'recovered_units': int(project_row['unsold_units'] * 0.15),
            'type': 'rec'
        })

    if project_row['developer_tier'] in ['New', 'Small', 'Luxury/New'] and pct < 80:
        issues.append(f"🟡 Developer brand not well established — buyers hesitant")
        recs.append({
            'icon': '⭐', 'priority': 'MEDIUM',
            'title': 'Get CRISIL DA1/DA2 credit rating + Bank home loan tie-up',
            'detail': 'NVG and MJR face brand trust deficit. A CRISIL developer rating costs '
                      '₹3–5L but unlocks access to SBI/HDFC approved project lists, reaching '
                      '3x more potential buyers. Pre-approved home loans from banks signal '
                      'financial credibility and reduce buyer due-diligence burden.',
            'recovered_units': int(project_row['unsold_units'] * 0.20),
            'type': 'rec'
        })

    recs.append({
        'icon': '📣', 'priority': 'LOW',
        'title': '20:80 payment plan — reduce upfront burden',
        'detail': 'Instead of 10% booking + construction-linked, offer 20% at booking and 80% at possession. '
                  'This is the single most effective tool for under-construction projects. '
                  'Kumar Plumeria can recover 25–30% more buyers with this scheme.',
        'recovered_units': int(project_row['unsold_units'] * 0.12),
        'type': 'rec'
    })

    if not issues:
        issues.append("✅ No critical issues detected — project is performing well")

    return issues, recs


# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏗️ Bengaluru RE Dashboard")
    st.caption("Six Sigma DMAIC · AI Map · Bagaluru Micro-Market")
    st.divider()

    # Dashboard module selector
    st.subheader("📂 Dashboard Module")
    module = st.radio("", [
        "🏙️ Six Sigma DMAIC",
        "🗺️ AI Map System",
    ], label_visibility="collapsed")

    st.divider()

    if module == "🏙️ Six Sigma DMAIC":
        st.subheader("🔍 Filter")
        all_devs = sorted(df['developer'].unique().tolist())
        selected_dev = st.selectbox(
            "Select Builder / Developer",
            options=["📊 All Builders (Market Overview)"] + all_devs,
            index=0
        )
        st.divider()
        st.subheader("⚙️ Digital Twin Settings")
        sim_months = st.slider("Simulation Duration (months)", 6, 24, 12)
        st.caption("Controls how far forward the Digital Twin projects sales")
        st.divider()
        st.markdown("**Navigation**")
        page = st.radio("", [
            "📊 Market Overview",
            "🏢 Builder Deep Dive",
            "🤖 Digital Twin Simulator",
            "💡 AI Recommendations",
            "📈 SPC Control Chart",
        ], label_visibility="collapsed")

    else:
        st.markdown("**Navigation**")
        page = st.radio("Navigate", [
            "🏠 Home",
            "📍 Interactive Map",
            "🤖 AI Suitability Analyzer",
            "📊 Price Analytics",
            "📋 Area Comparison",
            "📈 DMAIC Charts",
            "🌡️ Heatmap View",
        ], label_visibility="collapsed")
        st.divider()
        st.caption("Model: Random Forest (300 trees)")
        st.caption("Data: Bengaluru 25 zones + OSM amenities")

# ─────────────────────────────────────────────────────────────────
# FILTER DATA (DMAIC)
# ─────────────────────────────────────────────────────────────────
if module == "🏙️ Six Sigma DMAIC":
    if selected_dev == "📊 All Builders (Market Overview)":
        filtered_df = df.copy()
        dev_name = "All Builders"
    else:
        filtered_df = df[df['developer'] == selected_dev].copy()
        dev_name = selected_dev

# ═══════════════════════════════════════════════════════════════════
# ══════════  SIX SIGMA DMAIC PAGES  ════════════════════════════════
# ═══════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────
# PAGE 1: MARKET OVERVIEW
# ─────────────────────────────────────────────────────────────────
if module == "🏙️ Six Sigma DMAIC" and page == "📊 Market Overview":
    st.markdown(f"## 📊 Market Overview — {dev_name}")
    st.caption("Bagaluru Micro-Market | Dec 2022 – Nov 2025 | Six Sigma DMAIC Analysis")

    total_u   = filtered_df['total_units'].sum()
    sold_u    = filtered_df['absorbed_units'].sum()
    unsold_u  = filtered_df['unsold_units'].sum()
    dpmo      = (unsold_u / total_u) * 1_000_000
    sigma     = 0.8406 + np.sqrt(max(0, 29.37 - 2.221 * np.log(max(dpmo, 1))))
    n_defect  = filtered_df['is_defect'].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{total_u:,}</div><div class="metric-label">Total Units Launched</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card green"><div class="metric-val">{sold_u:,}</div><div class="metric-label">Units Sold ({sold_u/total_u*100:.1f}%)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card red"><div class="metric-val">{unsold_u:,}</div><div class="metric-label">Units Unsold ({unsold_u/total_u*100:.1f}%)</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card amber"><div class="metric-val">{sigma:.1f}σ</div><div class="metric-label">Sigma Level (Target: 6σ)</div></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="metric-card red"><div class="metric-val">{n_defect}/{len(filtered_df)}</div><div class="metric-label">Projects At-Risk (&lt;70% sold)</div></div>', unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("### 📊 Absorption Rate by Project")
        df_sorted = filtered_df.sort_values('pct_sold')
        colors = ['#E24B4A' if x < 70 else ('#EF9F27' if x < 95 else '#16A34A') for x in df_sorted['pct_sold']]
        fig = go.Figure(go.Bar(
            x=df_sorted['pct_sold'], y=df_sorted['project'],
            orientation='h', marker_color=colors,
            text=[f"{v:.1f}%" for v in df_sorted['pct_sold']],
            textposition='outside', hovertemplate="<b>%{y}</b><br>Sold: %{x:.1f}%<extra></extra>"
        ))
        fig.add_vline(x=70, line_dash="dash", line_color="orange", annotation_text="70% threshold")
        fig.add_vline(x=95, line_dash="dash", line_color="green",  annotation_text="95% target")
        fig.update_layout(height=420, xaxis_range=[0,115], showlegend=False,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          xaxis_title="% Units Sold", margin=dict(l=0,r=80,t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🥧 Sold vs Unsold Split")
        fig2 = go.Figure(go.Pie(
            labels=['Sold', 'Unsold'],
            values=[sold_u, unsold_u],
            hole=0.55,
            marker_colors=['#16A34A', '#E24B4A'],
            textinfo='label+percent',
            hoverinfo='label+value'
        ))
        fig2.add_annotation(text=f"{sold_u/total_u*100:.1f}%<br>Absorbed",
                            x=0.5, y=0.5, showarrow=False, font_size=16, font_color='#1e2d5a')
        fig2.update_layout(height=280, showlegend=False, margin=dict(l=0,r=0,t=10,b=10),
                           paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 🏷️ By Segment")
        seg_df = filtered_df.groupby('segment').agg(
            Total=('total_units','sum'), Sold=('absorbed_units','sum')
        ).reset_index()
        seg_df['Unsold'] = seg_df['Total'] - seg_df['Sold']
        seg_df['%Sold'] = (seg_df['Sold']/seg_df['Total']*100).round(1)
        for _, row in seg_df.iterrows():
            color = "green" if row['%Sold'] >= 95 else ("rec" if row['%Sold'] >= 70 else "red")
            st.markdown(f"**{row['segment']}** — {row['%Sold']}% sold ({row['Unsold']:,} unsold)")

    st.markdown("### 💹 Price vs Absorption (bubble size = total units)")
    fig3 = px.scatter(
        filtered_df, x='price_sqft', y='pct_sold',
        size='total_units', color='status',
        color_discrete_map={'✅ Healthy':'#16A34A','⚠️ At Risk':'#E24B4A','🔶 Moderate':'#EF9F27'},
        hover_name='project',
        hover_data={'developer':True,'total_units':True,'unsold_units':True,'delay_months':True},
        labels={'price_sqft':'Launch Price (₹/sqft)','pct_sold':'% Sold','status':'Status'}
    )
    fig3.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="70% threshold")
    fig3.add_vline(x=9500, line_dash="dash", line_color="red", annotation_text="₹9,500 danger zone")
    fig3.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# PAGE 2: BUILDER DEEP DIVE
# ─────────────────────────────────────────────────────────────────
elif module == "🏙️ Six Sigma DMAIC" and page == "🏢 Builder Deep Dive":
    st.markdown(f"## 🏢 Builder Deep Dive — {dev_name}")

    if selected_dev == "📊 All Builders (Market Overview)":
        st.info("👈 Select a specific builder from the sidebar to see their project-level details")
        bld_df = df.groupby('developer').agg(
            Total=('total_units','sum'), Sold=('absorbed_units','sum'),
            Projects=('project','count')
        ).reset_index()
        bld_df['Unsold'] = bld_df['Total'] - bld_df['Sold']
        bld_df['%Sold']  = (bld_df['Sold']/bld_df['Total']*100).round(1)
        bld_df = bld_df.sort_values('%Sold', ascending=False)

        fig = go.Figure()
        fig.add_bar(name='Sold', x=bld_df['developer'], y=bld_df['Sold'],
                    marker_color='#16A34A', text=bld_df['Sold'], textposition='inside')
        fig.add_bar(name='Unsold', x=bld_df['developer'], y=bld_df['Unsold'],
                    marker_color='#E24B4A', text=bld_df['Unsold'], textposition='inside')
        fig.update_layout(barmode='stack', title='All Builders — Total vs Sold vs Unsold',
                          height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(bld_df.style.background_gradient(subset=['%Sold'], cmap='RdYlGn'), use_container_width=True)

    else:
        dev_projects = filtered_df.copy()
        total_u  = dev_projects['total_units'].sum()
        sold_u   = dev_projects['absorbed_units'].sum()
        unsold_u = dev_projects['unsold_units'].sum()

        st.markdown(f"""
        <div style="background:#1e2d5a;color:white;padding:16px 22px;border-radius:12px;margin-bottom:16px">
          <div style="font-size:1.4rem;font-weight:700">{dev_name}</div>
          <div style="font-size:0.9rem;opacity:0.8">{len(dev_projects)} project phases · {total_u:,} total units · Bagaluru Micro-Market</div>
        </div>""", unsafe_allow_html=True)

        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Total Units",   f"{total_u:,}")
        k2.metric("Units Sold",    f"{sold_u:,}", f"{sold_u/total_u*100:.1f}%")
        k3.metric("Units Unsold",  f"{unsold_u:,}", f"-{unsold_u/total_u*100:.1f}%", delta_color="inverse")
        k4.metric("Avg Delay",     f"{dev_projects['delay_months'].mean():.1f} months")

        st.divider()

        st.markdown("### 📋 Project-Level Breakdown")
        display_cols = ['project','segment','total_units','absorbed_units','unsold_units','pct_sold','price_sqft','delay_months','construction_stage','status']
        st.dataframe(
            dev_projects[display_cols].rename(columns={
                'project':'Project','segment':'Segment','total_units':'Total',
                'absorbed_units':'Sold','unsold_units':'Unsold','pct_sold':'% Sold',
                'price_sqft':'Price/sqft','delay_months':'Delay(mo)',
                'construction_stage':'Stage','status':'Status'
            }).style.applymap(
                lambda v: 'background-color:#dcfce7' if '✅' in str(v) else
                          ('background-color:#fee2e2' if '⚠️' in str(v) else
                           'background-color:#fef3c7' if '🔶' in str(v) else ''),
                subset=['Status']
            ).background_gradient(subset=['% Sold'], cmap='RdYlGn'),
            use_container_width=True
        )

        st.markdown("### 🔢 Sold vs Unsold per Project")
        fig = go.Figure()
        fig.add_bar(name='Sold', x=dev_projects['project'],
                    y=dev_projects['absorbed_units'], marker_color='#16A34A',
                    text=dev_projects['absorbed_units'], textposition='inside')
        fig.add_bar(name='Unsold', x=dev_projects['project'],
                    y=dev_projects['unsold_units'], marker_color='#E24B4A',
                    text=dev_projects['unsold_units'], textposition='inside')
        fig.update_layout(barmode='stack', height=350,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

        at_risk = dev_projects[dev_projects['is_defect'] == 1]
        if len(at_risk) > 0:
            st.markdown(f"### ⚠️ At-Risk Projects ({len(at_risk)} below 70% sold)")
            for _, row in at_risk.iterrows():
                with st.expander(f"🔴 {row['project']} — {row['pct_sold']:.1f}% sold | {row['unsold_units']} units unsold"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Price/sqft", f"₹{row['price_sqft']:,}")
                    c2.metric("Delay", f"{row['delay_months']} months")
                    c3.metric("Stage", row['construction_stage'])
                    issues, recs = get_recommendations(row, df)
                    st.markdown("**Issues Detected:**")
                    for issue in issues:
                        st.markdown(f"- {issue}")
        else:
            st.success(f"✅ All {dev_name} projects are performing above 70% absorption!")


# ─────────────────────────────────────────────────────────────────
# PAGE 3: DIGITAL TWIN SIMULATOR
# ─────────────────────────────────────────────────────────────────
elif module == "🏙️ Six Sigma DMAIC" and page == "🤖 Digital Twin Simulator":
    st.markdown("## 🤖 Digital Twin Simulator (SimPy)")
    st.markdown("""
    <div class="twin-box">
    ▶  What is a Digital Twin?<br><br>
    A Digital Twin is a virtual replica of a real-world process that<br>
    simulates its behavior over time. Here, each project phase is<br>
    replicated as a SimPy event-based simulation — units are "sold"<br>
    each month based on a Poisson process (real market randomness).<br><br>
    You can inject a policy change (price cut, subvention scheme)<br>
    at any month and see how the absorption curve changes.<br><br>
    ▶  How SimPy is used:<br>
    env = simpy.Environment()  →  creates the simulation clock<br>
    env.timeout(1)             →  advances 1 month<br>
    Poisson(rate)              →  realistic monthly sale count<br>
    Intervention at month N    →  models policy/price change
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    all_projects = df['project'].tolist()
    if selected_dev != "📊 All Builders (Market Overview)":
        proj_options = filtered_df['project'].tolist()
    else:
        proj_options = all_projects

    sel_proj = st.selectbox("🏗️ Select Project to Simulate", proj_options)
    proj_row = df[df['project'] == sel_proj].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Project Facts**")
        st.markdown(f"""
        - Total Units: **{proj_row['total_units']:,}**
        - Currently Sold: **{proj_row['absorbed_units']:,}** ({proj_row['pct_sold']:.1f}%)
        - Currently Unsold: **{proj_row['unsold_units']:,}**
        - Price: **₹{proj_row['price_sqft']:,}/sqft**
        - Delay: **{proj_row['delay_months']} months**
        - Stage: **{proj_row['construction_stage']}**
        """)
    with col2:
        st.markdown("**Current Monthly Absorption Rate**")
        current_rate = max(5, int(proj_row['absorbed_units'] / 12))
        base_rate = st.slider("Base monthly sales rate (units/month)", 1, 100, int(current_rate), key='base_rate')

    st.divider()
    st.markdown("### 💉 Intervention — Simulate a Policy Change")
    apply_intervention = st.checkbox("Apply intervention mid-simulation (e.g., price cut, subvention)")
    intervention = None
    if apply_intervention:
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            intv_month = st.slider("At which month?", 1, sim_months, 3)
        with ic2:
            intv_rate = st.slider("New monthly sales rate after intervention", 1, 150, base_rate*2)
        with ic3:
            intv_label = st.text_input("Label this intervention", "Price cut + subvention")
        intervention = {'month': intv_month, 'new_rate': intv_rate, 'label': intv_label}

    if st.button("▶️ Run Digital Twin Simulation", type="primary", use_container_width=True):
        with st.spinner("SimPy simulation running..."):
            np.random.seed(42)
            results_base = run_digital_twin(
                proj_row['unsold_units'], base_rate, sim_months, None
            )
            if apply_intervention:
                np.random.seed(42)
                results_intv = run_digital_twin(
                    proj_row['unsold_units'], base_rate, sim_months, intervention
                )

        st.markdown("### 📈 Simulation Results")

        fig = go.Figure()
        fig.add_scatter(
            x=results_base['Month'], y=results_base['Cumulative Sold'],
            mode='lines+markers', name='Baseline (no change)',
            line=dict(color='#E24B4A', width=2, dash='dot'),
            marker=dict(size=6)
        )
        fig.add_bar(
            x=results_base['Month'], y=results_base['Sold This Month'],
            name='Monthly Sales (Baseline)', opacity=0.3,
            marker_color='#94a3b8', yaxis='y2'
        )

        if apply_intervention:
            fig.add_scatter(
                x=results_intv['Month'], y=results_intv['Cumulative Sold'],
                mode='lines+markers', name=f'After: {intv_label}',
                line=dict(color='#16A34A', width=3),
                marker=dict(size=8)
            )
            fig.add_vline(x=intv_month, line_dash='dash', line_color='#2E75B6',
                          annotation_text=f"Intervention: Month {intv_month}")

        fig.add_hline(y=proj_row['unsold_units'], line_dash='dash',
                      line_color='orange', annotation_text='All unsold cleared')

        fig.update_layout(
            title=f"Digital Twin: {sel_proj} — {sim_months}-Month Sales Projection",
            xaxis_title='Month', yaxis_title='Cumulative Units Sold',
            yaxis2=dict(overlaying='y', side='right', title='Monthly Sales'),
            height=420, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig, use_container_width=True)

        s1, s2, s3 = st.columns(3)
        final_sold_base = results_base['Cumulative Sold'].iloc[-1]
        s1.metric("Baseline — Units Sold in Simulation", f"{int(final_sold_base):,}",
                  f"{final_sold_base/proj_row['unsold_units']*100:.1f}% cleared")
        if apply_intervention:
            final_sold_intv = results_intv['Cumulative Sold'].iloc[-1]
            s2.metric(f"After Intervention — Units Sold", f"{int(final_sold_intv):,}",
                      f"+{int(final_sold_intv - final_sold_base):,} extra units")
            s3.metric("Recovery Gain", f"+{int(final_sold_intv - final_sold_base):,} units",
                      f"₹{int((final_sold_intv - final_sold_base) * proj_row['price_sqft'] * 1000 / 1e7):.1f} Cr revenue")

        st.markdown("### 🖥️ SimPy Event Log (First 10 Months)")
        log_df = results_base.head(10)[['Month','Sold This Month','Cumulative Sold','Remaining','Rate Used']]
        if apply_intervention:
            log_df = results_intv.head(10)[['Month','Sold This Month','Cumulative Sold','Remaining','Rate Used','Intervention']]
        st.dataframe(log_df, use_container_width=True)

        st.markdown("""
        > **How SimPy works here:** Each "tick" = 1 month. `env.timeout(1)` advances the clock.
        > Sales follow `Poisson(rate)` — a probability distribution that models random buyer arrivals.
        > When an intervention is injected at month N, the rate changes — simulating a price cut
        > or scheme launch. This is a real **Digital Twin** of the sales process.
        """)


# ─────────────────────────────────────────────────────────────────
# PAGE 4: AI RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────
elif module == "🏙️ Six Sigma DMAIC" and page == "💡 AI Recommendations":
    st.markdown("## 💡 AI-Powered Recommendations")
    st.caption("Recommendations are generated by learning from sold-out projects (95%+ absorbed)")

    if selected_dev == "📊 All Builders (Market Overview)":
        st.info("👈 Select a specific builder from the sidebar for targeted recommendations")
        at_risk_all = df[df['is_defect'] == 1].sort_values('pct_sold')
        st.markdown(f"### ⚠️ All At-Risk Projects ({len(at_risk_all)} below 70% sold)")
        for _, row in at_risk_all.iterrows():
            issues, recs = get_recommendations(row, df)
            with st.expander(f"🔴 {row['project']} ({row['developer']}) — {row['pct_sold']:.1f}% sold | {row['unsold_units']} unsold"):
                for issue in issues:
                    st.markdown(f"- {issue}")
                if recs:
                    top_rec = recs[0]
                    st.markdown(f"**Top Recommendation:** {top_rec['icon']} {top_rec['title']}")
    else:
        at_risk = filtered_df[filtered_df['is_defect'] == 1]
        healthy_dev = filtered_df[filtered_df['pct_sold'] >= 95]

        if len(at_risk) == 0:
            st.success(f"✅ All {dev_name} projects are above 70% absorption. No critical interventions needed.")
            if len(healthy_dev) > 0:
                st.markdown("### ✅ What made these projects successful?")
                for _, row in healthy_dev.iterrows():
                    st.markdown(f"""
                    <div class="rec-box">
                    <b>✅ {row['project']}</b> — {row['pct_sold']:.1f}% sold<br>
                    Price: ₹{row['price_sqft']:,}/sqft · Size: {row['unit_size_min']}–{row['unit_size_min']} sqft ·
                    Delay: {row['delay_months']} months · Stage: {row['construction_stage']}
                    </div>""", unsafe_allow_html=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### ✅ What SOLD projects did right")
                healthy_all = df[df['pct_sold'] >= 95]
                st.markdown(f"""
                <div class="rec-box">
                <b>Average successful project profile:</b><br>
                · Price: ₹{healthy_all['price_sqft'].mean():,.0f}/sqft (range: ₹{healthy_all['price_sqft'].min():,}–₹{healthy_all['price_sqft'].max():,})<br>
                · Unit size: {healthy_all['unit_size_min'].mean():,.0f} sqft avg<br>
                · Delay: {healthy_all['delay_months'].mean():.1f} months avg<br>
                · Examples: Brigade El Dorado (100%), Provident Ecopolitan V (99%), Sri Sai Dev (99%)
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown("### 🔴 What UNSOLD projects have in common")
                st.markdown(f"""
                <div class="rec-box warn">
                <b>Average at-risk project profile:</b><br>
                · Price: ₹{at_risk['price_sqft'].mean():,.0f}/sqft (often >₹9,500)<br>
                · Unit size: {at_risk['unit_size_min'].mean():,.0f} sqft avg (often >2,000)<br>
                · Delay: {at_risk['delay_months'].mean():.1f} months avg<br>
                · Examples: Kalyani T3/T4 (6.6%), Adarsh (11.2%), Kumar (17%)
                </div>""", unsafe_allow_html=True)

            st.divider()
            for _, row in at_risk.iterrows():
                st.markdown(f"### 🔴 {row['project']} — {row['pct_sold']:.1f}% sold ({row['unsold_units']} units unsold)")
                issues, recs = get_recommendations(row, df)

                st.markdown("**Root Issues Detected:**")
                for issue in issues:
                    st.markdown(f"- {issue}")

                st.markdown("**Recommended Actions (from sold-out project learnings):**")
                total_recoverable = sum(r.get('recovered_units', 0) for r in recs)
                st.info(f"🎯 Estimated recoverable units with all actions: ~{total_recoverable:,} of {row['unsold_units']} unsold")

                for rec in recs:
                    priority_color = "rec" if rec['priority'] == 'HIGH' else ("warn" if rec['priority'] == 'MEDIUM' else "info")
                    st.markdown(f"""
                    <div class="rec-box {priority_color}">
                    <b>{rec['icon']} [{rec['priority']}] {rec['title']}</b><br>
                    <span style="font-size:0.9rem">{rec['detail']}</span><br>
                    <span style="font-size:0.82rem;color:#64748b">Estimated recovery: ~{rec.get('recovered_units',0):,} units</span>
                    </div>""", unsafe_allow_html=True)

                base_rate = max(3, int(row['absorbed_units'] / max(12, 1)))
                st.markdown("**📊 Quick Digital Twin Preview — With vs Without Intervention**")
                np.random.seed(42)
                r_base = run_digital_twin(row['unsold_units'], base_rate, 12, None)
                np.random.seed(42)
                r_intv = run_digital_twin(row['unsold_units'], base_rate, 12,
                                          {'month': 3, 'new_rate': base_rate * 2})
                fig = go.Figure()
                fig.add_scatter(x=r_base['Month'], y=r_base['Cumulative Sold'],
                                name='No Action', line=dict(color='#E24B4A', dash='dot'))
                fig.add_scatter(x=r_intv['Month'], y=r_intv['Cumulative Sold'],
                                name='With Intervention', line=dict(color='#16A34A', width=2))
                fig.update_layout(height=260, margin=dict(l=0,r=0,t=10,b=30),
                                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                  xaxis_title='Month', yaxis_title='Cumulative Sold',
                                  legend=dict(x=0,y=1))
                st.plotly_chart(fig, use_container_width=True)
                st.divider()


# ─────────────────────────────────────────────────────────────────
# PAGE 5: SPC CONTROL CHART
# ─────────────────────────────────────────────────────────────────
elif module == "🏙️ Six Sigma DMAIC" and page == "📈 SPC Control Chart":
    st.markdown("## 📈 SPC Control Chart — Monthly Market Monitor")

    st.markdown("### ⚙️ Configure Baseline Period")
    bcol1, bcol2 = st.columns([2, 3])
    with bcol1:
        baseline_option = st.selectbox(
            "Baseline period (stable reference months)",
            options=[
                "Jan–Jun 2023  (6 months — pre-launch quiet period ✅ Recommended)",
                "Jan–Dec 2023  (12 months — includes big Jul-Dec launches ❌ Inflated)",
                "Jan–Mar 2023  (3 months — ultra-conservative)",
            ],
            index=0
        )
    with bcol2:
        st.info(
            "**Why does baseline matter?**  The baseline defines what 'normal' looks like. "
            "Using Jan–Dec 2023 was the bug — it included months with 324–587 sales, "
            "making UCL=820 so nothing ever looked out of control. "
            "The correct baseline is Jan–Jun 2023 (54–37 sales/month) — the true quiet period before big launches began."
        )

    if "6 months" in baseline_option:
        n_base = 6
        base_label = "Jan–Jun 2023 (6 months)"
    elif "12 months" in baseline_option:
        n_base = 12
        base_label = "Jan–Dec 2023 (12 months)"
    else:
        n_base = 3
        base_label = "Jan–Mar 2023 (3 months)"

    baseline_vals = ABSORPTION[:n_base]
    cl  = baseline_vals.mean()
    MR     = np.abs(np.diff(baseline_vals))
    d2     = 1.128
    sigma_mr = MR.mean() / d2 if len(MR) > 0 else baseline_vals.std()
    ucl = cl + 3 * sigma_mr
    lcl = max(0, cl - 3 * sigma_mr)
    uwl = cl + 2 * sigma_mr
    lwl = max(0, cl - 2 * sigma_mr)

    ooc       = (ABSORPTION > ucl) | (ABSORPTION < lcl)
    ooc_above = ABSORPTION > ucl
    ooc_below = ABSORPTION < lcl

    above_cl = ABSORPTION > cl
    runs_flag = np.zeros(len(ABSORPTION), dtype=bool)
    for i in range(7, len(ABSORPTION)):
        if all(above_cl[i-7:i+1]) or all(~above_cl[i-7:i+1]):
            runs_flag[i-7:i+1] = True

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Centre Line (CL)",          f"{cl:.0f}",        "units/month")
    k2.metric("UCL  (+3σ MR)",             f"{ucl:.0f}",       "units/month")
    k3.metric("LCL  (−3σ MR)",             f"{lcl:.0f}",       "units/month")
    k4.metric("Out-of-Control Points",     f"{ooc.sum()}",     f"of {len(ABSORPTION)} months")
    k5.metric("Runs Rule Violations",      f"{runs_flag.sum()}", "8-pt same side of CL")

    st.caption(f"Baseline: {base_label}  |  CL={cl:.1f}  UCL={ucl:.1f}  LCL={lcl:.1f}  |  Method: I-MR Chart (d2=1.128)")
    st.divider()

    st.markdown("### 📉 Individual Control Chart (I-Chart)")
    fig = go.Figure()
    fig.add_vrect(
        x0=MONTHS[0], x1=MONTHS[n_base - 1],
        fillcolor='rgba(59,130,246,0.08)', line_width=0,
        annotation_text=f"Baseline ({base_label})",
        annotation_position="top left", annotation_font_size=10
    )
    fig.add_hrect(y0=lwl, y1=uwl, fillcolor='rgba(22,163,74,0.06)', line_width=0)
    fig.add_scatter(x=MONTHS, y=[ucl]*len(MONTHS), mode='lines', name=f'UCL = {ucl:.0f}',
                    line=dict(color='#DC2626', dash='dash', width=1.8))
    fig.add_scatter(x=MONTHS, y=[lcl]*len(MONTHS), mode='lines', name=f'LCL = {lcl:.0f}',
                    line=dict(color='#DC2626', dash='dash', width=1.8))
    fig.add_scatter(x=MONTHS, y=[uwl]*len(MONTHS), mode='lines', name=f'UWL = {uwl:.0f}',
                    line=dict(color='#F59E0B', dash='dot', width=1))
    fig.add_scatter(x=MONTHS, y=[lwl]*len(MONTHS), mode='lines', name=f'LWL = {lwl:.0f}',
                    line=dict(color='#F59E0B', dash='dot', width=1))
    fig.add_scatter(x=MONTHS, y=[cl]*len(MONTHS), mode='lines', name=f'CL = {cl:.0f}',
                    line=dict(color='#16A34A', width=2.2))
    fig.add_scatter(x=MONTHS, y=ABSORPTION, mode='lines+markers', name='Monthly Absorption',
                    line=dict(color='#2563EB', width=2), marker=dict(size=6, color='#2563EB'))

    ooc_above_months = [MONTHS[i] for i in range(len(MONTHS)) if ooc_above[i]]
    ooc_above_vals   = [ABSORPTION[i] for i in range(len(ABSORPTION)) if ooc_above[i]]
    if ooc_above_months:
        fig.add_scatter(x=ooc_above_months, y=ooc_above_vals, mode='markers', name='Above UCL 🔴',
                        marker=dict(color='#DC2626', size=14, symbol='circle',
                                    line=dict(color='white', width=2)),
                        hovertemplate="<b>%{x}</b><br>Absorbed: %{y}<br><b>ABOVE UCL — Out of Control</b><extra></extra>")
    ooc_below_months = [MONTHS[i] for i in range(len(MONTHS)) if ooc_below[i]]
    ooc_below_vals   = [ABSORPTION[i] for i in range(len(ABSORPTION)) if ooc_below[i]]
    if ooc_below_months:
        fig.add_scatter(x=ooc_below_months, y=ooc_below_vals, mode='markers', name='Below LCL 🟠',
                        marker=dict(color='#D97706', size=14, symbol='diamond',
                                    line=dict(color='white', width=2)),
                        hovertemplate="<b>%{x}</b><br>Absorbed: %{y}<br><b>BELOW LCL — Out of Control</b><extra></extra>")
    runs_months = [MONTHS[i] for i in range(len(MONTHS)) if runs_flag[i]]
    runs_vals   = [ABSORPTION[i] for i in range(len(ABSORPTION)) if runs_flag[i]]
    if runs_months:
        fig.add_scatter(x=runs_months, y=runs_vals, mode='markers', name='Runs Rule 🟡',
                        marker=dict(color='rgba(0,0,0,0)', size=16, symbol='square-open',
                                    line=dict(color='#7C3AED', width=2)),
                        hovertemplate="<b>%{x}</b><br>Absorbed: %{y}<br><b>RUNS RULE VIOLATION</b><extra></extra>")

    fig.add_annotation(x='Jul-23', y=324, text='Big launches begin<br>Jul-23: 1,591 units', showarrow=True,
                       arrowcolor='#DC2626', font=dict(color='#DC2626', size=9), ax=60, ay=-50)
    fig.add_annotation(x='Dec-24', y=766, text='Supply shock peak<br>Dec-24: 766 sold', showarrow=True,
                       arrowcolor='#DC2626', font=dict(color='#DC2626', size=9), ax=55, ay=-55)
    fig.add_annotation(x='Oct-25', y=77, text='Market slowdown<br>Oct-25: 77 sold', showarrow=True,
                       arrowcolor='#D97706', font=dict(color='#92400e', size=9), ax=-70, ay=45)

    fig.update_layout(
        height=500, xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title='Units Absorbed per Month', yaxis=dict(rangemode='tozero'),
        legend=dict(x=1.01, y=1, bgcolor='rgba(0,0,0,0)'),
        hovermode='x unified', margin=dict(r=180)
    )
    st.plotly_chart(fig, use_container_width=True)

    if ooc.sum() > 0:
        st.markdown("### 🚨 Out-of-Control Events Detected")
        ooc_data = []
        for i in range(len(MONTHS)):
            if ooc[i]:
                direction = "↑ Above UCL" if ooc_above[i] else "↓ Below LCL"
                deviation = ABSORPTION[i] - cl
                action = (
                    "Investigate — supply shock or sudden large launch" if ooc_above[i]
                    else "Immediate action — pricing scheme or incentive needed"
                )
                ooc_data.append({
                    'Month': MONTHS[i], 'Absorbed': int(ABSORPTION[i]), 'CL': int(cl),
                    'Direction': direction, 'Deviation from CL': f"{deviation:+.0f}",
                    'Recommended Action': action
                })
        ooc_df = pd.DataFrame(ooc_data)
        st.dataframe(
            ooc_df.style.applymap(
                lambda v: 'background-color:#fee2e2;color:#991b1b' if '↑' in str(v)
                     else ('background-color:#fef3c7;color:#92400e' if '↓' in str(v) else ''),
                subset=['Direction']
            ), use_container_width=True
        )
    else:
        st.success("✅ No out-of-control points with this baseline. Try a different baseline period above.")

    st.markdown("### 📊 Moving Range Chart (MR-Chart)")
    st.caption("The MR-chart shows the month-to-month change in absorption. Spikes indicate sudden market shifts.")
    MR_all  = np.abs(np.diff(ABSORPTION))
    MR_ucl  = 3.267 * (MR.mean() if len(MR) > 0 else MR_all.mean())
    MR_cl   = MR.mean() if len(MR) > 0 else MR_all.mean()
    ooc_mr  = MR_all > MR_ucl

    fig_mr = go.Figure()
    fig_mr.add_scatter(x=MONTHS[1:], y=MR_all, mode='lines+markers', name='Moving Range',
                       line=dict(color='#7C3AED', width=2), marker=dict(size=5))
    fig_mr.add_scatter(x=MONTHS[1:], y=[MR_ucl]*len(MR_all), mode='lines',
                       name=f'MR UCL={MR_ucl:.0f}', line=dict(color='#DC2626', dash='dash', width=1.5))
    fig_mr.add_scatter(x=MONTHS[1:], y=[MR_cl]*len(MR_all), mode='lines',
                       name=f'MR CL={MR_cl:.0f}', line=dict(color='green', width=1.5))
    ooc_mr_months = [MONTHS[1:][i] for i in range(len(MR_all)) if ooc_mr[i]]
    ooc_mr_vals   = [MR_all[i] for i in range(len(MR_all)) if ooc_mr[i]]
    if ooc_mr_months:
        fig_mr.add_scatter(x=ooc_mr_months, y=ooc_mr_vals, mode='markers', name='MR Out-of-Control',
                           marker=dict(color='#DC2626', size=12))
    fig_mr.update_layout(height=260, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         yaxis_title='Moving Range', xaxis_tickangle=-45, margin=dict(r=20))
    st.plotly_chart(fig_mr, use_container_width=True)

    st.markdown("### 🔮 3-Month Moving Average + 6-Month Trend Forecast")
    ma3 = pd.Series(ABSORPTION).rolling(3, min_periods=1).mean().values
    recent = ABSORPTION[-12:]
    x_recent = np.arange(len(ABSORPTION) - 12, len(ABSORPTION))
    trend = np.polyfit(x_recent, recent, 1)
    x_forecast = np.arange(len(ABSORPTION), len(ABSORPTION) + 6)
    forecast_vals = np.polyval(trend, x_forecast)
    forecast_months = ['Dec-25', 'Jan-26', 'Feb-26', 'Mar-26', 'Apr-26', 'May-26']

    fig2 = go.Figure()
    fig2.add_scatter(x=MONTHS, y=ABSORPTION, mode='lines+markers', name='Actual Absorption',
                     line=dict(color='#2563EB', width=2), marker=dict(size=5))
    fig2.add_scatter(x=MONTHS, y=ma3, mode='lines', name='3-Month Moving Avg',
                     line=dict(color='#EF9F27', width=2, dash='dot'))
    fig2.add_scatter(x=forecast_months, y=np.clip(forecast_vals, 0, None).tolist(),
                     mode='lines+markers', name='6-Month Forecast',
                     line=dict(color='#16A34A', width=2, dash='dash'),
                     marker=dict(size=8, symbol='diamond'),
                     hovertemplate="<b>%{x}</b><br>Forecast: %{y:.0f} units<extra></extra>")
    fig2.add_vrect(x0='Dec-25', x1='May-26', fillcolor='rgba(22,163,74,0.06)', line_width=0,
                   annotation_text='Forecast Zone (based on last 12-month trend)',
                   annotation_position='top left', annotation_font_size=9)
    fig2.add_scatter(x=MONTHS, y=[ucl]*len(MONTHS), mode='lines',
                     name=f'UCL={ucl:.0f}', line=dict(color='#DC2626', dash='dash', width=1))
    fig2.add_scatter(x=MONTHS, y=[cl]*len(MONTHS), mode='lines',
                     name=f'CL={cl:.0f}', line=dict(color='green', width=1))
    fig2.update_layout(height=340, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                       xaxis_tickangle=-45, yaxis_title='Units / month', margin=dict(r=20))
    st.plotly_chart(fig2, use_container_width=True)

    fc1, fc2, fc3 = st.columns(3)
    fc1.metric("Avg Forecast (next 6 mo)", f"{int(np.clip(forecast_vals,0,None).mean())} units/month")
    fc2.metric("Trend Direction", "📉 Declining" if trend[0] < 0 else "📈 Rising")
    fc3.metric("Months to clear all unsold", f"~{int(filtered_df['unsold_units'].sum() / max(int(np.clip(forecast_vals,0,None).mean()),1))} months")

    st.markdown("""
    #### 🔑 Control Chart Interpretation Guide
    | Signal | Symbol | Meaning | Action |
    |--------|--------|---------|--------|
    | Point above UCL | 🔴 Red circle | Unusual sales surge — supply shock | Investigate cause immediately |
    | Point below LCL | 🟠 Orange diamond | Market slowdown crisis | Launch pricing schemes now |
    | Runs Rule (8 pts same side) | 🟡 Purple square | Sustained shift in market level | Plan structural adjustment |
    | MR spike above MR-UCL | Purple dot on MR chart | Sudden volatility — month-to-month jump | Check for external shock |
    | Downward trend (2025) | 📉 Forecast line | Absorption falling steadily | Delay new launches; clear existing stock |
    """)

    with st.expander("🐛 Why was the old SPC showing 0 out-of-control points? (Bug explained)"):
        st.markdown(f"""
        **Root Cause of the Bug:**

        The original code used `baseline = ABSORPTION[:12]` — all 12 months of Jan–Dec 2023 as the baseline.

        But Jul–Dec 2023 had very high values (324, 424, 401, 587, 462) because that's when big project launches started.
        This inflated the standard deviation to σ = 203, making UCL = 820.

        Since the highest value ever was 766 (Dec-24), and 766 < 820, **nothing ever crossed UCL**.
        Result: 0 out-of-control points shown, even though the market was clearly out of control.

        **The Fix:**
        - Baseline = Jan–Jun 2023 only (the true pre-launch quiet period: 54, 38, 29, 24, 37, 22)
        - Method = I-MR chart (Moving Range σ estimate using d2=1.128) — the proper standard
        - Result: UCL = {ucl:.0f}, which correctly flags {ooc.sum()} out-of-control months
        - Added: MR-Chart, Runs Rule detection, interactive baseline selector, OOC table
        """)


# ═══════════════════════════════════════════════════════════════════
# ══════════  AI MAP SYSTEM PAGES  ══════════════════════════════════
# ═══════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────────────────────────────────
elif module == "🗺️ AI Map System" and page == "🏠 Home":
    st.markdown("## 🗺️ Bengaluru Real Estate — AI Decision Support System")
    st.markdown("""
    An **AI-powered map dashboard** that helps identify the **best construction zones** in Bengaluru
    using Six Sigma DMAIC methodology, Machine Learning, and interactive geospatial analysis.
    """)
    st.divider()

    total_areas  = len(areas_df)
    avg_score    = areas_df["suitability"].mean()
    top_area     = areas_df.loc[areas_df["suitability"].idxmax(), "area"]
    avg_price    = areas_df["avg_price_sqft"].mean()
    high_suit    = (areas_df["suitability"] >= 75).sum()
    low_flood    = (areas_df["flood_risk"] == "Low").sum()

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    cards = [
        (c1, "Areas Analysed",       f"{total_areas}",         "Bengaluru zones"),
        (c2, "Avg Suitability",      f"{avg_score:.0f}/100",   "Market average"),
        (c3, "Best Zone",            top_area,                  "Highest score"),
        (c4, "Avg Price",            f"₹{avg_price:,.0f}/sqft","Market price"),
        (c5, "Highly Suitable",      f"{high_suit} zones",      "Score ≥ 75"),
        (c6, "Low Flood Risk",       f"{low_flood} zones",      "Safe for build"),
    ]
    for col, title, val, sub in cards:
        col.markdown(f"""
        <div class="kpi">
          <div class="kpi-t">{title}</div>
          <div class="kpi-v">{val}</div>
          <div class="kpi-s">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec">🏆 Top 5 Construction-Ready Areas</div>', unsafe_allow_html=True)
    top5 = areas_df.nlargest(5, "suitability")[
        ["area","suitability","avg_price_sqft","flood_risk","metro_dist_km","segment"]
    ].reset_index(drop=True)
    top5.index += 1
    top5.columns = ["Area","Score","Price/sqft","Flood Risk","Metro (km)","Segment"]
    top5["Score"] = top5["Score"].round(1)
    st.dataframe(top5.style.background_gradient(subset=["Score"], cmap="RdYlGn"), use_container_width=True)

    st.markdown('<div class="sec">📋 Feature Guide</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    features = [
        ("📍 Interactive Map",   "Color-coded area markers, metro stations, click for details"),
        ("🤖 AI Analyzer",       "Select any area → get ML suitability score + breakdown"),
        ("📊 Price Analytics",   "Price trends, segment analysis, correlation heatmap"),
        ("📋 Compare Areas",     "Side-by-side comparison of 2–3 areas"),
        ("📈 DMAIC Charts",      "Pareto, sigma level, control charts"),
        ("🌡️ Heatmap View",      "Visual price & suitability heatmap over Bengaluru"),
    ]
    for i, (title, desc) in enumerate(features):
        cols[i % 3].markdown(f"""
        <div class="area-card">
          <b style="color:#e6edf3">{title}</b><br>
          <span style="color:#8892b0;font-size:12px">{desc}</span>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────
# PAGE: INTERACTIVE MAP
# ─────────────────────────────────────────────────────────────────────────
elif module == "🗺️ AI Map System" and page == "📍 Interactive Map":
    st.markdown("## 📍 Interactive Map — Bengaluru Real Estate Zones")

    col_ctrl, col_map = st.columns([1, 3])
    with col_ctrl:
        show_metro   = st.checkbox("Show Metro Stations", True)
        show_heatmap = st.checkbox("Color by Suitability", True)
        sel_segment  = st.multiselect("Filter by Segment",
            options=areas_df["segment"].unique().tolist(),
            default=areas_df["segment"].unique().tolist())
        sel_flood    = st.multiselect("Filter by Flood Risk",
            options=["Low","Medium","High"], default=["Low","Medium","High"])
        st.divider()
        st.markdown("**Legend**")
        st.markdown("🟢 Score ≥ 75 — Highly Suitable")
        st.markdown("🟡 Score 50–74 — Moderate")
        st.markdown("🔴 Score < 50 — Less Suitable")
        st.markdown("🔵 Metro Station")

    filtered = areas_df[
        areas_df["segment"].isin(sel_segment) &
        areas_df["flood_risk"].isin(sel_flood)
    ]

    with col_map:
        if not FOLIUM_OK:
            st.warning("⚠️ `streamlit-folium` not installed. Run: `pip install folium streamlit-folium`")
            st.markdown("**Area Table (Map Fallback)**")
            st.dataframe(filtered[["area","lat","lng","suitability","avg_price_sqft","flood_risk"]].round(2),
                         use_container_width=True)
        else:
            m = folium.Map(location=[12.9716, 77.5946], zoom_start=11,
                           tiles="CartoDB dark_matter", attribution_control=False)
            # Hide Leaflet attribution bar
            folium.Element(
                '<style>.leaflet-control-attribution{display:none!important;}</style>'
            ).add_to(m)

            for _, row in filtered.iterrows():
                s = row["suitability"]
                color = "#3fb950" if s >= 75 else ("#d29922" if s >= 50 else "#f85149")
                icon_color = "green" if s >= 75 else ("orange" if s >= 50 else "red")
                popup_html = f"""
                <div style="font-family:Arial;min-width:200px">
                  <b style="font-size:14px">{row['area']}</b><br>
                  <span style="color:{color};font-size:16px;font-weight:bold">{s:.0f}/100</span>
                  <span style="font-size:11px"> Suitability</span><br><hr style="margin:4px">
                  💰 ₹{row['avg_price_sqft']:,}/sqft &nbsp;|&nbsp; 📈 +{row['price_trend_yoy']}% YoY<br>
                  🚇 Metro: {row['metro_dist_km']} km &nbsp;|&nbsp; 🏥 Hospital: {row['hospital_dist_km']} km<br>
                  🏫 School: {row['school_dist_km']} km &nbsp;|&nbsp; 🌊 Flood: {row['flood_risk']}<br>
                  🛣 Road: {row['road_connectivity']}/10 &nbsp;|&nbsp; 📦 Unsold: {row['unsold_pct']}%
                </div>"""

                folium.CircleMarker(
                    location=[row["lat"], row["lng"]],
                    radius=12 if show_heatmap else 8,
                    color=color, fill=True, fill_color=color,
                    fill_opacity=0.85, weight=2,
                    popup=folium.Popup(popup_html, max_width=280),
                    tooltip=f"{row['area']} — {s:.0f}/100"
                ).add_to(m)

                folium.Marker(
                    location=[row["lat"] + 0.003, row["lng"]],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size:9px;color:{color};'
                             f'font-weight:bold;white-space:nowrap">{row["area"]}</div>',
                        icon_size=(100, 15), icon_anchor=(50, 0)
                    )
                ).add_to(m)

            if show_metro:
                for st_data in METRO_STATIONS:
                    lc = "#388bfd" if st_data["line"] == "Purple" else \
                         ("#3fb950" if st_data["line"] == "Green" else "#d29922")
                    folium.CircleMarker(
                        location=[st_data["lat"], st_data["lng"]],
                        radius=6, color=lc, fill=True, fill_color=lc,
                        fill_opacity=1.0, weight=2,
                        tooltip=f"🚇 {st_data['name']} ({st_data['line']} Line)"
                    ).add_to(m)

            map_data = st_folium(m, width=None, height=520, returned_objects=["last_object_clicked"])

            if map_data and map_data.get("last_object_clicked"):
                click = map_data["last_object_clicked"]
                clat, clng = click.get("lat"), click.get("lng")
                if clat and clng:
                    dists = np.sqrt((areas_df["lat"] - clat)**2 + (areas_df["lng"] - clng)**2)
                    nearest = areas_df.loc[dists.idxmin()]
                    s = nearest["suitability"]
                    lbl, cls = score_label(s)
                    st.markdown(f"""
                    <div class="area-card">
                      <b style="color:#e6edf3;font-size:15px">{nearest['area']}</b> &nbsp;
                      <span class="score-badge {cls}">{s:.0f}/100</span> &nbsp; {lbl}<br>
                      <span style="color:#8892b0;font-size:12px">
                      💰 ₹{nearest['avg_price_sqft']:,}/sqft &nbsp;|&nbsp;
                      🚇 {nearest['metro_dist_km']} km to metro &nbsp;|&nbsp;
                      🌊 Flood: {nearest['flood_risk']} &nbsp;|&nbsp;
                      📈 +{nearest['price_trend_yoy']}% YoY
                      </span>
                    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────
# PAGE: AI SUITABILITY ANALYZER
# ─────────────────────────────────────────────────────────────────────────
elif module == "🗺️ AI Map System" and page == "🤖 AI Suitability Analyzer":
    st.markdown("## 🤖 AI Construction Suitability Analyzer")
    st.markdown("Select any area to get an **ML-powered suitability score** with full breakdown.")

    sel_area = st.selectbox("🏙️ Select Area", areas_df["area"].tolist())
    row = areas_df[areas_df["area"] == sel_area].iloc[0]
    score = predict_area_score(row.to_dict())
    lbl, cls = score_label(score)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
        <div class="area-card" style="text-align:center;padding:30px">
          <div style="font-size:13px;color:#8892b0;margin-bottom:8px">SUITABILITY SCORE</div>
          <div class="score-badge {cls}" style="font-size:42px;padding:14px 30px">{score:.0f}</div>
          <div style="font-size:18px;color:#e6edf3;margin-top:14px">{lbl}</div>
          <div style="font-size:13px;color:#8892b0;margin-top:6px">{row['segment']} Segment</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        categories = ["Road\nConn.", "Infrastructure", "Pop.\nGrowth",
                      "Low Flood", "Metro\nAccess", "Amenities"]
        values = [
            row["road_connectivity"] * 10,
            row["infrastructure_score"] * 10,
            min(row["population_growth"] * 5, 100),
            100 - row["flood_num"] * 40,
            max(0, 100 - row["metro_dist_km"] * 6),
            max(0, 100 - (row["hospital_dist_km"] + row["school_dist_km"]) * 5),
        ]
        fig = go.Figure(go.Scatterpolar(
            r=values + [values[0]], theta=categories + [categories[0]],
            fill="toself", fillcolor="rgba(56,139,253,0.2)",
            line=dict(color="#388bfd", width=2), marker=dict(size=6, color="#388bfd"),
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100],
                                gridcolor="#e2e8f0", tickfont=dict(color="#64748b", size=9)),
                angularaxis=dict(gridcolor="#e2e8f0", tickfont=dict(color="#1e2d5a", size=10)),
                bgcolor="#f0f4ff"
            ),
            paper_bgcolor="#ffffff", font_color="#1e2d5a",
            title=dict(text="Area Profile Radar", font_size=13),
            height=320, margin=dict(t=40, b=10, l=50, r=50)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sec">📊 Detailed Breakdown</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="area-card">
          <b style="color:#388bfd">💰 Price & Market</b><br><br>
          {'✅' if row['avg_price_sqft'] < 10000 else '⚠️'} Price: ₹{row['avg_price_sqft']:,}/sqft<br>
          {'✅' if row['price_trend_yoy'] >= 10 else '⚠️'} YoY Growth: +{row['price_trend_yoy']}%<br>
          {'✅' if row['unsold_pct'] < 20 else '❌'} Unsold Rate: {row['unsold_pct']}%<br>
          ℹ️ Segment: {row['segment']}
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="area-card">
          <b style="color:#3fb950">🚇 Connectivity</b><br><br>
          {'✅' if row['metro_dist_km'] < 3 else '⚠️' if row['metro_dist_km'] < 7 else '❌'} Metro: {row['metro_dist_km']} km<br>
          {'✅' if row['highway_dist_km'] < 4 else '⚠️'} Highway: {row['highway_dist_km']} km<br>
          {'✅' if row['road_connectivity'] >= 8 else '⚠️' if row['road_connectivity'] >= 6 else '❌'} Road Score: {row['road_connectivity']}/10<br>
          {'✅' if row['mall_dist_km'] < 5 else '⚠️'} Mall: {row['mall_dist_km']} km
        </div>""", unsafe_allow_html=True)
    with c3:
        flood_icon = "✅" if row["flood_risk"] == "Low" else ("⚠️" if row["flood_risk"] == "Medium" else "❌")
        st.markdown(f"""
        <div class="area-card">
          <b style="color:#d29922">🏥 Amenities & Safety</b><br><br>
          {'✅' if row['hospital_dist_km'] < 2 else '⚠️'} Hospital: {row['hospital_dist_km']} km<br>
          {'✅' if row['school_dist_km'] < 1 else '⚠️'} School: {row['school_dist_km']} km<br>
          {'✅' if row['park_dist_km'] < 2 else '⚠️'} Park: {row['park_dist_km']} km<br>
          {flood_icon} Flood Risk: {row['flood_risk']}
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec">💡 AI Recommendation</div>', unsafe_allow_html=True)
    if score >= 75:
        st.success(f"""
🟢 **{sel_area}** is an **excellent location** for construction/investment.

- 🛤️ Road connectivity: **{row['road_connectivity']}/10**
- 🚇 Metro within **{row['metro_dist_km']} km**
- 🌊 Flood risk: **{'Low ✅' if row['flood_risk'] == 'Low' else row['flood_risk'] + ' ⚠️'}**
- 📈 Price appreciation: **+{row['price_trend_yoy']}% YoY**

**Recommended for:** Mid to premium residential, commercial development.
        """)
    elif score >= 50:
        cond_metro  = f"- 🚇 Metro access needs improvement **({row['metro_dist_km']} km)**" if row['metro_dist_km'] > 5 else ""
        cond_price  = f"- 💰 High price **₹{row['avg_price_sqft']:,}/sqft** may limit buyer pool" if row['avg_price_sqft'] > 10000 else ""
        cond_flood  = f"- 🌊 Flood risk is **{row['flood_risk']}** — structural mitigation needed" if row['flood_risk'] != 'Low' else ""
        issues_text = "\n".join(x for x in [cond_metro, cond_price, cond_flood] if x)
        st.warning(f"""
🟡 **{sel_area}** has **moderate potential** but requires careful evaluation.

{issues_text if issues_text else "- No major issues detected"}

**Recommended for:** Affordable housing, budget segment, long-term hold.
        """)
    else:
        cond_flood  = f"- 🌊 Flood risk: **{row['flood_risk']}**" if row['flood_risk'] == 'High' else ""
        cond_unsold = f"- 📦 High unsold inventory: **{row['unsold_pct']}%**" if row['unsold_pct'] > 30 else ""
        cond_metro  = f"- 🚇 Poor metro connectivity: **{row['metro_dist_km']} km**" if row['metro_dist_km'] > 10 else ""
        issues_text = "\n".join(x for x in [cond_flood, cond_unsold, cond_metro] if x)
        st.error(f"""
🔴 **{sel_area}** currently has **significant challenges** for construction.

{issues_text if issues_text else "- Multiple compounding factors"}

**Consider:** Wait for infrastructure development or target very affordable pricing.
        """)


# ─────────────────────────────────────────────────────────────────────────
# PAGE: PRICE ANALYTICS
# ─────────────────────────────────────────────────────────────────────────
elif module == "🗺️ AI Map System" and page == "📊 Price Analytics":
    st.markdown("## 📊 Price Analytics — Bengaluru Real Estate")

    tab1, tab2, tab3 = st.tabs(["💰 Price Overview","📈 Trend Analysis","🔗 Correlation"])

    with tab1:
        fig = go.Figure(go.Bar(
            x=areas_df.sort_values("avg_price_sqft")["area"],
            y=areas_df.sort_values("avg_price_sqft")["avg_price_sqft"],
            marker=dict(
                color=areas_df.sort_values("avg_price_sqft")["avg_price_sqft"],
                colorscale="RdYlGn", showscale=True,
                colorbar=dict(title="₹/sqft", tickfont=dict(color="#1e2d5a"))
            ),
            text=[f"₹{v:,}" for v in areas_df.sort_values("avg_price_sqft")["avg_price_sqft"]],
            textposition="outside", textfont=dict(color="#1e2d5a", size=9)
        ))
        fig.update_layout(
            title="Average Price per sqft — All Areas",
            plot_bgcolor="#f8faff", paper_bgcolor="#ffffff", font_color="#1e2d5a",
            height=480, xaxis=dict(tickangle=-40, gridcolor="#e2e8f0"),
            yaxis=dict(title="₹ / sqft", gridcolor="#e2e8f0"), margin=dict(b=120)
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            seg = areas_df.groupby("segment")["avg_price_sqft"].mean().reset_index()
            fig2 = px.pie(seg, names="segment", values="avg_price_sqft",
                          title="Avg Price by Segment", hole=0.55,
                          color_discrete_sequence=["#388bfd","#3fb950","#d29922","#f85149"])
            fig2.update_layout(paper_bgcolor="#ffffff", font_color="#1e2d5a",
                               plot_bgcolor="#f8faff", height=320)
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            flood_price = areas_df.groupby("flood_risk")["avg_price_sqft"].mean().reset_index()
            fig3 = px.bar(flood_price, x="flood_risk", y="avg_price_sqft",
                          title="Avg Price by Flood Risk", color="flood_risk",
                          color_discrete_map={"Low":"#3fb950","Medium":"#d29922","High":"#f85149"})
            fig3.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#f8faff",
                               font_color="#1e2d5a", height=320, showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        fig = go.Figure()
        for seg_type in ["Luxury","Premium","Mid","Budget"]:
            sub = areas_df[areas_df["segment"] == seg_type].sort_values("avg_price_sqft")
            if len(sub) == 0: continue
            fig.add_scatter(
                x=sub["area"], y=sub["price_trend_yoy"],
                mode="markers+text", name=seg_type,
                text=[f"+{v}%" for v in sub["price_trend_yoy"]],
                textposition="top center", marker=dict(size=14)
            )
        fig.add_hline(y=10, line_dash="dash", line_color="#d29922", annotation_text="10% avg growth")
        fig.update_layout(
            title="Year-over-Year Price Growth % by Area",
            plot_bgcolor="#f8faff", paper_bgcolor="#ffffff", font_color="#1e2d5a",
            height=440, xaxis=dict(tickangle=-40, gridcolor="#e2e8f0"),
            yaxis=dict(title="YoY Growth (%)", gridcolor="#e2e8f0"), margin=dict(b=120)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="sec">🚀 Top Growth Areas</div>', unsafe_allow_html=True)
        top_growth = areas_df.nlargest(5, "price_trend_yoy")[
            ["area","avg_price_sqft","price_trend_yoy","segment","suitability"]
        ].reset_index(drop=True)
        top_growth.index += 1
        st.dataframe(top_growth.style.background_gradient(subset=["price_trend_yoy"], cmap="Greens"),
                     use_container_width=True)

    with tab3:
        num_cols = ["avg_price_sqft","suitability","metro_dist_km","flood_num",
                    "road_connectivity","population_growth","unsold_pct","hospital_dist_km"]
        labels   = ["Price/sqft","Suitability","Metro km","Flood Risk",
                    "Road","Pop.Growth","Unsold%","Hospital km"]
        corr = areas_df[num_cols].corr()
        corr.columns = corr.index = labels
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=labels, y=labels,
            colorscale="RdBu", zmid=0, zmin=-1, zmax=1,
            text=[[f"{v:.2f}" for v in row] for row in corr.values],
            texttemplate="%{text}", hoverongaps=False
        ))
        fig.update_layout(
            title="Feature Correlation Matrix",
            paper_bgcolor="#ffffff", plot_bgcolor="#f8faff",
            font_color="#1e2d5a", height=480, xaxis=dict(tickangle=-30)
        )
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────
# PAGE: AREA COMPARISON
# ─────────────────────────────────────────────────────────────────────────
elif module == "🗺️ AI Map System" and page == "📋 Area Comparison":
    st.markdown("## 📋 Side-by-Side Area Comparison")
    st.markdown("Compare **2 or 3 areas** across all key metrics.")

    area_list = areas_df["area"].tolist()
    c1, c2, c3 = st.columns(3)
    a1 = c1.selectbox("Area 1", area_list, index=0)
    a2 = c2.selectbox("Area 2", area_list, index=1)
    a3 = c3.selectbox("Area 3 (optional)", ["None"] + area_list, index=0)

    selected = [a1, a2] + ([a3] if a3 != "None" else [])
    comp_df  = areas_df[areas_df["area"].isin(selected)].copy()
    comp_df["suitability"] = comp_df.apply(lambda r: predict_area_score(r.to_dict()), axis=1)

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(len(selected))
    for col, area_name in zip(cols, selected):
        row = comp_df[comp_df["area"] == area_name].iloc[0]
        s = row["suitability"]
        lbl, cls = score_label(s)
        col.markdown(f"""
        <div class="area-card" style="text-align:center">
          <div style="font-size:14px;font-weight:700;color:#e6edf3;margin-bottom:10px">{area_name}</div>
          <div class="score-badge {cls}" style="font-size:28px;padding:10px 20px">{s:.0f}/100</div>
          <div style="font-size:12px;color:#8892b0;margin-top:8px">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec">📊 Comparison Table</div>', unsafe_allow_html=True)

    metrics = {
        "💰 Price/sqft":          ("avg_price_sqft",      "₹{:,}"),
        "📈 YoY Growth":          ("price_trend_yoy",     "+{}%"),
        "🤖 Suitability Score":   ("suitability",         "{:.0f}/100"),
        "🚇 Metro Distance":      ("metro_dist_km",       "{} km"),
        "🏥 Hospital Distance":   ("hospital_dist_km",    "{} km"),
        "🏫 School Distance":     ("school_dist_km",      "{} km"),
        "🛍 Mall Distance":       ("mall_dist_km",        "{} km"),
        "🛣 Highway Distance":    ("highway_dist_km",     "{} km"),
        "🌳 Park Distance":       ("park_dist_km",        "{} km"),
        "🌊 Flood Risk":          ("flood_risk",          "{}"),
        "🛤 Road Connectivity":   ("road_connectivity",   "{}/10"),
        "🏗 Infrastructure":      ("infrastructure_score","{}//10"),
        "👥 Pop. Growth":         ("population_growth",   "+{}% p.a."),
        "📦 Unsold Rate":         ("unsold_pct",          "{}%"),
        "🏷 Segment":             ("segment",             "{}"),
    }

    table_rows = []
    for metric_lbl, (col_key, fmt) in metrics.items():
        row_data = {"Feature": metric_lbl}
        for area_name in selected:
            val = comp_df[comp_df["area"] == area_name].iloc[0][col_key]
            try:
                row_data[area_name] = fmt.format(val)
            except Exception:
                row_data[area_name] = str(val)
        table_rows.append(row_data)

    table = pd.DataFrame(table_rows)
    st.dataframe(table.set_index("Feature"), use_container_width=True)

    st.markdown('<div class="sec">🕸️ Radar Comparison</div>', unsafe_allow_html=True)
    radar_cats = ["Road\nConn.","Infrastructure","Pop.\nGrowth","Low Flood","Metro\nAccess","Amenities"]
    colors = ["#388bfd","#3fb950","#d29922"]
    fig = go.Figure()
    for i, area_name in enumerate(selected):
        row = comp_df[comp_df["area"] == area_name].iloc[0]
        vals = [
            row["road_connectivity"] * 10,
            row["infrastructure_score"] * 10,
            min(row["population_growth"] * 5, 100),
            100 - row["flood_num"] * 40,
            max(0, 100 - row["metro_dist_km"] * 6),
            max(0, 100 - (row["hospital_dist_km"] + row["school_dist_km"]) * 5),
        ]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=radar_cats + [radar_cats[0]],
            fill="toself", name=area_name,
            line=dict(color=colors[i % len(colors)], width=2),
            fillcolor=f"rgba{tuple(list(bytes.fromhex(colors[i % len(colors)][1:])) + [40])}",
            marker=dict(size=6, color=colors[i % len(colors)])
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor="#e2e8f0", tickfont=dict(color="#64748b", size=8)),
            angularaxis=dict(gridcolor="#e2e8f0", tickfont=dict(color="#1e2d5a", size=10)),
            bgcolor="#f0f4ff"
        ),
        paper_bgcolor="#ffffff", font_color="#1e2d5a",
        title="Area Comparison Radar",
        height=420, legend=dict(orientation="h", y=-0.1)
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure(go.Bar(
        x=[r["area"] for _, r in comp_df.iterrows()],
        y=[r["suitability"] for _, r in comp_df.iterrows()],
        marker=dict(
            color=[r["suitability"] for _, r in comp_df.iterrows()],
            colorscale="RdYlGn", cmin=0, cmax=100, showscale=False
        ),
        text=[f"{r['suitability']:.0f}" for _, r in comp_df.iterrows()],
        textposition="outside", textfont=dict(size=16, color="#e6edf3"),
        width=0.4
    ))
    fig2.add_hline(y=75, line_dash="dash", line_color="#3fb950", annotation_text="High Suitability")
    fig2.add_hline(y=50, line_dash="dash", line_color="#d29922", annotation_text="Moderate")
    fig2.update_layout(
        title="Suitability Score Comparison",
        plot_bgcolor="#f8faff", paper_bgcolor="#ffffff", font_color="#1e2d5a",
        height=340, yaxis=dict(range=[0, 110], gridcolor="#e2e8f0"),
        xaxis=dict(gridcolor="#e2e8f0")
    )
    st.plotly_chart(fig2, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────
# PAGE: DMAIC CHARTS (Map Dashboard)
# ─────────────────────────────────────────────────────────────────────────
elif module == "🗺️ AI Map System" and page == "📈 DMAIC Charts":
    st.markdown("## 📈 DMAIC Analysis — Six Sigma Framework")

    tab_d, tab_m, tab_a, tab_i, tab_c = st.tabs([
        "📋 Define","📏 Measure","🔍 Analyze","⚙️ Improve","📊 Control"
    ])

    with tab_d:
        st.markdown('<div class="sec">📋 DEFINE — Problem & CTQ</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="area-card">
              <b style="color:#388bfd;font-size:14px">Problem Statement</b><br><br>
              Bengaluru's real estate market suffers from:<br>
              🔴 Unsold inventory accumulation<br>
              🔴 Price inconsistency across micro-markets<br>
              🔴 Poor construction zone selection<br>
              🔴 Infrastructure-demand mismatch<br><br>
              <b>CTQ:</b> Construction Suitability Score ≥ 75/100<br>
              <b>Defect:</b> Any zone scoring below 50/100
            </div>""", unsafe_allow_html=True)
        with c2:
            sipoc = pd.DataFrame({
                "SIPOC": ["Suppliers","Inputs","Process","Outputs","Customers"],
                "Details": [
                    "RERA, Builders, Metro Authority",
                    "Property data, OSM amenities, Flood maps",
                    "DMAIC → ML Scoring → Map Visualization",
                    "Suitability Score, Investment Report",
                    "Builders, Investors, Urban Planners"
                ]
            })
            st.dataframe(sipoc.set_index("SIPOC"), use_container_width=True)

    with tab_m:
        st.markdown('<div class="sec">📏 MEASURE — Baseline Metrics</div>', unsafe_allow_html=True)
        total_u_m    = 10283
        unsold_u_m   = 1741
        dpmo_m       = unsold_u_m / total_u_m * 1_000_000
        sigma_m      = 0.8406 + np.sqrt(max(0, 29.37 - 2.221 * np.log(max(dpmo_m, 1))))
        avg_s        = areas_df["suitability"].mean()
        below50      = (areas_df["suitability"] < 50).sum()

        c1,c2,c3,c4 = st.columns(4)
        for col, t, v, s in [
            (c1,"Process Sigma",    f"{sigma_m:.2f}σ",     "Target: 6σ"),
            (c2,"DPMO",            f"{dpmo_m:,.0f}",       "Defects/Million"),
            (c3,"Avg Suit. Score", f"{avg_s:.1f}/100",   "Across 25 areas"),
            (c4,"Low-Score Zones", f"{below50}",         "Score < 50"),
        ]:
            col.markdown(f"""
            <div class="kpi"><div class="kpi-t">{t}</div>
            <div class="kpi-v">{v}</div><div class="kpi-s">{s}</div></div>""",
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        fig = px.histogram(
            areas_df, x="suitability", nbins=10, color="flood_risk",
            title="Distribution of Suitability Scores",
            color_discrete_map={"Low":"#3fb950","Medium":"#d29922","High":"#f85149"},
            template="plotly_dark"
        )
        fig.add_vline(x=75, line_dash="dash", line_color="#388bfd", annotation_text="Target ≥75")
        fig.add_vline(x=50, line_dash="dash", line_color="#d29922", annotation_text="Threshold 50")
        fig.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#f8faff",
                          font_color="#1e2d5a", height=360)
        st.plotly_chart(fig, use_container_width=True)

    with tab_a:
        st.markdown('<div class="sec">🔍 ANALYZE — Pareto Root Cause</div>', unsafe_allow_html=True)
        causes = ["High Flood Risk","Poor Metro Access","High Price","Low Infrastructure",
                  "New Developer","Post-Sat. Launch","Oversized Units","Low Amenities"]
        units  = [420,380,310,215,180,155,95,60]
        cum    = np.cumsum(units) / sum(units) * 100

        fig = go.Figure()
        fig.add_bar(x=causes, y=units, name="Unsold Units",
                    marker_color=["#f85149","#f85149","#d29922","#d29922",
                                  "#d29922","#3fb950","#3fb950","#3fb950"],
                    text=units, textposition="outside")
        fig.add_scatter(x=causes, y=cum, mode="lines+markers+text", name="Cumulative %", yaxis="y2",
                        text=[f"{v:.0f}%" for v in cum], textposition="top center",
                        line=dict(color="white", width=2), marker=dict(size=8))
        fig.add_hline(y=80, line_dash="dash", line_color="#d29922",
                      annotation_text="80% Line", secondary_y=True)
        fig.update_layout(
            yaxis2=dict(overlaying="y", side="right", range=[0, 115]),
            paper_bgcolor="#ffffff", plot_bgcolor="#f8faff", font_color="#1e2d5a",
            height=420, title="Pareto — Root Causes of Low Suitability",
            legend=dict(orientation="h", y=1.08)
        )
        st.plotly_chart(fig, use_container_width=True)

        fi = pd.Series(map_rf_model.feature_importances_, index=MAP_FEAT_COLS).sort_values(ascending=True)
        fig2 = go.Figure(go.Bar(
            x=fi.values, y=fi.index, orientation="h",
            marker=dict(color=fi.values, colorscale="RdYlGn", showscale=False),
            text=[f"{v:.3f}" for v in fi.values], textposition="outside"
        ))
        fig2.update_layout(
            title="RF Feature Importance — Drivers of Suitability",
            paper_bgcolor="#ffffff", plot_bgcolor="#f8faff", font_color="#1e2d5a",
            height=380, xaxis=dict(gridcolor="#e2e8f0"),
            yaxis=dict(gridcolor="#e2e8f0"), margin=dict(l=130)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab_i:
        st.markdown('<div class="sec">⚙️ IMPROVE — Intervention What-If</div>', unsafe_allow_html=True)
        low_areas = areas_df[areas_df["suitability"] < 65].copy()
        if low_areas.empty:
            st.success("All areas already have high suitability!")
        else:
            whatif = []
            for _, row in low_areas.iterrows():
                before = predict_area_score(row.to_dict())
                new_row = row.copy()
                new_row["metro_dist_km"] = max(1.5, row["metro_dist_km"] * 0.5)
                new_row["infrastructure_score"] = min(10, row["infrastructure_score"] + 2)
                after = predict_area_score(new_row.to_dict())
                whatif.append({
                    "Area": row["area"], "Before": round(before, 1),
                    "After": round(after, 1), "Gain": round(after - before, 1),
                    "Key Action": (
                        "New metro station + infra upgrade" if row["metro_dist_km"] > 5
                        else "Infrastructure upgrade + connectivity boost"
                    )
                })
            wdf = pd.DataFrame(whatif).sort_values("Gain", ascending=False)
            fig = go.Figure()
            fig.add_bar(x=wdf["Area"], y=wdf["Before"], name="Current Score",
                        marker_color="#f85149", text=wdf["Before"].round(1), textposition="outside")
            fig.add_bar(x=wdf["Area"], y=wdf["After"], name="After Intervention",
                        marker_color="#3fb950", text=wdf["After"].round(1), textposition="outside")
            fig.update_layout(barmode="group", title="Before vs After Infrastructure Intervention",
                              paper_bgcolor="#ffffff", plot_bgcolor="#f8faff",
                              font_color="#1e2d5a", height=380,
                              yaxis=dict(range=[0, 110], gridcolor="#e2e8f0"),
                              xaxis=dict(gridcolor="#e2e8f0", tickangle=-30),
                              legend=dict(orientation="h", y=1.08))
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(wdf.style.background_gradient(subset=["Gain"], cmap="Greens"),
                         hide_index=True, use_container_width=True)

    with tab_c:
        st.markdown('<div class="sec">📊 CONTROL — SPC Control Chart</div>', unsafe_allow_html=True)
        months_ctrl = ["Jan-23","Apr-23","Jul-23","Oct-23","Jan-24","Apr-24",
                  "Jul-24","Oct-24","Jan-25","Apr-25","Jul-25"]
        absorption_ctrl = np.array([54,185,520,400,350,480,320,560,380,450,290], dtype=float)
        baseline_ctrl = absorption_ctrl[:4]
        cl_c  = baseline_ctrl.mean()
        mr_c  = np.abs(np.diff(baseline_ctrl)).mean()
        ucl_c = cl_c + 2.66 * mr_c
        lcl_c = max(0, cl_c - 2.66 * mr_c)

        colors_ctrl = ["#f85149" if v > ucl_c else "#3fb950" for v in absorption_ctrl]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_ctrl+months_ctrl[::-1], y=[ucl_c]*len(months_ctrl)+[lcl_c]*len(months_ctrl),
                                 fill="toself", fillcolor="rgba(56,139,253,0.08)",
                                 line=dict(width=0), name="Control Band"))
        fig.add_scatter(x=months_ctrl, y=[ucl_c]*len(months_ctrl), mode="lines",
                        line=dict(color="#f85149", dash="dash", width=1.5), name="UCL")
        fig.add_scatter(x=months_ctrl, y=[cl_c]*len(months_ctrl),  mode="lines",
                        line=dict(color="#1e2d5a", dash="solid", width=2), name="CL")
        fig.add_scatter(x=months_ctrl, y=[lcl_c]*len(months_ctrl), mode="lines",
                        line=dict(color="#388bfd", dash="dash", width=1.5), name="LCL")
        fig.add_scatter(x=months_ctrl, y=absorption_ctrl, mode="lines+markers",
                        marker=dict(color=colors_ctrl, size=10, line=dict(width=2, color="#fff")),
                        line=dict(color="#7c3aed", width=2), name="Monthly Sales")
        fig.update_layout(
            title=f"I-MR Control Chart — Monthly Absorption | CL={cl_c:.0f} UCL={ucl_c:.0f} LCL={lcl_c:.0f}",
            paper_bgcolor="#ffffff", plot_bgcolor="#f8faff", font_color="#1e2d5a",
            height=420, yaxis=dict(title="Units/month", gridcolor="#e2e8f0"),
            xaxis=dict(gridcolor="#e2e8f0"), legend=dict(orientation="h", y=1.08)
        )
        st.plotly_chart(fig, use_container_width=True)

        kc1, kc2, kc3 = st.columns(3)
        kc1.metric("Centre Line", f"{cl_c:.0f} units/mo")
        kc2.metric("UCL (3σ)",   f"{ucl_c:.0f} units/mo")
        kc3.metric("LCL (3σ)",   f"{lcl_c:.0f} units/mo")


# ─────────────────────────────────────────────────────────────────────────
# PAGE: HEATMAP VIEW
# ─────────────────────────────────────────────────────────────────────────
elif module == "🗺️ AI Map System" and page == "🌡️ Heatmap View":
    st.markdown("## 🌡️ Bengaluru Heatmap View")

    metric_choice = st.radio("Color by:",
        ["Suitability Score","Price per sqft","YoY Price Growth","Unsold %"],
        horizontal=True)

    col_map_h = {
        "Suitability Score":  ("suitability",      "RdYlGn", "Score"),
        "Price per sqft":     ("avg_price_sqft",   "Reds",   "₹/sqft"),
        "YoY Price Growth":   ("price_trend_yoy",  "Greens", "% Growth"),
        "Unsold %":           ("unsold_pct",        "Reds",   "% Unsold"),
    }
    col_key, cscale, ctitle = col_map_h[metric_choice]

    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        lat=areas_df["lat"], lon=areas_df["lng"],
        mode="markers+text",
        marker=dict(
            size=22,
            color=areas_df[col_key],
            colorscale=cscale, showscale=True,
            colorbar=dict(title=ctitle, tickfont=dict(color="#1e2d5a")),
            opacity=0.85
        ),
        text=areas_df["area"],
        textposition="top center",
        textfont=dict(color="#fff", size=9),
        customdata=np.stack([
            areas_df["avg_price_sqft"],
            areas_df["suitability"],
            areas_df["flood_risk"],
            areas_df["price_trend_yoy"]
        ], axis=-1),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "💰 ₹%{customdata[0]:,}/sqft<br>"
            "🤖 Suitability: %{customdata[1]:.0f}/100<br>"
            "🌊 Flood: %{customdata[2]}<br>"
            "📈 YoY: +%{customdata[3]}%<extra></extra>"
        )
    ))

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=12.97, lon=77.59),
            zoom=10
        ),
        paper_bgcolor="#ffffff", font_color="#1e2d5a",
        height=580, margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sec">📊 Rankings Table</div>', unsafe_allow_html=True)
    rank_df = areas_df.sort_values(col_key, ascending=(col_key in ["unsold_pct","metro_dist_km"]))[
        ["area","avg_price_sqft","suitability","price_trend_yoy","flood_risk","segment","unsold_pct"]
    ].reset_index(drop=True)
    rank_df.index += 1
    rank_df.columns = ["Area","Price/sqft","Suitability","YoY%","Flood Risk","Segment","Unsold%"]
    st.dataframe(
        rank_df.style.background_gradient(subset=["Suitability"], cmap="RdYlGn"),
        use_container_width=True
    )


# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:0.8rem;padding:10px">
Bengaluru Real Estate Unified Dashboard · Six Sigma DMAIC · AI Map Decision Support<br>
Built with Streamlit · SimPy Digital Twin · Plotly · Folium · Random Forest · Gradient Boosting
</div>""", unsafe_allow_html=True)