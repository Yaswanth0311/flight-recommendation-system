import streamlit as st
import pandas as pd
from datetime import date

# -------------------------------
# Load Data
# -------------------------------
df = pd.read_csv("flights.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# -------------------------------
# Session State Defaults
# -------------------------------
if "source" not in st.session_state:
    st.session_state.source = df["Source"].iloc[0]

if "destination" not in st.session_state:
    st.session_state.destination = df["Destination"].iloc[0]

if "airline" not in st.session_state:
    st.session_state.airline = "All"

if "price_range" not in st.session_state:
    st.session_state.price_range = (
        int(df["Price"].min()),
        int(df["Price"].max())
    )

if "travel_date" not in st.session_state:
    st.session_state.travel_date = df["Date"].iloc[0]

# -------------------------------
# TITLE
# -------------------------------
st.title("✈️ Flight Recommendation System")
st.subheader("✨ Smart AI-based Flight Finder")

# -------------------------------
# Clear Filters Button
# -------------------------------
col_title, col_btn = st.columns([4, 1])

with col_btn:
    if st.button("❌ Clear"):
        st.session_state.source = df["Source"].iloc[0]
        st.session_state.destination = df["Destination"].iloc[0]
        st.session_state.airline = "All"
        st.session_state.price_range = (
            int(df["Price"].min()),
            int(df["Price"].max())
        )
        st.session_state.travel_date = df["Date"].iloc[0]
        st.rerun()

# -------------------------------
# FILTERS UI
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    source = st.selectbox(
        "Source",
        sorted(df["Source"].unique()),
        key="source"
    )

with col2:
    destination = st.selectbox(
        "Destination",
        sorted(df["Destination"].unique()),
        key="destination"
    )

with col3:
    airline = st.selectbox(
        "Airline",
        ["All"] + sorted(df["Airline"].unique()),
        key="airline"
    )

with col4:
    travel_date = st.date_input(
        "Travel Date",
        key="travel_date"
    )

# Price Slider
price_range = st.slider(
    "Select Price Range",
    int(df["Price"].min()),
    int(df["Price"].max()),
    key="price_range"
)

# -------------------------------
# BUTTON
# -------------------------------
if st.button("🔍 Find Best Flights"):

    # ---------------------------
    # Filtering Logic
    # ---------------------------
    filtered_df = df[
        (df["Source"] == source) &
        (df["Destination"] == destination) &
        (df["Date"] == travel_date)
    ]

    if airline != "All":
        filtered_df = filtered_df[
            filtered_df["Airline"] == airline
        ]

    filtered_df = filtered_df[
        (filtered_df["Price"] >= price_range[0]) &
        (filtered_df["Price"] <= price_range[1])
    ]

    # ---------------------------
    # Results
    # ---------------------------
    if filtered_df.empty:
        st.warning("⚠️ No flights found for selected filters")
    else:
        st.success(f"✅ Found {len(filtered_df)} flights")

        # Best Flight (Cheapest)
        best_flight = filtered_df.sort_values(by="Price").iloc[0]

        st.subheader("🏆 Best Flight Recommendation")
        st.info(
            f"✈️ Airline: {best_flight['Airline']}  \n"
            f"💰 Price: ₹{best_flight['Price']}  \n"
            f"⏱ Duration: {best_flight['Duration']}  \n"
            f"📅 Date: {best_flight['Date']}"
        )

        # Show Top 10 Flights
        st.subheader("📊 Top Available Flights")
        st.dataframe(
            filtered_df.sort_values(by="Price").head(10).reset_index(drop=True)
        )