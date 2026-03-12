# Hospitality Procurement & Cost Monitoring Pipeline

Python | Pandas | SQLite | YAML | Pytest

An end-to-end **data engineering pipeline** that simulates how a hospitality business can monitor supplier pricing, track historical price changes, and automatically generate alerts when unusual price increases occur.

The project models a realistic hotel or restaurant procurement workflow where supplier invoices are **ingested, cleaned, transformed, and analyzed** to detect cost anomalies that could impact operational margins.

---

# Business Problem

Hospitality businesses rely on multiple suppliers for products such as:

- vegetables
- meat
- seafood
- dairy
- beverages

Over time, supplier prices can change gradually or spike unexpectedly.

Without a monitoring system, these changes may go unnoticed and lead to:

- rising food and beverage costs
- procurement inefficiencies
- weaker supplier negotiation leverage
- reduced operating margins

This pipeline demonstrates how a simple **data engineering system** can detect these changes automatically.

---

# Project Goals

This project demonstrates core **data engineering concepts** including:

- raw data generation and ingestion
- schema validation and data cleaning
- SQLite-based data storage
- transformation into analytics-ready tables
- automated monitoring logic for price increases
- configuration-driven pipeline behavior
- end-to-end pipeline execution from a single runner script

---

# Tech Stack

- **Python**
- **Pandas**
- **SQLite**
- **YAML (configuration)**
- **Pytest**

---

# Project Structure

```text
hospitality-procurement-monitoring-pipeline/
│
├── data/
│   ├── raw/
│   │   └── supplier_invoices.csv
│   └── processed/
│
├── db/
│   └── procurement.db
│
├── outputs/
│   └── price_alerts.csv
│
├── pipeline/
│   └── run_pipeline.py
│
├── src/
│   ├── config/
│   │   └── settings.yaml
│   ├── ingestion/
│   │   ├── generate_invoices.py
│   │   └── load_invoices.py
│   ├── monitoring/
│   │   └── detect_price_alerts.py
│   ├── transform/
│   │   └── build_price_history.py
│   └── utils/
│       └── helpers.py
│
├── tests/
│   └── test_pipeline.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

# Pipeline Architecture

Synthetic Supplier Invoice Data
        │
        ▼
Raw CSV Generation
        │
        ▼
Ingestion + Cleaning
        │
        ▼
SQLite Raw Table (raw_invoices)
        │
        ▼
Transformation Layer
        │
        ▼
SQLite Analytics Table (price_history)
        │
        ▼
Monitoring Logic
        │
        ▼
Alerts Table + CSV Export (price_alerts)

---

# Dataset

The project uses a **synthetic but realistic hospitality procurement dataset** containing:

- **5 suppliers**
- **20 hospitality-related products**
- **weekly invoice records**
- **changing supplier prices over time**
- **intentionally injected data quality issues**

Example columns:

- `invoice_id`
- `invoice_date`
- `supplier`
- `product`
- `category`
- `quantity`
- `unit_price`
- `total_amount`

---

# Example Data Quality Issues

To simulate real operational data challenges, the dataset includes:

- one missing unit price  
- one supplier naming inconsistency  
- one duplicate row  

These issues are automatically handled during the ingestion and cleaning stage.

---

# Tables Created

### `raw_invoices`
Cleaned invoice data stored in SQLite.

### `price_history`
A transformed analytics table containing:

- previous price  
- price change  
- percentage price change  

### `price_alerts`
Rows where the percentage price increase exceeds the configured alert threshold.

---

# Configuration

Pipeline configuration is stored in:

```
src/config/settings.yaml
```

This controls:

- dataset date range  
- database path  
- output CSV path  
- alert threshold  

Example:

```yaml
monitoring:
  alert_threshold_pct: 5.0
  ```

How to Run

### 1. Install dependencies

```
python -m pip install -r requirements.txt
```

### 2. Run the pipeline

```
python pipeline/run_pipeline.py
```

If using a specific interpreter:

```
"C:\path\to\python.exe" pipeline/run_pipeline.py
```

# Pipeline Steps

The pipeline executes the following stages:

### 1. generate_invoices.py

- generates synthetic weekly supplier invoice data

### 2. load_invoices.py

- validates schema
- standardizes supplier names
- removes critical nulls
- removes duplicate rows
- loads cleaned data into SQLite

### 3. build_price_history.py

- reads raw_invoices
- calculates previous price, price change, and percent change
- writes the price_history table

### 4. detect_price_alerts.py

- reads price_history
- flags price increases above the configured threshold
- writes price_alerts
- exports outputs/price_alerts.csv

# Outputs

After running the pipeline, the following artifacts are created:

db/procurement.db

outputs/price_alerts.csv

# Example Results

For the current dataset:

- 521 raw rows generated
- 519 clean rows loaded into SQLite
- 112 price alerts detected above the 5% threshold

# Skills Demonstrated

This project demonstrates:

- ETL pipeline design
- schema validation
- data cleaning
- SQL-based storage
- transformation logic
- monitoring and alert generation
- configuration-driven pipelines
- production-style project structuring

# Future Improvements

Possible extensions include:

- orchestration using Prefect
- migration from SQLite to PostgreSQL
- building a procurement monitoring dashboard
- deploying the pipeline on Azure
- expanding automated testing

# Why This Project Matters

This project intentionally focuses on a hospitality operations use case rather than a generic dataset. It combines domain relevance with data engineering structure to demonstrate practical pipeline design for real operational workflows.