import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from data import apply_filters
from components.detail_table import build_drill_table
from theme import CHART_LAYOUT, COLORS, TABLE_STYLE


# ── Pure aggregation functions ────────────────────────────────────────────────

def compute_shipping_cost_by_carrier(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("carrier", as_index=False)["shipping_cost"].mean().round(2)


def compute_transport_cost_by_mode(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("transport_mode", as_index=False)["transport_cost"].mean().round(2)


def compute_shipping_time_by_route(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("routes", as_index=False)["shipping_time"].mean().round(2)


# ── Layout ────────────────────────────────────────────────────────────────────

def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(dcc.Graph(id="logistics-carrier-cost-chart"), width=6),
            dbc.Col(dcc.Graph(id="logistics-transport-cost-chart"), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="logistics-route-time-chart"), width=6),
            dbc.Col(dcc.Graph(id="logistics-scatter-chart"), width=6),
        ]),
        dbc.Row([
            dbc.Col(html.H5("SKU Detail", className="mt-3",
                            style={"color": "#E2E8F0", "fontFamily": "Fira Sans, Inter, sans-serif",
                                   "fontWeight": "700", "fontSize": "0.85rem",
                                   "textTransform": "uppercase", "letterSpacing": "0.08em"}), width=12),
            dbc.Col(dash_table.DataTable(
                id="logistics-drill-table",
                page_size=10,
                **TABLE_STYLE,
            ), width=12),
        ]),
    ], fluid=True)


# ── Callbacks ─────────────────────────────────────────────────────────────────

def register_callbacks(app, df):
    @app.callback(
        Output("logistics-carrier-cost-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_carrier_cost(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_shipping_cost_by_carrier(filtered)
        fig = px.bar(data, x="carrier", y="shipping_cost",
                     title="Avg Shipping Cost by Carrier",
                     labels={"carrier": "Carrier", "shipping_cost": "Avg Shipping Cost ($)"},
                     color="carrier", color_discrete_sequence=COLORS)
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("logistics-transport-cost-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_transport_cost(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_transport_cost_by_mode(filtered)
        fig = px.bar(data, x="transport_mode", y="transport_cost",
                     title="Avg Transport Cost by Mode",
                     labels={"transport_mode": "Mode", "transport_cost": "Avg Cost ($)"},
                     color="transport_mode", color_discrete_sequence=COLORS)
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("logistics-route-time-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_route_time(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_shipping_time_by_route(filtered)
        fig = px.bar(data, x="routes", y="shipping_time",
                     title="Avg Shipping Time by Route",
                     labels={"routes": "Route", "shipping_time": "Avg Shipping Time (days)"},
                     color="routes", color_discrete_sequence=COLORS)
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("logistics-scatter-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_scatter(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        fig = px.scatter(filtered, x="shipping_cost", y="shipping_time",
                         color="transport_mode",
                         title="Shipping Cost vs. Shipping Time by Transport Mode",
                         labels={"shipping_cost": "Shipping Cost ($)", "shipping_time": "Shipping Time (days)"},
                         color_discrete_sequence=COLORS,
                         hover_data=["sku", "carrier"])
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("logistics-drill-table", "data"),
        Output("logistics-drill-table", "columns"),
        Input("logistics-carrier-cost-chart", "clickData"),
        State("filter-product-type", "value"),
        State("filter-location", "value"),
        State("filter-supplier", "value"),
    )
    def drill_down(click_data, product_type, location, supplier):
        if not click_data:
            return [], []
        clicked = click_data["points"][0]["x"]
        filtered = apply_filters(df, product_type, location, supplier)
        rows = filtered[filtered["carrier"] == clicked]
        columns, data = build_drill_table(rows)
        return data, columns
