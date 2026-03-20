# Customer Churn Analysis Portfolio Project

This repository contains a complete, end-to-end Data Science portfolio project predicting customer churn using the IBM Telco Customer Churn dataset.

## 📊 Step 3: Key Insights
Based on the Exploratory Data Analysis and Machine Learning feature importance, the following insights were discovered:

1. **Who is most likely to churn?**
   Customers on **Month-to-month contracts** are highly likely to churn, especially those who have been with the company for less than a year (low tenure).
2. **Top 3 factors driving churn:**
   - **Contract Type:** Month-to-month users leave easily; 1 or 2-year contract users stay.
   - **Tenure:** The first 6-12 months are critical. High churn happens early on.
   - **Total & Monthly Charges:** High monthly bills correlate strongly with higher churn rates.
3. **Average Monthly Charge comparison:**
   Customers who churned had a significantly **higher average monthly charge** (~$74) compared to those who stayed (~$61).

## 🚀 How to Run the Project

1. **Set up virtual environment & install requirements:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Clean Data and Generate EDA Plots:**
   ```bash
   python 1_data_cleaning.py
   python 2_eda.py
   ```

3. **Train the Machine Learning Model:**
   ```bash
   python 3_model.py
   ```

4. **Launch the Dashboard:**
   ```bash
   streamlit run 4_dashboard.py
   ```

The Streamlit dashboard provides an interactive UI to view churn by contract, tenure, and dynamically calculated top-level metrics.
