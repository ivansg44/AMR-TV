"""Point of entry for application.

Running this script launches the application.
"""

import dash
from dash import Dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
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
    name="foo",
    suppress_callback_exceptions=True
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
    """Populate empty container after launch.

    This includes an empty fig, and upload btn.
    """
    children = [
        dbc.Row(
            dbc.Col(
                dbc.Button("Upload data",
                           id="upload-data-btn",
                           color="primary")
            ),
            className="mt-1"
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Upload data"),
                dbc.ModalBody([
                    dcc.Upload(
                        dbc.Button("Select data file", id="select-file-btn"),
                        id="upload-file"
                    )
                ]),
                dbc.ModalFooter("Foo")
            ],
            id="upload-data-modal"
        ),
        dcc.Store("new-upload")
    ]

    return children


# @app.callback(
#     output=Output("main-container", "children"),
#     inputs=Input("first-launch", "data")
# )
# def launch_app(_):
#     """Populate empty container after launch."""
#     show_legend = True
#     height = "100vh"
#     width = "80vw"
# 
#     # # "senterica_clusters_11042021.tsv"
#     # get_app_data_args = {
#     #     "sample_file_path": "senterica_clusters_11042021.tsv",
#     #     "delimiter": "\t",
#     #     "node_id": "Sample",
#     #     "track": "site_order",
#     #     "date_attr": "collection_date",
#     #     "date_format": "%Y-%m-%d %H:%M:%S",
#     #     "label_attr": "Sample",
#     #     "attr_link_list": ["Cluster"],
#     #     "links_across_y": True,
#     #     "max_day_range": 5000000,
#     #     "null_vals": ["", "-"],
#     #     "selected_nodes": {}
#     #     "y_key": int
#     # }
# 
#     # # "senterica_clusters_12012021.tsv"
#     # get_app_data_args = {
#     #     "sample_file_path": "senterica_clusters_12012021.tsv",
#     #     "delimiter": "\t",
#     #     "node_id": "Sample",
#     #     "track": "site_order",
#     #     "date_attr": "collection_date",
#     #     "date_format": "%Y-%m-%d %H:%M:%S",
#     #     "label_attr": "Sample",
#     #     "attr_link_list": [
#     #         # "threshold_5",
#     #         "threshold_10",
#     #         # "threshold_20",
#     #         # "threshold_50",
#     #         # "threshold_100",
#     #         # "threshold_200",
#     #         # "threshold_1000",
#     #     ],
#     #     "node_color_attr": "serovar",
#     #     "node_symbol_attr": "serovar",
#     #     "links_across_y": True,
#     #     "max_day_range": 14,
#     #     "null_vals": ["", "-"],
#     #     "selected_nodes": {},
#     #     "y_key": "int"
#     # }
# 
#     # "sample_data.csv"
#     get_app_data_args = {
#         "sample_file_path": "sample_data.csv",
#         "delimiter": ",",
#         "node_id": "Sample ID / Isolate",
#         "track": "Location",
#         "date_attr": "Date of collection",
#         "date_format": "%B %Y",
#         "label_attr": "Patient ID",
#         "attr_link_list": [
#             "F1: MLST type",
#             "Resitance gene type",
#             "SNPs_homozygous",
#             "Left_flanks;Right_flanks",
#             "mash_neighbor_cluster",
#             "rep_type(s)"
#         ],
#         "node_color_attr": "mash_neighbor_cluster",
#         "node_symbol_attr": "Organism",
#         "links_across_y": True,
#         "max_day_range": 60,
#         "null_vals": ["", "-"],
#         "selected_nodes": {}
#     }
# 
#     app_data = get_app_data(**get_app_data_args)
# 
#     children = [
#         dbc.Col(
#             children=dcc.Graph(
#                 figure=get_main_fig(app_data),
#                 id="main-graph",
#                 # config={"displayModeBar": False},
#                 style={"height": height, "width": width}
#             ),
#             id="main-col",
#         )
#     ]
# 
#     if show_legend:
#         node_symbol_legend_fig = get_node_symbol_legend_fig(app_data)
#         link_legend_fig = get_link_legend_fig(app_data)
#         node_color_legend_fig = get_node_color_legend_fig(app_data)
#         node_color_legend_fig_height = \
#             "%svh" % (len(app_data["node_color_attr_dict"]) * 5)
# 
#         children.append(
#             dbc.Col(
#                 children=[
#                     dbc.Row(
#                         dbc.Col(
#                             dcc.Graph(
#                                 figure=node_symbol_legend_fig,
#                                 id="node-shape-legend-graph",
#                                 config={"displayModeBar": False},
#                                 style={"height": "25vh"}
# 
#                             ),
#                             id="node-shape-legend-col"
#                         ),
#                         id="node-shape-legend-row"
#                     ),
#                     dbc.Row(
#                         dbc.Col(
#                             dcc.Graph(
#                                 figure=link_legend_fig,
#                                 id="link-legend-graph",
#                                 config={"displayModeBar": False},
#                                 style={"height": "25vh"}
# 
#                             ),
#                             id="link-legend-col"
#                         ),
#                         id="link-legend-row"
#                     ),
#                     dbc.Row(
#                         dbc.Col(
#                             dcc.Graph(
#                                 figure=node_color_legend_fig,
#                                 id="node-color-legend-graph",
#                                 config={"displayModeBar": False},
#                                 style={
#                                     "height": node_color_legend_fig_height
#                                 }
# 
#                             ),
#                             id="node-color-legend-col"
#                         ),
#                         id="node-color-legend-row"
#                     )
#                 ],
#                 id="legend-col",
#                 width=2
#             )
#         )
# 
#     return [
#         dbc.Row(
#             children=children
#         ),
#         dcc.Store(id="get-app-data-args", data=get_app_data_args),
#         dcc.Store(id="selected-nodes", data={})
#     ]


