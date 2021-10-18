from dash import Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from data_parser import get_app_data
from main_fig_generator import get_main_fig
from legend_fig_generator import get_node_shape_legend_fig, get_link_legend_fig

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
                            track="location",
                            attr_link_list = [
                                "mlst",
                                "gene",
                                "homozygous_snps",
                                "flanks",
                                "mash_neighbour_cluster",
                                "replicon_types"
                            ],
                            links_across_y=False,
                            max_day_range=60)
    return [
        dbc.Row(
            children=[
                dbc.Col(
                    children=dcc.Graph(
                        figure=get_main_fig(app_data),
                        id="main-graph",
                        config={"displayModeBar": False},
                        style={"height": "90vh"}
                    ),
                    id="main-col",
                ),
                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    figure=get_node_shape_legend_fig(app_data),
                                    id="node-shape-legend-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "25vh"}

                                ),
                                id="node-shape-legend-col"
                            ),
                            id="node-shape-legend-row"
                        ),
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    figure=get_link_legend_fig(app_data),
                                    id="link-legend-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "25vh"}

                                ),
                                id="link-legend-col"
                            ),
                            id="link-legend-row"
                        )
                    ],
                    id="legend-col",
                    width=2
                )
            ]
        ),
        dcc.Store(id="app_data", data=app_data)
    ]


if __name__ == "__main__":
    app.run_server(debug=True)