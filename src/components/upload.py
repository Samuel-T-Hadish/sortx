""" This module contains the upload component."""

import dash_bootstrap_components as dbc
from dash import dcc, html

from . import ids


def render():
    upload_component = html.Div(
        id=ids.UPLOAD_CONTAINER,
        children=[
            html.H5("Upload a file"),
            dcc.Upload(
                id=ids.UPLOAD_FILE,
                children=[
                    html.Div(children=["Drag and Drop or ", html.A("Select Files")]),
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
        ],
    )

    folder_path_text_component = dbc.Container(
        id=ids.FOLDER_PATH_CONTAINER,
        children=[
            html.H5("Enter the top level folder path"),
            dcc.Input(
                id=ids.FOLDER_PATH_TEXT,
                placeholder="Please enter the top level folder path",
                className="form-control mt-3 mb-3",
            ),
            html.Div(id=ids.FOLDER_PATH_FEEDBACK,children=""),
        ],
    )

    return html.Div(
        [
            upload_component,
            html.Div(
                children=html.H6("No file uploaded yet."),
                id=ids.UPLOAD_FEEDBACK,
            ),
            folder_path_text_component,
            dcc.Store(id=ids.UPLOAD_FILE_STORE, data={}),
            dcc.Loading(
                dcc.Dropdown(
                    id=ids.DOC_NO_COLUMN_NAME,
                    placeholder="Please select the document number column name",
                    className="form-control mt-3 mb-3",
                    style={"display": "none"},
                )
            ),
        ]
    )
