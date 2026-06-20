# Nifty100 ETL Pipeline

## Project Overview

This project builds an ETL pipeline for Nifty100 financial data. It extracts data from Excel files, performs normalization and validation, and loads the cleaned data into a SQLite database. SQL queries and Power BI are used for analysis and visualization.

---

## Features

- Load Excel source files
- Normalize data
- Perform data quality validation
- Load data into SQLite
- Execute SQL queries
- Build Power BI dashboard
- Run unit tests

---

## Folder Structure

- data/
- src/
- db/
- tests/
- output/
- notebooks/

---

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Pytest
- Power BI

---

## Database Tables

- Companies
- Analysis
- Balance Sheet
- Cash Flow
- Documents
- Financial Ratios
- Peer Groups
- Profit & Loss
- Pros & Cons
- Sectors
- Stock Prices

---

## Data Quality Checks

- Empty Data Check
- Duplicate Check
- Missing Values Check
- Row Count Validation
- Column Count Validation

---

## Testing

Run the following command:

```bash
pytest
```

All unit tests passed successfully.

---

## Dashboard

The Power BI dashboard includes:

- Overview
- Financial Analysis
- Balance Sheet Analysis
- Profit & Loss Analysis