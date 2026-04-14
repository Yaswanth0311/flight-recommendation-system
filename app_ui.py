import streamlit as st
import pandas as pd
import base64

# ==============================
# BACKGROUND IMAGE
# ==============================
def set_bg():
    with open("bg.jpg", "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.75);
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg()

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("flights.csv")

df["Date"] = pd.to_datetime(df["Date"]).dt.date

min_date = df["Date"].min()
max_date = df["Date"].max()

# ==============================
# TITLE
# ==============================
st.markdown("<h1 style='color:white;'>✈️ Flight Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:lightgray;'>✨ Smart AI-based Flight Finder</h4>", unsafe_allow_html=True)

# ==============================
# CLEAR BUTTON
# ==============================
col1, col2 = st.columns([9,1])

with col2:
    if st.button("❌ Clear"):
        st.experimental_rerun()

# ==============================
# AVAILABLE DATE INFO
# ==============================
st.info(f"📅 Available Dates: {min_date} → {max_date}")

# ==============================
# SEARCH BAR
# ==============================
col1, col2, col3, col4 = st.columns(4)

with col1:
    source = st.selectbox("From", sorted(df["Source"].unique()))

with col2:
    destination = st.selectbox("To", sorted(df["Destination"].unique()))

with col3:
    airline = st.selectbox("Airline", ["All"] + sorted(df["Airline"].unique()))

with col4:
    travel_date = st.date_input("Date", min_value=min_date, max_value=max_date)

# ==============================
# PRICE SLIDER
# ==============================
price_range = st.slider(
    "Select Price Range",
    int(df["Price"].min()),
    int(df["Price"].max()),
    (int(df["Price"].min()), int(df["Price"].max()))
)

# ==============================
# BUTTON STYLE
# ==============================
st.markdown("""
<style>
div.stButton > button {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

search = st.button("🔍 Find Best Flights")

# ==============================
# CARD UI FUNCTION
# ==============================
def flight_card(airline, price, duration):
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        color:white;
    ">
        ✈️ <b>{airline}</b><br>
        💰 ₹{price} &nbsp;&nbsp; ⏱ {duration}
    </div>
    """, unsafe_allow_html=True)

# ==============================
# FILTER LOGIC
# ==============================
if search:

    filtered = df[
        (df["Source"] == source) &
        (df["Destination"] == destination) &
        (df["Price"] >= price_range[0]) &
        (df["Price"] <= price_range[1]) &
        (df["Date"] == travel_date)
    ]

    if airline != "All":
        filtered = filtered[filtered["Airline"] == airline]

    if filtered.empty:
        st.error("❌ No flights found!")
    else:
        st.success("🎉 Flights Found!")

        best = filtered.sort_values(by="Price").iloc[0]

        st.subheader("🏆 Best Flight Recommendation")
        flight_card(best["Airline"], best["Price"], best["Duration"])

        st.subheader("📊 Other Recommended Flights")

        for i, row in filtered.head(5).iterrows():
            flight_card(row["Airline"], row["Price"], row["Duration"])