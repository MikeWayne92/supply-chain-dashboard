import pandas as pd


def load_data(path: str = "supply_chain_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df = df.rename(columns={
        "lead_times": "product_lead_time",
        "lead_time": "supplier_lead_time",
        "number_of_products_sold": "units_sold",
        "revenue_generated": "revenue",
        "customer_demographics": "demographics",
        "stock_levels": "stock_level",
        "order_quantities": "order_quantity",
        "shipping_times": "shipping_time",
        "shipping_carriers": "carrier",
        "shipping_costs": "shipping_cost",
        "supplier_name": "supplier",
        "production_volumes": "production_volume",
        "manufacturing_lead_time": "mfg_lead_time",
        "manufacturing_costs": "mfg_cost",
        "inspection_results": "inspection_result",
        "defect_rates": "defect_rate",
        "transportation_modes": "transport_mode",
        "costs": "transport_cost",
    })
    numeric_cols = [
        "price", "availability", "units_sold", "revenue", "stock_level",
        "product_lead_time", "order_quantity", "shipping_time", "shipping_cost",
        "supplier_lead_time", "production_volume", "mfg_lead_time",
        "mfg_cost", "defect_rate", "transport_cost",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def apply_filters(
    df: pd.DataFrame,
    product_type: str = "All",
    location: str = "All",
    supplier: str = "All",
) -> pd.DataFrame:
    filtered = df.copy()
    if product_type and product_type != "All":
        filtered = filtered[filtered["product_type"] == product_type]
    if location and location != "All":
        filtered = filtered[filtered["location"] == location]
    if supplier and supplier != "All":
        filtered = filtered[filtered["supplier"] == supplier]
    return filtered
