from pathlib import Path
from typing import Self

import xlwings as xw
from pydantic import BaseModel, field_validator, model_validator


class NeedlistInput(BaseModel):
    """
    Pydantic model for the needlist data of the project.

    Attributes:
        folder_path: str
        excel_path: str
        sheet_name: str | int
        header_row: int
        column_name: str

    """

    folder_path: str
    excel_path: str
    sheet_name: str | int
    header_row: int
    column_name: str

    @model_validator(mode="after")
    def check_excel_path(self) -> Self:
        if not Path(self.excel_path).exists() and not self.excel_path.endswith(
            (".xls", ".xlsx")
        ):
            raise ValueError("Excel file does not exist.")
        with xw.App(visible=False):
            wb = xw.Book(self.excel_path)
            if isinstance(self.sheet_name, int):
                if self.sheet_name > len(wb.sheets):
                    raise ValueError("Sheet index out of range.")
            if isinstance(self.sheet_name, str):
                if self.sheet_name not in wb.sheets:
                    raise ValueError("Sheet name does not exist in the excel file.")

        return self

    @field_validator("folder_path")
    @classmethod
    def check_folder_path(cls, v: str):
        if not Path(v).exists():
            raise ValueError("Folder does not exist.")
        return v


class NeedlistOutput(BaseModel):
    """
    Pydantic model for the needlist data of the project.

    Attributes:

    """

    column_input_ready: bool = False
