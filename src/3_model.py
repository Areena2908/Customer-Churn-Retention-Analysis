import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, average_precision_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
import shap
from importlib.machinery import SourceFileLoader

# Load the cleaning function
cleaner = SourceFileLoader("cleaner", "1_data_cleaning.py").load_module()

def train_and_evaluate(data, save_dir='../models', plot_dir='../plots'):
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)
    
    print("Preparing data for machine learning...")
    df_ml = data.copy()
    
    # Save customer IDs for ROI targets later if present, though cleaner might drop it
    customer_ids = None
    if 'customerid' in df_ml.columns:
        customer_ids = df_ml['customerid'].copy()
        df_ml.drop('customerid', axis=1, inplace=True)
    
    # Label encode categorical variables
    label_encoders = {}
    for column in df_ml.select_dtypes(include=['object', 'category']).columns:
        le = LabelEncoder()
        df_ml[column] = le.fit_transform(df_ml[column])
        label_encoders[column] = le
        joblib.dump(le, f'{save_dir}/le_{column}.pkl')

    # Features (X) and Target (y)
    X = df_ml.drop('churn', axis=1)
    y = df_ml['churn']

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier with balanced class weights...")
    # Pillar 1: Handle class imbalance
    base_rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    
    # Pillar 1: Calibrate probabilities for ROI calculations
    print("Calibrating probabilities...")
    calibrated_rf = CalibratedClassifierCV(estimator=base_rf, method='sigmoid', cv=5)
    calibrated_rf.fit(X_train, y_train)

    # Predictions
    y_pred = calibrated_rf.predict(X_test)
    y_pred_proba = calibrated_rf.predict_proba(X_test)[:, 1]

    # Pillar 1: Honest Evaluation Metrics
    auc_pr = average_precision_score(y_test, y_pred_proba)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("--- Calibrated Model Performance ---")
    print(f"AUC-PR   : {auc_pr:.3f} (Primary Metric)")
    print(f"Recall   : {recall:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"F1 Score : {f1:.2f}")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Actual Churn')
    plt.xlabel('Predicted Churn')
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/confusion_matrix.png')
    plt.close()

    # Save model
    joblib.dump(calibrated_rf, f'{save_dir}/calibrated_rf_model.pkl')
    print(f"Model saved to {save_dir}/calibrated_rf_model.pkl")

    # Pillar 1: SHAP Driver Analysis
    print("Generating SHAP Explainer...")
    # SHAP requires the base uncalibrated tree estimator
    base_rf.fit(X_train, y_train)
    explainer = shap.TreeExplainer(base_rf)
    
    # Calculate SHAP values for a sample to save the summary plot
    # Use a small sample to speed up calculation for the plot
    X_sample = shap.sample(X_train, 500)
    shap_values = explainer.shap_values(X_sample)
    
    # Plot SHAP summary
    plt.figure(figsize=(10, 6))
    # SHAP for RandomForest classification returns a list of arrays (one for each class). We use [1] for churn class
    shap.summary_plot(shap_values[1] if isinstance(shap_values, list) else shap_values, X_sample, show=False)
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/shap_summary.png')
    plt.close()
    print(f"Saved SHAP summary plot to {plot_dir}/shap_summary.png")

    return calibrated_rf, label_encoders

if __name__ == "__main__":
    df = cleaner.load_and_clean_data('../data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    train_and_evaluate(df)
