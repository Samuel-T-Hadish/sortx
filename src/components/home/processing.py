import io
import logging
import zipfile

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from agility.skeleton.custom_components import ButtonCustom, ContainerCustom
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from sortx.file_crawler import FileCrawler
from sortx.loader import get_df_from_string_content

from . import ids
from .upload import column_name_dropdown, folder_path, process_button

logger = logging.getLogger(__name__)

download_button = ButtonCustom(label="Download", hidden=True)

download_container = html.Div(
    [
        dcc.Loading(
            download_button.layout,
        ),
        dcc.Loading(dcc.Download(id=ids.DOWNLOAD_FILE)),
        dcc.Store(id=ids.DOWNLOAD_STORE, data={}),
    ]
)


def export_container():
    return html.Div(
        [
            download_container,
        ]
    )


# callbacks
def register_callbacks():

    @callback(
        [
            Output(column_name_dropdown.id, "options"),
            Output(column_name_dropdown.id, "style"),
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

    @callback(
        [Output(ids.DOWNLOAD_STORE, "data"), Output(download_button.id, "style")],
        Input(process_button.id, "n_clicks"),
        [
            State(folder_path.id, "value"),
            State(ids.UPLOAD_FILE_STORE, "data"),
            State(column_name_dropdown.id, "value"),
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

    @callback(
        Output(ids.DOWNLOAD_FILE, "data"),
        Input(download_button.id, "n_clicks"),
        State(ids.DOWNLOAD_STORE, "data"),
        prevent_initial_call=True,
    )
    # def download_file(n_clicks: int, data: dict):
    #     if not n_clicks or not data:
    #         raise PreventUpdate
    #     try:
    #         df = pd.DataFrame(data)
    #     except ValueError as e:
    #         raise PreventUpdate from e
    #     return dcc.send_data_frame(df.to_excel, "processed_data.xlsx", index=False)
    def download_file(n_clicks: int, data: dict):
        if not n_clicks or not data:
            raise PreventUpdate

        # Use BytesIO as a buffer for the Excel file
        excel_io = io.BytesIO()
        try:
            df = pd.DataFrame(data)
            # Write DataFrame to Excel on the BytesIO object
            with pd.ExcelWriter(excel_io, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)

            # Important: seek to the beginning of the stream
            excel_io.seek(0)

            # Use BytesIO for the ZIP file
            zip_io = io.BytesIO()
            with zipfile.ZipFile(
                zip_io, mode="w", compression=zipfile.ZIP_DEFLATED
            ) as zf:
                # Add the Excel file to the ZIP file
                zf.writestr("processed_data.xlsx", excel_io.getvalue())

        except ValueError as e:
            raise PreventUpdate from e

        # Important: seek to the beginning of the ZIP stream
        zip_io.seek(0)

        return dcc.send_bytes(zip_io.getvalue(), "processed_data.zip")
