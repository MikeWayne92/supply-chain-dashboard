COLORS = ["#3B82F6", "#D97706", "#10B981", "#8B5CF6", "#F43F5E", "#06B6D4"]

INSPECTION_COLORS = {"Pass": "#10B981", "Fail": "#F43F5E", "Pending": "#D97706"}

_BG = "#0B0F1A"
_PAPER = "#131929"
_GRID = "#1E2D45"
_FONT = "#E2E8F0"

CHART_LAYOUT = dict(
    paper_bgcolor=_PAPER,
    plot_bgcolor=_BG,
    font=dict(color=_FONT, family="Fira Sans, Inter, sans-serif", size=12),
    xaxis=dict(gridcolor=_GRID, linecolor=_GRID, zerolinecolor=_GRID),
    yaxis=dict(gridcolor=_GRID, linecolor=_GRID, zerolinecolor=_GRID),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=_FONT)),
    margin=dict(t=50, b=40, l=50, r=20),
    title=dict(font=dict(size=14, color=_FONT)),
    colorway=COLORS,
)

TABLE_STYLE = dict(
    style_table={"overflowX": "auto", "backgroundColor": _PAPER, "borderRadius": "6px"},
    style_cell={
        "textAlign": "left",
        "padding": "10px 12px",
        "backgroundColor": _PAPER,
        "color": _FONT,
        "border": f"1px solid {_GRID}",
        "fontFamily": "Fira Sans, Inter, sans-serif",
        "fontSize": "13px",
    },
    style_header={
        "fontWeight": "700",
        "backgroundColor": "#1E2D45",
        "color": "#3B82F6",
        "border": f"1px solid {_GRID}",
        "letterSpacing": "0.05em",
        "textTransform": "uppercase",
        "fontSize": "11px",
    },
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "#0F1824"},
    ],
)

KPI_CARD_STYLE = {
    "backgroundColor": _PAPER,
    "border": "1px solid #1E2D45",
    "borderLeft": "4px solid #3B82F6",
    "borderRadius": "8px",
    "boxShadow": "0 4px 20px rgba(59,130,246,0.1)",
}

KPI_VALUE_STYLE = {
    "color": "#3B82F6",
    "fontFamily": "Fira Code, monospace",
    "fontWeight": "700",
    "fontSize": "1.5rem",
    "marginBottom": "0",
}

KPI_LABEL_STYLE = {
    "color": "#94A3B8",
    "fontFamily": "Fira Sans, Inter, sans-serif",
    "fontSize": "0.75rem",
    "textTransform": "uppercase",
    "letterSpacing": "0.08em",
    "marginBottom": "4px",
}
