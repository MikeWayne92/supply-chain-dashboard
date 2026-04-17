import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from data import load_data
from pages.logistics import (
    compute_shipping_cost_by_carrier,
    compute_transport_cost_by_mode,
    compute_shipping_time_by_route,
)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "supply_chain_data.csv")


@pytest.fixture
def df():
    return load_data(CSV_PATH)


def test_compute_shipping_cost_by_carrier_has_three_carriers(df):
    result = compute_shipping_cost_by_carrier(df)
    assert set(result["carrier"]) == {"Carrier A", "Carrier B", "Carrier C"}


def test_compute_shipping_cost_by_carrier_costs_positive(df):
    result = compute_shipping_cost_by_carrier(df)
    assert all(result["shipping_cost"] > 0)


def test_compute_transport_cost_by_mode_has_all_modes(df):
    result = compute_transport_cost_by_mode(df)
    assert set(result["transport_mode"]) == {"Road", "Air", "Rail", "Sea"}


def test_compute_transport_cost_by_mode_costs_positive(df):
    result = compute_transport_cost_by_mode(df)
    assert all(result["transport_cost"] > 0)


def test_compute_shipping_time_by_route_has_three_routes(df):
    result = compute_shipping_time_by_route(df)
    assert set(result["routes"]) == {"Route A", "Route B", "Route C"}


def test_compute_shipping_time_by_route_times_positive(df):
    result = compute_shipping_time_by_route(df)
    assert all(result["shipping_time"] > 0)
