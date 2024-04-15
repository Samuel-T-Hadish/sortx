"""
src/callbacks/input_validation.py
This module contains the input validation callbacks.
"""

import logging
from pathlib import Path

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

from components import ids


def register_callbacks(app: Dash):
    upload_callback(app)
    validate_folder_path_callback(app)


def upload_callback(app: Dash):

    @app.callback(
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


def validate_folder_path_callback(app: Dash):

    @app.callback(
        Output(ids.FOLDER_PATH_FEEDBACK, "children"),
        Output(ids.PROCESS_BUTTON, "style"),
        Input(ids.FOLDER_PATH_TEXT, "value"),
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
