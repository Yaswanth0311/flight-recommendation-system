import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Container */
.container {
    background: rgba(255,255,255,0.06);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    margin-top: 10px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 200px;
    font-size: 16px;
}

/* Reduce top space */
.block-container {
    padding-top: 2rem;
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
st.caption("Smart AI-based Flight Finder")

# ---------------- INFO ----------------
st.info(f"Available Dates: {df['Date'].min()} → {df['Date'].max()}")

# ---------------- FILTER HEADER ----------------
col1, col2 = st.columns([8,2])

with col1:
    st.markdown("### Filters")

with col2:
    clear = st.button("Clear Filters")

if clear:
    st.session_state.clear()
    st.rerun()

# ---------------- FILTER CARD ----------------
st.markdown("<div class='container'>", unsafe_allow_html=True)

# ROW 1
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

# ROW 2
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

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SEARCH BUTTON ----------------
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

    # ---------------- SORT ----------------
    data["Duration_Min"] = data["Duration"].apply(convert_duration)

    if sort_option == "Cheapest":
        data = data.sort_values("Price")

    elif sort_option == "Fastest":
        data = data.sort_values("Duration_Min")

    elif sort_option == "Best Value":
        data["Score"] = data["Price"] * 0.7 + data["Duration_Min"] * 0.3
        data = data.sort_values("Score")

    elif sort_option == "Premium":
        premium_airlines = ["IndiGo", "Air India", "Vistara"]
        data["Premium"] = data["Airline"].apply(
            lambda x: 0 if x in premium_airlines else 1
        )
        data = data.sort_values(["Premium", "Price"])

    # ---------------- RESULT ----------------
    if not data.empty:

        st.success("Flights Found")

        best = data.iloc[0]

        st.subheader("Best Flight")

        st.markdown(f"""
        <div class='container'>
        Airline: {best['Airline']} <br>
        Route: {best['Source']} → {best['Destination']} <br>
        Price: ₹{best['Price']} <br>
        Duration: {best['Duration']} <br>
        Stops: {best['Stops']}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("All Flights")
        st.dataframe(data.reset_index(drop=True))

    else:
        st.error("No flights found")