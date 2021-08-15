"""Entry point to application.

``$ python app.py``

Visit http://127.0.0.1:8050/.

This file consists of the global variable ``app``, which is served as
the application, and associated ``app`` callbacks.
"""

from dash import Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import data_parser
from main_fig_generator import get_main_fig, get_main_fig_legend_cols

app = Dash(
    external_stylesheets=[dbc.themes.UNITED],
    # Fixes bug with debugger in Pycharm. See
    # https://bit.ly/3j86GL1.
    name="foo"
)

# We initially serve an empty container
app.layout = dbc.Container(
    children=dcc.Store("first-launch"),
    id="main-container",
    fluid=True
)


@app.callback(
    output=Output("main-container", "children"),
    inputs=Input("first-launch", "data")
)
def launch_app(_):
    """Populate empty container after launch."""
    app_data = data_parser.get_app_data("stub_sample_data.tsv",
                                        "stub_transmission_data.tsv")
    return [
        dbc.Row(
            children=get_main_fig_legend_cols(app_data["species_color_dict"])
        ),
        dbc.Row(
            children=dbc.Col(
                children=dcc.Graph(
                    figure=get_main_fig(app_data),
                    id="main-graph",
                    config={"displayModeBar": False},
                    style={"height": "90vh"}
                ),
                id="main-col"
            ),
            id="main-row"
        ),
        dcc.Store(id="app_data", data=app_data)
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
