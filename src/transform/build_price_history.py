from pathlib import Path
import sqlite3
import pandas as pd


def get_db_path() -> Path:
    """Return the SQLite database path."""
    project_root = Path(__file__).resolve().parents[2]
    return project_root / "db" / "procurement.db"


def extract_raw_invoices(db_path: Path, table_name: str = "raw_invoices") -> pd.DataFrame:
    """Read raw invoice data from SQLite."""
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    query = f"SELECT * FROM {table_name}"

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(query, conn)

    print(f"Extracted {len(df)} rows from '{table_name}'.")
    return df


def transform_price_history(df: pd.DataFrame) -> pd.DataFrame:
    """Build price history table with prior price and price change metrics."""
    transformed = df.copy()

    transformed["invoice_date"] = pd.to_datetime(transformed["invoice_date"])

    transformed = transformed.sort_values(
        by=["supplier", "product", "invoice_date"]
    ).reset_index(drop=True)

    transformed["previous_price"] = (
        transformed.groupby(["supplier", "product"])["unit_price"].shift(1)
    )

    transformed["price_change"] = (
        transformed["unit_price"] - transformed["previous_price"]
    ).round(2)

    transformed["pct_change"] = (
        (transformed["price_change"] / transformed["previous_price"]) * 100
    ).round(2)

    print("Price history transformation complete.")
    return transformed


def load_price_history(
    df: pd.DataFrame,
    db_path: Path,
    table_name: str = "price_history",
) -> None:
    """Load transformed price history into SQLite."""
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Loaded {len(df)} rows into SQLite table '{table_name}'.")


def main():
    db_path = get_db_path()
    raw_df = extract_raw_invoices(db_path)
    price_history_df = transform_price_history(raw_df)
    load_price_history(price_history_df, db_path)


if __name__ == "__main__":
    main()