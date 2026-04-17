import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, dash_table
from data import apply_filters
from components.detail_table import build_drill_table
from theme import CHART_LAYOUT, COLORS, INSPECTION_COLORS, KPI_CARD_STYLE, KPI_VALUE_STYLE, KPI_LABEL_STYLE


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

def _kpi_card(label, kpi_id, accent="#3B82F6"):
    style = {**KPI_CARD_STYLE, "borderLeftColor": accent}
    return dbc.Card(
        dbc.CardBody([
            html.P(label, style=KPI_LABEL_STYLE),
            html.H4(id=kpi_id, style={**KPI_VALUE_STYLE, "color": accent}),
        ], style={"padding": "16px 20px"}),
        style=style,
    )


def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(_kpi_card("Total Revenue", "kpi-revenue", "#3B82F6"), width=3),
            dbc.Col(_kpi_card("Avg Defect Rate (%)", "kpi-defect", "#F43F5E"), width=3),
            dbc.Col(_kpi_card("Avg Shipping Cost ($)", "kpi-shipping", "#D97706"), width=3),
            dbc.Col(_kpi_card("Avg Lead Time (days)", "kpi-lead", "#10B981"), width=3),
        ], className="mb-4 mt-2"),
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
        fig = px.bar(data, x="product_type", y="revenue",
                     title="Revenue by Product Type",
                     labels={"product_type": "Product Type", "revenue": "Revenue ($)"},
                     color="product_type", color_discrete_sequence=COLORS)
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("overview-revenue-location", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_revenue_location(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_revenue_by_location(filtered)
        fig = px.bar(data, x="location", y="revenue",
                     title="Revenue by City",
                     labels={"location": "City", "revenue": "Revenue ($)"},
                     color="location", color_discrete_sequence=COLORS)
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("overview-inspection-pie", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_inspection_pie(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_inspection_distribution(filtered)
        fig = px.pie(data, names="inspection_result", values="count",
                     title="Inspection Result Distribution",
                     color="inspection_result",
                     color_discrete_map=INSPECTION_COLORS)
        fig.update_layout(**CHART_LAYOUT)
        fig.update_traces(textfont_color="#E2E8F0")
        return fig
