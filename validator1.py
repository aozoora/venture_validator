import å as st
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Venture Validator",
    page_icon="🚀",
    layout="centered"
)

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
    .big-font { font-size:20px !important; }
    .stProgress > div > div > div > div { background-color: #4CAF50; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🚀 Venture Validator")
st.markdown("""
This tool evaluates new business ideas using a 3-part framework:
1.  **Visionary Test:** Is the market growing?
2.  **Analyst Test:** Is the business model structurally sound?
3.  **Unit Economics:** Can you make money on one sale?
""")
st.divider()

# --- INPUT SECTION ---

# 1. VISIONARY TEST
st.header("Step 1: The Visionary Test (Macro)")
st.info("Goal: Determine if the market tide is rising or falling.")

col1, col2 = st.columns(2)
with col1:
    growth_rate = st.number_input(
        "Annual Market Growth Rate (%)",
        min_value=-10.0, max_value=500.0, value=5.0, step=1.0,
        help="How fast is this specific sector growing year-over-year?"
    )

with col2:
    inevitability = st.selectbox(
        "Is this future inevitable?",
        options=[
            "No (Purely consumer preference)",
            "Maybe (Some favorable trends)",
            "Yes (Laws/Physics mandate it)"
        ],
        index=0,
        help="Example of Yes: 'Energy transition'. Example of No: 'A new flavor of soda'."
    )

# 2. ANALYST TEST
st.header("Step 2: The Analyst Test (Micro)")
st.info("Goal: Determine if you have pricing power or are a commodity.")

col3, col4 = st.columns(2)
with col3:
    value_chain_pos = st.selectbox(
        "Value Chain Position",
        options=[
            "Commodity Producer (Price Taker)",
            "Middleman/Distributor (Squeezed)",
            "Aggregator/Platform (Owns Customer)",
            "IP/Bottleneck Owner (Price Maker)"
        ],
        index=0
    )

with col4:
    asset_intensity = st.selectbox(
        "Asset Intensity",
        options=[
            "Heavy (Factories/Inventory)",
            "Medium (Leased Assets)",
            "Light (Software/IP)"
        ],
        index=0
    )

# 3. UNIT ECONOMICS
st.header("Step 3: Unit Economics")
st.info("Goal: Can you make money on ONE transaction?")

col5, col6, col7 = st.columns(3)
with col5:
    price = st.number_input("Avg Price per Unit ($)", value=100.0)
with col6:
    cogs = st.number_input("COGS per Unit ($)", value=60.0, help="Direct cost to make one unit")
with col7:
    cac = st.number_input("CAC ($)", value=20.0, help="Cost to acquire one customer")

# --- CALCULATIONS ---

# Step 1 Score
visionary_score = 0
if growth_rate > 20: visionary_score += 50
elif growth_rate > 5: visionary_score += 20
else: visionary_score -= 10

if "Yes" in inevitability: visionary_score += 50
elif "Maybe" in inevitability: visionary_score += 10

# Step 2 Score
analyst_score = 0
if "Commodity" in value_chain_pos: analyst_score += 0
elif "Middleman" in value_chain_pos: analyst_score += 20
elif "Aggregator" in value_chain_pos: analyst_score += 80
elif "IP" in value_chain_pos: analyst_score += 100

if "Heavy" in asset_intensity: analyst_score += 10
elif "Medium" in asset_intensity: analyst_score += 40
elif "Light" in asset_intensity: analyst_score += 60

# Normalize Step 2 to 100
analyst_score = min(100, (analyst_score / 160) * 100)

# Step 3 Score
contribution_margin = price - cogs
net_unit_profit = contribution_margin - cac
unit_score = 0

if contribution_margin <= 0: unit_score = 0
elif net_unit_profit < 0: unit_score = 40
else: unit_score = 100

# Final Weighted Score
final_score = (visionary_score * 0.3) + (analyst_score * 0.3) + (unit_score * 0.4)
final_score = max(0, min(100, final_score)) # Clamp between 0-100

# --- RESULTS DISPLAY ---
st.divider()
st.header("📊 The Verdict")

# Create a colorful gauge using columns
c1, c2, c3 = st.columns(3)
c1.metric("Visionary Score", f"{visionary_score}/100")
c2.metric("Analyst Score", f"{int(analyst_score)}/100")
c3.metric("Unit Score", f"{unit_score}/100")

st.subheader(f"Final Venture Score: {int(final_score)} / 100")
st.progress(int(final_score) / 100)

if final_score >= 80:
    st.success("## 🦄 VERDICT: UNICORN POTENTIAL\nHigh growth, strong structure, and profitable unit economics.")
elif final_score >= 50:
    st.warning("## ⚠️ VERDICT: CAUTION\nGood potential, but significant risks exist. Check the 'Unit Economics' or 'Analyst' inputs.")
else:
    st.error("## 🛑 VERDICT: NO GO\nStructural headwinds are too strong. Pivot required.")

# Detailed Breakdown Expander
with st.expander("See Calculation Details"):
    st.write(f"**Contribution Margin:** ${contribution_margin:.2f}")
    st.write(f"**Net Profit on First Unit:** ${net_unit_profit:.2f}")
    st.write(f"**Visionary Weight:** 30% | **Analyst Weight:** 30% | **Economics Weight:** 40%")
