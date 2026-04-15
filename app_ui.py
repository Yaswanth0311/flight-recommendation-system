import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Flight Booking App", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("flights.csv")

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -----------------------------
# SESSION STATE
# -----------------------------
if "recent" not in st.session_state:
    st.session_state.recent = []

if "booking" not in st.session_state:
    st.session_state.booking = None

# -----------------------------
# CLEAR FILTERS
# -----------------------------
def clear_filters():
    st.session_state.source = "Select All"
    st.session_state.destination = "Select All"
    st.session_state.airline = "Select All"

# -----------------------------
# AIRLINE LOGOS
# -----------------------------
logos = {
    "IndiGo": "https://1000logos.net/wp-content/uploads/2020/03/IndiGo-logo.png",
    "Air India": "https://1000logos.net/wp-content/uploads/2020/03/Air-India-logo.png",
    "SpiceJet": "https://1000logos.net/wp-content/uploads/2020/03/SpiceJet-logo.png",
    "Vistara": "https://1000logos.net/wp-content/uploads/2021/04/Vistara-logo.png",
    "GoAir": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Go_First_logo.svg"
}

# -----------------------------
# HEADER
# -----------------------------
st.title("✈ Flight Booking App")
st.caption("Production Level AI Flight Finder")

# -----------------------------
# DASHBOARD
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Flights", len(df))
col2.metric("Avg Price", f"₹{int(df['Price'].mean())}")
col3.metric("Airlines", df["Airline"].nunique())

st.divider()

# -----------------------------
# FILTERS
# -----------------------------
sources = ["Select All"] + sorted(df["Source"].unique())
destinations = ["Select All"] + sorted(df["Destination"].unique())
airlines = ["Select All"] + sorted(df["Airline"].unique())

c1, c2, c3, c4 = st.columns(4)

source = c1.selectbox("From", sources, key="source")
destination = c2.selectbox("To", destinations, key="destination")
airline = c3.selectbox("Airline", airlines, key="airline")

if c4.button("🔄 Swap"):
    st.session_state.source, st.session_state.destination = destination, source

st.button("❌ Clear Filters", on_click=clear_filters)

# -----------------------------
# PRICE FILTER
# -----------------------------
price_range = st.slider(
    "Price Range",
    int(df["Price"].min()),
    int(df["Price"].max()),
    (2000, 15000)
)

# -----------------------------
# SEARCH
# -----------------------------
valid = source != "Select All" and destination != "Select All"

search = st.button("🔍 Search Flights", disabled=not valid)

# -----------------------------
# RESULTS
# -----------------------------
if search:

    data = df.copy()

    if source != "Select All":
        data = data[data["Source"] == source]

    if destination != "Select All":
        data = data[data["Destination"] == destination]

    if airline != "Select All":
        data = data[data["Airline"] == airline]

    data = data[
        (data["Price"] >= price_range[0]) &
        (data["Price"] <= price_range[1])
    ]

    st.success("Flights Found")

    st.session_state.recent.insert(0, f"{source} → {destination}")
    st.session_state.recent = st.session_state.recent[:5]

    for i, row in data.head(10).iterrows():

        duration = row.get("Duration", "N/A")
        stops = row.get("Stops", row.get("Total_Stops", "N/A"))

        logo = logos.get(row["Airline"], "")

        col_left, col_mid, col_right = st.columns([1, 4, 2])

        # Logo
        with col_left:
            if logo:
                st.image(logo, width=60)

        # Details
        with col_mid:
            st.markdown(f"### {row['Airline']}")
            st.write(f"{row['Source']} → {row['Destination']}")
            st.caption(f"{duration} | {stops}")

        # Price + Booking
        with col_right:
            st.markdown(
                f"<h3 style='text-align:right;'>₹{int(row['Price'])}</h3>",
                unsafe_allow_html=True
            )

            if st.button(f"Book Now {i}"):
                st.session_state.booking = row

        st.divider()

# -----------------------------
# BOOKING FLOW
# -----------------------------
if st.session_state.booking is not None:

    st.subheader("💳 Booking Summary")

    flight = st.session_state.booking

    st.write(f"**Airline:** {flight['Airline']}")
    st.write(f"**Route:** {flight['Source']} → {flight['Destination']}")
    st.write(f"**Price:** ₹{int(flight['Price'])}")

    if st.button("💰 Pay Now"):
        st.success("✅ Payment Successful! Ticket Booked 🎉")
        st.session_state.booking = None

# -----------------------------
# RECENT SEARCHES
# -----------------------------
if st.session_state.recent:
    st.subheader("🕘 Recent Searches")

    cols = st.columns(len(st.session_state.recent))

    for i, item in enumerate(st.session_state.recent):
        cols[i].info(item)