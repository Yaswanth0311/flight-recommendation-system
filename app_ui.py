import streamlit as st
import pandas as pd

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Flight Recommendation System", layout="wide")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    return pd.read_csv("flights.csv")

data = load_data()

# -------------------- TITLE --------------------
st.markdown("## ✈️ Flight Recommendation System")
st.caption("Smart AI-based Flight Finder")

# -------------------- FILTER UI --------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    source = st.selectbox("From", ["Select All"] + sorted(data["Source"].unique()))

with col2:
    destination = st.selectbox("To", ["Select All"] + sorted(data["Destination"].unique()))

with col3:
    airline = st.selectbox("Airline", ["Select All"] + sorted(data["Airline"].unique()))

with col4:
    sort_by = st.selectbox("Sort By", ["Select", "Cheapest", "Premium"])

with col5:
    travel_date = st.date_input("Travel Date")

with col6:
    clear = st.button("❌ Clear")

# -------------------- CLEAR FILTER --------------------
if clear:
    st.experimental_rerun()

# -------------------- PRICE SLIDER --------------------
price_min, price_max = int(data["Price"].min()), int(data["Price"].max())

price = st.slider(
    "Price Range",
    price_min,
    price_max,
    (price_min, price_max)
)

# -------------------- SEARCH BUTTON --------------------
search_clicked = st.button("🔍 Search Flights")

# -------------------- FILTER LOGIC --------------------
filtered_data = data.copy()

if source != "Select All":
    filtered_data = filtered_data[filtered_data["Source"] == source]

if destination != "Select All":
    filtered_data = filtered_data[filtered_data["Destination"] == destination]

if airline != "Select All":
    filtered_data = filtered_data[filtered_data["Airline"] == airline]

filtered_data = filtered_data[
    (filtered_data["Price"] >= price[0]) &
    (filtered_data["Price"] <= price[1])
]

# -------------------- SORT --------------------
if sort_by == "Cheapest":
    filtered_data = filtered_data.sort_values(by="Price")

elif sort_by == "Premium":
    filtered_data = filtered_data.sort_values(by="Price", ascending=False)

# -------------------- VALIDATION --------------------
if source == "Select All" or destination == "Select All":
    st.warning("⚠️ Please select From & To locations")

# -------------------- RESULTS --------------------
if search_clicked:

    if filtered_data.empty:
        st.error("❌ No flights found")

    else:
        st.success("✅ Flights Found")

        for i, row in filtered_data.head(10).iterrows():

            duration = row["Duration"] if "Duration" in data.columns else "N/A"
            stops = row["Stops"] if "Stops" in data.columns else row.get("Total_Stops", "N/A")

            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.05);
                padding:20px;
                border-radius:12px;
                margin-bottom:12px;
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">

                <div>
                    <h4 style="margin:0;">{row['Airline']}</h4>
                    <p style="margin:0;">{row['Source']} → {row['Destination']}</p>
                    <p style="margin:0;">{duration} | {stops}</p>
                </div>

                <div style="text-align:right;">
                    <h2 style="margin:0;">₹{int(row['Price'])}</h2>
                </div>

            </div>
            """, unsafe_allow_html=True)