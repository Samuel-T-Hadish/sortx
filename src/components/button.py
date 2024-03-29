"""button.py"""

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

from ..data.file_crawler import FileCrawler
from ..data.loader import get_df_from_string_content
from . import ids


def run_file_crawler(file_crawler: FileCrawler):
    print(file_crawler.df.head(5))
    print(file_crawler.folder_directory)


def render(app: Dash) -> html.Div:
    """
    Renders the button component.

    Args:
        app (Dash): The Dash application object.

    Returns:
        html.Div: The rendered button component.
    """

    @app.callback(
        Output(ids.PROCESS_BUTTON_INFO, "children"),
        Output(ids.DOWNLOAD_STORE, "data"),
        Input(ids.PROCESS_BUTTON, "n_clicks"),
        State(ids.UPLOAD_FILE_STORE, "data"),
        State(ids.FOLDER_PATH_TEXT, "value"),
    )
    def update_data_table(n_clicks: int, data: dict, folder_path: str):
        """
        Updates the data table with the uploaded data.

        Args:
            n_clicks (int): The number of times the button has been clicked.
            data (dict): The uploaded data.

        Returns:
            html.H4 | dcc.Loading: The data table or a loading spinner.
        """
        if n_clicks:
            if data:
                df = get_df_from_string_content(data["content"], data["filename"])
                file_crawl = FileCrawler(
                    df, folder_path, doc_no_column_name="Name"
                )  # FIXME: doc_no_column_name should be a parameter
                file_crawl.update_folder_link()
                output_dict = file_crawl.get_output_dict()

                return (
                    ("Data table updated", output_dict)
                    if output_dict
                    else ("Data table updated", {})
                )
        return ("No data uploaded yet", {})

    return html.Div(
        [
            html.Button(
                "Update Data Table",
                id=ids.PROCESS_BUTTON,
                n_clicks=0,
                className="btn btn-primary",
            ),
            dcc.Loading(
                id=ids.PROCESS_BUTTON_LOADING,
                children=[html.H4(id=ids.PROCESS_BUTTON_INFO)],
                type="default",
            ),
        ]
    )
