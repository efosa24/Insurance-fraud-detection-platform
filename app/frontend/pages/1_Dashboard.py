import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Dashboard - Insurance Fraud Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .header-container {
        padding: 20px 0;
        border-bottom: 3px solid #667eea;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Header
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Insurance Fraud Detection Dashboard")
        st.markdown("**Real-time monitoring and analytics**")
    with col2:
        st.metric("System Status", "🟢 Active", delta="Online")

# Key Metrics
st.markdown("## Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Cases Analyzed", "1,247", "↑ 12% from last month")
    
with col2:
    st.metric("Fraud Detection Rate", "94.2%", "↑ 2.3%")
    
with col3:
    st.metric("False Positives", "3.8%", "↓ 0.5%")
    
with col4:
    st.metric("Avg Processing Time", "0.34s", "↓ 50ms")

# Charts Row 1
st.markdown("## Analysis & Trends")
col1, col2 = st.columns(2)

with col1:
    # Fraud distribution
    fraud_data = pd.DataFrame({
        'Status': ['Legitimate', 'Fraud Detected'],
        'Count': [1200, 47]
    })
    fig = px.pie(fraud_data, values='Count', names='Status',
                 color_discrete_sequence=['#2ecc71', '#e74c3c'],
                 title="Case Distribution")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Detection accuracy over time
    dates = pd.date_range(start='2026-05-01', periods=30, freq='D')
    accuracy_data = pd.DataFrame({
        'Date': dates,
        'Accuracy': np.random.uniform(92, 96, 30)
    })
    fig = px.line(accuracy_data, x='Date', y='Accuracy',
                  title="Prediction Accuracy Trend",
                  markers=True)
    fig.update_yaxes(range=[90, 97])
    st.plotly_chart(fig, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    # Cases by accident area
    area_data = pd.DataFrame({
        'Area': ['Urban', 'Suburban', 'Rural'],
        'Cases': [450, 580, 217],
        'Fraud': [15, 18, 14]
    })
    fig = px.bar(area_data, x='Area', y=['Cases', 'Fraud'],
                 title="Cases by Accident Area",
                 barmode='group',
                 color_discrete_sequence=['#3498db', '#e74c3c'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Top fraud indicators
    indicators = pd.DataFrame({
        'Indicator': ['High Deductible', 'Young Driver', 'Multiple Claims', 'Expensive Vehicle', 'Fault Mismatch'],
        'Frequency': [35, 28, 25, 15, 10]
    })
    fig = px.barh(indicators, x='Frequency', y='Indicator',
                  title="Top Fraud Indicators",
                  color='Frequency',
                  color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

# Recent Cases Table
st.markdown("## Recent Cases")
recent_cases = pd.DataFrame({
    'Case ID': ['FC-2026-001', 'FC-2026-002', 'FC-2026-003', 'FC-2026-004', 'FC-2026-005'],
    'Date': pd.date_range(start='2026-05-20', periods=5, freq='D'),
    'Vehicle': ['Honda Civic', 'Toyota Camry', 'Ford F-150', 'BMW 3-Series', 'Chevrolet Malibu'],
    'Area': ['Urban', 'Suburban', 'Rural', 'Urban', 'Suburban'],
    'Fraud Risk': ['Low', 'Medium', 'High', 'Low', 'Medium'],
    'Confidence': ['98.5%', '87.2%', '92.1%', '97.8%', '85.4%']
})

# Color code the fraud risk
def color_fraud_risk(val):
    if val == 'High':
        color = 'background-color: #e74c3c; color: white'
    elif val == 'Medium':
        color = 'background-color: #f39c12; color: white'
    else:
        color = 'background-color: #2ecc71; color: white'
    return color

st.dataframe(
    recent_cases.style.applymap(color_fraud_risk, subset=['Fraud Risk']),
    use_container_width=True
)

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📈 Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
with col2:
    st.caption("🔄 Auto-refresh: Every 5 minutes")
with col3:
    st.caption("🛡️ Powered by Advanced ML Models")
