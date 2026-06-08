import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from importlib.machinery import SourceFileLoader
from PIL import Image

# Setup page config
st.set_page_config(page_title="Churn Retention ROI", layout="wide", page_icon="📉")

# Load data
@st.cache_data
def load_data():
    cleaner = SourceFileLoader("cleaner", "1_data_cleaning.py").load_module()
    df_raw = cleaner.load_and_clean_data('../data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df_targets = pd.read_csv('../retention_targets.csv')
    return df_raw, df_targets

df_raw, df_targets = load_data()

# App Title
st.title("📊 Customer Churn & Retention ROI Dashboard")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Driver Analysis", "Retention Action List"])

with tab1:
    st.header("Executive Overview")
    
    # Calculate Metrics
    total_customers = len(df_raw)
    churn_rate = len(df_raw[df_raw['churn'] == 'Yes']) / total_customers * 100
    total_targets = len(df_targets)
    projected_savings = df_targets['Expected_Value_of_Action'].sum()
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
    col3.metric("High-Risk Targets", f"{total_targets:,}")
    col4.metric("Projected Net Savings", f"${projected_savings:,.0f}")
    
    st.divider()
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Churn Rate by Contract Type")
        contract_df = df_raw.groupby('contract').apply(
            lambda x: len(x[x['churn'] == 'Yes']) / len(x) * 100
        ).reset_index(name='Churn Rate (%)')
        fig = px.bar(contract_df, x='contract', y='Churn Rate (%)', text_auto='.1f', color='contract')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.subheader("Churn by Tenure")
        fig = px.histogram(df_raw, x='tenure', color='churn', barmode='group', nbins=20)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Driver Analysis & Explainability")
    
    st.markdown("""
    Our calibrated Random Forest model highlights the top features driving customer churn risk. 
    Below is the SHAP (SHapley Additive exPlanations) summary plot. 
    Red dots indicate high feature values, and their position on the X-axis shows their impact on increasing/decreasing churn risk.
    """)
    
    # Show SHAP plot image
    try:
        image = Image.open('../plots/shap_summary.png')
        st.image(image, caption='SHAP Feature Importance Plot', use_container_width=True)
    except:
        st.warning("SHAP plot not found. Run the modeling script first.")
        
    st.divider()
    
    st.subheader("Cross-Tab: Contract vs Internet Service")
    crosstab = pd.crosstab(df_raw['contract'], df_raw['internetservice'], normalize='index') * 100
    fig = px.imshow(crosstab, text_auto='.1f', aspect="auto", title="Churn Rate % Heatmap", color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Retention Action List (ROI Engine)")
    st.markdown(f"**Targeting Rule:** Only target customers where `Expected Value of Action > $0` based on a $50 intervention cost.")
    
    # Editable ROI Slider
    st.sidebar.header("ROI Assumptions")
    intervention_cost = st.sidebar.slider("Intervention Cost ($)", 10, 100, 50)
    success_rate = st.sidebar.slider("Intervention Success Rate (%)", 10, 80, 30) / 100
    
    # Recalculate based on slider
    df_sim = df_targets.copy()
    df_sim['Sim_Expected_Value'] = (df_sim['Churn_Probability'] * df_sim['CLV'] * success_rate) - intervention_cost
    sim_targets = df_sim[df_sim['Sim_Expected_Value'] > 0].sort_values(by='Sim_Expected_Value', ascending=False)
    sim_savings = sim_targets['Sim_Expected_Value'].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("Adjusted Target List Size", f"{len(sim_targets):,}")
    col2.metric("Adjusted Projected Savings", f"${sim_savings:,.0f}")
    
    st.dataframe(
        sim_targets[['Rank', 'CustomerID', 'Churn_Probability', 'MonthlyCharges', 'CLV', 'Sim_Expected_Value']]
        .style.format({
            'Churn_Probability': '{:.1%}',
            'MonthlyCharges': '${:.2f}',
            'CLV': '${:.2f}',
            'Sim_Expected_Value': '${:.2f}'
        }),
        use_container_width=True,
        height=500
    )
