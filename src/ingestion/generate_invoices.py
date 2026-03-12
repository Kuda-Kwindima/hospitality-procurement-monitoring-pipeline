from pathlib import Path
from datetime import timedelta
import random
import pandas as pd


def generate_supplier_product_map():
    """Return hospitality-focused supplier and product definitions."""
    return {
        "FreshFarm Produce": [
            ("Tomatoes", "Vegetables", 2.50),
            ("Onions", "Vegetables", 1.80),
            ("Lettuce", "Vegetables", 2.20),
            ("Cucumbers", "Vegetables", 2.10),
        ],
        "Desert Meat Co": [
            ("Chicken Breast", "Meat", 18.00),
            ("Beef Tenderloin", "Meat", 48.00),
            ("Lamb Chops", "Meat", 42.00),
            ("Minced Beef", "Meat", 24.00),
        ],
        "Red Sea Seafood": [
            ("Salmon Fillet", "Seafood", 55.00),
            ("Prawns", "Seafood", 38.00),
            ("Sea Bass", "Seafood", 44.00),
            ("Calamari", "Seafood", 30.00),
        ],
        "Gulf Dairy": [
            ("Milk", "Dairy", 6.50),
            ("Yogurt", "Dairy", 4.20),
            ("Cream", "Dairy", 8.50),
            ("Cheddar Cheese", "Dairy", 16.00),
        ],
        "Oasis Beverage Supply": [
            ("Sparkling Water", "Beverages", 3.00),
            ("Orange Juice", "Beverages", 5.50),
            ("Apple Juice", "Beverages", 5.20),
            ("Tonic Water", "Beverages", 4.00),
        ],
    }


def generate_weekly_dates(start_date: str, end_date: str) -> list[pd.Timestamp]:
    """Generate weekly dates between start and end date."""
    return list(pd.date_range(start=start_date, end=end_date, freq="W-MON"))


def apply_price_variation(base_price: float) -> float:
    """
    Apply small random weekly price movement.
    Most changes are small, but sometimes a bigger jump happens.
    """
    change_pct = random.uniform(-0.03, 0.08)
    new_price = base_price * (1 + change_pct)
    return round(max(new_price, 0.5), 2)


def generate_quantity(category: str) -> int:
    """Generate quantity ranges based on category."""
    quantity_ranges = {
        "Vegetables": (20, 80),
        "Meat": (10, 40),
        "Seafood": (8, 30),
        "Dairy": (15, 50),
        "Beverages": (24, 100),
    }
    low, high = quantity_ranges.get(category, (10, 50))
    return random.randint(low, high)


def build_invoice_dataset(start_date: str, end_date: str) -> pd.DataFrame:
    """Build a full synthetic invoice dataset."""
    supplier_map = generate_supplier_product_map()
    invoice_dates = generate_weekly_dates(start_date, end_date)

    records = []
    invoice_counter = 1000
    latest_prices = {}

    for supplier, products in supplier_map.items():
        for product, category, base_price in products:
            latest_prices[(supplier, product)] = base_price

    for invoice_date in invoice_dates:
        for supplier, products in supplier_map.items():
            for product, category, _ in products:
                current_price = latest_prices[(supplier, product)]
                updated_price = apply_price_variation(current_price)
                latest_prices[(supplier, product)] = updated_price

                quantity = generate_quantity(category)
                total_amount = round(quantity * updated_price, 2)

                invoice_counter += 1
                invoice_id = f"INV-{invoice_counter}"

                records.append(
                    {
                        "invoice_id": invoice_id,
                        "invoice_date": invoice_date.date(),
                        "supplier": supplier,
                        "product": product,
                        "category": category,
                        "quantity": quantity,
                        "unit_price": updated_price,
                        "total_amount": total_amount,
                    }
                )

    return pd.DataFrame(records)


def inject_data_quality_issues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Inject a few realistic data quality issues so later we can clean them.
    """
    df = df.copy()

    if len(df) > 20:
        df.loc[5, "unit_price"] = None
        df.loc[12, "supplier"] = "Fresh Farm Produce"

        duplicate_row = df.iloc[[18]].copy()
        df = pd.concat([df, duplicate_row], ignore_index=True)

    return df


def save_dataset(df: pd.DataFrame, output_path: Path) -> None:
    """Save dataset to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to: {output_path}")
    print(f"Total rows: {len(df)}")
    print("\nSample:")
    print(df.head())


if __name__ == "__main__":
    random.seed(42)

    project_root = Path(__file__).resolve().parents[2]
    output_file = project_root / "data" / "raw" / "supplier_invoices.csv"

    invoices_df = build_invoice_dataset(
        start_date="2024-01-01",
        end_date="2024-06-30",
    )

    invoices_df = inject_data_quality_issues(invoices_df)
    save_dataset(invoices_df, output_file)