import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.07);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
    border-radius: 8px;
    height: 40px;
    width: 180px;
}

/* Center button */
.center-btn {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
df = pd.read_csv("flights.csv")
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# ---------------- TITLE ----------------
st.title("Flight Recommendation System")
st.caption("Smart AI-based Flight Finder")

st.info(f"Available Dates: {df['Date'].min()} → {df['Date'].max()}")

# ---------------- FILTERS ----------------
col1, col2 = st.columns([8,2])

with col1:
    st.subheader("Filters")

with col2:
    if st.button("Clear Filters"):
        st.session_state.clear()
        st.rerun()

# FILTER GRID (NO EMPTY BAR NOW)
col1, col2, col3, col4 = st.columns(4)

with col1:
    source = st.selectbox("From", ["Select"] + sorted(df["Source"].unique()))

with col2:
    destination = st.selectbox("To", ["Select"] + sorted(df["Destination"].unique()))

with col3:
    airline = st.selectbox("Airline", ["All"] + sorted(df["Airline"].unique()))

with col4:
    travel_date = st.selectbox(
        "Date",
        ["Select"] + sorted(df["Date"].astype(str).unique())
    )

col5, col6, col7 = st.columns(3)

with col5:
    price_range = st.slider(
        "Price Range",
        int(df["Price"].min()),
        int(df["Price"].max()),
        (int(df["Price"].min()), int(df["Price"].max()))
    )

with col6:
    sort_option = st.selectbox(
        "Sort By",
        ["Cheapest", "Fastest", "Best Value", "Premium"]
    )

with col7:
    stops = st.selectbox(
        "Stops",
        ["All", "Non-stop", "1 Stop", "2+ Stops"]
    )

# SEARCH BUTTON CENTER
col1, col2, col3 = st.columns([1,2,1])
with col2:
    search = st.button("Search Flights")

# ---------------- LOGO MAPPING ----------------
logos = {
    "IndiGo": "https://upload.wikimedia.org/wikipedia/commons/0/0b/IndiGo_Logo.svg",
    "Air India": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Air_India_Logo.svg",
    "SpiceJet": "https://upload.wikimedia.org/wikipedia/commons/9/9b/SpiceJet_logo.svg",
    "GoAir": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Go_First_logo.svg"
}

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

    # Stops filter
    if stops == "Non-stop":
        data = data[data["Stops"] == "non-stop"]
    elif stops == "1 Stop":
        data = data[data["Stops"] == "1 stop"]
    elif stops == "2+ Stops":
        data = data[data["Stops"].isin(["2 stops", "3 stops"])]

    # Sorting
    data["Duration_Min"] = data["Duration"].str.extract(r'(\d+)').astype(int)

    if sort_option == "Cheapest":
        data = data.sort_values("Price")

    elif sort_option == "Fastest":
        data = data.sort_values("Duration_Min")

    elif sort_option == "Best Value":
        data["Score"] = data["Price"] * 0.7 + data["Duration_Min"] * 0.3
        data = data.sort_values("Score")

    elif sort_option == "Premium":
        premium = ["IndiGo", "Air India"]
        data["Premium"] = data["Airline"].apply(lambda x: 0 if x in premium else 1)
        data = data.sort_values(["Premium", "Price"])

    # ---------------- RESULTS ----------------
    if not data.empty:

        st.success("Flights Found")

        for i, row in data.head(10).iterrows():

            logo_url = logos.get(row["Airline"], "")

            st.markdown(f"""
            <div class='card'>
                <div style="display:flex; justify-content:space-between; align-items:center;">

                    <div>
                        <img src="{logo_url}" width="80"><br>
                        <b>{row['Airline']}</b><br>
                        {row['Source']} → {row['Destination']}<br>
                        {row['Duration']} | {row['Stops']}
                    </div>

                    <div style="text-align:right;">
                        <h3>₹{row['Price']}</h3>
                        <button style="background:#ff4b2b;color:white;border:none;padding:8px 15px;border-radius:6px;">
                            Book Now
                        </button>
                    </div>

                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.error("No flights found")