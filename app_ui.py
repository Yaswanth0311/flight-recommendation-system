import streamlit as st
import pandas as pd
import random

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

if "source" not in st.session_state:
    st.session_state.source = "Select All"

if "destination" not in st.session_state:
    st.session_state.destination = "Select All"

if "airline" not in st.session_state:
    st.session_state.airline = "Select All"

if "sort" not in st.session_state:
    st.session_state.sort = "Select"

if "date" not in st.session_state:
    st.session_state.date = "Select All"

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
st.write("Smart AI-based Flight Finder")

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs(["✈ Flights", "🏨 Hotels", "🚆 Trains"])

with tab1:

    # -----------------------------
    # FILTERS
    # -----------------------------
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    sources = ["Select All"] + sorted(df["Source"].unique())
    destinations = ["Select All"] + sorted(df["Destination"].unique())
    airlines = ["Select All"] + sorted(df["Airline"].unique())
    dates = ["Select All"] + sorted(df["Date"].astype(str).unique())

    source = col1.selectbox(
        "From",
        sources,
        index=sources.index(st.session_state.source),
        key="source"
    )

    destination = col2.selectbox(
        "To",
        destinations,
        index=destinations.index(st.session_state.destination),
        key="destination"
    )

    airline = col3.selectbox(
        "Airline",
        airlines,
        index=airlines.index(st.session_state.airline),
        key="airline"
    )

    sort = col4.selectbox(
        "Sort By",
        ["Select", "Cheapest", "Premium", "Fastest", "Best"],
        index=0,
        key="sort"
    )

    selected_date = col5.selectbox(
        "Travel Date",
        dates,
        index=dates.index(st.session_state.date),
        key="date"
    )

    col6.button("❌ Clear", on_click=clear_filters)

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
    # SEARCH BUTTON
    # -----------------------------
    is_valid = source != "Select All" and destination != "Select All"
    search = st.button("🔍 Search Flights", disabled=not is_valid)

    if not is_valid:
        st.warning("Please select From and To")

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

        # SAVE RECENT SEARCH
        st.session_state.recent_searches.insert(0, f"{source} → {destination}")
        st.session_state.recent_searches = st.session_state.recent_searches[:5]

        # -----------------------------
        # RESULT CARDS
        # -----------------------------
        for i, row in data.head(10).iterrows():

            discount = random.randint(200, 800)
            final_price = row["Price"] - discount

            # SAFE ACCESS (NO ERROR)
            duration = row.get("Duration", "N/A")
            stops = row.get("Stops", row.get("Total_Stops", "N/A"))

            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.05);
                padding:20px;
                border-radius:12px;
                margin-bottom:10px;
                display:flex;
                justify-content:space-between;
            ">
                <div>
                    <b>{row['Airline']}</b><br>
                    {row['Source']} → {row['Destination']}<br>
                    {duration} | {stops}<br><br>

                    <span style="background:#ff4b2b;padding:4px 10px;border-radius:6px;">
                        OFFER
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