import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Flight App", layout="wide")

# -----------------------------
# CSS (PRO UI)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.metric {
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:10px;
    text-align:center;
}
.stButton>button {
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white;
    border-radius:8px;
    padding:8px 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("flights.csv")

# Ensure Date format
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# -----------------------------
# HEADER
# -----------------------------
st.title("Flight Recommendation System")
st.write("Smart AI-based Flight Finder")

# -----------------------------
# ANALYTICS
# -----------------------------
c1, c2, c3 = st.columns(3)

c1.markdown(f"<div class='metric'>Flights<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric'>Avg Price<br><h2>₹{int(df['Price'].mean())}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric'>Airlines<br><h2>{df['Airline'].nunique()}</h2></div>", unsafe_allow_html=True)

st.write("---")

# -----------------------------
# FILTERS (MAKE MY TRIP STYLE)
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

source = col1.selectbox("From", ["Select"] + sorted(df["Source"].unique()))
destination = col2.selectbox("To", ["Select"] + sorted(df["Destination"].unique()))
airline = col3.selectbox("Airline", ["All"] + sorted(df["Airline"].unique()))
sort = col4.selectbox("Sort By", ["Cheapest", "Premium", "Fastest", "Best"])

# 👉 CALENDAR UI (🔥 MAIN FEATURE)
min_date = df["Date"].min()
max_date = df["Date"].max()

travel_date = col5.date_input(
    "Travel Date",
    min_value=min_date,
    max_value=max_date,
    value=min_date
)

# -----------------------------
# PRICE SLIDER
# -----------------------------
price_range = st.slider(
    "Price Range",
    int(df["Price"].min()),
    int(df["Price"].max()),
    (2000, 15000)
)

search = st.button("Search Flights")

# -----------------------------
# OFFER LOGIC
# -----------------------------
def get_offer(row):
    price = row["Price"]
    discount = 200
    tag = "Offer"

    if price > 5000:
        discount = 500
        tag = "Best Deal"

    if "non" in str(row["Stops"]).lower():
        discount += 150
        tag = "Non-stop Special"

    final_price = price - discount
    return discount, final_price, tag

# -----------------------------
# FILTER LOGIC
# -----------------------------
if search:

    data = df.copy()

    if source != "Select":
        data = data[data["Source"] == source]

    if destination != "Select":
        data = data[data["Destination"] == destination]

    if airline != "All":
        data = data[data["Airline"] == airline]

    # DATE FILTER 🔥
    if travel_date:
        data = data[data["Date"] == travel_date]

    # PRICE FILTER
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

    st.success("Flights Found")

    # -----------------------------
    # DISPLAY RESULTS
    # -----------------------------
    for i, row in data.head(15).iterrows():

        discount, final_price, tag = get_offer(row)

        st.subheader(f"{row['Airline']} | {row['Source']} → {row['Destination']}")

        st.write(f"Date: {row['Date']}")
        st.write(f"Duration: {row['Duration']} | {row['Stops']}")
        st.write(f"{tag} | ₹{discount} OFF")

        st.write(f"~~₹{row['Price']}~~ → ₹{final_price}")

        if st.button("Book Now", key=f"book_{i}"):
            st.success(f"Booked {row['Airline']} at ₹{final_price}")

        st.write("---")

else:
    st.info("Select filters and click Search Flights")