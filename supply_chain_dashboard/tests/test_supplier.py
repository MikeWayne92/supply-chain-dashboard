import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from data import load_data
from pages.supplier import (
    compute_defect_by_supplier,
    compute_mfg_cost_by_supplier,
    compute_inspection_by_supplier,
)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "supply_chain_data.csv")


@pytest.fixture
def df():
    return load_data(CSV_PATH)


def test_compute_defect_by_supplier_has_all_suppliers(df):
    result = compute_defect_by_supplier(df)
    assert set(result["supplier"]) == {"Supplier 1", "Supplier 2", "Supplier 3", "Supplier 4", "Supplier 5"}


def test_compute_defect_by_supplier_defect_rate_non_negative(df):
    result = compute_defect_by_supplier(df)
    assert all(result["defect_rate"] >= 0)


def test_compute_mfg_cost_by_supplier_returns_dataframe(df):
    result = compute_mfg_cost_by_supplier(df)
    assert "supplier" in result.columns
    assert "mfg_cost" in result.columns


def test_compute_mfg_cost_by_supplier_costs_positive(df):
    result = compute_mfg_cost_by_supplier(df)
    assert all(result["mfg_cost"] > 0)


def test_compute_inspection_by_supplier_has_three_statuses(df):
    result = compute_inspection_by_supplier(df)
    assert set(result["inspection_result"]).issubset({"Pass", "Fail", "Pending"})


def test_compute_inspection_by_supplier_count_positive(df):
    result = compute_inspection_by_supplier(df)
    assert all(result["count"] > 0)
