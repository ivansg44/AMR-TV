from dash import Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from data_parser import get_app_data
from main_fig_generator import get_main_fig
from legend_fig_generator import (get_node_symbol_legend_fig,
                                  get_link_legend_fig,
                                  get_node_color_legend_fig)

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
    show_legend = False
    height = "100vh"
    width = "100vw"

    # app_data = get_app_data(
    #     "sample_data.csv",
    #     delimiter=",",
    #     node_id="Sample ID / Isolate",
    #     track="Location",
    #     date_attr="Date of collection",
    #     date_format="%B %Y",
    #     label_attr="Patient ID",
    #     attr_link_list=[
    #         "F1: MLST type",
    #         "Resitance gene type",
    #         "SNPs_homozygous",
    #         "Left_flanks;Right_flanks",
    #         "mash_neighbor_cluster",
    #         "rep_type(s)"
    #     ],
    #     links_across_y=True,
    #     max_day_range=60,
    #     null_vals=["", "-"],
    #     node_symbol_attr="Organism",
    #     node_color_attr="mash_neighbor_cluster"
    # )
    app_data = get_app_data(
        "senterica_clusters_11042021.tsv",
        delimiter="\t",
        node_id="Sample",
        track="site_order",
        date_attr="collection_date",
        date_format="%Y-%m-%d %H:%M:%S",
        label_attr="Sample",
        attr_link_list=[
            "Cluster"
        ],
        links_across_y=True,
        max_day_range=5000000,
        null_vals=["", "-"],
        # node_symbol_attr="Organism",
        # node_color_attr="Cluster",
        y_key=int
    )

    node_symbol_legend_fig = get_node_symbol_legend_fig(app_data)
    node_color_legend_fig_height = \
        "%svh" % (len(app_data["node_color_attr_dict"]) * 5)

    children = [
        dbc.Col(
            children=dcc.Graph(
                figure=get_main_fig(app_data),
                id="main-graph",
                # config={"displayModeBar": False},
                style={"height": height, "width": width}
            ),
            id="main-col",
        )
    ]

    if show_legend:
        children.append(
            dbc.Col(
                children=[
                    dbc.Row(
                        dbc.Col(
                            dcc.Graph(
                                figure=node_symbol_legend_fig,
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
                    ),
                    dbc.Row(
                        dbc.Col(
                            dcc.Graph(
                                figure=get_node_color_legend_fig(app_data),
                                id="node-color-legend-graph",
                                config={"displayModeBar": False},
                                style={
                                    "height": node_color_legend_fig_height
                                }

                            ),
                            id="node-color-legend-col"
                        ),
                        id="node-color-legend-row"
                    )
                ],
                id="legend-col",
                width=2
            )
        )

    return [
        dbc.Row(
            children=children
        ),
        dcc.Store(id="app_data", data=app_data)
    ]


if __name__ == "__main__":
    app.run_server(debug=True)