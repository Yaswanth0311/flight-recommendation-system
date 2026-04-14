import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Flight App", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("flights.csv")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -----------------------------
# SESSION STATE
# -----------------------------
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []

# -----------------------------
# CLEAR FILTERS
# -----------------------------
def clear_filters():
    st.session_state.source = "Select All"
    st.session_state.destination = "Select All"
    st.session_state.airline = "Select All"
    st.session_state.sort = "Select"
    st.session_state.date = "Select All"

# -----------------------------
# HEADER
# -----------------------------
st.title("Flight Recommendation System")
st.caption("Smart AI-based Flight Finder")

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs(["✈ Flights", "🏨 Hotels", "🚆 Trains"])

# =============================
# FLIGHTS TAB
# =============================
with tab1:

    # Dropdown values
    sources = ["Select All"] + sorted(df["Source"].dropna().unique())
    destinations = ["Select All"] + sorted(df["Destination"].dropna().unique())
    airlines = ["Select All"] + sorted(df["Airline"].dropna().unique())
    dates = ["Select All"] + sorted(df["Date"].dropna().astype(str).unique())

    # Layout
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    source = col1.selectbox("From", sources, key="source")
    destination = col2.selectbox("To", destinations, key="destination")
    airline = col3.selectbox("Airline", airlines, key="airline")
    sort = col4.selectbox("Sort By", ["Select", "Cheapest", "Premium"], key="sort")
    selected_date = col5.selectbox("Travel Date", dates, key="date")

    col6.button("❌ Clear", on_click=clear_filters)

    # -----------------------------
    # PRICE SLIDER
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
    valid = source != "Select All" and destination != "Select All"
    search = st.button("🔍 Search Flights", disabled=not valid)

    if not valid:
        st.warning("Please select From & To locations")

    # -----------------------------
    # SEARCH LOGIC
    # -----------------------------
    if search:

        data = df.copy()

        if source != "Select All":
            data = data[data["Source"] == source]

        if destination != "Select All":
            data = data[data["Destination"] == destination]

        if airline != "Select All":
            data = data[data["Airline"] == airline]

        if selected_date != "Select All":
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

        # Save recent
        st.session_state.recent_searches.insert(0, f"{source} → {destination}")
        st.session_state.recent_searches = st.session_state.recent_searches[:5]

        # -----------------------------
        # RESULT CARDS (FIXED)
        # -----------------------------
        for i, row in data.head(10).iterrows():

            discount = random.randint(200, 800)
            final_price = int(row["Price"]) - discount

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

                    <span style="
                        background:#ff4b2b;
                        padding:4px 10px;
                        border-radius:6px;
                        font-size:12px;
                    ">
                        OFFER
                    </span>

                    <p style="color:#00ff9d;margin:5px 0;">
                        ₹{discount} OFF
                    </p>
                </div>

                <div style="text-align:right;">
                    <p style="text-decoration:line-through;margin:0;">
                        ₹{int(row['Price'])}
                    </p>
                    <h2 style="margin:0;">
                        ₹{final_price}
                    </h2>
                </div>
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
# OTHER TABS
# -----------------------------
with tab2:
    st.info("Hotels coming soon")

with tab3:
    st.info("Trains coming soon")