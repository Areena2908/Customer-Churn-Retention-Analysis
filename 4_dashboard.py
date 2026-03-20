import streamlit as st
import pandas as pd
import plotly.express as px
from importlib.machinery import SourceFileLoader

# Load the cleaning function
cleaner = SourceFileLoader("cleaner", "1_data_cleaning.py").load_module()

# --- Page Config ---
st.set_page_config(page_title="Customer Churn Analysis", layout="wide")

# --- Data Loading (Cached for performance) ---
@st.cache_data
def load_data():
    return cleaner.load_and_clean_data('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset. Please ensure the CSV is properly downloaded. Error: {e}")
    st.stop()

# --- Dashboard Layout ---
st.title("📊 Customer Churn Analysis Portfolio Project")
st.markdown("Exploring the IBM Telco Telecom Dataset to find out why customers leave.")

# Calculate top level metrics
total_customers = len(df)
churned_customers = len(df[df['churn'] == 'Yes'])
churn_rate = (churned_customers / total_customers) * 100

# Big Numbers
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Total Churned", f"{churned_customers:,}")
col3.metric("Overall Churn Rate", f"{churn_rate:.1f}%")

st.divider()

# Charts Side by Side
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Churn by Contract Type")
    contract_df = df.groupby(['contract', 'churn']).size().reset_index(name='Count')
    fig_contract = px.bar(
        contract_df, x='contract', y='Count', color='churn', barmode='group',
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    st.plotly_chart(fig_contract, use_container_width=True)

with col_right:
    st.subheader("Churn by Tenure (Months)")
    # Interactive Histogram
    fig_tenure = px.histogram(
        df, x='tenure', color='churn', nbins=30, 
        color_discrete_sequence=['#e74c3c', '#2ecc71'], opacity=0.7
    )
    st.plotly_chart(fig_tenure, use_container_width=True)

st.divider()

st.subheader("💡 Top Factors Driving Churn")
st.markdown("""
1. **Contract Type**: Customers on **Month-to-month** contracts are significantly more likely to churn. Locking customers into 1 or 2 year contracts drastically improves retention.
2. **Tenure**: The highest risk of churn is within the **first 10 months**. If a customer survives the first year, they are likely to stay long-term.
3. **Monthly Charges**: Customers with **higher monthly bills** churn at higher rates. A pricing review for basic services might be required.
""")
