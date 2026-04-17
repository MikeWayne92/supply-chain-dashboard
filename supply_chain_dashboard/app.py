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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Supply Chain Dashboard"

PRODUCT_TYPES = ["All"] + sorted(df["product_type"].unique().tolist())
LOCATIONS = ["All"] + sorted(df["location"].unique().tolist())
SUPPLIERS = ["All"] + sorted(df["supplier"].unique().tolist())

filter_bar = dbc.Row([
    dbc.Col([
        html.Label("Product Type"),
        dcc.Dropdown(id="filter-product-type", options=PRODUCT_TYPES,
                     value="All", clearable=False),
    ], width=3),
    dbc.Col([
        html.Label("Location"),
        dcc.Dropdown(id="filter-location", options=LOCATIONS,
                     value="All", clearable=False),
    ], width=3),
    dbc.Col([
        html.Label("Supplier"),
        dcc.Dropdown(id="filter-supplier", options=SUPPLIERS,
                     value="All", clearable=False),
    ], width=3),
    dbc.Col([
        html.Label("\u00a0"),
        dbc.Button("Reset Filters", id="btn-reset", color="secondary",
                   className="d-block w-100"),
    ], width=3),
], className="mb-4 mt-2 align-items-end")

app.layout = dbc.Container([
    html.H2("Supply Chain Operations Dashboard", className="mt-3 mb-1"),
    html.Hr(),
    filter_bar,
    dbc.Tabs([
        dbc.Tab(overview.layout(), label="Overview", tab_id="tab-overview"),
        dbc.Tab(supplier.layout(), label="Supplier Performance", tab_id="tab-supplier"),
        dbc.Tab(logistics.layout(), label="Logistics & Shipping", tab_id="tab-logistics"),
        dbc.Tab(inventory.layout(), label="Inventory & Demand", tab_id="tab-inventory"),
    ], id="tabs", active_tab="tab-overview"),
], fluid=True)


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
