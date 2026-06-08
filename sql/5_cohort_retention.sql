SELECT 
    tenure as months_survived,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_at_this_month
FROM read_csv_auto('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
GROUP BY tenure
ORDER BY tenure;
