"""functions to validate and run calculations for page1 of the project."""

from typing import Any, Dict, List, Tuple

from agility.utils.pydantic import process_pydantic_errors, validate_data
from pydantic import ValidationError

from sortx.core.file_crawler import FileCrawler
from sortx.schemas.needlist import NeedlistInput


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
    )
    file_crawler.main()

    return data
