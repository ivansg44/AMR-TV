from dash import Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from data_parser import get_app_data
from main_fig_generator import get_main_fig

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
    app_data = get_app_data("sample_data.csv",
                            links_across_y=False,
                            max_day_range=60)
    return [
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