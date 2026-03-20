import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from importlib.machinery import SourceFileLoader

# Load the cleaning function from step 1
cleaner = SourceFileLoader("cleaner", "1_data_cleaning.py").load_module()

def run_eda(data, save_dir='plots'):
    # Ensure plots directory exists
    os.makedirs(save_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    print("Generating EDA Visualizations...")

    # Figure 1: Overall and Categorical Highlights
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Customer Churn Exploratory Data Analysis', fontsize=16)

    # 1. Overall Churn Rate (Pie Chart)
    churn_counts = data['churn'].value_counts()
    axes[0, 0].pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', 
                   colors=['#66b3ff', '#ff9999'], startangle=90)
    axes[0, 0].set_title('Overall Churn Rate')

    # 2. Churn by Contract Type (Bar Chart)
    sns.countplot(data=data, x='contract', hue='churn', ax=axes[0, 1], palette='Set2')
    axes[0, 1].set_title('Churn by Contract Type')

    # 3. Churn by Senior Citizen Status
    sns.countplot(data=data, x='seniorcitizen', hue='churn', ax=axes[1, 0], palette='Set2')
    axes[1, 0].set_title('Churn by Senior Citizen (0=No, 1=Yes)')

    # 4. Monthly Charges vs Churn (Box Plot)
    sns.boxplot(data=data, x='churn', y='monthlycharges', ax=axes[1, 1], palette='Set2')
    axes[1, 1].set_title('Monthly Charges vs Churn')

    plt.tight_layout()
    plt.savefig(f'{save_dir}/churn_overview.png')
    print(f"Saved overview plot to {save_dir}/churn_overview.png")
    plt.close()

    # Figure 2: Tenure Distribution Map (KDE)
    plt.figure(figsize=(8, 5))
    sns.kdeplot(data=data[data['churn'] == 'No']['tenure'], fill=True, color='blue', label='Retained')
    sns.kdeplot(data=data[data['churn'] == 'Yes']['tenure'], fill=True, color='red', label='Churned')
    plt.title('Tenure Distribution by Churn')
    plt.xlabel('Tenure (Months)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{save_dir}/tenure_distribution.png')
    print(f"Saved tenure plot to {save_dir}/tenure_distribution.png")
    plt.close()

if __name__ == "__main__":
    df = cleaner.load_and_clean_data('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    run_eda(df)
