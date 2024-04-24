""" This module contains the upload component."""

from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from agility.skeleton.custom_components import (
    ButtonCustom,
    ContainerCustom,
    DropdownCustom,
    InputCustom,
)
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

from . import ids

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

folder_path = InputCustom(
    label="Folder Path",
    help_text="Please enter the top level folder path",
)

process_button = ButtonCustom(
    label="Update Data Table",
    hidden=True,
)


process_button_container = html.Div(
    [
        process_button.layout,
        dcc.Loading(
            id=ids.PROCESS_BUTTON_LOADING,
            children=[html.H4(id=ids.PROCESS_BUTTON_INFO)],
            type="default",
        ),
    ]
)

column_name_dropdown = DropdownCustom(
    options=["will be loaded after file upload"],
    label="Document Number Column Name",
    help_text="Please select the document number column name",
)


def export_container():

    return html.Div(
        [
            upload_component,
            html.Div(
                children=html.H6("No file uploaded yet."),
                id=ids.UPLOAD_FEEDBACK,
            ),
            folder_path.layout,
            dcc.Store(id=ids.UPLOAD_FILE_STORE, data={}),
            dcc.Loading(
                [column_name_dropdown.layout],
            ),
            process_button.layout,
        ]
    )


def register_callbacks():

    @callback(
        [
            Output(ids.UPLOAD_FILE_STORE, "data"),
            Output(ids.UPLOAD_FEEDBACK, "children"),
            Output(ids.UPLOAD_FILE, "style"),
        ],
        Input(ids.UPLOAD_FILE, "contents"),
        State(ids.UPLOAD_FILE, "filename"),
        prevent_initial_call=True,
    )
    def store_uploaded_file(contents: str, filename: str):

        if contents:
            uploaded_data = {
                "content": contents,
                "filename": filename,
            }
            feedback_message = html.Div(f"File {filename} has been uploaded.")
            style = {"display": "none"}
            return (uploaded_data, feedback_message, style)

        return (dash.no_update, dash.no_update, dash.no_update)

    @callback(
        Output(folder_path.help_text_id, "children"),
        Output(process_button.id, "style"),
        Input(folder_path.id, "value"),
        prevent_initial_call=True,
    )
    def validate_folder_path(folder_path: str):
        if not folder_path:
            return html.Div(["Please enter the top level folder path", html.Span()]), {
                "display": "none"
            }
        if not Path(folder_path).is_dir():
            return html.Div(
                [
                    "The folder path does not exist.",
                    html.I(
                        className="fa-solid fa-times",
                        style={"color": "red", "marginLeft": "8px"},
                    ),
                ]
            ), {"display": "none"}
        if not list(Path(folder_path).rglob("*")):
            return html.Div(
                [
                    "The folder is empty.",
                    html.I(
                        className="fa-solid fa-times",
                        style={"color": "red", "marginLeft": "8px"},
                    ),
                ]
            ), {"display": "none"}
        return html.Div(
            [
                "The folder path is valid.",
                html.I(
                    className="fa-solid fa-check",
                    style={"color": "green", "marginLeft": "8px"},
                ),
            ]
        ), {"display": "block"}
