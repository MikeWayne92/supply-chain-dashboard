import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import pandas as pd
from data import load_data, apply_filters

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "supply_chain_data.csv")


def test_load_data_returns_dataframe():
    df = load_data(CSV_PATH)
    assert isinstance(df, pd.DataFrame)


def test_load_data_row_count():
    df = load_data(CSV_PATH)
    assert len(df) == 100


def test_load_data_expected_columns():
    df = load_data(CSV_PATH)
    expected = [
        "product_type", "sku", "price", "availability", "units_sold",
        "revenue", "demographics", "stock_level", "product_lead_time",
        "order_quantity", "shipping_time", "carrier", "shipping_cost",
        "supplier", "location", "supplier_lead_time", "production_volume",
        "mfg_lead_time", "mfg_cost", "inspection_result", "defect_rate",
        "transport_mode", "routes", "transport_cost",
    ]
    for col in expected:
        assert col in df.columns, f"Missing column: {col}"


def test_numeric_columns_are_numeric():
    df = load_data(CSV_PATH)
    numeric_cols = [
        "price", "availability", "units_sold", "revenue", "stock_level",
        "product_lead_time", "order_quantity", "shipping_time", "shipping_cost",
        "supplier_lead_time", "production_volume", "mfg_lead_time",
        "mfg_cost", "defect_rate", "transport_cost",
    ]
    for col in numeric_cols:
        assert pd.api.types.is_numeric_dtype(df[col]), f"{col} is not numeric"


def test_apply_filters_product_type():
    df = load_data(CSV_PATH)
    result = apply_filters(df, product_type="skincare", location="All", supplier="All")
    assert all(result["product_type"] == "skincare")
    assert len(result) > 0


def test_apply_filters_location():
    df = load_data(CSV_PATH)
    result = apply_filters(df, product_type="All", location="Mumbai", supplier="All")
    assert all(result["location"] == "Mumbai")


def test_apply_filters_supplier():
    df = load_data(CSV_PATH)
    result = apply_filters(df, product_type="All", location="All", supplier="Supplier 1")
    assert all(result["supplier"] == "Supplier 1")


def test_apply_filters_all_returns_full_df():
    df = load_data(CSV_PATH)
    result = apply_filters(df, product_type="All", location="All", supplier="All")
    assert len(result) == len(df)


def test_apply_filters_combined():
    df = load_data(CSV_PATH)
    result = apply_filters(df, product_type="skincare", location="Mumbai", supplier="All")
    assert all(result["product_type"] == "skincare")
    assert all(result["location"] == "Mumbai")
