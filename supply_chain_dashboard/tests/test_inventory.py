import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from data import load_data
from pages.inventory import (
    compute_top_skus_stock_vs_sold,
    compute_lead_time_by_supplier_location,
    compute_production_vs_mfg_lead_time,
)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "supply_chain_data.csv")


@pytest.fixture
def df():
    return load_data(CSV_PATH)


def test_compute_top_skus_returns_at_most_20(df):
    result = compute_top_skus_stock_vs_sold(df, n=20)
    assert len(result) <= 20


def test_compute_top_skus_sorted_by_units_sold(df):
    result = compute_top_skus_stock_vs_sold(df, n=20)
    assert list(result["units_sold"]) == sorted(result["units_sold"], reverse=True)


def test_compute_lead_time_by_supplier_location_has_columns(df):
    result = compute_lead_time_by_supplier_location(df)
    assert "supplier" in result.columns
    assert "location" in result.columns
    assert "product_lead_time" in result.columns


def test_compute_lead_time_by_supplier_location_times_positive(df):
    result = compute_lead_time_by_supplier_location(df)
    assert all(result["product_lead_time"] > 0)


def test_compute_production_vs_mfg_lead_time_has_columns(df):
    result = compute_production_vs_mfg_lead_time(df)
    assert "product_type" in result.columns
    assert "production_volume" in result.columns
    assert "mfg_lead_time" in result.columns
