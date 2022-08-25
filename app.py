"""Point of entry for application.

Running this script launches the application.
"""

import dash
from dash import Dash
from dash.dependencies import ClientsideFunction, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from data_parser import get_app_data
from main_fig_generator import (get_main_figs,
                                get_main_fig_x_axis,
                                get_main_fig_y_axis)
from modal_generator import get_upload_data_modal, get_create_config_file_modal
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

    :param _: Application launched in browser
    :return: Several empty figs for the viz to be, and an upload btn
    :rtype: list
    """
    children = [
        dbc.Row(
            dbc.Col([
                dbc.Button("Upload data",
                           id="upload-data-btn",
                           className="mr-1",
                           color="primary"),
                dbc.Button("Create config file",
                           id="create-config-file-btn")
            ]),
            className="my-1"
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Tabs(
                        children=[
                            dbc.Tab(children=[
                                dbc.Row(children=[
                                    dbc.Col(
                                        dcc.Graph(
                                            figure={},
                                            id="main-graph-y-axis",
                                            config={"displayModeBar": False},
                                            style={"height": "100%",
                                                   "width": "100%"}
                                        ),
                                        id="main-graph-y-axis-col",
                                        className="p-0",
                                        style={"height": "80vh",
                                               "width": "10vw",
                                               "overflow": "hidden"},
                                        width=2
                                    ),
                                    dbc.Col(
                                        dcc.Graph(
                                            figure={},
                                            id="main-graph",
                                            config={"displayModeBar": False},
                                            style={"height": "100%",
                                                   "width": "100%"}
                                        ),
                                        id="main-graph-col",
                                        className="p-0",
                                        style={"height": "80vh",
                                               "width": "70vw",
                                               "overflow": "scroll"},
                                        width=10
                                    ),
                                ]),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(
                                            figure={},
                                            id="main-graph-x-axis",
                                            config={"displayModeBar": False},
                                            style={"height": "100%",
                                                   "width": "100%"}
                                        ),
                                        id="main-graph-x-axis-col",
                                        className="p-0",
                                        style={"height": "10vh",
                                               "width": "70vw",
                                               "overflow": "hidden"},
                                        width={"size": 10, "offset": 2}
                                    ),
                                )],
                                id="main-graph-tab",
                                tab_id="main-graph-tab",
                                label="Zoomed in",
                                style={"height": "90vh",
                                       "width": "80vw"}
                            ),
                            dbc.Tab(
                                dcc.Graph(
                                    figure={},
                                    id="zoomed-out-main-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "85vh",
                                           "width": "75vw"}
                                ),
                                id="zoomed-out-main-graph-tab",
                                label="Zoomed out",
                                style={"height": "90vh",
                                       "width": "80vw"}
                            )
                        ],
                        id="main-viz-tabs"
                    )
                ),
                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    figure={},
                                    id="node-shape-legend-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "30vh"}
                                ),
                            ),
                        ),
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    figure={},
                                    id="link-legend-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "30vh"}

                                ),
                            ),
                        ),
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    figure={},
                                    id="node-color-legend-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "30vh"}

                                ),
                            ),
                        )
                    ],
                    width=2
                )
            ]
        ),
        get_upload_data_modal(),
        get_create_config_file_modal(),
        dcc.Store(id="selected-nodes", data={}),
        dcc.Store(id="added-scroll-handlers", data=False),
        dcc.Store("new-upload")
    ]

    return children


@app.callback(
    Output("upload-data-modal", "is_open"),
    inputs=[
        Input("upload-data-btn", "n_clicks"),
        Input("main-graph", "figure"),
    ],
    prevent_intial_call=True
)
def toggle_upload_data_modal(_, __):
    """Toggle upload data modal.

    Current triggers:

    * Clicking upload data btn -> open
    * New data vized -> closed

    :param _: Upload btn clicked
    :param __: New data viz
    :return: Whether modal is open or closed
    :rtype: bool
    :raise RuntimeError: Unexpected trigger trying to toggle modal
    """
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"]
    if trigger == ".":
        raise PreventUpdate
    elif trigger == "upload-data-btn.n_clicks":
        return True
    elif trigger == "main-graph.figure":
        return False
    else:
        msg = "Unexpected trigger trying to " \
              "toggle upload data modal: %s" % trigger
        raise RuntimeError(msg)


@app.callback(
    Output("select-sample-file-btn", "children"),
    Output("select-sample-file-btn", "color"),
    Input("upload-sample-file", "contents"),
    Input("upload-sample-file", "filename"),
    prevent_initial_call=True
)
def edit_modal_after_sample_file_upload(_, filename):
    """Edit upload data modal css after user uploads sample file.

    Current changes:

    * Filename replaces content of upload sample file btn
    * Upload sample file btn color changes

    :param _: User uploaded sample file
    :param filename: Sample filename
    :type filename: str
    :return: Text inside upload sample file btn, and btn color
    :rtype: (str, str)
    """
    return filename, "success"


@app.callback(
    Output("select-config-file-btn", "children"),
    Output("select-config-file-btn", "color"),
    Input("upload-config-file", "contents"),
    Input("upload-config-file", "filename"),
    prevent_initial_call=True
)
def edit_modal_after_config_file_upload(_, filename):
    """Edit upload data modal css after user uploads config file.

    Current changes:

    * Filename replaces content of upload config file btn
    * Upload config file btn color changes

    :param _: User uploaded config file
    :param filename: Config filename
    :type filename: str
    :return: Text inside upload config file btn, and btn color
    :rtype: (str, str)
    """
    return filename, "success"


@app.callback(
    Output("viz-btn", "color"),
    Input("upload-sample-file", "contents"),
    Input("upload-config-file", "contents"),
    prevent_initial_call=True
)
def toggle_viz_btn_color(sample_file_contents, config_file_contents):
    """"Edit viz btn color after user uploads all files.

    :param sample_file_contents: Contents of uploaded sample file
    :type sample_file_contents: str
    :param config_file_contents: Contents of upload config file
    :type config_file_contents: str
    :return: New viz btn color
    :rtype: str
    """
    if None not in [sample_file_contents, config_file_contents]:
        return "primary"
    else:
        return "secondary"


@app.callback(
    Output("create-config-file-modal", "is_open"),
    inputs=[
        Input("create-config-file-btn", "n_clicks")
    ],
    prevent_intial_call=True
)
def toggle_create_config_file_modal(_):
    """TODO"""
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"]
    if trigger == ".":
        raise PreventUpdate
    elif trigger == "create-config-file-btn.n_clicks":
        return True
    else:
        msg = "Unexpected trigger trying to " \
              "toggle create config file modal: %s" % trigger
        raise RuntimeError(msg)


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
    :type selected_nodes: dict
    :return: New table of selected nodes
    :rtype: dict
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
        Input("viz-btn", "n_clicks")
    ],
    state=[
        State("upload-sample-file", "contents"),
        State("upload-config-file", "contents")
    ],
    output=[
        Output("main-graph", "figure"),
        Output("main-graph", "style"),
        Output("main-graph-x-axis", "figure"),
        Output("main-graph-x-axis", "style"),
        Output("main-graph-y-axis", "figure"),
        Output("main-graph-y-axis", "style"),
        Output("zoomed-out-main-graph", "figure"),
        Output("node-shape-legend-graph", "figure"),
        Output("link-legend-graph", "figure"),
        Output("node-color-legend-graph", "figure")
    ],
    prevent_initial_call=True
)
def update_main_viz(selected_nodes, _, sample_file_contents,
                    config_file_contents):
    """Update main graph, axes, zoomed-out main graph, and legends.

    Current triggers:

    * User clicks viz btn (after uploading data)
    * User selects node in main graph

    :param selected_nodes: Currently selected nodes
    :type selected_nodes: dict
    :param _: User clicked viz btn
    :param sample_file_contents: Contents of uploaded sample file
    :type sample_file_contents: str
    :param config_file_contents: Contents of uploaded config file
    :type config_file_contents: str
    :return: New main graphs, axes, and legends
    :rtype: tuple[plotly.graph_objects.Figure]
    """
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"]

    if None in [sample_file_contents, config_file_contents]:
        raise PreventUpdate

    sample_file_base64_str = sample_file_contents.split(",")[1]
    config_file_base64_str = config_file_contents.split(",")[1]

    if trigger == "selected-nodes.data":
        app_data = get_app_data(sample_file_base64_str,
                                config_file_base64_str,
                                selected_nodes=selected_nodes)
        main_fig, zoomed_out_main_fig = get_main_figs(app_data)
    elif trigger == "viz-btn.n_clicks":
        app_data = get_app_data(sample_file_base64_str, config_file_base64_str)
        main_fig, zoomed_out_main_fig = get_main_figs(app_data)
    else:
        msg = "Unexpected trigger trying to update main graph: %s" % trigger
        raise RuntimeError(msg)

    main_fig_x_axis = get_main_fig_x_axis(app_data)
    main_fig_x_axis_style = {"height": "100%",
                             "width": app_data["main_fig_width"]}

    main_fig_y_axis = get_main_fig_y_axis(app_data)
    main_fig_y_axis_style = {"height": app_data["main_fig_height"],
                             "width": "100%"}

    main_fig_style = {"height": app_data["main_fig_height"],
                      "width": app_data["main_fig_width"]}
    node_symbol_legend_fig = get_node_symbol_legend_fig(app_data)
    link_legend_fig = get_link_legend_fig(app_data)
    node_color_legend_fig = get_node_color_legend_fig(app_data)

    return (main_fig,
            main_fig_style,
            main_fig_x_axis,
            main_fig_x_axis_style,
            main_fig_y_axis,
            main_fig_y_axis_style,
            zoomed_out_main_fig,
            node_symbol_legend_fig,
            link_legend_fig,
            node_color_legend_fig)


# Switch to main graph tab and scroll to corresponding node, after
# clicking node in zoomed-out main graph.
app.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="scrollToNode"
    ),
    Output("main-viz-tabs", "active_tab"),
    Output("zoomed-out-main-graph", "clickData"),
    Input("zoomed-out-main-graph", "clickData"),
    prevent_initial_call=True
)
# Add event handlers to main graph axes figs to sync scrolling w/ main
# graph.
app.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="addMainVizScrollHandlers"
    ),
    Output("added-scroll-handlers", "data"),
    Input("main-graph", "figure"),
    prevent_initial_call=True
)

if __name__ == "__main__":
    app.run_server(debug=True)
