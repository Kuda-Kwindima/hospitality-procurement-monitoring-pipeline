from pathlib import Path

import pandas as pd

from src.database.postgres_connection import get_postgres_engine


ALERT_THRESHOLD_PCT = 5.0


def extract_price_history(table_name: str = "price_history") -> pd.DataFrame:
    """Read price history data from PostgreSQL."""
    engine = get_postgres_engine()

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)

    print(f"Extracted {len(df)} rows from PostgreSQL table '{table_name}'.")
    return df


def detect_price_alerts(
    df: pd.DataFrame,
    threshold_pct: float = ALERT_THRESHOLD_PCT,
) -> pd.DataFrame:
    """Detect supplier-product price increases above the threshold."""
    alerts = df[
        (df["pct_change"].notna())
        & (df["pct_change"] > threshold_pct)
    ].copy()

    alerts["alert_type"] = "PRICE_INCREASE"
    alerts["alert_threshold_pct"] = threshold_pct

    print(f"Detected {len(alerts)} price alerts above {threshold_pct}%.")
    return alerts


def load_price_alerts(
    df: pd.DataFrame,
    table_name: str = "price_alerts",
) -> None:
    """Load price alerts into PostgreSQL."""
    engine = get_postgres_engine()

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {len(df)} rows into PostgreSQL table '{table_name}'.")


def save_alerts_csv(df: pd.DataFrame) -> None:
    """Save price alerts as a CSV output file."""
    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / "outputs" / "price_alerts.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Saved alerts CSV to: {output_path}")


def main():
    price_history_df = extract_price_history()
    alerts_df = detect_price_alerts(price_history_df)
    load_price_alerts(alerts_df)
    save_alerts_csv(alerts_df)


if __name__ == "__main__":
    main()