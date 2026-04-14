import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Flight App", layout="wide")

# -----------------------------
# CSS (Professional UI)
# -----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    backdrop-filter: blur(10px);
}

.metric {
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:12px;
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

# Safe defaults if missing
if "Stops" not in df.columns:
    df["Stops"] = "non-stop"

# -----------------------------
# OFFER LOGIC
# -----------------------------
def get_offer(row):
    price = row["Price"]
    stops = str(row["Stops"]).lower()
    airline = row["Airline"]

    discount = 0
    tag = ""

    if price > 6000:
        discount = 800
        tag = "Super Saver"
    elif price > 4000:
        discount = 500
        tag = "Best Deal"
    else:
        discount = 200
        tag = "Budget"

    if "non" in stops:
        discount += 150
        tag = "Non-stop Special"

    if airline == "IndiGo":
        discount += 100
        tag = "IndiGo Offer"

    final_price = max(price - discount, int(price * 0.5))
    return discount, final_price, tag

# -----------------------------
# HEADER
# -----------------------------
st.title("Flight Recommendation System")
st.write("Smart AI-based Flight Finder")

# -----------------------------
# ANALYTICS (TOP CARDS)
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='metric'>Total Flights<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric'>Avg Price<br><h2>₹{int(df['Price'].mean())}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric'>Airlines<br><h2>{df['Airline'].nunique()}</h2></div>", unsafe_allow_html=True)

st.write("---")

# -----------------------------
# FILTERS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

source = col1.selectbox("From", ["Select"] + sorted(df["Source"].unique()))
destination = col2.selectbox("To", ["Select"] + sorted(df["Destination"].unique()))
airline = col3.selectbox("Airline", ["All"] + sorted(df["Airline"].unique()))
sort = col4.selectbox("Sort By", ["Cheapest", "Fastest", "Best Value", "Premium"])

price_range = st.slider("Price Range", int(df["Price"].min()), int(df["Price"].max()), (2000, 15000))

st.write("")

search = st.button("Search Flights")

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

    data = data[(data["Price"] >= price_range[0]) & (data["Price"] <= price_range[1])]

    # Sorting
    if sort == "Cheapest":
        data = data.sort_values("Price")
    elif sort == "Fastest":
        data = data.sort_values("Duration")
    elif sort == "Premium":
        data = data.sort_values("Price", ascending=False)

    st.success("Flights Found")

    # -----------------------------
    # RESULTS (CARDS)
    # -----------------------------
    for i, row in data.head(20).iterrows():

        discount, final_price, tag = get_offer(row)

        st.markdown(f"""
        <div class='card'>
            <div style="display:flex; justify-content:space-between;">

                <div>
                    <b>{row['Airline']}</b><br>
                    {row['Source']} → {row['Destination']}<br>
                    {row['Duration']} | {row['Stops']}<br><br>

                    <span style="background:#ff4b2b;padding:4px 10px;border-radius:6px;font-size:12px;">
                        {tag}
                    </span><br><br>

                    <span style="color:#00ff9d;">
                        ₹{discount} OFF
                    </span>
                </div>

                <div style="text-align:right;">
                    <p style="text-decoration:line-through;">
                        ₹{row['Price']}
                    </p>
                    <h2>₹{final_price}</h2>
                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Book Now", key=f"book_{i}"):
            st.success(f"{row['Airline']} booked at ₹{final_price} ✈️")

else:
    st.info("Select filters and click Search Flights")