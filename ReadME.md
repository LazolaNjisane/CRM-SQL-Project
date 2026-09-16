# 📊 CRM Sales Pipeline & Performance Analytics

## 🎯 1. Ask (Business Objective)
**Business Question:** *Which sales agents, product lines, and regional offices drive the highest win rates and conversion velocity, and how can the business optimize its sales pipeline performance?*
* **Stakeholders:** Sales Directors, Regional Managers, and Marketing Teams.
* **Goal:** Identify high-performing behaviors, product bottlenecks, and geographic trends to improve overall pipeline health and revenue generation.

---

## 🗂️ 2. Prepare (Data Sources & Structure)
The dataset originates from Maven Analytics and simulates an enterprise CRM sales pipeline across four interconnected relational tables:
1. **`sales_pipeline`**: Contains opportunity IDs, stages (Won, Lost, In Progress), timestamps (`engage_date`, `close_date`), and duration.
2. **`sales_teams`**: Maps sales agents to managers and regional offices (Central, East, West).
3. **`products`**: Tracks product catalogs, series categories, and unit sales prices.
4. **`accounts`**: Details enterprise client information, sectors, office locations, and revenue sizes.

---

## 🧹 3. Process (Data Cleaning & Validation)
* **Tool:** VS Code / Python (Pandas) / BigQuery
* **Actions Taken:**
  * Inspected schema types, handled string stripping, and verified primary/foreign key relationships across CSV files.
  * Used BigQuery `FORMAT_DATE()` and `EXTRACT()` functions to parse date fields safely without casting errors.
  * Handled table header alignments and managed `NULL` values in active deals.

---

## 📈 4. Analyze (SQL Queries & Insights)
Key metrics were extracted using multi-table `JOIN`s, conditional aggregations (`CASE WHEN`), and window/grouping functions in Google BigQuery.

### Sample Query: Win Rates by Product
```sql
SELECT 
  p.product,
  COUNT(opportunity_id) AS total_Deals,
  SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END) AS won_deals,
  ROUND(
    SUM(CASE WHEN sp.deal_stage = 'Won' THEN 1 ELSE 0 END)*100/COUNT(sp.opportunity_id),2) AS win_rate_percent,
  (COUNT(sp.opportunity_id) * MAX(p.sales_price)) AS Revenue
FROM 
  `CRM_Dataset.Sales_pipeline` AS sp
JOIN 
  `CRM_Dataset.Products` AS p ON sp.product=p.product
GROUP BY 
  product
ORDER BY 
  win_rate_percent DESC;