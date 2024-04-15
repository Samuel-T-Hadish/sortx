""" download.py"""

from dash import dcc, html
import dash_bootstrap_components as dbc

from . import ids


def render():
    return html.Div(
        [
            dcc.Loading(
                dbc.Button(
                    id=ids.DOWNLOAD_BUTTON,
                    children="Download",
                    className="fa fa-download mr-1",
                    style={"display": "none"},
                    color="success",
                )
            ),
            dcc.Loading(dcc.Download(id=ids.DOWNLOAD_FILE)),
            dcc.Store(id=ids.DOWNLOAD_STORE, data={}),
        ]
    )
