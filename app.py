"""app.py: Main entry point for the application."""

import dash_bootstrap_components as dbc
from dash import Dash

from src.components.layout import create_layout

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "sortX"
app.layout = dbc.Container(create_layout(app))

if __name__ == "__main__":
    app.run(debug=True, port="80")
