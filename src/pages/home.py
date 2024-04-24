""" layout.py 
This module contains the layout for the Dash application."""

import dash
from dash import html

from components.home import processing, upload

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        upload.export_container(),
        processing.export_container(),
    ]
)

upload.register_callbacks()
processing.register_callbacks()
