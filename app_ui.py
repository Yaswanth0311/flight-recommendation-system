import streamlit as st
import pandas as pd

st.set_page_config(page_title="Flight Recommendation System", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("flights.csv")

# Safe handling
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -----------------------------
# DEFAULT SESSION VALUES
# -----------------------------
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
st.caption("Smart AI-based Flight Finder")

# -----------------------------
# FILTER UI
# -----------------------------
sources = ["Select All"] + sorted(df["Source"].dropna().unique())
destinations = ["Select All"] + sorted(df["Destination"].dropna().unique())
airlines = ["Select All"] + sorted(df["Airline"].dropna().unique())

dates = ["Select All"]
if "Date" in df.columns:
    dates += sorted(df["Date"].dropna().astype(str).unique())

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
min_price = int(df["Price"].min())
max_price = int(df["Price"].max())

price_range = st.slider(
    "Price Range",
    min_price,
    max_price,
    (min_price, max_price)
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

    if selected_date != "Select All" and "Date" in data.columns:
        data = data[data["Date"].astype(str) == selected_date]

    # Price filter
    data = data[
        (data["Price"] >= price_range[0]) &
        (data["Price"] <= price_range[1])
    ]

    # Sorting
    if sort == "Cheapest":
        data = data.sort_values("Price")
    elif sort == "Premium":
        data = data.sort_values("Price", ascending=False)

    st.success("Flights Found")

    # -----------------------------
    # DISPLAY CARDS (NO HTML BUG)
    # -----------------------------
    for i, row in data.head(10).iterrows():

        duration = row["Duration"] if "Duration" in data.columns else "N/A"

        if "Stops" in data.columns:
            stops = row["Stops"]
        else:
            stops = row.get("Total_Stops", "N/A")

        # Layout columns instead of HTML (100% safe)
        left, right = st.columns([4, 1])

        with left:
            st.markdown(f"### {row['Airline']}")
            st.write(f"{row['Source']} → {row['Destination']}")
            st.caption(f"{duration} | {stops}")

        with right:
            st.markdown(
                f"<h3 style='text-align:right;'>₹{int(row['Price'])}</h3>",
                unsafe_allow_html=True
            )

        st.divider()

else:
    st.info("Select filters and click Search Flights")