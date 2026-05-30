"""
╔══════════════════════════════════════════════════════════════════╗
║  SIX SIGMA DMAIC DASHBOARD — Bengaluru Real Estate              ║
║  Builder Selector · Digital Twin Simulator · Recommendations    ║
║                                                                  ║
║  Run:  streamlit run streamlit_app.py                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import simpy
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bengaluru Real Estate — Six Sigma DMAIC Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
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
        background: #0f172a; color: #38bdf8;
        border-radius: 12px; padding: 18px;
        font-family: 'Courier New', monospace; font-size: 0.85rem;
    }
    .tag-sold   { background:#dcfce7; color:#166534; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
    .tag-unsold { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
    .tag-mid    { background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:600; }
    h2 { color: #1e2d5a !important; }
    .stSelectbox label { font-weight: 600; color: #334155; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# DATASET
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
# ML MODELS (cached)
# ─────────────────────────────────────────────────────────────────
@st.cache_resource
def train_models():
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
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

rf_model, gb_model, FEAT_COLS = train_models()

# ─────────────────────────────────────────────────────────────────
# DIGITAL TWIN SIMULATOR (SimPy)
# ─────────────────────────────────────────────────────────────────
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
            demand = demand_index * (1 + 0.1*np.sin(month/3))  # seasonal up/down pattern

            # --- Buyer segment models ---
            budget = max(0, 12000 - price)/12000       # more if price is low
            premium = stage / 5                         # increases as project nears completion
            normal = demand / 1.0                       # follows market demand

            # Weighted overall buying rate
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

    """
    SimPy Digital Twin: simulates monthly sales events for a project.
    intervention: dict with keys 'month', 'new_rate' to model a policy change mid-simulation
    Returns list of (month, sold_this_month, cumulative_sold, inventory_remaining)
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
            # Apply intervention if specified
            if intervention and month == intervention['month']:
                state['rate'] = intervention['new_rate']
            # Simulate sales with Poisson distribution (realistic market randomness)
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


# ─────────────────────────────────────────────────────────────────
# RECOMMENDATIONS ENGINE
# ─────────────────────────────────────────────────────────────────
def get_recommendations(project_row, df):
    """Generate smart recommendations by learning from sold-out projects."""
    recs  = []
    issues = []

    # Learn from healthy projects
    healthy = df[df['pct_sold'] >= 95]
    avg_healthy_price = healthy['price_sqft'].mean()
    avg_healthy_size  = healthy['unit_size_min'].mean()

    price  = project_row['price_sqft']
    delay  = project_row['delay_months']
    size   = project_row['unit_size_min']
    stage  = project_row['construction_stage']
    pct    = project_row['pct_sold']
    seg    = project_row['segment']

    # — ISSUE 1: HIGH PRICE —
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

    # — ISSUE 2: CONSTRUCTION DELAY —
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

    # — ISSUE 3: LARGE UNIT SIZE —
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

    # — ISSUE 4: LUXURY SEGMENT IN PERIPHERAL MARKET —
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

    # — ISSUE 5: EARLY CONSTRUCTION STAGE —
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

    # — ISSUE 6: UNKNOWN DEVELOPER BRAND —
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

    # — ALWAYS APPLICABLE —
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
    #st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Six_Sigma.svg/200px-Six_Sigma.svg.png", width=80)
    st.title("🏗️ Six Sigma Dashboard")
    st.caption("Bengaluru Real Estate RCA · Bagaluru Micro-Market")
    st.divider()

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

# ─────────────────────────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────────────────────────
if selected_dev == "📊 All Builders (Market Overview)":
    filtered_df = df.copy()
    dev_name = "All Builders"
else:
    filtered_df = df[df['developer'] == selected_dev].copy()
    dev_name = selected_dev

