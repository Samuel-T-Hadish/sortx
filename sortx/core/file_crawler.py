"""
file_crawler.py
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd
import xlwings as xw

from sortx.core.definitions import NeedListColumn

# Setup logging with a more informative format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FileCrawler:
    master_df: pd.DataFrame
    unmapped_df: pd.DataFrame

    def __init__(
        self,
        excel_file_path: str,
        folder_directory: str,
        doc_no_column_name: Optional[str],
        sheet_name: str,
        header: int,
    ):
        self.excel_file_path = excel_file_path
        self.folder_directory = folder_directory
        self.doc_no_column_name = doc_no_column_name
        self.header = header
        self.sheet_name = sheet_name
        self.not_found_list: List[dict] = []

    def read_excel(self):
        try:
            # Read the main sheet
            self.master_df = pd.read_excel(
                self.excel_file_path, sheet_name=self.sheet_name, header=self.header - 1
            )
            logger.info("Main Excel sheet read successfully.")

            # Read the UnMapped sheet if it exists
            try:
                self.unmapped_df = pd.read_excel(
                    self.excel_file_path, sheet_name="UnMapped"
                )
                logger.info("UnMapped sheet read successfully.")
            except ValueError:
                self.unmapped_df = pd.DataFrame(
                    columns=[
                        self.doc_no_column_name,
                        NeedListColumn.FILE_PATH,
                        NeedListColumn.PROCESSED_DATE,
                    ]
                )
                logger.info(
                    "UnMapped sheet does not exist. Initialized empty DataFrame."
                )
        except Exception as e:
            logger.error(f"Error reading excel file: {e}")

    def update_links(self, link_type: str):
        """
        Update the DataFrame with folder or file links based on the link_type argument.

        Args:
            link_type: 'folder' or 'file' to specify the type of link to update.
        """
        if self.master_df is None:
            logger.error("DataFrame is empty or not initialized.")
            raise ValueError("DataFrame is empty or not initialized.")

        for file_path in Path(self.folder_directory).rglob("*"):
            if link_type == "folder" and file_path.is_dir():
                self.__update_folder_links(file_path)
            elif link_type == "file" and file_path.is_file():
                self.__update_file_links(file_path)

        # Convert not_found_list to DataFrame
        new_unmapped_df = pd.DataFrame(self.not_found_list)

        # Append new_unmapped_df to existing unmapped_files
        self.unmapped_df = pd.concat(
            [self.unmapped_df, new_unmapped_df], ignore_index=True
        )

        # Remove duplicates in the FILE_PATH column
        self.unmapped_df.drop_duplicates(
            subset=[NeedListColumn.FILE_PATH], inplace=True
        )

        logger.info(f"{link_type.capitalize()} links updated successfully.")

    def save_excel(self):
        app = xw.App(visible=False)
        try:
            wb = app.books.open(self.excel_file_path)
            try:
                # Save the main DataFrame to the original sheet
                sheet = wb.sheets[self.sheet_name]
                starting_cell = sheet.range(f"A{self.header}")
                sheet.range(starting_cell).expand("table").clear_contents()
                sheet.range(starting_cell).options(index=False).value = self.master_df

                # Save the unmapped files DataFrame to the "UnMapped" sheet
                if "UnMapped" in wb.sheet_names:
                    unmapped_sheet = wb.sheets["UnMapped"]
                else:
                    unmapped_sheet = wb.sheets.add("UnMapped")

                unmapped_sheet.clear_contents()
                unmapped_sheet.range("A1").options(index=False).value = self.unmapped_df

                wb.save()
            except PermissionError as e:
                logger.error(f"Permission error while saving Excel file: {e}")
                raise ValueError("Error saving Excel file due to permission issues.")
            except Exception as e:
                logger.error(f"Error saving excel file: {e}")
                raise ValueError("Unexpected error saving Excel file.")
            finally:
                wb.close()
        except Exception as e:
            logger.error(f"Error opening Excel file: {e}")
            raise ValueError("Error opening Excel file.")
        finally:
            app.quit()

    def main(self, link_type: str):
        """
        Main to read the excel file, update the folder or file links, and save the excel file.
        Also saves the unmapped files to a separate sheet named 'UnMapped' in the same Excel file.

        Args:
            link_type: 'folder' or 'file' to specify the type of link to update.
        """
        if link_type not in ["folder", "file"]:
            err_msg = "Invalid link_type argument. Choose 'folder' or 'file'."
            logger.error(err_msg)
            raise ValueError(err_msg)
        self.read_excel()
        self.update_links(link_type)
        self.save_excel()

    # Private methods
    def __update_file_links(self, file_path: Path):
        """ "
        Private method to update the DataFrame with file links.
        Used by the update_links method.

        Args:
            file_path: Path object of the file to update in the DataFrame.

        Generates:
            Updates the master_df DataFrame and appends to the not_found_list if the file is not found.

        """
        if file_path.stem in self.master_df[self.doc_no_column_name].values:
            self.master_df.loc[
                self.master_df[self.doc_no_column_name] == file_path.stem,
                [
                    NeedListColumn.STATUS,
                    NeedListColumn.FILE_PATH,
                    NeedListColumn.PROCESSED_DATE,
                ],
            ] = [
                "Yes",
                str(file_path),
                datetime.now().strftime("%Y-%m-%d"),
            ]
        else:
            self.__update_unmapped_files(file_path)

    def __update_folder_links(self, file_path: Path):
        """
        Private method to update the DataFrame with folder links.
        Used by the update_links method.

        Args:
            file_path: Path object of the folder to update in the DataFrame.

        Generates:
            Updates the master_df DataFrame and appends to the not_found_list if the folder is not found.

        """
        if file_path.name in self.master_df[self.doc_no_column_name].values:
            self.master_df.loc[
                self.master_df[self.doc_no_column_name] == file_path.name,
                [
                    NeedListColumn.STATUS,
                    NeedListColumn.FILE_PATH,
                    NeedListColumn.PROCESSED_DATE,
                ],
            ] = [
                "Yes",
                str(file_path),
                datetime.now().strftime("%Y-%m-%d"),
            ]
        else:
            self.__update_unmapped_files(file_path)

    def __update_unmapped_files(self, file_path: Path):
        """
        Private method to update the unmapped files DataFrame.
        Used by the update_links method.

        Args:
            file_path: Path object of the file or folder to update in the unmapped DataFrame.

        Generates:
            Appends only the file to the not_found_list if it is not found in the main DataFrame.

        """
        if file_path.is_file():
            self.not_found_list.append(
                {
                    self.doc_no_column_name: file_path.stem,
                    NeedListColumn.FILE_PATH: str(file_path),
                    NeedListColumn.PROCESSED_DATE: datetime.now().strftime("%Y-%m-%d"),
                }
            )
