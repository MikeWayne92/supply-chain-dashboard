import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from data import apply_filters
from components.detail_table import build_drill_table
from theme import CHART_LAYOUT, COLORS, INSPECTION_COLORS, TABLE_STYLE


# ── Pure aggregation functions ────────────────────────────────────────────────

def compute_defect_by_supplier(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("supplier", as_index=False)["defect_rate"].mean().round(2)


def compute_mfg_cost_by_supplier(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("supplier", as_index=False)["mfg_cost"].mean().round(2)


def compute_inspection_by_supplier(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["supplier", "inspection_result"], as_index=False).size().rename(columns={"size": "count"})


# ── Layout ────────────────────────────────────────────────────────────────────

def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(dcc.Graph(id="supplier-defect-chart"), width=6),
            dbc.Col(dcc.Graph(id="supplier-mfg-cost-chart"), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="supplier-inspection-chart"), width=6),
            dbc.Col(dcc.Graph(id="supplier-scatter-chart"), width=6),
        ]),
        dbc.Row([
            dbc.Col(html.H5("SKU Detail", className="mt-3",
                            style={"color": "#E2E8F0", "fontFamily": "Fira Sans, Inter, sans-serif",
                                   "fontWeight": "700", "fontSize": "0.85rem",
                                   "textTransform": "uppercase", "letterSpacing": "0.08em"}), width=12),
            dbc.Col(dash_table.DataTable(
                id="supplier-drill-table",
                page_size=10,
                **TABLE_STYLE,
            ), width=12),
        ]),
    ], fluid=True)


# ── Callbacks ─────────────────────────────────────────────────────────────────

def register_callbacks(app, df):
    @app.callback(
        Output("supplier-defect-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_defect_chart(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_defect_by_supplier(filtered)
        fig = px.bar(data, x="supplier", y="defect_rate",
                     title="Avg Defect Rate by Supplier",
                     labels={"supplier": "Supplier", "defect_rate": "Avg Defect Rate (%)"},
                     color="supplier", color_discrete_sequence=COLORS)
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("supplier-mfg-cost-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_mfg_cost_chart(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_mfg_cost_by_supplier(filtered)
        fig = px.bar(data, x="supplier", y="mfg_cost",
                     title="Avg Manufacturing Cost by Supplier",
                     labels={"supplier": "Supplier", "mfg_cost": "Avg Mfg Cost ($)"},
                     color="supplier", color_discrete_sequence=COLORS)
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("supplier-inspection-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_inspection_chart(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        data = compute_inspection_by_supplier(filtered)
        fig = px.bar(data, x="supplier", y="count", color="inspection_result",
                     title="Inspection Results by Supplier",
                     labels={"supplier": "Supplier", "count": "Count"},
                     barmode="group",
                     color_discrete_map=INSPECTION_COLORS)
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("supplier-scatter-chart", "figure"),
        Input("filter-product-type", "value"),
        Input("filter-location", "value"),
        Input("filter-supplier", "value"),
    )
    def update_scatter_chart(product_type, location, supplier):
        filtered = apply_filters(df, product_type, location, supplier)
        fig = px.scatter(filtered, x="mfg_cost", y="defect_rate",
                         size="production_volume", color="supplier",
                         title="Manufacturing Cost vs. Defect Rate",
                         labels={"mfg_cost": "Mfg Cost ($)", "defect_rate": "Defect Rate (%)"},
                         color_discrete_sequence=COLORS,
                         hover_data=["sku"])
        fig.update_layout(**CHART_LAYOUT)
        return fig

    @app.callback(
        Output("supplier-drill-table", "data"),
        Output("supplier-drill-table", "columns"),
        Input("supplier-defect-chart", "clickData"),
        State("filter-product-type", "value"),
        State("filter-location", "value"),
        State("filter-supplier", "value"),
    )
    def drill_down(click_data, product_type, location, supplier):
        if not click_data:
            return [], []
        clicked = click_data["points"][0]["x"]
        filtered = apply_filters(df, product_type, location, supplier)
        rows = filtered[filtered["supplier"] == clicked]
        columns, data = build_drill_table(rows)
        return data, columns
