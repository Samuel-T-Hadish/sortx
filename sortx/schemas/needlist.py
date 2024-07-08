"""Schema for the needlist data of the project."""

from pathlib import Path
from typing import List, Optional, Self

import openpyxl
from pydantic import BaseModel, Field, field_validator, model_validator


class NeedlistInput(BaseModel):
    """
    Pydantic model for the needlist data of the project.

    Attributes:
        folder_path: str
        excel_path: str
        sheet_name: str | int
        header_row: int
        column_names: List[str]
        doc_no_column_name: str
        search_level: str

    """

    folder_path: str
    excel_path: str
    sheet_name: str | int
    header_row: int
    column_names: List[str] = Field(default_factory=list)
    doc_no_column_name: Optional[str] = None
    search_level: str = "file"

    @field_validator("folder_path")
    @classmethod
    def check_folder_path(cls, v: str):
        if not Path(v).exists():
            raise ValueError("Folder does not exist.")
        return v

    @model_validator(mode="after")
    def check_excel_path(self) -> Self:
        if not Path(self.excel_path).exists() or not self.excel_path.endswith(
            (".xls", ".xlsx")
        ):
            raise ValueError("Excel file does not exist.")

        wb = None
        try:
            wb = openpyxl.load_workbook(self.excel_path, read_only=True)
            if isinstance(self.sheet_name, int):
                if self.sheet_name >= len(wb.sheetnames):
                    raise ValueError("Sheet index out of range.")
                ws = wb[wb.sheetnames[self.sheet_name]]
            elif isinstance(self.sheet_name, str):
                if self.sheet_name not in wb.sheetnames:
                    raise ValueError("Sheet name does not exist in the excel file.")
                ws = wb[self.sheet_name]
            else:
                raise ValueError("Sheet name must be a string or an integer.")

            row = list(
                ws.iter_rows(
                    min_row=self.header_row, max_row=self.header_row, values_only=True
                )
            )[0]
            self.column_names = [cell for cell in row if cell is not None]

        except Exception as e:
            raise ValueError(f"Error reading Excel file: {e}")
        finally:
            if wb:
                wb.close()

        return self

    @field_validator("search_level")
    @classmethod
    def check_search_level(cls, v: str):
        if v not in ["folder", "file"]:
            raise ValueError("Search level should be either 'folder' or 'file'.")
        return v
