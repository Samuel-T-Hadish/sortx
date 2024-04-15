"""
src/callbacks/process_excel.py
This module contains the callbacks for the Excel processing page.
"""

import logging

import dash
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from components import ids
from sortx.file_crawler import FileCrawler
from sortx.loader import get_df_from_string_content

logger = logging.getLogger(__name__)


def register_callbacks(app: Dash):
    load_column_names_callback(app)
    run_file_crawler_callback(app)
    download_callback(app)


def load_column_names_callback(app: Dash):

    @app.callback(
        [
            Output(ids.DOC_NO_COLUMN_NAME, "options"),
            Output(ids.DOC_NO_COLUMN_NAME, "style"),
        ],
        Input(ids.UPLOAD_FILE_STORE, "data"),
        prevent_initial_call=True,
    )
    def load_column_names(uploaded_data: dict):
        if not uploaded_data:
            logger.info("No uploaded data found.")
            return ([], True)
        df = get_df_from_string_content(
            uploaded_data["content"], uploaded_data["filename"]
        )
        logger.info(df)
        options = [{"label": col, "value": col} for col in df.columns]
        style = {"display": "block"}
        return (options, style)


def run_file_crawler_callback(app: Dash):

    @app.callback(
        [Output(ids.DOWNLOAD_STORE, "data"), Output(ids.DOWNLOAD_BUTTON, "style")],
        Input(ids.PROCESS_BUTTON, "n_clicks"),
        [
            State(ids.FOLDER_PATH_TEXT, "value"),
            State(ids.UPLOAD_FILE_STORE, "data"),
            State(ids.DOC_NO_COLUMN_NAME, "value"),
        ],
        prevent_initial_call=True,
    )
    def run_file_crawler(
        _: int, folder_path: str, uploaded_data: dict, doc_no_column_name: str
    ):
        if uploaded_data:
            df = get_df_from_string_content(
                uploaded_data["content"], uploaded_data["filename"]
            )
            filecrawler = FileCrawler(
                df=df,
                folder_directory=folder_path,
                doc_no_column_name=doc_no_column_name,
            )
            filecrawler.update_folder_link()
            processed_data = filecrawler.get_output_dict()
            return processed_data, {"display": "block"}
        return dash.no_update, dash.no_update


def download_callback(app: Dash):

    @app.callback(
        Output(ids.DOWNLOAD_FILE, "data"),
        Input(ids.DOWNLOAD_BUTTON, "n_clicks"),
        State(ids.DOWNLOAD_STORE, "data"),
        prevent_initial_call=True,
    )
    def download_file(n_clicks: int, data: dict):
        if not n_clicks or not data:
            raise PreventUpdate
        try:
            df = pd.DataFrame(data)
        except ValueError as e:
            raise PreventUpdate from e
        return dcc.send_data_frame(df.to_excel, "processed_data.xlsx", index=False)
