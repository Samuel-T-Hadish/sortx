""" download.py"""

import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from . import ids


def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.DOWNLOAD_FILE, "data"),
        Input(ids.DOWNLOAD_BUTTON, "n_clicks"),
        State(ids.DOWNLOAD_STORE, "data"),
        prevent_initial_call=True,
    )
    def download_file(n_clicks: int, data: dict):
        if not n_clicks or not data:
            print(f"data:{data}")
            print("PreventUpdate")
            raise PreventUpdate
        try:
            df = pd.DataFrame(data)
        except ValueError as e:
            raise PreventUpdate from e
        return dcc.send_data_frame(df.to_csv, "data.csv", index=False)

    return html.Div(
        [
            html.Button(id=ids.DOWNLOAD_BUTTON, children="Download", n_clicks=0,className = "btn btn-success"),
            dcc.Download(id=ids.DOWNLOAD_FILE),
            dcc.Store(id=ids.DOWNLOAD_STORE, data={}),
        ]
    )
