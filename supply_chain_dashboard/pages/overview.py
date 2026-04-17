import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, dash_table
from data import apply_filters
from components.detail_table import build_drill_table


# ── Pure aggregation functions (testable) ────────────────────────────────────

def compute_kpis(df: pd.DataFrame) -> dict:
    return {
        "total_revenue": round(df["revenue"].sum(), 2),
        "avg_defect_rate": round(df["defect_rate"].mean(), 2),
        "avg_shipping_cost": round(df["shipping_cost"].mean(), 2),
        "avg_lead_time": round(df["product_lead_time"].mean(), 2),
    }


def compute_revenue_by_product(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("product_type", as_index=False)["revenue"].sum()


def compute_revenue_by_location(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("location", as_index=False)["revenue"].sum()


def compute_inspection_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return df["inspection_result"].value_counts().reset_index()


# ── Layout ────────────────────────────────────────────────────────────────────

def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([html.H6("Total Revenue"), html.H4(id="kpi-revenue")])]), width=3),
            dbc.Col(dbc.Card([dbc.CardBody([html.H6("Avg Defect Rate (%)"), html.H4(id="kpi-defect")])]), width=3),
            dbc.Col(dbc.Card([dbc.CardBody([html.H6("Avg Shipping Cost ($)"), html.H4(id="kpi-shipping")])]), width=3),
            dbc.Col(dbc.Card([dbc.CardBody([html.H6("Avg Lead Time (days)"), html.H4(id="kpi-lead")])]), width=3),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="overview-revenue-product"), width=6),
            dbc.Col(dcc.Graph(id="overview-revenue-location"), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="overview-inspection-pie"), width=6),
        ]),
    ], fluid=True)


# ── Callbacks ─────────────────────────────────────────────────────────────────

def register_callbacks(app, df):
    @app.callback(
        Output("kpi-revenue", "children"),
        Output("kpi-defect", "children"),
        Output("kpi-shipping", "children"),
        Output("kpi-lead", "children"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_kpis(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        kpis = compute_kpis(filtered)
        return (
            f"${kpis['total_revenue']:,.0f}",
            f"{kpis['avg_defect_rate']:.2f}%",
            f"${kpis['avg_shipping_cost']:.2f}",
            f"{kpis['avg_lead_time']:.1f} days",
        )

    @app.callback(
        Output("overview-revenue-product", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_revenue_product(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_revenue_by_product(filtered)
        return px.bar(data, x="product_type", y="revenue",
                      title="Revenue by Product Type",
                      labels={"product_type": "Product Type", "revenue": "Revenue ($)"},
                      color="product_type")

    @app.callback(
        Output("overview-revenue-location", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_revenue_location(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_revenue_by_location(filtered)
        return px.bar(data, x="location", y="revenue",
                      title="Revenue by City",
                      labels={"location": "City", "revenue": "Revenue ($)"},
                      color="location")

    @app.callback(
        Output("overview-inspection-pie", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_inspection_pie(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_inspection_distribution(filtered)
        return px.pie(data, names="inspection_result", values="count",
                      title="Inspection Result Distribution",
                      color="inspection_result",
                      color_discrete_map={"Pass": "#2ecc71", "Fail": "#e74c3c", "Pending": "#f39c12"})
