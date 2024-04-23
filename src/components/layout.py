import dash
from dash import html
import dash_bootstrap_components as dbc
from .sidebar import create_sidebar


def create_layout():
    return dbc.Container(
        children=[
            dbc.Row(
                [
                    dbc.Col(html.H1("sortX", className="header-title"), width=4),
                    dbc.Col(create_sidebar(), width=8, style={"text-align": "right"}),
                ]
            ),
            html.Hr(),
            dbc.Row([dash.page_container]),
        ],
        fluid=True,
    )
