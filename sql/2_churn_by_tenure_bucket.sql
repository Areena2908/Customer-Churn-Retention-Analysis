WITH tenure_buckets AS (
    SELECT 
        CASE 
            WHEN tenure < 12 THEN '0-12 months'
            WHEN tenure < 24 THEN '12-24 months'
            WHEN tenure < 48 THEN '24-48 months'
            ELSE '48+ months'
        END as tenure_bucket,
        Churn
    FROM read_csv_auto('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
)
SELECT 
    tenure_bucket,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
FROM tenure_buckets
GROUP BY tenure_bucket
ORDER BY 
    CASE tenure_bucket 
        WHEN '0-12 months' THEN 1
        WHEN '12-24 months' THEN 2
        WHEN '24-48 months' THEN 3
        ELSE 4
    END;
