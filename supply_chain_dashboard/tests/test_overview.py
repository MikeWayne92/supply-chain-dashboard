import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from data import load_data
from pages.overview import compute_kpis, compute_revenue_by_product, compute_revenue_by_location

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "supply_chain_data.csv")


@pytest.fixture
def df():
    return load_data(CSV_PATH)


def test_compute_kpis_returns_four_values(df):
    kpis = compute_kpis(df)
    assert "total_revenue" in kpis
    assert "avg_defect_rate" in kpis
    assert "avg_shipping_cost" in kpis
    assert "avg_lead_time" in kpis


def test_compute_kpis_total_revenue_positive(df):
    kpis = compute_kpis(df)
    assert kpis["total_revenue"] > 0


def test_compute_kpis_avg_defect_rate_between_0_and_100(df):
    kpis = compute_kpis(df)
    assert 0 <= kpis["avg_defect_rate"] <= 100


def test_compute_revenue_by_product_has_three_types(df):
    result = compute_revenue_by_product(df)
    assert set(result["product_type"]) == {"haircare", "skincare", "cosmetics"}


def test_compute_revenue_by_product_revenue_positive(df):
    result = compute_revenue_by_product(df)
    assert all(result["revenue"] > 0)


def test_compute_revenue_by_location_returns_dataframe(df):
    result = compute_revenue_by_location(df)
    assert "location" in result.columns
    assert "revenue" in result.columns
    assert len(result) > 0


def test_compute_inspection_distribution_returns_dataframe(df):
    from pages.overview import compute_inspection_distribution
    result = compute_inspection_distribution(df)
    assert "inspection_result" in result.columns
    assert "count" in result.columns
    assert set(result["inspection_result"]).issubset({"Pass", "Fail", "Pending"})
    assert all(result["count"] > 0)