@app.callback(
    Output("upload-data-modal", "is_open"),
    Input("upload-data-btn", "n_clicks"),
    prevent_intial_call=True
)
def open_upload_data_modal(n_clicks):
    """TODO

    :param n_clicks:
    :type n_clicks:
    :return:
    :rtype:
    """
    return n_clicks


@app.callback(
    Output("select-file-btn", "children"),
    Output("select-file-btn", "color"),
    Input("upload-file", "contents"),
    Input("upload-file", "filename"),
    prevent_initial_call=True
)
def process_upload(_, filename):
    """TODO"""
    return filename, "success"


@app.callback(
    inputs=Input("main-graph", "clickData"),
    state=State("selected-nodes", "data"),
    output=[
        Output("selected-nodes", "data"),
        Output("main-graph", "clickData")
    ],
    prevent_initial_call=True
)
def select_nodes(click_data, selected_nodes):
    """Update selected nodes browser variable after clicking node.

    The selected nodes are stored as str numbers representing the
    0-based order they appear in the original dataset. i.e., if you
    click the node corresponding to the fifth row in the original
    dataset, "4" is added to the list of selected nodes.

    :param click_data: Information on node clicked by user
    :type click_data: dict
    :param selected_nodes: Currently selected nodes
    :type selected_nodes: list[str]
    :return: New list of selected nodes
    :rtype: list[str]
    """
    new_selected_nodes = selected_nodes
    clicked_node = str(click_data["points"][0]["pointIndex"])
    if clicked_node in selected_nodes:
        new_selected_nodes.pop(clicked_node)
    else:
        new_selected_nodes[clicked_node] = None
    return new_selected_nodes, None


@app.callback(
    inputs=[
        Input("selected-nodes", "data"),
        Input("main-graph", "relayoutData")
    ],
    state=[
        State("get-app-data-args", "data")
    ],
    output=[
        Output("main-graph", "figure"),
        Output("get-app-data-args", "data")
    ],
    prevent_initial_call=True
)
def update_main_graph(selected_nodes, relayout_data, get_app_data_args):
    """Update main graph after page launch.

    Current triggers:

    * Select nodes browser var updated
    * User zooms/pans across graph

    :param selected_nodes: Currently selected nodes
    :type selected_nodes: list[str]
    :param relayout_data: Information on graph after zooming/panning
    :type relayout_data: dict
    :param get_app_data_args: Args previously passed to get app data fn
    :type get_app_data_args: dict
    :return: New main graph and new args for getting app data
    :rtype: (plotly.graph_objects.Figure, dict)
    """
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"]

    if trigger == "selected-nodes.data":
        get_app_data_args["selected_nodes"] = selected_nodes
        new_main_fig = get_main_fig(get_app_data(**get_app_data_args))
    elif trigger == "main-graph.relayoutData":
        try:
            x1 = relayout_data["xaxis.range[0]"]
            x2 = relayout_data["xaxis.range[1]"]
            y1 = relayout_data["yaxis.range[0]"]
            y2 = relayout_data["yaxis.range[1]"]
        except KeyError:
            raise PreventUpdate

        get_app_data_args["xaxis_range"] = [x1, x2]
        get_app_data_args["yaxis_range"] = [y1, y2]
        new_main_fig = get_main_fig(get_app_data(**get_app_data_args))
    else:
        msg = "Unexpected trigger trying to update main graph: %s" % trigger
        raise RuntimeError(msg)

    return new_main_fig, get_app_data_args


if __name__ == "__main__":
    app.run_server(debug=True)
