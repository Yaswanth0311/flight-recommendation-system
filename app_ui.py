import streamlit as st
import pandas as pd
import pickle
from db import create_tables
from auth import login, signup
from booking import save_booking

# Init DB
create_tables()

# Load data
data = pd.read_csv("flights.csv")

# Load model
model, columns = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Flight App", layout="wide")

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
if st.session_state.user is None:

    st.title("🔐 Login / Signup")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(user, pwd):
                st.session_state.user = user
                st.success("Logged in")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pwd = st.text_input("New Password", type="password")

        if st.button("Signup"):
            signup(new_user, new_pwd)
            st.success("Account created")

# ---------------- MAIN APP ----------------
else:
    st.title("✈️ Flight Recommendation System")

    st.write(f"Welcome, {st.session_state.user}")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        source = st.selectbox("From", data["Source"].unique())

    with col2:
        dest = st.selectbox("To", data["Destination"].unique())

    with col3:
        airline = st.selectbox("Airline", data["Airline"].unique())

    price_range = st.slider("Max Price", 1000, 20000, 10000)

    # Search
    if st.button("Search Flights"):

        df = data[
            (data["Source"] == source) &
            (data["Destination"] == dest) &
            (data["Price"] <= price_range)
        ]

        st.success("Flights Found")

        for i, row in df.head(5).iterrows():

            # ML Prediction
            input_df = pd.DataFrame([row[["Airline","Source","Destination","Duration","Total_Stops"]]])
            input_df = pd.get_dummies(input_df).reindex(columns=columns, fill_value=0)

            predicted_price = int(model.predict(input_df)[0])

            st.markdown(f"""
            ### {row['Airline']}
            {row['Source']} → {row['Destination']}  
            💰 Actual: ₹{row['Price']}  
            🤖 Predicted: ₹{predicted_price}
            """)

            if st.button(f"Book {i}"):

                save_booking(
                    st.session_state.user,
                    row["Source"],
                    row["Destination"],
                    row["Price"],
                    "2026-04-20"
                )

                st.success("Booking saved!")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()