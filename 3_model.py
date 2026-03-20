import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from importlib.machinery import SourceFileLoader

# Load the cleaning function
cleaner = SourceFileLoader("cleaner", "1_data_cleaning.py").load_module()

def train_and_evaluate(data, save_dir='models', plot_dir='plots'):
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)
    
    print("Preparing data for machine learning...")
    df_ml = data.copy()
    
    # Drop CustomerID as it has no predictive power
    if 'customerid' in df_ml.columns:
        df_ml.drop('customerid', axis=1, inplace=True)
    
    # Label encode categorical variables
    label_encoders = {}
    for column in df_ml.select_dtypes(include=['object', 'category']).columns:
        le = LabelEncoder()
        df_ml[column] = le.fit_transform(df_ml[column])
        label_encoders[column] = le
        # Save encoder
        joblib.dump(le, f'{save_dir}/le_{column}.pkl')

    # Features (X) and Target (y)
    X = df_ml.drop('churn', axis=1)
    y = df_ml['churn']

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Predictions
    y_pred = rf_model.predict(X_test)

    # Evaluation
    print("--- Model Performance ---")
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.2f}")
    print(f"Precision: {precision_score(y_test, y_pred):.2f}")
    print(f"Recall   : {recall_score(y_test, y_pred):.2f}")
    print(f"F1 Score : {f1_score(y_test, y_pred):.2f}")

    # Save model
    joblib.dump(rf_model, f'{save_dir}/rf_model.pkl')
    print(f"Model saved to {save_dir}/rf_model.pkl")

    # Feature Importance Plot
    feature_importances = pd.Series(rf_model.feature_importances_, index=X.columns)
    top_features = feature_importances.nlargest(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_features.values, y=top_features.index, palette='viridis')
    plt.title('Top 10 Factors for Predicting Customer Churn')
    plt.xlabel('Importance Score')
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/feature_importance.png')
    print(f"Saved feature importance plot to {plot_dir}/feature_importance.png")
    plt.close()
    
    return rf_model, label_encoders

if __name__ == "__main__":
    df = cleaner.load_and_clean_data('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    train_and_evaluate(df)
