# Philippine Agricultural Market Price Monitoring & Analytics System

## Overview

**AgriPrice Monitor** is an end-to-end data analytics project that collects agricultural market prices from the Philippine Department of Agriculture's **DA Bantay Presyo**, processes and validates the data using Python, stores it in MySQL, and presents the results through an interactive Power BI dashboard.

### Coverage

**Cities**

* Paranaque
* Las Pinas
* Muntinlupa

**Commodities**

* Rice
* Vegetable
* Meat
* Fruits

## Technology Stack

* Python
* Pandas
* Requests
* BeautifulSoup
* MySQL
* SQL
* Power BI
* DAX

## Data Pipeline

```text
DA Bantay Presyo
       ↓
Python Extraction
       ↓
Data Cleaning & Validation
       ↓
MySQL Database
       ↓
SQL Analytics View
       ↓
Power BI Dashboard
```

## Key Features

* Automated extraction from DA Bantay Presyo
* Multi-category agricultural price collection
* Market-specific filtering
* Data cleaning and validation
* Duplicate-safe MySQL loading
* SQL analytical view: `vw_price_analysis`
* Interactive Power BI dashboard
* Market and item price comparison
* Historical price trend analysis

## Database

Database:

`agriproject_db`

Main tables:

```text
cities
markets
categories
subcategories
units
items
sources
price_records
```

Analytics view:

`vw_price_analysis`

## Power BI Dashboard

The dashboard contains:

### Market Price Overview

* Average Price
* Items Covered
* Markets Covered
* Latest Price Date
* Price Trends
* Category Comparison
* Market Comparison

### Market & Item Comparison

* Average Price by Market
* Market Price Matrix
* Minimum / Average / Maximum Price
* Price Difference
* Price Difference %

### Price Data Explorer

* Filterable detailed price records
* Category, city, market, item, and date filters

## Project Structure

```text
AgriPriceMonitor/
│
├── extract/
│   └── da_scraper.py
├── transform/
│   └── data_cleaner.py
├── load/
│   ├── db_connection.py
│   └── items_loader.py
├── sql/
│   ├── schema.sql
│   ├── views.sql
│   └── analysis_queries.sql
├── dashboard/
│   ├── AgriPriceMonitor.pbix
│   └── screenshots/
├── data/
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Data Source

Philippine Department of Agriculture — **DA Bantay Presyo**

`http://www.bantaypresyo.da.gov.ph`

## Project Status

Core ETL pipeline, MySQL database, SQL analytics, and Power BI dashboard are completed.

PDF-based historical data integration is planned as a future enhancement.

## Portfolio Purpose

This project demonstrates practical skills in **Python, ETL, data cleaning, SQL/MySQL, data validation, and Power BI analytics**.
