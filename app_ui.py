import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ---------------- BACKGROUND ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95));
}

.glass {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

div.stButton > button {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 200px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("flights.csv")
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# ---------------- HELPER ----------------
def convert_duration(duration):
    parts = duration.replace("h", "").replace("m", "").split()
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 1:
        return int(parts[0]) * 60
    return 0

# ---------------- TITLE ----------------
st.title("Flight Recommendation System")
st.subheader("Smart AI-based Flight Finder")

# ---------------- DATE RANGE ----------------
st.info(f"Available Dates: {df['Date'].min()} → {df['Date'].max()}")

# ---------------- CLEAR BUTTON ----------------
col1, col2 = st.columns([8,2])
with col2:
    if st.button("Clear Filters"):
        st.session_state.clear()
        st.rerun()

# ---------------- FILTER CARD ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# SOURCE
with col1:
    source = st.selectbox(
        "From",
        ["Select"] + sorted(df["Source"].unique())
    )

# DESTINATION
with col2:
    destination = st.selectbox(
        "To",
        ["Select"] + sorted(df["Destination"].unique())
    )

# AIRLINE
with col3:
    airline = st.selectbox(
        "Airline",
        ["All"] + sorted(df["Airline"].unique())
    )

# DATE
with col4:
    travel_date = st.selectbox(
        "Travel Date",
        ["Select"] + sorted(df["Date"].astype(str).unique())
    )

# ---------------- EXTRA FILTERS ----------------
col5, col6 = st.columns(2)

# PRICE
with col5:
    price_range = st.slider(
        "Price Range",
        int(df["Price"].min()),
        int(df["Price"].max()),
        (int(df["Price"].min()), int(df["Price"].max()))
    )

# SORT + STOPS
with col6:
    sort_option = st.selectbox(
        "Sort By",
        ["Cheapest", "Fastest"]
    )

    stops = st.selectbox(
        "Stops",
        ["All", "Non-stop", "1 Stop", "2+ Stops"]
    )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CENTER BUTTON ----------------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    search = st.button("Search Flights")

# ---------------- SEARCH LOGIC ----------------
if search:

    data = df.copy()

    if source != "Select":
        data = data[data["Source"] == source]

    if destination != "Select":
        data = data[data["Destination"] == destination]

    if airline != "All":
        data = data[data["Airline"] == airline]

    if travel_date != "Select":
        data = data[data["Date"].astype(str) == travel_date]

    data = data[
        (data["Price"] >= price_range[0]) &
        (data["Price"] <= price_range[1])
    ]

    # ---------------- STOPS FILTER ----------------
    if stops == "Non-stop":
        data = data[data["Stops"] == "non-stop"]
    elif stops == "1 Stop":
        data = data[data["Stops"] == "1 stop"]
    elif stops == "2+ Stops":
        data = data[data["Stops"].isin(["2 stops", "3 stops"])]

    # ---------------- SORTING ----------------
    data["Duration_Min"] = data["Duration"].apply(convert_duration)

    if sort_option == "Cheapest":
        data = data.sort_values("Price")
    else:
        data = data.sort_values("Duration_Min")

    # ---------------- RESULTS ----------------
    if not data.empty:

        st.success("Flights Found")

        best = data.iloc[0]

        st.subheader("Best Flight Recommendation")

        st.markdown(f"""
        <div class='glass'>
        Airline: {best['Airline']} <br>
        Price: ₹{best['Price']} <br>
        Duration: {best['Duration']} <br>
        Stops: {best['Stops']} <br>
        Date: {best['Date']}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Other Flights")
        st.dataframe(data.reset_index(drop=True))

    else:
        st.error("No flights found")