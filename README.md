<h1 align="center">📉 Telco Customer Churn Prediction</h1>

<p align="center">
  <strong>An End-to-End Machine Learning & Analytics Portfolio Project</strong>
</p>

## 📖 Overview
Customer churn is one of the most important metrics for a growing, subscriber-based business. Retaining an existing customer costs far less than acquiring a new one. This project utilizes the **IBM Telco Customer Churn dataset** to build a comprehensive data pipeline that not only predicts *which* customers are likely to leave, but also identifies the primary business drivers causing the churn.

### 🎯 Key Objectives
- **Data Engineering:** Extract, clean, and preprocess raw telecom data.
- **Exploratory Data Analysis (EDA):** Uncover statistical patterns separating loyal customers from flight risks.
- **Predictive Modeling:** Train a Random Forest Classifier to identify high-risk accounts with ~80% accuracy.
- **Interactive Dashboard:** Deploy a Streamlit web application summarizing actionable business insights.

## 🛠 Tech Stack
*   **Python**
*   **Pandas & NumPy:** Data manipulation and cleaning.
*   **Matplotlib & Seaborn:** Statistical data visualization.
*   **Scikit-Learn:** Machine Learning algorithms and label encoding.
*   **Streamlit & Plotly:** Interactive web dashboard and deployment.

## 📊 Key Business Insights
Based on our EDA and Machine Learning Feature Importance extraction, we discovered the following:

1. **The Contract Trap:** Customers on **Month-to-month contracts** are overwhelmingly more likely to churn compared to those on 1-year or 2-year lock-in periods. 
2. **The "Danger Zone" Tenure:** The highest flight risk occurs within the **first 6 to 12 months**. If a customer remains for over a year, their probability of churning drops significantly.
3. **Price Sensitivity:** High monthly charges strongly correlate with higher churn rates, indicating that a pricing review for basic service tiers may drastically improve retention.

<br>

## 🚀 How to Run Locally

### 1. Setup Environment
Clone the repository and set up a Python virtual environment:
```bash
git clone https://github.com/Areena2908/CustomerChurn-Prediction.git
cd CustomerChurn-Prediction
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Execute the Pipeline
Run the data wrangling and modeling scripts sequentially:
```bash
python 1_data_cleaning.py
python 2_eda.py
python 3_model.py
```
*This will generate model evaluation metrics in the console, save visualizations to `/plots`, and rebuild the predictive `.pkl` models required for the dashboard.*

### 3. Launch Dashboard
Start the interactive Streamlit application:
```bash
streamlit run 4_dashboard.py
```
*Navigate to `http://localhost:8501` in your browser to view the interactive web app.*
