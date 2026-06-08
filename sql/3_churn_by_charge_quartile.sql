WITH charge_quartiles AS (
    SELECT 
        MonthlyCharges,
        Churn,
        NTILE(4) OVER (ORDER BY MonthlyCharges) as charge_quartile
    FROM read_csv_auto('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
)
SELECT 
    charge_quartile,
    MIN(MonthlyCharges) as min_charge,
    MAX(MonthlyCharges) as max_charge,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
FROM charge_quartiles
GROUP BY charge_quartile
ORDER BY charge_quartile;
