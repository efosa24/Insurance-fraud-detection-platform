import streamlit as st
import requests

st.title("Insurance Fraud Detection")

month = st.selectbox("Month", ["Jan", "Feb", "Mar"])
age = st.number_input("Age", 18, 100)
deductible = st.number_input("Deductible", 100, 2000)

if st.button("Predict Fraud"):

    payload = {
        "Month": month,
        "WeekOfMonth": 1,
        "DayOfWeek": "Monday",
        "Make": "Honda",
        "AccidentArea": "Urban",
        "Age": age,
        "Fault": "Policy Holder",
        "PolicyType": "Sedan - Collision",
        "VehicleCategory": "Sedan",
        "VehiclePrice": "20000 to 29000",
        "Deductible": deductible,
        "DriverRating": 3,
        "Year": 1994,
        "BasePolicy": "Collision"
    }

    response = requests.post(
        "http://localhost:8000/predict",
        json=payload
    )

    st.write(response.json())