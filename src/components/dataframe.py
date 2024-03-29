""" dataframe.py """


from typing import Dict

from dash import Dash, dash_table, html
from dash.dependencies import Input, Output

from . import ids
from ..data.loader import get_df_from_string_content


def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.STORED_DATA_TABLE, "children"), Input(ids.UPLOAD_FILE_STORE, "data")
    )
    def get_data_table(data: Dict[str, str]) -> dash_table.DataTable | None:
        if data:
            df = get_df_from_string_content(data["content"], data["filename"]).head(5)
            return dash_table.DataTable(
                df.to_dict("records"), [{"name": i, "id": i} for i in df.columns]
            )
        return None

    return html.Div(id=ids.STORED_DATA_TABLE)
