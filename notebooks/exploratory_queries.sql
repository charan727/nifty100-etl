-- Query 1
SELECT COUNT(*) FROM companies;

-- Query 2
SELECT * FROM companies LIMIT 10;

-- Query 3
SELECT COUNT(*) FROM profitandloss;

-- Query 4
SELECT COUNT(*) FROM balancesheet;

-- Query 5
SELECT COUNT(*) FROM cashflow;

-- Query 6
SELECT company_id, AVG(profit) AS avg_profit
FROM profitandloss
GROUP BY company_id;

-- Query 7
SELECT sector, COUNT(*)
FROM companies
GROUP BY sector;

-- Query 8
SELECT *
FROM stock_prices
ORDER BY trade_date DESC
LIMIT 10;

-- Query 9
SELECT company_id, COUNT(*)
FROM financial_ratios
GROUP BY company_id;

-- Query 10
SELECT company_id, pros, cons
FROM prosandcons;


-- Top Revenue Companies
SELECT company_id,
       SUM(revenue) AS total_revenue
FROM profitandloss
GROUP BY company_id
ORDER BY total_revenue DESC;

-- Top Profit Companies
SELECT company_id,
       SUM(profit) AS total_profit
FROM profitandloss
GROUP BY company_id
ORDER BY total_profit DESC;

-- Highest ROE
SELECT company_id,
       MAX(roe) AS highest_roe
FROM analysis
GROUP BY company_id
ORDER BY highest_roe DESC;

-- Highest ROCE
SELECT company_id,
       MAX(roce) AS highest_roce
FROM analysis
GROUP BY company_id
ORDER BY highest_roce DESC;

-- Top Market Cap Companies
SELECT company_name,
       market_cap
FROM companies
ORDER BY market_cap DESC
LIMIT 10;

-- Highest Stock Price
SELECT company_id,
       MAX(close_price) AS highest_price
FROM stock_prices
GROUP BY company_id
ORDER BY highest_price DESC;

-- Average PE Ratio
SELECT company_id,
       AVG(pe_ratio) AS avg_pe
FROM financial_ratios
GROUP BY company_id
ORDER BY avg_pe DESC;

-- Average PB Ratio
SELECT company_id,
       AVG(pb_ratio) AS avg_pb
FROM financial_ratios
GROUP BY company_id
ORDER BY avg_pb DESC;

-- Average Revenue by Year
SELECT year,
       AVG(revenue) AS avg_revenue
FROM profitandloss
GROUP BY year
ORDER BY year;

-- Average Profit by Year
SELECT year,
       AVG(profit) AS avg_profit
FROM profitandloss
GROUP BY year
ORDER BY year;