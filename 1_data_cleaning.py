import pandas as pd
import numpy as np

def load_and_clean_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Initial shape: {df.shape}")
    
    # 1. Remove duplicates
    df = df.drop_duplicates()
    
    # 2. Fix data types: TotalCharges is string because of spaces
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # 3. Handle missing values: Fill missing TotalCharges with 0 (usually new customers)
    missing_before = df['TotalCharges'].isnull().sum()
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    print(f"Filled {missing_before} missing TotalCharges with 0.")
    
    # 4. Standardize columns to lowercase for easier access
    df.columns = [col.lower() for col in df.columns]
    
    print(f"Data shape after cleaning: {df.shape}")
    return df

if __name__ == "__main__":
    # If run directly, clean the dataset and save a copy
    clean_df = load_and_clean_data('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    
    # Save cleaned data to be used by the app later if needed
    clean_df.to_csv('data/cleaned_churn_data.csv', index=False)
    print("Cleaned data saved to data/cleaned_churn_data.csv")
