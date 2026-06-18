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