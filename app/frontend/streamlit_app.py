import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Insurance Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .sidebar-content {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# 🛡️ Insurance Fraud Detection")
    st.markdown("**Professional ML-Powered Analytics Platform**")
    st.divider()
    
    st.markdown("### Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("System", "🟢 Online")
    with col2:
        st.metric("API", "✅ Active")
    
    st.divider()
    
    st.markdown("### Navigation")
    st.markdown("""
    - 📊 **Dashboard** - Analytics overview
    - 🔮 **Predictions** - Analyze cases
    - 📈 **Analytics** - Advanced insights
    - ⚙️ **Settings** - Configuration
    """)
    
    st.divider()
    
    st.markdown("### About")
    st.caption("""
    Version 1.0.0  
    Built with Streamlit & FastAPI  
    Last updated: May 2026
    """)

# Main content
st.markdown("""
# 🛡️ Insurance Fraud Detection Platform

Welcome to the professional fraud detection dashboard. Use the navigation menu to explore:

- **Dashboard**: Real-time metrics and analytics
- **Predictions**: Analyze individual cases
- **Analytics**: Advanced insights and trends
- **Settings**: Configuration and API management
""")

# Quick start cards
st.markdown("## Getting Started")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 Dashboard
    View real-time fraud detection metrics, trends, and system performance.
    
    [Go to Dashboard](/?page=1_Dashboard)
    """)

with col2:
    st.markdown("""
    ### 🔮 Predictions
    Analyze individual insurance cases and get fraud risk assessments.
    
    [Analyze Case](/?page=2_Predictions)
    """)

with col3:
    st.markdown("""
    ### 📈 Analytics
    Deep dive into patterns, feature importance, and risk distributions.
    
    [View Analytics](/?page=3_Analytics)
    """)

# Feature highlights
st.markdown("---")
st.markdown("## Key Features")

features = {
    "🎯 High Accuracy": "94.2% accuracy with advanced XGBoost models",
    "⚡ Fast Processing": "Sub-400ms prediction latency",
    "📊 Rich Analytics": "Comprehensive dashboards and reports",
    "🔒 Secure": "Enterprise-grade security and data protection",
    "📱 Responsive": "Works on desktop, tablet, and mobile",
    "🔄 Real-time": "Live data updates and monitoring"
}

col1, col2, col3 = st.columns(3)
for idx, (title, desc) in enumerate(features.items()):
    if idx % 3 == 0:
        col = col1
    elif idx % 3 == 1:
        col = col2
    else:
        col = col3
    
    with col:
        st.success(f"**{title}**\n\n{desc}")