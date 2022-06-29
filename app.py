"""Point of entry for application.

Running this script launches the application.
"""

import dash
from dash import Dash
from dash.dash import no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from data_parser import get_app_data
from main_fig_generator import get_main_figs
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
            dbc.Col(
                dbc.Button("Upload data",
                           id="upload-data-btn",
                           color="primary")
            ),
            className="my-1"
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Tabs(
                        children=[
                            dbc.Tab(
                                dcc.Graph(
                                    figure={},
                                    id="main-graph",
                                    config={"displayModeBar": False}
                                ),
                                label="Zoomed in",
                                style={"height": "90vh",
                                       "width": "80vw",
                                       "overflow": "scroll"}
                            ),
                            dbc.Tab(
                                dcc.Graph(
                                    figure={},
                                    id="zoomed-out-main-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "85vh",
                                           "width": "75vw"}
                                ),
                                label="Zoomed out",
                                style={"height": "90vh",
                                       "width": "80vw"}
                            )
                        ]
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
        # TODO probably a separate file for modal generation later
        dbc.Modal(
            [
                dbc.ModalHeader("Upload data"),
                dbc.ModalBody([
                    dcc.Upload(
                        dbc.Button("Select sample data file",
                                   id="select-sample-file-btn"),
                        id="upload-sample-file"
                    ),
                    dcc.Upload(
                        dbc.Button("Select config file",
                                   id="select-config-file-btn"),
                        id="upload-config-file",
                        className="mt-1"
                    )
                ]),
                dbc.ModalFooter(
                    dbc.Button("Visualize", id="viz-btn")
                )
            ],
            id="upload-data-modal"
        ),
        dcc.Store(id="selected-nodes", data={}),
        # TODO remove ranges and dragmode
        dcc.Store(id="xaxis-range"),
        dcc.Store(id="yaxis-range"),
        dcc.Store(id="dragmode", data="zoom"),
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
        msg = "Unexpected trigger trying to toggle modal: %s" % trigger
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
    inputs=Input("main-graph", "relayoutData"),
    state= State("dragmode", "data"),
    output=[
        Output("xaxis-range", "data"),
        Output("yaxis-range", "data"),
        Output("dragmode", "data")
    ],
    prevent_initial_call=True
)
def update_ranges(relayout_data, dragmode):
    """Update axes range and drag mode browser vars after relayout.
    TODO remove this

    :param relayout_data: Information on graph after automatic Plotly-
        or user-driven layout updates
    :type relayout_data: dict
    :param dragmode: Current dragmode of main graph Plotly fig
    :type dragmode: str
    :return: New xaxis and yaxis ranges, and new dragmode
    :rtype: (list, list, str)
    :raises PreventUpdate: In certain situations, we do not want to
        update anything.
    """
    # Fires when figure first loads
    if "autosize" in relayout_data:
        raise PreventUpdate

    # When fig gets autoscaled or reset
    autorange_keys = ["xaxis.autorange", "yaxis.autorange"]
    if any(k in relayout_data for k in autorange_keys):
        return None, None, "zoom"

    # User decides to show spikes
    showspikes_keys = ["xaxis.showspikes", "yaxis.showspikes"]
    if any(k in relayout_data for k in showspikes_keys):
        raise PreventUpdate

    # Switching b/w zoom, pan, lasso, etc.
    if "dragmode" in relayout_data:
        return no_update, no_update, relayout_data["dragmode"]

    try:
        x1 = relayout_data["xaxis.range[0]"]
        x2 = relayout_data["xaxis.range[1]"]
        y1 = relayout_data["yaxis.range[0]"]
        y2 = relayout_data["yaxis.range[1]"]
    except KeyError:
        return None, None, no_update

    # Range actually got modified
    return [x1, x2], [y1, y2], dragmode


@app.callback(
    inputs=[
        Input("selected-nodes", "data"),
        Input("xaxis-range", "data"),
        Input("yaxis-range", "data"),
        Input("viz-btn", "n_clicks")
    ],
    state=[
        State("upload-sample-file", "contents"),
        State("upload-config-file", "contents"),
        State("dragmode", "data")
    ],
    output=[
        Output("main-graph", "figure"),
        Output("main-graph", "style"),
        Output("zoomed-out-main-graph", "figure"),
        Output("node-shape-legend-graph", "figure"),
        Output("link-legend-graph", "figure"),
        Output("node-color-legend-graph", "figure"),
    ],
    prevent_initial_call=True
)
def update_main_viz(selected_nodes, xaxis_range, yaxis_range, _,
                    sample_file_contents, config_file_contents, dragmode):
    """Update main graph and legends. TODO
    TODO remove dragmode

    Current triggers:

    * User clicks viz btn (after uploading data)
    * User selects node
    * User zooms/pans across main graph

    :param selected_nodes: Currently selected nodes
    :type selected_nodes: dict
    :param xaxis_range: [xmin, xmax]
    :type xaxis_range: list
    :param yaxis_range: [ymin, ymax]
    :type yaxis_range: list
    :param _: User clicked viz btn
    :param sample_file_contents: Contents of uploaded sample file
    :type sample_file_contents: str
    :param config_file_contents: Contents of uploaded config file
    :type config_file_contents: str
    :param dragmode: Current dragmode for main graph Plotly fig
    :type dragmode: str
    :return: New main graph (including height) and legends
    :rtype: tuple[plotly.graph_objects.Figure]
    """
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"]

    # Do not update if range changed due to user panning graph
    if trigger in ["xaxis-range.data", "yaxis-range.data"]:
        if dragmode == "pan":
            raise PreventUpdate

    if None in [sample_file_contents, config_file_contents]:
        raise PreventUpdate

    sample_file_base64_str = sample_file_contents.split(",")[1]
    config_file_base64_str = config_file_contents.split(",")[1]

    if trigger in ["selected-nodes.data",
                   "xaxis-range.data",
                   "yaxis-range.data"]:
        app_data = get_app_data(sample_file_base64_str,
                                config_file_base64_str,
                                xaxis_range=xaxis_range,
                                yaxis_range=yaxis_range,
                                selected_nodes=selected_nodes)
        main_fig, zoomed_out_main_fig = get_main_figs(app_data)
    elif trigger == "viz-btn.n_clicks":
        app_data = get_app_data(sample_file_base64_str, config_file_base64_str)
        main_fig, zoomed_out_main_fig = get_main_figs(app_data)
    else:
        msg = "Unexpected trigger trying to update main graph: %s" % trigger
        raise RuntimeError(msg)

    main_fig_style = {"height": app_data["main_fig_height"],
                                "width": app_data["main_fig_width"]}
    node_symbol_legend_fig = get_node_symbol_legend_fig(app_data)
    link_legend_fig = get_link_legend_fig(app_data)
    node_color_legend_fig = get_node_color_legend_fig(app_data)

    return (main_fig,
            main_fig_style,
            zoomed_out_main_fig,
            node_symbol_legend_fig,
            link_legend_fig,
            node_color_legend_fig)


if __name__ == "__main__":
    app.run_server(debug=True)
