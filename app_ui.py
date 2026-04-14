import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Flight App", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("flights.csv")
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# -----------------------------
# SESSION STATE
# -----------------------------
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []

# -----------------------------
# HEADER
# -----------------------------
st.title("Flight Recommendation System")
st.write("Smart AI-based Flight Finder")

# -----------------------------
# ANALYTICS
# -----------------------------
c1, c2, c3 = st.columns(3)

c1.metric("Flights", len(df))
c2.metric("Avg Price", f"₹{int(df['Price'].mean())}")
c3.metric("Airlines", df["Airline"].nunique())

st.write("---")

# -----------------------------
# FILTERS
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

sources = ["Select"] + sorted(df["Source"].unique())
destinations = ["Select"] + sorted(df["Destination"].unique())

# Initialize session values
if "source" not in st.session_state:
    st.session_state.source = "Select"
if "destination" not in st.session_state:
    st.session_state.destination = "Select"

# -----------------------------
# SWAP BUTTON
# -----------------------------
def swap():
    st.session_state.source, st.session_state.destination = (
        st.session_state.destination,
        st.session_state.source,
    )

# -----------------------------
# INPUTS
# -----------------------------
source = col1.selectbox("From", sources, key="source")
destination = col2.selectbox("To", destinations, key="destination")

col2.button("🔁", on_click=swap)

airline = col3.selectbox("Airline", ["Select"] + sorted(df["Airline"].unique()))
sort = col4.selectbox("Sort By", ["Select", "Cheapest", "Premium", "Fastest", "Best"])

# DATE SELECT
date_list = ["Select"] + sorted(df["Date"].astype(str).unique())
selected_date = col5.selectbox("Travel Date", date_list)

# -----------------------------
# PRICE RANGE
# -----------------------------
price_range = st.slider(
    "Price Range",
    int(df["Price"].min()),
    int(df["Price"].max()),
    (2000, 15000)
)

# -----------------------------
# DISABLE SEARCH BUTTON
# -----------------------------
is_valid = source != "Select" and destination != "Select"

search = st.button("Search Flights", disabled=not is_valid)

if not is_valid:
    st.warning("Please select From and To locations")

# -----------------------------
# FILTER LOGIC
# -----------------------------
if search:

    data = df.copy()

    if source != "Select":
        data = data[data["Source"] == source]

    if destination != "Select":
        data = data[data["Destination"] == destination]

    if airline != "Select":
        data = data[data["Airline"] == airline]

    if selected_date != "Select":
        data = data[data["Date"].astype(str) == selected_date]

    data = data[
        (data["Price"] >= price_range[0]) &
        (data["Price"] <= price_range[1])
    ]

    # SORTING
    if sort == "Cheapest":
        data = data.sort_values("Price")
    elif sort == "Premium":
        data = data.sort_values("Price", ascending=False)
    elif sort == "Fastest":
        data = data.sort_values("Duration")
    elif sort == "Best":
        data = data.sort_values(["Price", "Duration"])

    # SAVE RECENT SEARCH
    st.session_state.recent_searches.insert(0, f"{source} → {destination}")
    st.session_state.recent_searches = st.session_state.recent_searches[:5]

    st.success("Flights Found")

    for i, row in data.head(10).iterrows():
        st.subheader(f"{row['Airline']} | {row['Source']} → {row['Destination']}")
        st.write(f"{row['Duration']} | {row['Stops']}")
        st.write(f"₹{row['Price']}")

        if st.button("Book Now", key=i):
            st.success("Flight booked!")

        st.write("---")

# -----------------------------
# RECENT SEARCHES
# -----------------------------
if st.session_state.recent_searches:
    st.write("### 🕘 Recent Searches")

    for item in st.session_state.recent_searches:
        st.write(f"• {item}")