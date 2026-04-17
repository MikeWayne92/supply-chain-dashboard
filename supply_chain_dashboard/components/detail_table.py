import pandas as pd

DRILL_COLS = [
    ("sku", "SKU"),
    ("product_type", "Product Type"),
    ("price", "Price ($)"),
    ("revenue", "Revenue ($)"),
    ("defect_rate", "Defect Rate (%)"),
    ("inspection_result", "Inspection"),
    ("product_lead_time", "Lead Time (days)"),
    ("shipping_cost", "Shipping Cost ($)"),
    ("mfg_cost", "Mfg Cost ($)"),
    ("supplier", "Supplier"),
    ("location", "Location"),
]


def build_drill_table(df: pd.DataFrame):
    """Return (columns, data) for a dash_table.DataTable."""
    columns = [{"name": label, "id": col_id} for col_id, label in DRILL_COLS]
    available = [c for c in [col_id for col_id, _ in DRILL_COLS] if c in df.columns]
    rows = df[available].round(2)
    data = rows.to_dict("records")
    return columns, data
