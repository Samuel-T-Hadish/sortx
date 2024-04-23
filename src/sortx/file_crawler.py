"""
file_crawler.py
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

# Setup logging with a more informative format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class InputData:
    excel_file: str
    sheet_name: str
    folder_directory: str
    doc_no_column_name: str
    df: Optional[pd.DataFrame] = field(default=None, init=False)

    def __post_init__(self):
        self.excel_file = f"data/{self.excel_file}"
        self.validate_excel_file()
        self.validate_sheet_name()
        self.validate_folder_directory()
        self.create_df()

    def validate_excel_file(self):
        if not Path(self.excel_file).is_file():
            logger.error(f"Excel file not found: {self.excel_file}")
            raise FileNotFoundError(f"Excel file not found: {self.excel_file}")

    def validate_sheet_name(self):
        try:
            with pd.ExcelFile(self.excel_file) as xls:
                if self.sheet_name not in xls.sheet_names:
                    logger.error(
                        f"Sheet name '{self.sheet_name}' not found in {self.excel_file}"
                    )
                    raise ValueError(f"Sheet name '{self.sheet_name}' not found.")
        except Exception as e:
            logger.error(f"Error accessing Excel file '{self.excel_file}': {e}")
            raise

    def validate_folder_directory(self):
        if not Path(self.folder_directory).is_dir():
            logger.error(f"Folder directory not found: {self.folder_directory}")
            raise NotADirectoryError(
                f"Folder directory not found: {self.folder_directory}"
            )

    def create_df(self):
        try:
            with pd.ExcelFile(self.excel_file) as xls:
                self.df = pd.read_excel(xls, sheet_name=self.sheet_name)
            if self.doc_no_column_name not in self.df.columns:
                logger.error(
                    f"Column '{self.doc_no_column_name}' not found in DataFrame."
                )
                raise ValueError(f"Column '{self.doc_no_column_name}' not found.")
            logger.info(f"DataFrame successfully created from {self.excel_file}.")
        except Exception as e:
            logger.error(f"Error creating DataFrame: {e}")
            raise


class FileCrawler:
    def __init__(
        self,
        df: pd.DataFrame,
        folder_directory: str,
        doc_no_column_name: str,
    ):
        self.df = df
        self.folder_directory = folder_directory
        self.doc_no_column_name = doc_no_column_name

    def update_folder_link(
        self,
    ):  # TODO: Input atttribute for file extension, other options
        if self.df is None:
            logger.error("DataFrame is empty or not initialized.")
            raise ValueError("DataFrame is empty or not initialized.")

        df_column_values = set(self.df[self.doc_no_column_name].astype(str).values)
        for file_path in Path(self.folder_directory).rglob("*"):
            if (
                file_path.is_file() and file_path.suffix == ".pdf"
            ) or file_path.is_dir():
                matched_docs = [
                    doc_no for doc_no in df_column_values if doc_no in file_path.name
                ]
                if matched_docs:
                    for doc_no in matched_docs:
                        self.df.loc[
                            self.df[self.doc_no_column_name] == doc_no,
                            ["status", "filepath", "processed_date"],
                        ] = [
                            "Yes",
                            str(file_path),
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        ]
        logger.info("Folder link updated successfully.")

    def get_output_dict(self):
        return self.df.to_dict(orient="records")
