import streamlit as st
import pandas as pd

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("flights.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# -----------------------------
# Session State Defaults
# -----------------------------
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

# -----------------------------
# Title
# -----------------------------
st.title("✈️ Flight Recommendation System")
st.subheader("✨ Smart AI-based Flight Finder")

# -----------------------------
# Clear Filters Button
# -----------------------------
col1, col2 = st.columns([8, 1])

with col2:
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

# -----------------------------
# Get Available Date Range
# -----------------------------
min_date = df["Date"].min()
max_date = df["Date"].max()

st.caption(f"📅 Available Dates: {min_date} → {max_date}")

# -----------------------------
# Filters UI
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    source = st.selectbox(
        "Source",
        df["Source"].unique(),
        key="source"
    )

with col2:
    destination = st.selectbox(
        "Destination",
        df["Destination"].unique(),
        key="destination"
    )

with col3:
    airline = st.selectbox(
        "Airline",
        ["All"] + list(df["Airline"].unique()),
        key="airline"
    )

with col4:
    travel_date = st.date_input(
        "Travel Date",
        value=st.session_state.travel_date,
        min_value=min_date,
        max_value=max_date,
        key="travel_date"
    )

# -----------------------------
# Price Slider
# -----------------------------
price_range = st.slider(
    "Select Price Range",
    int(df["Price"].min()),
    int(df["Price"].max()),
    key="price_range"
)

# -----------------------------
# Search Button
# -----------------------------
if st.button("🔍 Find Best Flights"):

    filtered_df = df[
        (df["Source"] == source) &
        (df["Destination"] == destination) &
        (df["Price"] >= price_range[0]) &
        (df["Price"] <= price_range[1]) &
        (df["Date"] == travel_date)
    ]

    if airline != "All":
        filtered_df = filtered_df[
            filtered_df["Airline"] == airline
        ]

    # -----------------------------
    # Results
    # -----------------------------
    if filtered_df.empty:
        st.error("❌ No flights found!")
    else:
        st.success("🎉 Flights Found!")

        # Best flight
        best_flight = filtered_df.sort_values(by="Price").iloc[0]

        st.markdown("## 🏆 Best Flight Recommendation")
        st.success(
            f"✈ Airline: {best_flight['Airline']}  \n"
            f"💰 Price: ₹{best_flight['Price']}  \n"
            f"⏱ Duration: {best_flight['Duration']}"
        )

        # Table
        st.markdown("## 📊 Other Recommended Flights")
        st.dataframe(filtered_df.reset_index(drop=True))