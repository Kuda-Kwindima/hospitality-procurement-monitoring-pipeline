from pathlib import Path
import sqlite3
import pandas as pd
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.utils.helpers import load_config, get_project_root


def get_project_paths():
    """Return database and output paths from config."""
    config = load_config()
    project_root = get_project_root()

    db_path = project_root / config["database"]["db_path"]
    output_csv_path = project_root / config["outputs"]["alerts_csv_path"]
    threshold_pct = config["monitoring"]["alert_threshold_pct"]

    return db_path, output_csv_path, threshold_pct


def extract_price_history(db_path: Path, table_name: str = "price_history") -> pd.DataFrame:
    """Read transformed price history from SQLite."""
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    query = f"SELECT * FROM {table_name}"

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(query, conn)

    print(f"Extracted {len(df)} rows from '{table_name}'.")
    return df


def build_price_alerts(df: pd.DataFrame, threshold_pct: float) -> pd.DataFrame:
    """Flag rows where price increase exceeds threshold."""
    alerts = df.copy()

    alerts["alert_flag"] = (
        alerts["previous_price"].notna() &
        (alerts["pct_change"] > threshold_pct)
    )

    alerts["alert_reason"] = alerts.apply(
        lambda row: f"Price increased by {row['pct_change']}% from previous invoice."
        if row["alert_flag"] else None,
        axis=1,
    )

    alert_rows = alerts[alerts["alert_flag"]].copy()

    alert_rows = alert_rows[
        [
            "invoice_id",
            "invoice_date",
            "supplier",
            "product",
            "category",
            "unit_price",
            "previous_price",
            "price_change",
            "pct_change",
            "alert_flag",
            "alert_reason",
        ]
    ].reset_index(drop=True)

    print(f"Detected {len(alert_rows)} price alerts above {threshold_pct}%.")
    return alert_rows


def load_alerts_to_sqlite(
    df: pd.DataFrame,
    db_path: Path,
    table_name: str = "price_alerts",
) -> None:
    """Load alerts table into SQLite."""
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Loaded {len(df)} rows into SQLite table '{table_name}'.")


def export_alerts_to_csv(df: pd.DataFrame, output_csv_path: Path) -> None:
    """Export alerts to CSV."""
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print(f"Exported alerts CSV to: {output_csv_path}")


def main():
    db_path, output_csv_path, threshold_pct = get_project_paths()

    price_history_df = extract_price_history(db_path)
    alerts_df = build_price_alerts(price_history_df, threshold_pct)

    load_alerts_to_sqlite(alerts_df, db_path)
    export_alerts_to_csv(alerts_df, output_csv_path)


if __name__ == "__main__":
    main()