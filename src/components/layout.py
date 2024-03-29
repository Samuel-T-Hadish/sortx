""" layout.py 
This module contains the layout for the Dash application."""

from dash import Dash, html

from src.components import button, dataframe, download, upload


def create_layout(app: Dash) -> html.Div:
    """
    Creates the layout for the Dash application.

    Args:
        app (Dash): The Dash application object.

    Returns:
        html.Div: The layout of the Dash application.
    """
    return html.Div(
        [
            html.H1(app.title),
            html.Hr(),
            upload.render(app),
            dataframe.render(app),
            button.render(app),
            download.render(app),
        ]
    )
