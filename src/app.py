import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

from callbacks import input_validation
from callbacks import excel_processing
from components import layout

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
    ],
)
app.title = "sortX"
app.layout = layout.create_layout()

input_validation.register_callbacks(app)
excel_processing.register_callbacks(app)

if __name__ == "__main__":
    # app.run(debug=True, host="10.29.3.31")
    app.run(debug=True)
