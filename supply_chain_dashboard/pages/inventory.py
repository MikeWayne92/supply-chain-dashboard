import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from data import apply_filters
from components.detail_table import build_drill_table


# ── Pure aggregation functions ────────────────────────────────────────────────

def compute_top_skus_stock_vs_sold(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    return df.nlargest(n, "units_sold")[["sku", "units_sold", "stock_level"]].reset_index(drop=True)


def compute_lead_time_by_supplier_location(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["supplier", "location"], as_index=False)["product_lead_time"]
        .mean()
        .round(2)
        .sort_values("product_lead_time", ascending=False)
    )


def compute_production_vs_mfg_lead_time(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("product_type", as_index=False).agg(
        production_volume=("production_volume", "mean"),
        mfg_lead_time=("mfg_lead_time", "mean"),
    ).round(2)


# ── Layout ────────────────────────────────────────────────────────────────────

def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(dcc.Graph(id="inventory-stock-sold-chart"), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="inventory-order-avail-scatter"), width=6),
            dbc.Col(dcc.Graph(id="inventory-lead-time-chart"), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="inventory-prod-mfg-chart"), width=6),
        ]),
        dbc.Row([
            dbc.Col(html.H5("SKU Detail", className="mt-3"), width=12),
            dbc.Col(dash_table.DataTable(
                id="inventory-drill-table",
                page_size=10,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "padding": "8px"},
                style_header={"fontWeight": "bold"},
            ), width=12),
        ]),
    ], fluid=True)


# ── Callbacks ─────────────────────────────────────────────────────────────────

def register_callbacks(app, df):
    @app.callback(
        Output("inventory-stock-sold-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_stock_sold(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_top_skus_stock_vs_sold(filtered)
        fig = px.bar(data, x="sku", y=["units_sold", "stock_level"],
                     title="Top 20 SKUs: Units Sold vs Stock Level",
                     labels={"value": "Units", "variable": "Metric"},
                     barmode="group")
        return fig

    @app.callback(
        Output("inventory-order-avail-scatter", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_order_avail(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        return px.scatter(filtered, x="order_quantity", y="availability",
                          color="product_type",
                          title="Order Quantity vs Availability",
                          labels={"order_quantity": "Order Quantity", "availability": "Availability (%)"},
                          hover_data=["sku"])

    @app.callback(
        Output("inventory-lead-time-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_lead_time(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_lead_time_by_supplier_location(filtered)
        data["supplier_location"] = data["supplier"] + " / " + data["location"]
        return px.bar(data, x="supplier_location", y="product_lead_time",
                      title="Avg Lead Time by Supplier & Location",
                      labels={"supplier_location": "Supplier / Location", "product_lead_time": "Avg Lead Time (days)"},
                      color="supplier")

    @app.callback(
        Output("inventory-prod-mfg-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_prod_mfg(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_production_vs_mfg_lead_time(filtered)
        return px.bar(data, x="product_type", y=["production_volume", "mfg_lead_time"],
                      title="Avg Production Volume vs Manufacturing Lead Time",
                      labels={"value": "Value", "variable": "Metric"},
                      barmode="group")

    @app.callback(
        Output("inventory-drill-table", "data"),
        Output("inventory-drill-table", "columns"),
        Input("inventory-stock-sold-chart", "clickData"),
        State("filter-product-type", "value"),
        State("filter-location", "value"),
        State("filter-supplier", "value"),
    )
    def drill_down(click_data, product_type, location, supplier):
        if not click_data:
            return [], []
        clicked_sku = click_data["points"][0]["x"]
        filtered = apply_filters(df, product_type, location, supplier)
        rows = filtered[filtered["sku"] == clicked_sku]
        columns, data = build_drill_table(rows)
        return data, columns
