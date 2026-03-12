import pandas as pd
from src.transform.build_price_history import transform_price_history


def test_transform_price_history_creates_expected_columns():
    sample_data = pd.DataFrame(
        {
            "invoice_id": ["INV-1", "INV-2"],
            "invoice_date": ["2024-01-01", "2024-01-08"],
            "supplier": ["FreshFarm Produce", "FreshFarm Produce"],
            "product": ["Tomatoes", "Tomatoes"],
            "category": ["Vegetables", "Vegetables"],
            "quantity": [20, 20],
            "unit_price": [2.50, 2.75],
            "total_amount": [50.00, 55.00],
        }
    )

    result = transform_price_history(sample_data)

    assert "previous_price" in result.columns
    assert "price_change" in result.columns
    assert "pct_change" in result.columns
    assert pd.isna(result.loc[0, "previous_price"])
    assert result.loc[1, "previous_price"] == 2.50
    assert result.loc[1, "price_change"] == 0.25
    assert result.loc[1, "pct_change"] == 10.0