"""pages/sx-needlist.py"""

import os
import traceback
from typing import Final

import dash
from agility.components import (
    ButtonCustom,
    DropdownCustom,
    InputCustom,
    MessageCustom,
    RadioItems,
)
from agility.utils.pydantic import process_pydantic_errors
from dash import Dash, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
from pydantic import ValidationError

from sortx.config.main import STORE_ID
from sortx.project import needlist
from sortx.schemas.needlist import NeedlistInput, PathInput

dash.register_page(
    __name__,
    title="SortX - Needlist Updation",
    description="Update needlist with folder links",
)
app: Dash = dash.get_app()


PAGE_TITLE = "Needlist Updation"


class PageIDs:
    filename = os.path.basename(__file__)
    prefix: Final[str] = filename.replace(".py", "")
    STATUS: Final[str] = f"{prefix}_status"
    INPUT_LAYOUT: Final[str] = f"{prefix}_input_layout"
    PATH_INPUT_CONTAINER: Final[str] = f"{prefix}_path_input_container"
    EXCEL_INFO_CONTAINER: Final[str] = f"{prefix}_excel_info_container"
    COLUMN_DROPDOWN_CONTAINER: Final[str] = f"{prefix}_column_dropdown_container"
    SAVE_CONTAINER: Final[str] = f"{prefix}_save_container"
    GENERATE_COLUMN_BTN: Final[str] = f"{prefix}_generate_column_btn"
    SEARCH_LEVEL: Final[str] = f"{prefix}_search_level"
    SAVE_BTN: Final[str] = f"{prefix}_save_btn"
    FEEDBACK_SAVE: Final[str] = f"{prefix}_feedback_save"
    RUN_BTN: Final[str] = f"{prefix}_run_btn"
    RUN_CONTAINER: Final[str] = f"{prefix}_run_container"
    FEEDBACK_RUN: Final[str] = f"{prefix}_feedback_run"
    OUTPUT: Final[str] = f"{prefix}_output"
    NEEDLIST_PATH: Final[str] = "needlist-path"
    FOLDER_PATH: Final[str] = "folder-path"
    COLUMN_NAME_DROPDOWN: Final[str] = "column-name-dropdown"
    SHEET_NAME: Final[str] = "sheet-name"
    HEADER: Final[str] = "header"


ids = PageIDs()

layout = html.Div(
    [
        html.H1(
            "SortX",
            className="app-title",
        ),
        html.H2(
            PAGE_TITLE,
            className="page-title",
        ),
        html.Hr(),
        html.Div(id=ids.STATUS),
        html.Div(id=ids.INPUT_LAYOUT),
        html.Div(id=ids.SAVE_CONTAINER),
        html.Div(id=ids.FEEDBACK_SAVE),
        html.Div(id=ids.RUN_CONTAINER),
        dcc.Loading(html.Div(id=ids.FEEDBACK_RUN)),
        dcc.Loading(html.Div(id=ids.OUTPUT)),
    ],
    className="w-full px-10",
)


@app.callback(
    Output(ids.STATUS, "children"),
    [Input(STORE_ID, "data")],
)
def load_status(data):

    if data is None:
        return MessageCustom(
            messages="Project not loaded. Go to start page and create new or open existing project.",
            success=False,
        ).layout
    return dash.no_update


