import streamlit as st
import pandas as pd
from datetime import date

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Flight AI System", layout="wide")

# ---------------------------
# BACKGROUND IMAGE + DARK OVERLAY
# ---------------------------
def set_bg():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.85)),
                    url("bg.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Glass card effect */
    .glass {
        background: rgba(255,255,255,0.08);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #ff4b2b, #ff416c);
        color: white;
        border-radius: 10px;
        height: 45px;
        font-size: 16px;
        width: 150px !important;
        white-space: nowrap;
    }

    /* Slider color */
    .stSlider > div > div {
        color: #ff4b2b;
    }

    </style>
    """, unsafe_allow_html=True)

set_bg()

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("flights.csv")

# Convert date
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# ---------------------------
# TITLE
# ---------------------------
st.title("✈️ Flight Recommendation System")
st.subheader("✨ Smart AI-based Flight Finder")

# ---------------------------
# DATE RANGE INFO
# ---------------------------
min_date = df["Date"].min()
max_date = df["Date"].max()

st.info(f"📅 Available Dates: {min_date} → {max_date}")

# ---------------------------
# CLEAR BUTTON
# ---------------------------
col1, col2 = st.columns([8,2])

with col2:
    if st.button("❌ Clear Filters"):
        st.session_state.clear()
        st.rerun()

# ---------------------------
# FILTER UI
# ---------------------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Source
with col1:
    source = st.selectbox(
        "From",
        ["Select"] + sorted(df["Source"].unique().tolist())
    )

# Destination
with col2:
    destination = st.selectbox(
        "To",
        ["Select"] + sorted(df["Destination"].unique().tolist())
    )

# Airline
with col3:
    airline = st.selectbox(
        "Airline",
        ["All"] + sorted(df["Airline"].unique().tolist())
    )

# Date picker
with col4:
    travel_date = st.date_input(
        "Travel Date",
        min_value=min_date,
        max_value=max_date
    )

# Price slider
price_range = st.slider(
    "Select Price Range",
    int(df["Price"].min()),
    int(df["Price"].max()),
    (int(df["Price"].min()), int(df["Price"].max()))
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# SEARCH BUTTON
# ---------------------------
if st.button("🔍 Find Best Flights"):

    filtered_df = df.copy()

    # Apply filters
    if source != "Select":
        filtered_df = filtered_df[filtered_df["Source"] == source]

    if destination != "Select":
        filtered_df = filtered_df[filtered_df["Destination"] == destination]

    if airline != "All":
        filtered_df = filtered_df[filtered_df["Airline"] == airline]

    filtered_df = filtered_df[
        (filtered_df["Price"] >= price_range[0]) &
        (filtered_df["Price"] <= price_range[1])
    ]

    filtered_df = filtered_df[
        filtered_df["Date"] == travel_date
    ]

    # ---------------------------
    # RESULTS
    # ---------------------------
    if not filtered_df.empty:

        st.success("🎉 Flights Found!")

        best_flight = filtered_df.sort_values("Price").iloc[0]

        st.markdown("### 🏆 Best Flight Recommendation")
        st.markdown(f"""
        <div class="glass">
        ✈ Airline: {best_flight['Airline']} <br>
        💰 Price: ₹{best_flight['Price']} <br>
        ⏱ Duration: {best_flight['Duration']} <br>
        📅 Date: {best_flight['Date']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Other Recommended Flights")
        st.dataframe(filtered_df.reset_index(drop=True))

    else:
        st.error("❌ No flights found!")