# Hospitality Procurement & Cost Monitoring Pipeline

Python | Pandas | PostgreSQL | SQLAlchemy | Docker | Docker Compose | Apache Airflow | YAML | Pytest

An end-to-end data engineering pipeline that simulates how a hospitality business can monitor supplier pricing, track historical price changes, and generate alerts when supplier-product prices increase above a defined threshold.

The project models a realistic hotel or restaurant procurement workflow where supplier invoices are generated, ingested, cleaned, transformed, stored in PostgreSQL, and monitored for cost anomalies that could affect operating margins.

---

## Business Problem

Hospitality businesses rely on multiple suppliers for products such as vegetables, meat, seafood, dairy, and beverages.

Over time, supplier prices may change gradually or spike unexpectedly. Without a monitoring system, these changes can go unnoticed and lead to:

* rising food and beverage costs
* weaker supplier negotiation control
* procurement inefficiencies
* reduced operating margins

This pipeline demonstrates how a data engineering system can help detect supplier price increases automatically.

---

## Project Goals

This project demonstrates core data engineering concepts, including:

* raw data generation and ingestion
* schema validation and data cleaning
* PostgreSQL-based data storage
* Dockerized database and orchestration services
* Apache Airflow DAG orchestration
* task dependency management
* transformation into analytics-ready tables
* automated monitoring logic for price increases
* local pipeline execution through a runner script
* unit testing with Pytest
* environment-based database configuration

---

## Tech Stack

* Python
* Pandas
* PostgreSQL
* SQLAlchemy
* Docker
* Docker Compose
* Apache Airflow
* YAML
* Pytest
* Git and GitHub

---

## Project Structure

```text
hospitality-procurement-monitoring-pipeline/
|
|-- airflow/
|   |-- dags/
|       |-- procurement_monitoring_dag.py
|
|-- data/
|   |-- raw/
|       |-- supplier_invoices.csv
|
|-- outputs/
|   |-- price_alerts.csv
|
|-- pipeline/
|   |-- run_pipeline.py
|
|-- src/
|   |-- config/
|   |   |-- settings.yaml
|   |
|   |-- database/
|   |   |-- postgres_connection.py
|   |
|   |-- ingestion/
|   |   |-- generate_invoices.py
|   |   |-- load_invoices.py
|   |
|   |-- transform/
|   |   |-- build_price_history.py
|   |
|   |-- monitoring/
|       |-- detect_price_alerts.py
|
|-- tests/
|   |-- test_pipeline.py
|
|-- .dockerignore
|-- .env.example
|-- .gitignore
|-- docker-compose.yml
|-- Dockerfile
|-- pytest.ini
|-- README.md
|-- requirements.txt
|-- requirements-airflow.txt
```

---

## Pipeline Architecture

```text
Synthetic supplier invoice data
        |
        v
generate_invoices.py
        |
        v
load_invoices.py
        |
        v
PostgreSQL: stg_supplier_invoices
        |
        v
build_price_history.py
        |
        v
PostgreSQL: price_history
        |
        v
detect_price_alerts.py
        |
        v
PostgreSQL: price_alerts
        |
        v
outputs/price_alerts.csv
```

The pipeline can be executed in two ways:

1. Locally using `pipeline/run_pipeline.py`
2. Through Apache Airflow using the DAG in `airflow/dags/procurement_monitoring_dag.py`

---

## Dataset

The project uses a synthetic but realistic hospitality procurement dataset containing:

* 5 suppliers
* 20 hospitality-related products
* weekly invoice records
* changing supplier prices over time
* intentionally injected data quality issues

Example columns:

* `invoice_id`
* `invoice_date`
* `supplier`
* `product`
* `category`
* `quantity`
* `unit_price`
* `total_amount`

---

## Example Data Quality Issues

To simulate real operational data challenges, the dataset includes:

* one missing unit price
* one supplier naming inconsistency
* one duplicate row

These issues are handled during the ingestion and cleaning stage.

---

## Tables Created

### `stg_supplier_invoices`

Cleaned and standardized supplier invoice data loaded into PostgreSQL as the staging table.

### `price_history`

A transformed table containing historical supplier-product price movement, including:

* previous price
* price change
* percentage price change

### `price_alerts`

A business monitoring output table containing supplier-product records where the percentage price increase exceeds the configured threshold.

---

## Configuration

Database connection values are managed through environment variables.

Create a local `.env` file using `.env.example` as a template:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=procurement_db
```

Important:

* `.env` is local and should not be committed.
* `.env.example` is safe to commit because it documents the required variables.
* Local Python connects to PostgreSQL through `localhost:5433`.
* Airflow containers connect to PostgreSQL through `postgres:5432`.

The project also includes `src/config/settings.yaml` for pipeline reference settings such as dataset dates, alert threshold, and output path. Some runtime database values are managed through `.env` and Docker Compose.

---

## How to Run Locally

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start PostgreSQL with Docker Compose

```bash
docker compose up -d postgres
```

### 4. Create `.env`

Copy `.env.example` to `.env` and confirm the values match your local Docker Compose setup.

### 5. Run the pipeline

```bash
python -m pipeline.run_pipeline
```

Expected outputs:

* PostgreSQL table: `stg_supplier_invoices`
* PostgreSQL table: `price_history`
* PostgreSQL table: `price_alerts`
* CSV output: `outputs/price_alerts.csv`

---

## How to Run with Airflow

Start the full Docker Compose environment:

```bash
docker compose up -d
```

This starts:

* PostgreSQL
* Airflow init
* Airflow webserver
* Airflow scheduler

Open Airflow:

```text
http://localhost:8080
```

Login:

```text
Username: admin
Password: admin
```

Unpause and trigger the DAG:

```text
hospitality_procurement_monitoring
```

The DAG runs the following tasks:

```text
generate_invoices
        |
        v
