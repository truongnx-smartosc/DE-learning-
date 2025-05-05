-- Query to select all records from the sales dataset
SELECT * FROM `top-broker-458809-c0.my_dataset.sale_table`;

-- Revenue by Region and Segment
SELECT 
  Region,
  Segment,
  COUNT(*) AS total_opportunities,
  SUM(`Forecasted Monthly Revenue`) AS total_forecasted_revenue,
  SUM(`Weighted Revenue`) AS total_weighted_revenue
FROM `top-broker-458809-c0.my_dataset.sale_table`
GROUP BY Region, Segment
ORDER BY total_forecasted_revenue DESC;

-- Salesperson performance: leads count, closed leads, conversion rate
SELECT 
  Salesperson,
  COUNT(*) AS total_leads,
  SUM(CASE WHEN `Closed Opportunity` = TRUE THEN 1 ELSE 0 END) AS closed_leads,
  ROUND(SAFE_DIVIDE(SUM(CAST(`Closed Opportunity` AS INT64)), COUNT(*)) * 100, 2) AS conversion_rate_percent
FROM `top-broker-458809-c0.my_dataset.sale_table`
GROUP BY Salesperson
ORDER BY conversion_rate_percent DESC;
