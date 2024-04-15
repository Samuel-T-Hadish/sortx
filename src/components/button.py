"""button.py"""

from dash import dcc, html
import dash_bootstrap_components as dbc

from . import ids


def render() -> html.Div:
    return html.Div(
        [
            dbc.Button(
                id=ids.PROCESS_BUTTON,
                children=[html.I(className="fa-solid fa-pen mr-5"), " Update Data Table"],
                color="success",
                className="mt-1",
                style={"display": "none"},
            ),
            dcc.Loading(
                id=ids.PROCESS_BUTTON_LOADING,
                children=[html.H4(id=ids.PROCESS_BUTTON_INFO)],
                type="default",
            ),
        ]
    )
