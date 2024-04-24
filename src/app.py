import dash
from agility.skeleton.custom_components import NavbarCustom
from dash import Dash, html

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
    ],
)
app.title = "sortX"
navbar = NavbarCustom(app.title)
app.layout = html.Div(
    [
        navbar.layout,
        # side.layout,
        html.Div(
            dash.page_container,
            className="p-4 w-full ml-12",
        ),
    ],
    className="flex flex-col h-screen",
)

if __name__ == "__main__":
    # app.run(debug=True)
    #10.29.3.31
    app.run(host="10.29.3.31", debug=True)
