import pandas as pd
import numpy as np
import joblib
from importlib.machinery import SourceFileLoader

# Load the cleaning function
cleaner = SourceFileLoader("cleaner", "1_data_cleaning.py").load_module()

def calculate_roi_targets():
    print("Loading data and calibrated model...")
    df = cleaner.load_and_clean_data('../data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    
    # We only want to target customers who have NOT churned yet (we are predicting future churn)
    # The dataset has 'Churn' indicating if they left. If we are running a real campaign,
    # we would run this on current active customers.
    # For the sake of the portfolio, we will score ALL customers as if we are predicting them right now.
    
    # Reload model and encoders
    model = joblib.load('../models/calibrated_rf_model.pkl')
    
    df_ml = df.copy()
    customer_ids = df_ml['customerid'].copy()
    if 'customerid' in df_ml.columns:
        df_ml.drop('customerid', axis=1, inplace=True)
        
    for column in df_ml.select_dtypes(include=['object', 'category']).columns:
        if column != 'churn':  # skip target if present
            le = joblib.load(f'../models/le_{column}.pkl')
            # Handle unseen labels just in case
            df_ml[column] = le.transform(df_ml[column])
            
    X = df_ml.drop('churn', axis=1) if 'churn' in df_ml.columns else df_ml

    # Get calibrated probabilities
    churn_probs = model.predict_proba(X)[:, 1]
    
    # Assumptions based on spec
    expected_remaining_months = 24
    intervention_cost = 50.0  # e.g., a $50 discount or hardware credit
    intervention_success_rate = 0.30  # 30% chance the offer prevents churn
    
    # Calculate ROI logic
    results = pd.DataFrame({
        'CustomerID': customer_ids,
        'MonthlyCharges': df['monthlycharges'],
        'Churn_Probability': churn_probs,
    })
    
    results['CLV'] = results['MonthlyCharges'] * expected_remaining_months
    results['Expected_Loss'] = results['Churn_Probability'] * results['CLV']
    
    # Expected Value of Action (EVA)
    results['Expected_Value_of_Action'] = (results['Churn_Probability'] * results['CLV'] * intervention_success_rate) - intervention_cost
    
    # Target only positive EVA, sort descending
    targets = results[results['Expected_Value_of_Action'] > 0].copy()
    targets = targets.sort_values(by='Expected_Value_of_Action', ascending=False)
    targets['Rank'] = np.arange(1, len(targets) + 1)
    
    # Reorder columns
    targets = targets[['Rank', 'CustomerID', 'Churn_Probability', 'MonthlyCharges', 'CLV', 'Expected_Loss', 'Expected_Value_of_Action']]
    
    # Save to CSV
    targets.to_csv('../retention_targets.csv', index=False)
    
    # Output Headline Metrics
    total_savings = targets['Expected_Value_of_Action'].sum()
    print("\n--- Retention ROI Simulation Results ---")
    print(f"Total Active Customers Scored: {len(results):,}")
    print(f"High-ROI Target Customers    : {len(targets):,}")
    print(f"Projected Net Savings        : ${total_savings:,.2f}")
    print("\nAssumptions:")
    print(f"- Time Horizon      : {expected_remaining_months} months")
    print(f"- Intervention Cost : ${intervention_cost}")
    print(f"- Success Rate      : {intervention_success_rate * 100}%")

if __name__ == "__main__":
    calculate_roi_targets()
