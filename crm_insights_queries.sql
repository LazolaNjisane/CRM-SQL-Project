-- Total deals closed per Month
SELECT
  FORMAT_DATE('%Y-%m', engage_date) AS Engage_Month_Year,
  COUNT(opportunity_id) AS total_closed_deals
from `CRM_Dataset.Sales_pipeline`
where close_date is not null
group by Engage_Month_Year
order by total_closed_deals DESC;

-- Win Rates by Product 
SELECT 
  p.product,
  COUNT(opportunity_id) AS total_Deals,
  SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END) AS won_deals,
  ROUND(
    SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END)*100/COUNT(sp.opportunity_id),2) AS win_rate_parecnt,
  SUM(sp.close_value) AS Revenue
FROM 
  `CRM_Dataset.Sales_pipeline` AS sp
JOIN 
  `CRM_Dataset.Products` AS p ON sp.product=p.product
GROUP BY 
  product
ORDER BY 
  win_rate_parecnt DESC;

--Sales Agent Performance & Deal Duration
SELECT 
  sp.sales_agent,
  st.regional_office,
  COUNT(opportunity_id) AS total_Deals,
  SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END) AS won_deals,
  CEILING(AVG(duration)) AS Average_Duration,
  ROUND(
    SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END)*100/COUNT(sp.opportunity_id),2) AS win_rate_percent
FROM 
  `CRM_Dataset.Sales_pipeline` AS sp
JOIN 
  `CRM_Dataset.Sales_teams` AS st ON sp.sales_agent = st.sales_agent
GROUP BY
  sp.sales_agent,
  st.regional_office
ORDER BY
  win_rate_percent DESC;

-- Succesful deals across all client locations
SELECT 
    a.office_location,
    STRING_AGG(DISTINCT st.regional_office, ', '), 
  COUNT(sp.opportunity_id) AS total_Deals,
  SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END) AS won_deals,
  ROUND(
    SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END)*100/COUNT(sp.opportunity_id),2) AS win_rate_percent,
  SUM(sp.close_value) AS Revenue
FROM
  `CRM_Dataset.Accounts` AS a 
JOIN 
  `CRM_Dataset.Sales_pipeline` AS sp ON a.account=sp.account 
JOIN
  `CRM_Dataset.Sales_teams` AS st ON sp.sales_agent=st.sales_agent
JOIN
  `CRM_Dataset.Products` AS p ON sp.product = p.product
GROUP BY
  office_location
ORDER BY
  win_rate_percent DESC;

  -- Regional Office Performance
SELECT 
  st.regional_office,
  COUNT(opportunity_id) AS total_Deals,
  SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END) AS won_deals,
  ROUND(
    SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END)*100/COUNT(sp.opportunity_id),2) AS win_rate_percent
FROM 
  `CRM_Dataset.Sales_pipeline` AS sp
JOIN 
  `CRM_Dataset.Sales_teams` AS st ON sp.sales_agent = st.sales_agent
GROUP BY
  st.regional_office
ORDER BY
  win_rate_percent DESC;