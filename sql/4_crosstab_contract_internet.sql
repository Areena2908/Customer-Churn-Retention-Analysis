SELECT 
    Contract,
    InternetService,
    COUNT(*) as total_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
FROM read_csv_auto('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
GROUP BY Contract, InternetService
ORDER BY Contract, churn_rate_pct DESC;
