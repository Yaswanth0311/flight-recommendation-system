import streamlit as st
import pandas as pd

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
# CSS (MAKE MY TRIP STYLE)
# -----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main-card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:15px;
    backdrop-filter: blur(10px);
}

.stButton>button {
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white;
    border-radius:10px;
    padding:10px 24px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("Flight Recommendation System")
st.write("Smart AI-based Flight Finder")

# -----------------------------
# NAVIGATION TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs(["✈ Flights", "🏨 Hotels", "🚆 Trains"])

with tab1:

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    # -----------------------------
    # FILTERS
    # -----------------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    sources = ["Select"] + sorted(df["Source"].unique())
    destinations = ["Select"] + sorted(df["Destination"].unique())

    if "source" not in st.session_state:
        st.session_state.source = "Select"
    if "destination" not in st.session_state:
        st.session_state.destination = "Select"

    def swap():
        st.session_state.source, st.session_state.destination = (
            st.session_state.destination,
            st.session_state.source,
        )

    source = col1.selectbox("From", sources, key="source")
    destination = col2.selectbox("To", destinations, key="destination")

    st.markdown("<br>", unsafe_allow_html=True)
    col2.button("🔁 Swap", on_click=swap)

    airline = col3.selectbox("Airline", ["Select"] + sorted(df["Airline"].unique()))
    sort = col4.selectbox("Sort By", ["Select", "Cheapest", "Premium", "Fastest", "Best"])

    date_list = ["Select"] + sorted(df["Date"].astype(str).unique())
    selected_date = col5.selectbox("Travel Date", date_list)

    # -----------------------------
    # PRICE
    # -----------------------------
    price_range = st.slider(
        "Price Range",
        int(df["Price"].min()),
        int(df["Price"].max()),
        (2000, 15000)
    )

    # -----------------------------
    # SEARCH BUTTON
    # -----------------------------
    is_valid = source != "Select" and destination != "Select"

    search = st.button("🔍 Search Flights", disabled=not is_valid)

    if not is_valid:
        st.warning("Select From & To")

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # RESULTS
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

        if sort == "Cheapest":
            data = data.sort_values("Price")
        elif sort == "Premium":
            data = data.sort_values("Price", ascending=False)

        st.success("Flights Found")

        # SAVE RECENT
        st.session_state.recent_searches.insert(0, f"{source} → {destination}")
        st.session_state.recent_searches = st.session_state.recent_searches[:5]

        for i, row in data.head(8).iterrows():

            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.05);
                padding:20px;
                border-radius:12px;
                margin-bottom:10px;
            ">
                <b>{row['Airline']}</b><br>
                {row['Source']} → {row['Destination']}<br>
                {row['Duration']} | {row['Stops']}<br>
                <h3>₹{row['Price']}</h3>
            </div>
            """, unsafe_allow_html=True)

    # -----------------------------
    # RECENT SEARCHES
    # -----------------------------
    if st.session_state.recent_searches:
        st.write("### 🕘 Recent Searches")

        cols = st.columns(len(st.session_state.recent_searches))

        for i, item in enumerate(st.session_state.recent_searches):
            cols[i].markdown(f"""
            <div style="
                background: rgba(255,255,255,0.05);
                padding:10px;
                border-radius:8px;
                text-align:center;
            ">
                {item}
            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# OTHER TABS (PLACEHOLDER)
# -----------------------------
with tab2:
    st.info("Hotel booking coming soon")

with tab3:
    st.info("Train booking coming soon")