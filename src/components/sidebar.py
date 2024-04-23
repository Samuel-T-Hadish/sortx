import dash
import dash_bootstrap_components as dbc
from dash import html


def create_sidebar():
    return dbc.Nav(
        [
            dbc.NavLink(
                [html.Div(page["name"], className="sidebar-text")],
                href=page["path"],
                active="exact",
            )
            for page in dash.page_registry.values()
        ],
        vertical=False,
        pills=True,
    )