# callback function to display the input fields and save btn if project is loaded
@app.callback(
    Output(ids.INPUT_LAYOUT, "children"),
    Output(ids.SAVE_CONTAINER, "children"),
    [Input(STORE_ID, "data")],
)
def display_input(data):

    if data is None:
        raise PreventUpdate

    needlist_input = data.get("needlist_input", {})
    needlist_input, errors = needlist.validate_input(needlist_input)
    print(errors)

    path_container = html.Div(
        [
            InputCustom(
                id=ids.NEEDLIST_PATH,
                label="Needlist Path",
                help_text="Please enter the complete needlist excel path along with the extension",
                value=needlist_input.get("path_input", {}).get("excel_path", ""),
                error_message=errors.get("path_input", {}).get("excel_path", ""),
            ).layout,
            InputCustom(
                id=ids.FOLDER_PATH,
                label="Folder Path",
                help_text="Please enter the top level folder path where the received files are stored",
                value=needlist_input.get("path_input", {}).get("folder_path", ""),
                error_message=errors.get("path_input", {}).get("folder_path", ""),
            ).layout,
        ],
        id=ids.PATH_INPUT_CONTAINER,
    )

    excel_info = html.Div(
        [
            InputCustom(
                id=ids.SHEET_NAME,
                label="Sheet Name",
                help_text="Please enter the sheet name",
                value=needlist_input.get("excel_input", {}).get("sheet_name", ""),
                error_message=errors.get("excel_input", {}).get("sheet_name", ""),
            ).layout,
            InputCustom(
                id=ids.HEADER,
                label="Header Row Number",
                help_text="Please enter the header row number",
                value=needlist_input.get("excel_input", {}).get("header_row", ""),
                error_message=errors.get("excel_input", {}).get("header_row", ""),
            ).layout,
        ],
        id=ids.EXCEL_INFO_CONTAINER,
    )

    column_dropdown = html.Div(
        [
            dcc.Loading(
                DropdownCustom(
                    id=ids.COLUMN_NAME_DROPDOWN,
                    label="Column Name",
                    help_text="Please select the column name",
                    value=needlist_input.get("column_input", {}).get(
                        "doc_no_column_name", ""
                    ),
                    error_message=errors.get("column_input", {}).get(
                        "doc_no_column_name", ""
                    ),
                    options=needlist_input.get("column_input", {}).get(
                        "column_names", []
                    ),
                ).layout
            ),
            RadioItems(
                id=ids.SEARCH_LEVEL,
                label="Search Level",
                options=[
                    {"label": "File", "value": "file"},
                    {"label": "Folder", "value": "folder"},
                ],
                value=needlist_input.get("search_level", "file"),
                help_text="Please select whether to search for files or folders names",
                inline=True,
            ).layout,
        ],
        id=ids.COLUMN_DROPDOWN_CONTAINER,
    )

    input_fields = html.Div([path_container, excel_info, column_dropdown])

    save_btn = ButtonCustom(
        id=ids.SAVE_BTN,
        label="Save",
        color="bg-blue-500",
    ).layout

    return input_fields, save_btn


# hide the container if the store is empty
@app.callback(
    Output(ids.EXCEL_INFO_CONTAINER, "style", allow_duplicate=True),
    Output(ids.COLUMN_DROPDOWN_CONTAINER, "style"),
    [Input(STORE_ID, "data")],
    prevent_initial_call=True,
)
def hide_container(data):
    if data is None:
        raise PreventUpdate
    needlist_input = data.get("needlist_input", {})

    excel_info_style = {"display": "none"}
    column_dropdown_style = {"display": "none"}

    if needlist_input.get("path_input", {}):
        excel_info_style = {"display": "block"}
    if needlist_input.get("column_input", {}):
        column_dropdown_style = {"display": "block"}
    return excel_info_style, column_dropdown_style


# show excel info fields when path inputs are filled and validated
@app.callback(
    Output(STORE_ID, "data", allow_duplicate=True),
    Output(f"{ids.NEEDLIST_PATH}-error", "children", allow_duplicate=True),
    Output(ids.EXCEL_INFO_CONTAINER, "style", allow_duplicate=True),
    Input(ids.NEEDLIST_PATH, "value"),
    Input(ids.FOLDER_PATH, "value"),
    State(STORE_ID, "data"),
    prevent_initial_call="initial_duplicate",
)
def show_excel_info(needlist_path, folder_path, data):
    if data is None:
        raise PreventUpdate

    data, error = needlist.validate_path_input(data)

    if error:
        return (
            data,
            MessageCustom(messages=str(error), success=False).layout,
            dash.no_update,
        )
    return data, dash.no_update, {"display": "block"}


