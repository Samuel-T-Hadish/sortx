"""
project/needlist.py
functions to validate and run calculations for page1 of the project.
"""

from typing import Any, Dict, List, Tuple

import openpyxl
from agility.utils.pydantic import validate_data
from pydantic import ValidationError

from sortx.core.file_crawler import FileCrawler
from sortx.schemas.needlist import ColumnInput, ExcelInput, NeedlistInput, PathInput


def validate_path_input(data: dict):
    """
    Check if the path_input data is valid and update the values in the data dictionary.

    return:
        data: dict
        errors: dict

    """

    errors = {}

    if (
        not data
        or "needlist_input" not in data
        or "path_input" not in data["needlist_input"]
    ):
        errors["path_input"] = "Path input data is missing"
        return data, errors

    path_input_data = data["needlist_input"]["path_input"]

    validated_data, error = validate_data(path_input_data, PathInput)
    data["needlist_input"]["path_input"] = validated_data

    return data, error


def validate_excel_input(data: dict):
    """
    Check if the excel_input data is valid.
    """
    excel_input, errors = validate_data(data, ExcelInput)


def get_sheet_names(excel_path: str) -> List[str]:
    """
    Get the sheet names from the excel file.
    """
    wb = openpyxl.load_workbook(excel_path)
    return wb.sheetnames


def validate_input(page_input):
    """
    Check if the page_input data is valid.
    """
    page_input, errors = validate_data(page_input, NeedlistInput)
    return page_input, errors


def all_inputs_ready(data):
    msgs = []
    ready = True
    if not data or "needlist_input" not in data:
        message = "Missing NeedList Page input in data"
        msgs.append(message)
        ready = False

    needlist_input = data["needlist_input"]
    needlist_input, needlist_errors = validate_input(needlist_input)

    if needlist_errors:
        ready = False
        msgs.append("Needlist Page Inputs Invalid")

    return ready, msgs


def column_input_ready(data: dict) -> Tuple[bool, dict, list]:
    """
    Check if required inputs are available to generate the list of columns from the excel file.

    return:
        status: bool
        data: dict
        messages: list
    """
    if data["needlist_input"]["column_names"][0] != "":
        return True, data, ["Column List Generated Successfully"]
    try:
        needlist_input = NeedlistInput(**data["needlist_input"])
        data["needlist_input"]["column_names"] = needlist_input.column_names
        return True, data, ["Column List Generated Successfully"]
    except ValidationError:
        return False, data, ["Fill the above form to generate the column list."]


def run_calculation(data) -> dict:

    needlist_input = NeedlistInput.model_construct(**data["needlist_input"])

    file_crawler = FileCrawler(
        excel_file_path=needlist_input.excel_path,
        folder_directory=needlist_input.folder_path,
        doc_no_column_name=needlist_input.doc_no_column_name,
        sheet_name=needlist_input.sheet_name,
        header=int(needlist_input.header_row),
    )
    file_crawler.main(needlist_input.search_level)

    return data
