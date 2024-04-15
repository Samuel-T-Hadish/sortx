"""app.py: Main entry point for the application."""

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

from callbacks import excel_processing, input_validation

FONT_AWESOME = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
)

app = Dash(
    name=__name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
)
app.title = "sortX"
side_bar = dbc.Nav(
    [
        dbc.NavLink(
            [html.Div(page["name"], className="sidebar-text")],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=False,
    pills=True,
)

layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        html.H1("sortX", className="header-title"),
                    ],
                    xs=4,
                    md=4,
                    lg=4,
                    xl=4,
                ),
                dbc.Col(
                    children=[
                        side_bar,
                    ],
                    xs=8,
                    md=8,
                    lg=8,
                    xl=8,
                    style={"text-align": "right"},
                ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [dash.page_container],
        ),
    ],
    fluid=True,
)
app.layout = layout

# registering the callbacks
excel_processing.register_callbacks(app)
input_validation.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host="10.29.3.31")