# Generate column list on click of generate column list button
@app.callback(
    Output(ids.COLUMN_NAME_DROPDOWN, "options"),
    Output(STORE_ID, "data", allow_duplicate=True),
    Output(f"{ids.GENERATE_COLUMN_BTN}-feedback", "children", allow_duplicate=True),
    [Input(ids.GENERATE_COLUMN_BTN, "n_clicks")],
    [State(STORE_ID, "data")],
    prevent_initial_call=True,
)
def generate_column_list(n_clicks, data):
    if n_clicks is None:
        return dash.no_update, dash.no_update, dash.no_update

    status, updated_data, msg = needlist.column_input_ready(data)
    if not status:
        return dash.no_update, data, MessageCustom(messages=msg, success=False).layout

    column_names = updated_data["needlist_input"]["column_names"]
    return (
        column_names,
        updated_data,
        MessageCustom(messages=msg, success=True).layout,
    )


# Save the input data
@app.callback(
    Output(STORE_ID, "data", allow_duplicate=True),
    Output(ids.FEEDBACK_SAVE, "children", allow_duplicate=True),
    [Input(ids.SAVE_BTN, "n_clicks")],
    [
        State(ids.NEEDLIST_PATH, "value"),
        State(ids.FOLDER_PATH, "value"),
        State(ids.SHEET_NAME, "value"),
        State(ids.HEADER, "value"),
        State(ids.COLUMN_NAME_DROPDOWN, "value"),
        State(ids.COLUMN_NAME_DROPDOWN, "options"),
        State(ids.SEARCH_LEVEL, "value"),
        State(STORE_ID, "data"),
    ],
    prevent_initial_call=True,
)
def save_data(
    n_clicks,
    needlist_path,
    folder_path,
    sheet_name,
    header_row,
    doc_no_column_name,
    column_names,
    search_level,
    data,
):
    if n_clicks is None:
        raise PreventUpdate

    needlist_input = {
        "excel_path": needlist_path,
        "folder_path": folder_path,
        "sheet_name": sheet_name,
        "header_row": header_row,
        "doc_no_column_name": doc_no_column_name,
        "column_names": column_names,
        "search_level": search_level,
    }

    needlist_input_validated, errors = needlist.validate_input(needlist_input)

    if errors:
        data["needlist_input"] = needlist_input
        return (
            data,
            MessageCustom(messages="Please correct the errors", success=False).layout,
        )

    data["needlist_input"] = needlist_input_validated
    return (
        data,
        MessageCustom(messages="Data saved successfully", success=True).layout,
    )


# callback function to show the run button if data is valid and all inputs ready
@app.callback(
    Output(ids.RUN_CONTAINER, "children"),
    [Input(STORE_ID, "data")],
)
def display_run_btn(data):
    if data is None:
        raise PreventUpdate

    all_inputs_ready, messages = needlist.all_inputs_ready(data)
    if all_inputs_ready:
        return ButtonCustom(
            id=ids.RUN_BTN,
            label="Update Needlist",
            color="bg-purple-500",
        ).layout

    return MessageCustom(messages=messages, success=False).layout


# perform the calculation
@app.callback(
    Output(STORE_ID, "data", allow_duplicate=True),
    Output(ids.FEEDBACK_RUN, "children"),
    [Input(ids.RUN_BTN, "n_clicks")],
    [State(STORE_ID, "data")],
    prevent_initial_call=True,
)
def run_calculation(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    message = []

    is_ready, msg = needlist.all_inputs_ready(data)
    if is_ready:
        try:
            data = needlist.run_calculation(data)
            message.append("Needlist Updated Successfully with Folder Links")
            feedback_html = MessageCustom(messages=message, success=True).layout
            return data, feedback_html
        except Exception as e:
            traceback.print_exc()
            message.append("Failure in Page Calculations")
            message.append(f"Error: {str(e)}")
            feedback_html = MessageCustom(messages=message, success=False).layout
            return data, feedback_html
    else:
        message.append(msg)
        feedback_html = MessageCustom(messages=message, success=False).layout
        return data, feedback_html
