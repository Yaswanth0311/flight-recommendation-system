import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Flight AI System", layout="wide")

# Custom CSS (BACKGROUND + TEXT)
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: white;
    }

    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }

    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
df = pd.read_csv("flights.csv")

# Title
st.title("✈️ Flight Recommendation System")
st.markdown("### ✨ Smart AI-based Flight Finder")
st.write("")

# Filters layout
col1, col2, col3 = st.columns(3)

with col1:
    source = st.selectbox("Source", df["Source"].unique())

with col2:
    destination = st.selectbox("Destination", df["Destination"].unique())

with col3:
    airline = st.selectbox("Airline (Optional)", ["All"] + list(df["Airline"].unique()))

# Price slider
price_range = st.slider(
    "Select Price Range",
    int(df["Price"].min()),
    int(df["Price"].max()),
    (int(df["Price"].min()), int(df["Price"].quantile(0.75)))
)

# Button
if st.button("🔍 Find Best Flights"):
    filtered = df[
        (df["Source"] == source) &
        (df["Destination"] == destination)
    ].copy()

    # Airline filter
    if airline != "All":
        filtered = filtered[filtered["Airline"] == airline]

    # Price filter
    filtered = filtered[
        (filtered["Price"] >= price_range[0]) &
        (filtered["Price"] <= price_range[1])
    ]

    if filtered.empty:
        st.warning("❌ No flights found!")
    else:
        # AI logic
        filtered["Duration_num"] = filtered["Duration"].str.extract(r'(\d+)').astype(float)
        filtered["Score"] = filtered["Price"] + filtered["Duration_num"] * 100

        best = filtered.sort_values(by="Score")

        # Best flight highlight
        st.subheader("🏆 Best Flight Recommendation")
        st.success(
            f"""
            ✈️ Airline: {best.iloc[0]['Airline']}  
            💰 Price: ₹{best.iloc[0]['Price']}  
            ⏱ Duration: {best.iloc[0]['Duration']}
            """
        )

        st.write("")

        # Table
        st.subheader("📊 Other Recommended Flights")
        st.dataframe(best[["Airline", "Price", "Duration"]].head(10))