"""functions to validate and run calculations for page1 of the project."""

from agility.utils.pydantic import validate_data

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

    page1_input = data["needlist_input"]
    page1_input, page1_errors = validate_input(page1_input)

    if page1_errors:
        ready = False
        msgs.append("Needlist Page Inputs Invalid")

    return ready, msgs


def column_input_ready(data):
    """
    Check if required inputs are available to generate the list of columns from the excel file.
    """
    try:
        needlist_input = NeedlistInput(**data["needlist_input"])
        


def run_calculation(data) -> dict:

    needlist_input = NeedlistInput(**data["needlist_input"])

    file_crawler = FileCrawler(
        excel_file_path=needlist_input.excel_path,
        folder_directory=needlist_input.folder_path,
        doc_no_column_name=needlist_input.column_name,
        sheet_name=needlist_input.sheet_name,
    )
    print("Running Calculation...")

    return data
