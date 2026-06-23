from src.database.postgres_connection import get_postgres_engine
from pathlib import Path
import sqlite3
import pandas as pd


REQUIRED_COLUMNS = [
    "invoice_id",
    "invoice_date",
    "supplier",
    "product",
    "category",
    "quantity",
    "unit_price",
    "total_amount",
]


def get_project_paths():
    """Return key project paths."""
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "raw" / "supplier_invoices.csv"
    db_path = project_root / "db" / "procurement.db"
    return project_root, csv_path, db_path


def extract_invoices(csv_path: Path) -> pd.DataFrame:
    """Read raw invoice CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw invoice file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Extracted {len(df)} rows from raw CSV.")
    return df


def validate_schema(df: pd.DataFrame) -> None:
    """Ensure required columns exist."""
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    extra_cols = [col for col in df.columns if col not in REQUIRED_COLUMNS]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if extra_cols:
        print(f"Warning: extra columns found and kept: {extra_cols}")

    print("Schema validation passed.")


def clean_invoices(df: pd.DataFrame) -> pd.DataFrame:
    """Clean basic data quality issues."""
    cleaned = df.copy()

    # Standardize supplier names
    cleaned["supplier"] = cleaned["supplier"].replace(
        {
            "Fresh Farm Produce": "FreshFarm Produce",
        }
    )

    # Convert date column
    cleaned["invoice_date"] = pd.to_datetime(cleaned["invoice_date"], errors="coerce")

    # Convert numeric columns
    cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce")
    cleaned["unit_price"] = pd.to_numeric(cleaned["unit_price"], errors="coerce")
    cleaned["total_amount"] = pd.to_numeric(cleaned["total_amount"], errors="coerce")

    # Drop rows with critical nulls
    before_null_drop = len(cleaned)
    cleaned = cleaned.dropna(
        subset=["invoice_id", "invoice_date", "supplier", "product", "quantity", "unit_price"]
    )
    dropped_nulls = before_null_drop - len(cleaned)

    # Drop duplicate rows
    before_dedup = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    dropped_duplicates = before_dedup - len(cleaned)

    # Recalculate total_amount to ensure consistency
    cleaned["total_amount"] = (cleaned["quantity"] * cleaned["unit_price"]).round(2)

    print(f"Dropped {dropped_nulls} rows due to critical nulls.")
    print(f"Dropped {dropped_duplicates} duplicate rows.")
    print(f"Cleaned dataset has {len(cleaned)} rows.")

    return cleaned


def load_to_sqlite(df: pd.DataFrame, db_path: Path, table_name: str = "stg_supplier_invoices") -> None:
    """Load cleaned data into SQLite."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Loaded {len(df)} rows into SQLite table '{table_name}'.")
    print(f"Database saved at: {db_path}")

def load_to_postgres(
    df: pd.DataFrame,
    table_name: str = "stg_supplier_invoices"
) -> None:
    """Load cleaned data into PostgreSQL."""

    engine = get_postgres_engine()

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(
        f"Loaded {len(df)} rows into PostgreSQL table '{table_name}'."
    )

def main():
    _, csv_path, db_path = get_project_paths()

    invoices_df = extract_invoices(csv_path)
    validate_schema(invoices_df)
    cleaned_df = clean_invoices(invoices_df)
    load_to_postgres(cleaned_df)


if __name__ == "__main__":
    main()