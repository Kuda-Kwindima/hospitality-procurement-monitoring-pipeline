from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "kuda",
    "retries": 1,
}


with DAG(
    dag_id="hospitality_procurement_monitoring",
    default_args=default_args,
    description="Run hospitality procurement monitoring pipeline",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["procurement", "data-engineering", "monitoring"],
) as dag:

    generate_invoices = BashOperator(
        task_id="generate_invoices",
        bash_command="cd /opt/airflow && python -m src.ingestion.generate_invoices",
    )

    load_invoices = BashOperator(
        task_id="load_invoices",
        bash_command="cd /opt/airflow && python -m src.ingestion.load_invoices",
    )

    build_price_history = BashOperator(
        task_id="build_price_history",
        bash_command="cd /opt/airflow && python -m src.transform.build_price_history",
    )

    detect_price_alerts = BashOperator(
        task_id="detect_price_alerts",
        bash_command="cd /opt/airflow && python -m src.monitoring.detect_price_alerts",
    )

    generate_invoices >> load_invoices >> build_price_history >> detect_price_alerts