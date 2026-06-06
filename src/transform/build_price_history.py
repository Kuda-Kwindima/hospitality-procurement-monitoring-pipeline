import pandas as pd

from src.database.postgres_connection import get_postgres_engine


def extract_raw_invoices(table_name: str = "raw_invoices") -> pd.DataFrame:
    """Read raw invoice data from PostgreSQL."""
    engine = get_postgres_engine()

    query = f"SELECT * FROM {table_name}"

    df = pd.read_sql(query, engine)

    print(f"Extracted {len(df)} rows from PostgreSQL table '{table_name}'.")
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
    table_name: str = "price_history",
) -> None:
    """Load transformed price history into PostgreSQL."""
    engine = get_postgres_engine()

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {len(df)} rows into PostgreSQL table '{table_name}'.")


def main():
    raw_df = extract_raw_invoices()
    price_history_df = transform_price_history(raw_df)
    load_price_history(price_history_df)


if __name__ == "__main__":
    main()