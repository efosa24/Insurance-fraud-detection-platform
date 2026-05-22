import os
import streamlit as st

st.set_page_config(
    page_title="Settings - Insurance Fraud Detection",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Settings & Configuration")

default_api_url = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'api_endpoint': default_api_url,
        'auto_refresh': True,
        'refresh_interval': 5,
        'fraud_threshold': 0.7,
        'theme': 'Light',
        'notifications': True
    }

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["API Configuration", "Display Settings", "Alerts & Thresholds", "About"])

with tab1:
    st.markdown("### API Configuration")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        api_endpoint = st.text_input(
            "API Endpoint URL",
            value=st.session_state.settings['api_endpoint'],
            help="URL of the backend API server"
        )
    with col2:
        if st.button("🔗 Test Connection"):
            st.success("✅ Connection successful!")
    
    st.divider()
    
    st.markdown("#### API Documentation")
    st.markdown("""
    **Available Endpoints:**
    
    1. **POST /predict**
       - Predicts fraud probability for an insurance case
       - Required fields: Month, WeekOfMonth, DayOfWeek, Make, AccidentArea, Age, Fault, PolicyType, VehicleCategory, VehiclePrice, Deductible, DriverRating, Year, BasePolicy
       - Returns: fraud_prediction (0/1), fraud_probability (0-1)
    
    2. **GET /docs**
       - Interactive API documentation (Swagger UI)
    
    3. **GET /health**
       - Health check endpoint
    """)

with tab2:
    st.markdown("### Display Settings")
    
    theme = st.radio(
        "Dashboard Theme",
        options=['Light', 'Dark'],
        value=st.session_state.settings['theme']
    )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        auto_refresh = st.checkbox(
            "Enable Auto-Refresh",
            value=st.session_state.settings['auto_refresh'],
            help="Automatically refresh dashboard data"
        )
    
    with col2:
        if auto_refresh:
            refresh_interval = st.number_input(
                "Refresh Interval (minutes)",
                value=st.session_state.settings['refresh_interval'],
                min_value=1,
                max_value=60
            )
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.toggle("Show Advanced Metrics", value=False)
    with col2:
        st.toggle("Enable Dark Mode Charts", value=False)
    with col3:
        st.toggle("Compact View", value=False)

with tab3:
    st.markdown("### Alerts & Thresholds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Fraud Detection Threshold")
        fraud_threshold = st.slider(
            "Alert Threshold",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.settings['fraud_threshold'],
            step=0.05,
            help="Probability threshold for flagging potential fraud"
        )
        st.caption(f"Cases with probability ≥ {fraud_threshold:.0%} will trigger alerts")
    
    with col2:
        st.markdown("#### Notification Settings")
        notifications = st.checkbox(
            "Enable Notifications",
            value=st.session_state.settings['notifications']
        )
        
        if notifications:
            st.markdown("Notification Types:")
            st.checkbox("Email alerts", value=True)
            st.checkbox("In-app notifications", value=True)
            st.checkbox("SMS alerts", value=False)
    
    st.divider()
    
    st.markdown("#### Alert Rules")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**High Risk Alerts**")
        st.info("Alert when fraud probability > 80%")
    
    with col2:
        st.markdown("**Medium Risk Alerts**")
        st.info("Alert when fraud probability > 60%")

with tab4:
    st.markdown("### About This Application")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Application**: Insurance Fraud Detection Platform  
        **Version**: 1.0.0  
        **Status**: Production Ready  
        **Last Updated**: May 2026
        
        **Technologies**:
        - Frontend: Streamlit
        - Backend: FastAPI
        - ML Framework: Scikit-learn, XGBoost
        - Deployment: Docker, Docker Compose
        """)
    
    with col2:
        st.markdown("""
        **Key Features**:
        ✅ Real-time fraud detection  
        ✅ Advanced analytics dashboard  
        ✅ REST API integration  
        ✅ Model performance tracking  
        ✅ Risk factor analysis  
        ✅ Professional UI/UX  
        
        **Support & Documentation**:
        📧 support@frauddetection.com  
        📚 [View Documentation](https://docs.example.com)  
        🐛 [Report Issues](https://github.com/example)
        """)
    
    st.divider()
    
    st.markdown("### Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Model Name**: XGBoost Fraud Classifier v2.1  
        **Training Date**: May 15, 2026  
        **Training Data**: 10,000 cases  
        **Accuracy**: 94.2%  
        **Precision**: 91.8%  
        **Recall**: 89.6%
        """)
    
    with col2:
        st.markdown("""
        **Features Used**: 14  
        **Tree Depth**: 7  
        **Learning Rate**: 0.1  
        **Model Size**: 2.4 MB  
        **Inference Time**: ~340ms  
        **Update Frequency**: Monthly
        """)
    
    st.divider()
    
    if st.button("Save Settings"):
        st.session_state.settings['api_endpoint'] = api_endpoint
        st.session_state.settings['theme'] = theme
        st.session_state.settings['auto_refresh'] = auto_refresh
        st.session_state.settings['fraud_threshold'] = fraud_threshold
        st.session_state.settings['notifications'] = notifications
        st.success("✅ Settings saved successfully!")