load_invoices
        |
        v
build_price_history
        |
        v
detect_price_alerts
```

---

## Pipeline Steps

### 1. `generate_invoices.py`

Generates synthetic weekly supplier invoice data and saves it to:

```text
data/raw/supplier_invoices.csv
```

### 2. `load_invoices.py`

Reads the raw CSV, validates schema, cleans the data, standardizes supplier names, removes bad records, removes duplicates, recalculates totals, and loads the cleaned data into:

```text
stg_supplier_invoices
```

### 3. `build_price_history.py`

Reads `stg_supplier_invoices`, calculates previous price, price change, and percentage change for each supplier-product combination, and writes:

```text
price_history
```

### 4. `detect_price_alerts.py`

Reads `price_history`, filters price increases above the alert threshold, writes the alert table, and exports a CSV:

```text
price_alerts
outputs/price_alerts.csv
```

---

## Apache Airflow Orchestration

The Airflow DAG is defined in:

```text
airflow/dags/procurement_monitoring_dag.py
```

Airflow provides:

* workflow orchestration
* task dependency management
* manual triggering
* task-level logs
* retry capability
* execution monitoring through the Airflow UI

The DAG currently uses manual triggering with:

```python
schedule_interval=None
```

This means the pipeline runs when triggered from the Airflow UI, rather than on an automatic schedule.

---

## Docker Architecture

The project uses Docker Compose for local infrastructure.

Services:

### PostgreSQL

Stores the pipeline output tables.

Container name:

```text
procurement_postgres
```

Local connection:

```text
localhost:5433
```

Internal Docker connection:

```text
postgres:5432
```

### Airflow Init

Initializes the Airflow metadata database and creates the admin user.

### Airflow Webserver

Provides the Airflow browser UI on:

```text
http://localhost:8080
```

### Airflow Scheduler

Monitors DAGs and triggers task execution.

Note: The Python pipeline is currently run locally through the virtual environment or orchestrated through Airflow tasks. The Dockerfile provides a base for containerizing the Python pipeline, but the current Docker Compose file does not define a separate pipeline container.

---

## Verify PostgreSQL Output

Enter the PostgreSQL container:

```bash
docker exec -it procurement_postgres psql -U postgres -d procurement_db
```

List tables:

```sql
\dt
```

Check row counts:

```sql
SELECT COUNT(*) FROM stg_supplier_invoices;
SELECT COUNT(*) FROM price_history;
SELECT COUNT(*) FROM price_alerts;
```

Expected result for the current dataset:

```text
stg_supplier_invoices: 519 rows
price_history: 519 rows
price_alerts: 112 rows
```

Exit PostgreSQL:

```sql
\q
```

---

## Testing

Run tests with:

```bash
pytest
```

The current test validates the core price history transformation logic, including:

* creation of `previous_price`
* creation of `price_change`
* creation of `pct_change`
* correct calculation of percentage change

---

## Example Results

For the current dataset:

* 521 raw rows generated
* 519 clean rows loaded into PostgreSQL
* 112 price alerts detected above the 5% threshold

Example business interpretation:

```text
A supplier-product price increase above 5% is flagged for procurement review.
```

This allows a hospitality procurement team to investigate whether the increase is expected, seasonal, negotiated, or requires supplier follow-up.

---

## Skills Demonstrated

This project demonstrates:

* ETL pipeline development
* data cleaning and validation
* PostgreSQL integration
* SQLAlchemy database connectivity
* Docker-based local infrastructure
* Docker Compose service orchestration
* Apache Airflow DAG orchestration
* task dependency management
* unit testing with Pytest
* environment variable management
* Git version control
* hospitality operations data use case design

---

## Future Improvements

Possible extensions include:

* read more configuration values directly from `settings.yaml`
* add stronger tests for ingestion and alert detection
* add a dedicated Docker Compose pipeline service
* separate Airflow metadata database from the procurement warehouse database
* add Power BI procurement analytics dashboard
* add email or Slack alert notifications
* add incremental loading strategy
* add CI/CD automation with GitHub Actions
* deploy to Azure or another cloud platform

---

## Why This Project Matters

This project focuses on a hospitality operations use case rather than a generic dataset. It combines domain relevance with data engineering structure to demonstrate practical pipeline design for real operational workflows.

It shows how supplier invoice data can be transformed into procurement monitoring outputs that support cost control, supplier review, and operational decision-making.
