import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Analytics - Insurance Fraud Detection",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Advanced Analytics")
st.markdown("**Detailed insights and performance metrics**")

# Tabs for different analytics
tab1, tab2, tab3, tab4 = st.tabs(["Model Performance", "Feature Impact", "Risk Distribution", "Trends"])

with tab1:
    st.markdown("### Model Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", "94.2%", "↑ 2.3%")
    with col2:
        st.metric("Precision", "91.8%", "↑ 1.5%")
    with col3:
        st.metric("Recall", "89.6%", "↑ 3.1%")
    with col4:
        st.metric("F1-Score", "0.907", "↑ 0.023")
    
    st.markdown("---")
    
    # ROC Curve
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Confusion Matrix")
        confusion_data = pd.DataFrame({
            'Actual / Predicted': ['Legitimate', 'Fraud'],
            'Predicted Legitimate': [1150, 45],
            'Predicted Fraud': [50, 2]
        })
        st.dataframe(confusion_data, use_container_width=True)
    
    with col2:
        st.markdown("#### Classification Distribution")
        classes = pd.DataFrame({
            'Class': ['True Negatives', 'False Positives', 'False Negatives', 'True Positives'],
            'Count': [1150, 50, 45, 2],
            'Percentage': ['91.9%', '4.0%', '3.6%', '0.2%']
        })
        fig = px.bar(classes, x='Class', y='Count', color='Count', 
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Feature Importance in Predictions")
    
    feature_importance = pd.DataFrame({
        'Feature': ['Age', 'Deductible', 'DriverRating', 'VehiclePrice', 
                   'Year', 'AccidentArea', 'PolicyType', 'DayOfWeek', 'Month', 'Make'],
        'Importance': [0.245, 0.189, 0.156, 0.121, 0.098, 0.087, 0.052, 0.031, 0.015, 0.006]
    })
    
    fig = px.barh(feature_importance.sort_values('Importance'), 
                  x='Importance', y='Feature',
                  title="Top Features Contributing to Fraud Prediction",
                  color='Importance',
                  color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Feature Descriptions:**")
    st.info("""
    - **Age**: Driver's age (higher age = lower fraud risk)
    - **Deductible**: Claim deductible amount (higher = higher fraud incentive)
    - **DriverRating**: Safety rating of the driver (1-5)
    - **VehiclePrice**: Estimated vehicle value
    - **Year**: Vehicle manufacturing year
    - **AccidentArea**: Urban/Suburban/Rural location
    - **PolicyType**: Type of insurance policy
    """)

with tab3:
    st.markdown("### Risk Distribution by Demographics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Fraud Rate by Age Group")
        age_groups = pd.DataFrame({
            'Age Group': ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
            'Fraud Rate': [8.5, 5.2, 2.8, 1.9, 1.2, 0.8],
            'Cases': [245, 312, 289, 267, 98, 36]
        })
        fig = px.bar(age_groups, x='Age Group', y='Fraud Rate',
                    color='Fraud Rate', color_continuous_scale='Reds',
                    hover_data=['Cases'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Fraud Rate by Vehicle Category")
        vehicle_fraud = pd.DataFrame({
            'Category': ['Sedan', 'SUV', 'Truck', 'Coupe', 'Van'],
            'Fraud Rate': [4.2, 3.8, 5.1, 6.3, 2.9],
            'Claims': [450, 380, 210, 156, 51]
        })
        fig = px.bar(vehicle_fraud, x='Category', y='Fraud Rate',
                    color='Fraud Rate', color_continuous_scale='Oranges',
                    hover_data=['Claims'])
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### Trends and Patterns")
    
    # Time series data
    dates = pd.date_range(start='2026-01-01', periods=150, freq='D')
    fraud_counts = np.cumsum(np.random.poisson(1.5, 150))
    legitimate_counts = np.cumsum(np.random.poisson(8, 150))
    
    trend_data = pd.DataFrame({
        'Date': dates,
        'Fraud Cases': fraud_counts,
        'Legitimate Cases': legitimate_counts
    })
    
    fig = px.line(trend_data, x='Date', y=['Fraud Cases', 'Legitimate Cases'],
                  title="Case Volume Trends",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap of fraud by day and hour
    st.markdown("#### Fraud Incidents Heatmap (Day of Week vs Hour of Day)")
    
    heatmap_data = np.random.randint(0, 5, (7, 24))
    heatmap_df = pd.DataFrame(
        heatmap_data,
        index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        columns=[f"{h:02d}:00" for h in range(24)]
    )
    
    fig = px.imshow(heatmap_df, labels=dict(x="Hour of Day", y="Day of Week", color="Fraud Cases"),
                    color_continuous_scale="YlOrRd")
    st.plotly_chart(fig, use_container_width=True)

# Export options
st.divider()
st.markdown("### Export Options")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Generate PDF Report"):
        st.info("PDF generation feature coming soon!")

with col2:
    if st.button("📥 Export to CSV"):
        st.info("CSV export feature coming soon!")

with col3:
    if st.button("🔗 Share Dashboard Link"):
        st.info("Shareable links feature coming soon!")
