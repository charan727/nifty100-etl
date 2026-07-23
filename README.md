# Nifty100 Financial Analytics Platform

## Project Overview

The Nifty100 Financial Analytics Platform is an end-to-end data engineering and financial analytics project built using Python, SQLite, Pandas, Plotly, and Streamlit.

The project extracts financial data from Excel files, performs data normalization and quality validation, loads the processed data into a SQLite database, calculates more than 50 financial KPIs, and provides an interactive dashboard for financial analysis, stock screening, peer comparison, trend analysis, and valuation.

---

## Features

- ETL Pipeline for Excel Financial Data
- Data Normalization
- Data Quality Validation
- SQLite Database Integration
- Financial Ratio Engine
- CAGR Calculation Engine
- Composite Quality Score
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Analysis
- Valuation Engine
- Interactive Streamlit Dashboard
- Interactive Plotly Visualizations
- CSV Report Export
- Unit Testing using Pytest

---

## Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- SQL
- Streamlit
- Plotly
- OpenPyXL
- Pytest

---

## Project Structure

```
nifty100-etl/
│
├── data/
├── db/
├── notebooks/
├── output/
├── src/
│   ├── analytics/
│   ├── dashboard/
│   ├── etl/
│   ├── validation/
│   └── utils/
├── tests/
├── requirements.txt
├── README.md
└── main.py
```

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

## Data Quality Validation

The following validation rules are implemented:

- Empty Data Validation
- Duplicate Record Validation
- Missing Value Validation
- Row Count Validation
- Column Count Validation

---

## Financial KPIs

The project calculates more than 50 financial KPIs, including:

- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Net Profit Margin
- Operating Profit Margin
- Debt-to-Equity Ratio
- Interest Coverage Ratio
- Revenue CAGR
- PAT CAGR
- Free Cash Flow
- Composite Quality Score

---

## Dashboard Modules

- Home Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Analysis
- Reports Center

---

## Project Architecture

```
Excel Source Files
        │
        ▼
ETL Pipeline
        │
        ▼
Data Validation
        │
        ▼
Data Normalization
        │
        ▼
SQLite Database
        │
        ▼
Financial Ratio Engine
        │
        ▼
Analytics Engine
        │
        ▼
Streamlit Dashboard
```

---

## Testing

Run all unit tests using:

```bash
pytest
```

All **22 unit tests** passed successfully.

---

## Sprint 1

### Status

Completed Successfully

### Deliverables

- Environment Setup
- Excel Data Loader
- Data Normalization
- SQLite Database Integration
- Data Quality Validation

---

## Sprint 2

### Status

Completed Successfully

### Deliverables

- Financial Ratio Engine
- CAGR Engine
- Cash Flow KPIs
- Financial Ratios Table
- Automated KPI Population

---

## Sprint 3

### Status

Completed Successfully

### Deliverables

- Financial Screener Engine
- Composite Quality Score
- Peer Percentile Engine
- Radar Chart Generation
- Peer Comparison Report
- Benchmark Company Highlight
- SQLite Peer Percentiles

### Dataset Limitation

The source financial dataset does not contain the following market-based metrics:

- Price-to-Earnings (P/E) Ratio
- Price-to-Book (P/B) Ratio
- Dividend Yield
- Market Capitalization
- Sales

The application automatically skips unavailable metrics while applying screening filters.

---

## Sprint 4

### Status

Completed Successfully

### Deliverables

- Interactive Streamlit Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Analysis
- Reports Center
- Interactive Plotly Charts
- CSV Report Export
- Valuation Summary

---

## Project Statistics

| Item | Count |
|------|------:|
| Source Excel Files | 12 |
| Database Tables | 11 |
| Dashboard Pages | 8 |
| Financial KPIs | 50+ |
| Unit Tests | 22 Passed |

---

## Future Enhancements

- Live NSE/BSE Data Integration
- Portfolio Tracking
- User Authentication
- REST API Development
- Email Notifications
- Machine Learning Based Stock Recommendation
- Cloud Deployment using AWS or Azure

---

## Author

Developed as a Financial Analytics and Data Engineering Capstone Project using Python, SQLite, Streamlit, and Plotly.