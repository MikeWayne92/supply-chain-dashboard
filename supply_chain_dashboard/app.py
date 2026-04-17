import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

from data import load_data
import pages.overview as overview
import pages.supplier as supplier
import pages.logistics as logistics
import pages.inventory as inventory

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "supply_chain_data.csv")
df = load_data(DATA_PATH)

_FONTS_URL = "https://fonts.googleapis.com/css2?family=Fira+Code:wght@600&family=Fira+Sans:wght@400;500;700&display=swap"

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG, _FONTS_URL],
)
app.title = "Supply Chain Dashboard"

PRODUCT_TYPES = ["All"] + sorted(df["product_type"].unique().tolist())
LOCATIONS = ["All"] + sorted(df["location"].unique().tolist())
SUPPLIERS = ["All"] + sorted(df["supplier"].unique().tolist())

_LABEL_STYLE = {
    "color": "#94A3B8",
    "fontSize": "0.7rem",
    "textTransform": "uppercase",
    "letterSpacing": "0.08em",
    "fontFamily": "Fira Sans, Inter, sans-serif",
    "marginBottom": "4px",
    "display": "block",
}

_DROPDOWN_STYLE = {"fontFamily": "Fira Sans, Inter, sans-serif", "fontSize": "13px"}

filter_bar = dbc.Row([
    dbc.Col([
        html.Label("Product Type", style=_LABEL_STYLE),
        dcc.Dropdown(id="filter-product-type", options=PRODUCT_TYPES,
                     value="All", clearable=False, style=_DROPDOWN_STYLE),
    ], width=3),
    dbc.Col([
        html.Label("Location", style=_LABEL_STYLE),
        dcc.Dropdown(id="filter-location", options=LOCATIONS,
                     value="All", clearable=False, style=_DROPDOWN_STYLE),
    ], width=3),
    dbc.Col([
        html.Label("Supplier", style=_LABEL_STYLE),
        dcc.Dropdown(id="filter-supplier", options=SUPPLIERS,
                     value="All", clearable=False, style=_DROPDOWN_STYLE),
    ], width=3),
    dbc.Col([
        html.Label("\u00a0", style=_LABEL_STYLE),
        dbc.Button("Reset Filters", id="btn-reset", color="outline-primary",
                   className="d-block w-100",
                   style={"fontFamily": "Fira Sans, Inter, sans-serif", "fontSize": "13px"}),
    ], width=3),
], className="mb-4 mt-2 align-items-end",
   style={
       "backgroundColor": "#131929",
       "border": "1px solid #1E2D45",
       "borderRadius": "8px",
       "padding": "16px 12px",
   })

app.layout = dbc.Container([
    html.Div([
        html.H2(
            "Supply Chain Operations Dashboard",
            style={
                "fontFamily": "Fira Code, monospace",
                "fontWeight": "600",
                "color": "#E2E8F0",
                "letterSpacing": "-0.02em",
                "marginBottom": "2px",
            },
        ),
        html.P(
            "Real-time supply chain analytics · 100 SKUs",
            style={"color": "#3B82F6", "fontSize": "0.8rem", "fontFamily": "Fira Sans, Inter, sans-serif",
                   "letterSpacing": "0.05em", "textTransform": "uppercase", "marginBottom": "0"},
        ),
    ], className="mt-3 mb-3"),
    html.Hr(style={"borderColor": "#1E2D45", "marginBottom": "16px"}),
    filter_bar,
    dbc.Tabs([
        dbc.Tab(overview.layout(), label="Overview", tab_id="tab-overview"),
        dbc.Tab(supplier.layout(), label="Supplier Performance", tab_id="tab-supplier"),
        dbc.Tab(logistics.layout(), label="Logistics & Shipping", tab_id="tab-logistics"),
        dbc.Tab(inventory.layout(), label="Inventory & Demand", tab_id="tab-inventory"),
    ], id="tabs", active_tab="tab-overview"),
], fluid=True, style={"backgroundColor": "#0B0F1A", "minHeight": "100vh", "padding": "0 24px 24px 24px"})


@app.callback(
    Output("filter-product-type", "value"),
    Output("filter-location", "value"),
    Output("filter-supplier", "value"),
    Input("btn-reset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(_):
    return "All", "All", "All"


overview.register_callbacks(app, df)
supplier.register_callbacks(app, df)
logistics.register_callbacks(app, df)
inventory.register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)
