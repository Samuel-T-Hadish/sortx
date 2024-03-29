""" This module contains the upload component."""

from typing import Dict

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

from . import ids


def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.UPLOAD_FILE_STORE, "data"),
        Input(ids.UPLOAD_FILE, "contents"),
        State(ids.UPLOAD_FILE, "filename"),
    )
    def store_uploaded_file(contents: str, filename: str) -> Dict[str, str]:

        if contents is not None:
            children = {
                "content": contents,
                "filename": filename,
            }
            return children
        return {}

    return html.Div(
        [
            html.H4("Upload the excel file which contains the document number"),
            dcc.Upload(
                id=ids.UPLOAD_FILE,
                children=[
                    html.Div(children=["Drag and Drop or ", html.A("Select Files")]),
                    html.Div(id=ids.UPLOAD_FEEDBACK),
                ],
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                multiple=False,
            ),
            dcc.Store(id=ids.UPLOAD_FILE_STORE, data={}),
            dcc.Textarea(
                id=ids.FOLDER_PATH_TEXT,
                placeholder="Please enter the top level folder path",
                className="form-control mt-3 mb-3",
            ),
        ]
    )