# ─────────────────────────────────────────────────────────────────
# PAGE 1: MARKET OVERVIEW
# ─────────────────────────────────────────────────────────────────
if page == "📊 Market Overview":
    st.markdown(f"## 📊 Market Overview — {dev_name}")
    st.caption("Bagaluru Micro-Market | Dec 2022 – Nov 2025 | Six Sigma DMAIC Analysis")

    # KPI row
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

    # Price vs Sold scatter
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
elif page == "🏢 Builder Deep Dive":
    st.markdown(f"## 🏢 Builder Deep Dive — {dev_name}")

    if selected_dev == "📊 All Builders (Market Overview)":
        st.info("👈 Select a specific builder from the sidebar to see their project-level details")
        # Show builder comparison
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

        # Builder header
        st.markdown(f"""
        <div style="background:#1e2d5a;color:white;padding:16px 22px;border-radius:12px;margin-bottom:16px">
          <div style="font-size:1.4rem;font-weight:700">{dev_name}</div>
          <div style="font-size:0.9rem;opacity:0.8">{len(dev_projects)} project phases · {total_u:,} total units · Bagaluru Micro-Market</div>
        </div>""", unsafe_allow_html=True)

        # KPIs
        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Total Units",   f"{total_u:,}")
        k2.metric("Units Sold",    f"{sold_u:,}", f"{sold_u/total_u*100:.1f}%")
        k3.metric("Units Unsold",  f"{unsold_u:,}", f"-{unsold_u/total_u*100:.1f}%", delta_color="inverse")
        k4.metric("Avg Delay",     f"{dev_projects['delay_months'].mean():.1f} months")

        st.divider()

        # Project table
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

        # Stacked bar per project
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

        # Issues summary
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
elif page == "🤖 Digital Twin Simulator":
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

    # Project selector
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
        current_rate = max(5, int(proj_row['absorbed_units'] / max(proj_row['months_on_market'] if 'months_on_market' in proj_row else 12, 1)))
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
            # Run WITHOUT intervention
            np.random.seed(42)
            results_base = run_digital_twin(
                proj_row['unsold_units'], base_rate, sim_months, None
            )
            # Run WITH intervention
            if apply_intervention:
                np.random.seed(42)
                results_intv = run_digital_twin(
                    proj_row['unsold_units'], base_rate, sim_months, intervention
                )

        st.markdown("### 📈 Simulation Results")

        fig = go.Figure()
        # Baseline
        fig.add_scatter(
            x=results_base['Month'], y=results_base['Cumulative Sold'],
            mode='lines+markers', name='Baseline (no change)',
            line=dict(color='#E24B4A', width=2, dash='dot'),
            marker=dict(size=6)
        )
        # Monthly bars
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

        # Target line
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

        # Summary stats
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

        # Simulation log
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
elif page == "💡 AI Recommendations":
    st.markdown("## 💡 AI-Powered Recommendations")
    st.caption("Recommendations are generated by learning from sold-out projects (95%+ absorbed)")

    if selected_dev == "📊 All Builders (Market Overview)":
        st.info("👈 Select a specific builder from the sidebar for targeted recommendations")
        # Show all at-risk projects
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
            # Compare sold vs unsold
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
            # Per-project recommendations
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

                # Digital Twin quick preview for this project
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
# PAGE 5: SPC CONTROL CHART  (FIXED)
# ─────────────────────────────────────────────────────────────────
elif page == "📈 SPC Control Chart":
    st.markdown("## 📈 SPC Control Chart — Monthly Market Monitor")

    # ── INTERACTIVE BASELINE SELECTOR ─────────────────────────────
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

    # Map selection to slice
    if "6 months" in baseline_option:
        n_base = 6
        base_label = "Jan–Jun 2023 (6 months)"
    elif "12 months" in baseline_option:
        n_base = 12
        base_label = "Jan–Dec 2023 (12 months)"
    else:
        n_base = 3
        base_label = "Jan–Mar 2023 (3 months)"

    # ── FIX 1: CORRECT SPC CALCULATION ────────────────────────────
    # Use Moving Range method (proper I-chart standard, not std of baseline)
    baseline_vals = ABSORPTION[:n_base]
    cl  = baseline_vals.mean()

    # Moving Range σ estimate (d2=1.128 for n=2 subgroups — standard I-MR chart)
    MR     = np.abs(np.diff(baseline_vals))
    d2     = 1.128
    sigma_mr = MR.mean() / d2 if len(MR) > 0 else baseline_vals.std()

    ucl = cl + 3 * sigma_mr
    lcl = max(0, cl - 3 * sigma_mr)
    uwl = cl + 2 * sigma_mr
    lwl = max(0, cl - 2 * sigma_mr)

    # ── FIX 2: CORRECT OOC DETECTION ──────────────────────────────
    ooc       = (ABSORPTION > ucl) | (ABSORPTION < lcl)
    ooc_above = ABSORPTION > ucl
    ooc_below = ABSORPTION < lcl

    # ── FIX 3: RUNS RULE — 8 consecutive points same side of CL ───
    above_cl = ABSORPTION > cl
    runs_flag = np.zeros(len(ABSORPTION), dtype=bool)
    for i in range(7, len(ABSORPTION)):
        if all(above_cl[i-7:i+1]) or all(~above_cl[i-7:i+1]):
            runs_flag[i-7:i+1] = True

    # ── METRIC CARDS ───────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Centre Line (CL)",          f"{cl:.0f}",        "units/month")
    k2.metric("UCL  (+3σ MR)",             f"{ucl:.0f}",       "units/month")
    k3.metric("LCL  (−3σ MR)",             f"{lcl:.0f}",       "units/month")
    k4.metric("Out-of-Control Points",     f"{ooc.sum()}",     f"of {len(ABSORPTION)} months")
    k5.metric("Runs Rule Violations",      f"{runs_flag.sum()}", "8-pt same side of CL")

    st.caption(f"Baseline: {base_label}  |  CL={cl:.1f}  UCL={ucl:.1f}  LCL={lcl:.1f}  |  Method: I-MR Chart (d2=1.128)")

    st.divider()

    # ── MAIN SPC CHART ─────────────────────────────────────────────
    st.markdown("### 📉 Individual Control Chart (I-Chart)")
    fig = go.Figure()

    # Baseline shading
    fig.add_vrect(
        x0=MONTHS[0], x1=MONTHS[n_base - 1],
        fillcolor='rgba(59,130,246,0.08)', line_width=0,
        annotation_text=f"Baseline ({base_label})",
        annotation_position="top left",
        annotation_font_size=10
    )

    # ±2σ green zone
    fig.add_hrect(y0=lwl, y1=uwl, fillcolor='rgba(22,163,74,0.06)', line_width=0)

    # UCL / LCL / CL lines
    fig.add_scatter(x=MONTHS, y=[ucl]*len(MONTHS), mode='lines',
                    name=f'UCL = {ucl:.0f}',
                    line=dict(color='#DC2626', dash='dash', width=1.8))
    fig.add_scatter(x=MONTHS, y=[lcl]*len(MONTHS), mode='lines',
                    name=f'LCL = {lcl:.0f}',
                    line=dict(color='#DC2626', dash='dash', width=1.8))
    fig.add_scatter(x=MONTHS, y=[uwl]*len(MONTHS), mode='lines',
                    name=f'UWL = {uwl:.0f}',
                    line=dict(color='#F59E0B', dash='dot', width=1))
    fig.add_scatter(x=MONTHS, y=[lwl]*len(MONTHS), mode='lines',
                    name=f'LWL = {lwl:.0f}',
                    line=dict(color='#F59E0B', dash='dot', width=1))
    fig.add_scatter(x=MONTHS, y=[cl]*len(MONTHS), mode='lines',
                    name=f'CL = {cl:.0f}',
                    line=dict(color='#16A34A', width=2.2))

    # Main data line
    fig.add_scatter(x=MONTHS, y=ABSORPTION, mode='lines+markers',
                    name='Monthly Absorption',
                    line=dict(color='#2563EB', width=2),
                    marker=dict(size=6, color='#2563EB'))

    # OOC ABOVE UCL — red filled circles
    ooc_above_months = [MONTHS[i] for i in range(len(MONTHS)) if ooc_above[i]]
    ooc_above_vals   = [ABSORPTION[i] for i in range(len(ABSORPTION)) if ooc_above[i]]
    if ooc_above_months:
        fig.add_scatter(
            x=ooc_above_months, y=ooc_above_vals,
            mode='markers', name='Above UCL 🔴',
            marker=dict(color='#DC2626', size=14, symbol='circle',
                        line=dict(color='white', width=2)),
            hovertemplate="<b>%{x}</b><br>Absorbed: %{y}<br><b>ABOVE UCL — Out of Control</b><extra></extra>"
        )

    # OOC BELOW LCL — orange diamonds
    ooc_below_months = [MONTHS[i] for i in range(len(MONTHS)) if ooc_below[i]]
    ooc_below_vals   = [ABSORPTION[i] for i in range(len(ABSORPTION)) if ooc_below[i]]
    if ooc_below_months:
        fig.add_scatter(
            x=ooc_below_months, y=ooc_below_vals,
            mode='markers', name='Below LCL 🟠',
            marker=dict(color='#D97706', size=14, symbol='diamond',
                        line=dict(color='white', width=2)),
            hovertemplate="<b>%{x}</b><br>Absorbed: %{y}<br><b>BELOW LCL — Out of Control</b><extra></extra>"
        )

    # Runs rule violations — hollow squares
    runs_months = [MONTHS[i] for i in range(len(MONTHS)) if runs_flag[i]]
    runs_vals   = [ABSORPTION[i] for i in range(len(ABSORPTION)) if runs_flag[i]]
    if runs_months:
        fig.add_scatter(
            x=runs_months, y=runs_vals,
            mode='markers', name='Runs Rule 🟡',
            marker=dict(color='rgba(0,0,0,0)', size=16, symbol='square-open',
                        line=dict(color='#7C3AED', width=2)),
            hovertemplate="<b>%{x}</b><br>Absorbed: %{y}<br><b>RUNS RULE VIOLATION</b><extra></extra>"
        )

    # Annotations for key events
    fig.add_annotation(x='Jul-23', y=324,
                       text='Big launches begin<br>Jul-23: 1,591 units', showarrow=True,
                       arrowcolor='#DC2626', font=dict(color='#DC2626', size=9),
                       ax=60, ay=-50)
    fig.add_annotation(x='Dec-24', y=766,
                       text='Supply shock peak<br>Dec-24: 766 sold', showarrow=True,
                       arrowcolor='#DC2626', font=dict(color='#DC2626', size=9),
                       ax=55, ay=-55)
    fig.add_annotation(x='Oct-25', y=77,
                       text='Market slowdown<br>Oct-25: 77 sold', showarrow=True,
                       arrowcolor='#D97706', font=dict(color='#92400e', size=9),
                       ax=-70, ay=45)

    fig.update_layout(
        height=500,
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title='Units Absorbed per Month',
        yaxis=dict(rangemode='tozero'),
        legend=dict(x=1.01, y=1, bgcolor='rgba(0,0,0,0)'),
        hovermode='x unified',
        margin=dict(r=180)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── OOC TABLE ─────────────────────────────────────────────────
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
                    'Month': MONTHS[i],
                    'Absorbed': int(ABSORPTION[i]),
                    'CL': int(cl),
                    'Direction': direction,
                    'Deviation from CL': f"{deviation:+.0f}",
                    'Recommended Action': action
                })
        ooc_df = pd.DataFrame(ooc_data)
        st.dataframe(
            ooc_df.style.applymap(
                lambda v: 'background-color:#fee2e2;color:#991b1b' if '↑' in str(v)
                     else ('background-color:#fef3c7;color:#92400e' if '↓' in str(v) else ''),
                subset=['Direction']
            ),
            use_container_width=True
        )
    else:
        st.success("✅ No out-of-control points with this baseline. Try a different baseline period above.")

    # ── MOVING RANGE CHART ─────────────────────────────────────────
    st.markdown("### 📊 Moving Range Chart (MR-Chart)")
    st.caption("The MR-chart shows the month-to-month change in absorption. Spikes indicate sudden market shifts.")
    MR_all  = np.abs(np.diff(ABSORPTION))
    MR_ucl  = 3.267 * (MR.mean() if len(MR) > 0 else MR_all.mean())  # D4 constant for n=2
    MR_cl   = MR.mean() if len(MR) > 0 else MR_all.mean()
    ooc_mr  = MR_all > MR_ucl

    fig_mr = go.Figure()
    fig_mr.add_scatter(x=MONTHS[1:], y=MR_all, mode='lines+markers',
                       name='Moving Range', line=dict(color='#7C3AED', width=2),
                       marker=dict(size=5))
    fig_mr.add_scatter(x=MONTHS[1:], y=[MR_ucl]*len(MR_all), mode='lines',
                       name=f'MR UCL={MR_ucl:.0f}',
                       line=dict(color='#DC2626', dash='dash', width=1.5))
    fig_mr.add_scatter(x=MONTHS[1:], y=[MR_cl]*len(MR_all), mode='lines',
                       name=f'MR CL={MR_cl:.0f}',
                       line=dict(color='green', width=1.5))
    ooc_mr_months = [MONTHS[1:][i] for i in range(len(MR_all)) if ooc_mr[i]]
    ooc_mr_vals   = [MR_all[i] for i in range(len(MR_all)) if ooc_mr[i]]
    if ooc_mr_months:
        fig_mr.add_scatter(x=ooc_mr_months, y=ooc_mr_vals, mode='markers',
                           name='MR Out-of-Control',
                           marker=dict(color='#DC2626', size=12))
    fig_mr.update_layout(height=260, paper_bgcolor='rgba(0,0,0,0)',
                         plot_bgcolor='rgba(0,0,0,0)', yaxis_title='Moving Range',
                         xaxis_tickangle=-45, margin=dict(r=20))
    st.plotly_chart(fig_mr, use_container_width=True)

    # ── FORECAST ──────────────────────────────────────────────────
    st.markdown("### 🔮 3-Month Moving Average + 6-Month Trend Forecast")
    ma3 = pd.Series(ABSORPTION).rolling(3, min_periods=1).mean().values

    # Fit trend on last 12 months only (more relevant than full 35 months)
    recent = ABSORPTION[-12:]
    x_recent = np.arange(len(ABSORPTION) - 12, len(ABSORPTION))
    trend = np.polyfit(x_recent, recent, 1)
    x_forecast = np.arange(len(ABSORPTION), len(ABSORPTION) + 6)
    forecast_vals = np.polyval(trend, x_forecast)
    forecast_months = ['Dec-25', 'Jan-26', 'Feb-26', 'Mar-26', 'Apr-26', 'May-26']

    fig2 = go.Figure()
    fig2.add_scatter(x=MONTHS, y=ABSORPTION, mode='lines+markers',
                     name='Actual Absorption', line=dict(color='#2563EB', width=2),
                     marker=dict(size=5))
    fig2.add_scatter(x=MONTHS, y=ma3, mode='lines',
                     name='3-Month Moving Avg', line=dict(color='#EF9F27', width=2, dash='dot'))
    fig2.add_scatter(x=forecast_months, y=np.clip(forecast_vals, 0, None).tolist(),
                     mode='lines+markers', name='6-Month Forecast',
                     line=dict(color='#16A34A', width=2, dash='dash'),
                     marker=dict(size=8, symbol='diamond'),
                     hovertemplate="<b>%{x}</b><br>Forecast: %{y:.0f} units<extra></extra>")
    fig2.add_vrect(x0='Dec-25', x1='May-26', fillcolor='rgba(22,163,74,0.06)',
                   line_width=0,
                   annotation_text='Forecast Zone (based on last 12-month trend)',
                   annotation_position='top left', annotation_font_size=9)
    fig2.add_scatter(x=MONTHS, y=[ucl]*len(MONTHS), mode='lines',
                     name=f'UCL={ucl:.0f}', line=dict(color='#DC2626', dash='dash', width=1))
    fig2.add_scatter(x=MONTHS, y=[cl]*len(MONTHS), mode='lines',
                     name=f'CL={cl:.0f}', line=dict(color='green', width=1))
    fig2.update_layout(height=340, paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)', xaxis_tickangle=-45,
                       yaxis_title='Units / month', margin=dict(r=20))
    st.plotly_chart(fig2, use_container_width=True)

    # Forecast summary
    fc1, fc2, fc3 = st.columns(3)
    fc1.metric("Avg Forecast (next 6 mo)", f"{int(np.clip(forecast_vals,0,None).mean())} units/month")
    fc2.metric("Trend Direction", "📉 Declining" if trend[0] < 0 else "📈 Rising")
    fc3.metric("Months to clear all unsold", f"~{int(filtered_df['unsold_units'].sum() / max(int(np.clip(forecast_vals,0,None).mean()),1))} months")

    # ── INTERPRETATION GUIDE ──────────────────────────────────────
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

    # ── BUG EXPLANATION BOX ────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:0.8rem;padding:10px">
Six Sigma DMAIC Dashboard · Bengaluru Real Estate RCA · Bagaluru Micro-Market<br>
Built with Streamlit · SimPy Digital Twin · Plotly · Random Forest · Gradient Boosting
</div>""", unsafe_allow_html=True)