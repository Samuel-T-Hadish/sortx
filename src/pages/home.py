""" layout.py 
This module contains the layout for the Dash application."""

import dash
import dash_bootstrap_components as dbc

from components import button, download, upload

dash.register_page(__name__, path="/")


def layout() -> (
    dbc.Container
):  # TODO: Input atttribute for file extension, other options

    return dbc.Container(
        [
            upload.render(),
            button.render(),
            download.render(),
        ]
    )
