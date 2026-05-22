import os
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Predictions - Insurance Fraud Detection",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Fraud Detection Predictions")
st.markdown("**Analyze individual cases for fraud risk**")

# Initialize session state for history
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []

# Sidebar for API configuration
default_api_url = os.getenv("API_URL", "http://localhost:8000")
if 'api_endpoint' not in st.session_state:
    st.session_state['api_endpoint'] = default_api_url

with st.sidebar:
    st.markdown("### API Configuration")
    api_url = st.text_input("API Endpoint", value=st.session_state['api_endpoint'])
    st.divider()

# Persist endpoint for this session
st.session_state['api_endpoint'] = api_url

# Form for prediction
st.markdown("## Case Information")

col1, col2 = st.columns(2)

with col1:
    month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June",
                                   "July", "August", "September", "October", "November", "December"])
    week_of_month = st.slider("Week of Month", 1, 4, 2)
    day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", 
                                               "Friday", "Saturday", "Sunday"])
    age = st.number_input("Driver Age", 18, 100, 35)
    driver_rating = st.slider("Driver Rating (1-5)", 1, 5, 3)

with col2:
    accident_area = st.selectbox("Accident Area", ["Urban", "Suburban", "Rural"])
    fault = st.selectbox("Fault", ["Policy Holder", "Third Party"])
    make = st.selectbox("Vehicle Make", ["Honda", "Toyota", "Ford", "BMW", "Chevrolet", 
                                         "Nissan", "Mercedes", "Audi", "Volkswagen", "Other"])
    vehicle_category = st.selectbox("Vehicle Category", ["Sedan", "SUV", "Truck", "Coupe", "Van"])
    year = st.slider("Vehicle Year", 1990, 2026, 2015)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    vehicle_price = st.selectbox("Vehicle Price", ["10000 to 19000", "20000 to 29000", 
                                                    "30000 to 39000", "40000 to 49000", "50000+"])

with col2:
    deductible = st.number_input("Deductible ($)", 100, 5000, 500, step=100)

with col3:
    policy_type = st.selectbox("Policy Type", ["Sedan - Collision", "SUV - Comprehensive",
                                               "Truck - Liability", "Coupe - Full Coverage"])

with col4:
    base_policy = st.selectbox("Base Policy", ["Collision", "Comprehensive", "Liability", "Full Coverage"])

# Prediction button
if st.button("🔍 Analyze for Fraud Risk", key="predict_btn", use_container_width=True):
    
    # Prepare payload
    payload = {
        "Month": month,
        "WeekOfMonth": week_of_month,
        "DayOfWeek": day_of_week,
        "Make": make,
        "AccidentArea": accident_area,
        "Age": age,
        "Fault": fault,
        "PolicyType": policy_type,
        "VehicleCategory": vehicle_category,
        "VehiclePrice": vehicle_price,
        "Deductible": deductible,
        "DriverRating": driver_rating,
        "Year": year,
        "BasePolicy": base_policy
    }
    
    try:
        with st.spinner("Analyzing case..."):
            response = requests.post(
                f"{api_url}/predict",
                json=payload,
                timeout=10
            )
            
        if response.status_code == 200:
            result = response.json()
            
            # Add to history
            st.session_state.predictions_history.append({
                'timestamp': datetime.now(),
                'case': f"{make} {vehicle_category}",
                'fraud_prediction': result['fraud_prediction'],
                'fraud_probability': result['fraud_probability']
            })
            
            # Display result
            col1, col2, col3 = st.columns(3)
            
            fraud_prob = result['fraud_probability']
            is_fraud = result['fraud_prediction']
            
            with col1:
                if is_fraud == 1:
                    st.error("⚠️ FRAUD DETECTED")
                else:
                    st.success("✅ LEGITIMATE CASE")
            
            with col2:
                st.metric("Fraud Probability", f"{fraud_prob*100:.2f}%")
            
            with col3:
                confidence = (fraud_prob if is_fraud == 1 else 1 - fraud_prob) * 100
                st.metric("Model Confidence", f"{confidence:.2f}%")
            
            # Gauge chart for visualization
            st.markdown("### Risk Assessment")
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=fraud_prob * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Fraud Risk Score"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#e74c3c" if fraud_prob > 0.5 else "#2ecc71"},
                    'steps': [
                        {'range': [0, 25], 'color': "#d5f4e6"},
                        {'range': [25, 50], 'color': "#a9dfbf"},
                        {'range': [50, 75], 'color': "#f5b7b1"},
                        {'range': [75, 100], 'color': "#ec7063"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk factors explanation
            st.markdown("### Risk Factors Analysis")
            
            risk_factors = []
            
            if age < 25:
                risk_factors.append(("Young Driver", "High fraud rate in 18-24 age group"))
            if deductible > 1000:
                risk_factors.append(("High Deductible", "Higher incentive for fraudulent claims"))
            if driver_rating < 3:
                risk_factors.append(("Low Driver Rating", "Indicates risky driving behavior"))
            if accident_area == "Urban":
                risk_factors.append(("Urban Area", "Higher fraud rates in urban locations"))
            if year < 2000:
                risk_factors.append(("Old Vehicle", "Older vehicles have higher claim rates"))
            
            if risk_factors:
                for factor, explanation in risk_factors:
                    st.warning(f"**{factor}**: {explanation}")
            else:
                st.info("✅ No significant risk factors detected")
                
        else:
            st.error(f"API Error: {response.status_code}")
            st.error(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Make sure the API server is running.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Prediction History
if st.session_state.predictions_history:
    st.markdown("---")
    st.markdown("### Prediction History")
    
    history_df = pd.DataFrame([
        {
            'Time': h['timestamp'].strftime("%H:%M:%S"),
            'Case': h['case'],
            'Result': "🔴 Fraud" if h['fraud_prediction'] == 1 else "🟢 Legitimate",
            'Probability': f"{h['fraud_probability']*100:.2f}%"
        }
        for h in st.session_state.predictions_history
    ])
    
    st.dataframe(history_df, use_container_width=True)
    
    if st.button("Clear History"):
        st.session_state.predictions_history = []
        st.rerun()
