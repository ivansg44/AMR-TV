"""Point of entry for application.

Running this script launches the application.
"""

from sys import maxsize

import dash
from dash import Dash
from dash.dependencies import (ClientsideFunction,
                               Input,
                               Output,
                               State,
                               ALL,
                               MATCH)
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_html_components import Div

from data_parser import get_app_data, parse_fields_from_example_file
from main_fig_generator import (get_main_figs,
                                get_main_fig_x_axis,
                                get_main_fig_y_axis)
from modal_generator import (get_upload_data_modal,
                             get_create_config_file_modal,
                             get_create_config_modal_form,
                             get_duplicating_select_field,
                             get_duplicating_link_section,
                             get_duplicating_attr_filter_section)
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
        dcc.Store("new-upload"),
        dcc.Store("example-file-field-opts"),
        dcc.Store("config-file-generation-started", data=False)
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
def edit_upload_data_modal_after_sample_file_upload(_, filename):
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
def edit_upload_data_modal_after_config_file_upload(_, filename):
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
    """Edit viz btn color after user uploads all files.

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
    Output("select-example-file-btn", "children"),
    Output("select-example-file-btn", "color"),
    Input("upload-example-file", "filename"),
    prevent_initial_call=True
)
def edit_create_config_modal_after_example_file_upload(filename):
    """TODO"""
    return filename, "success"


@app.callback(
    Output("create-config-file-modal-form", "children"),
    Output("generate-config-file-btn", "color"),
    Output("example-file-field-opts", "data"),
    Input("upload-example-file", "contents"),
    Input("delimiter-select", "value"),
    prevent_initial_call=True
)
def add_create_config_modal_form(example_file_contents, delimiter):
    """TODO"""
    if None in [example_file_contents, delimiter]:
        raise PreventUpdate

    example_file_base64_str = example_file_contents.split(",")[1]
    example_file_fields = \
        parse_fields_from_example_file(example_file_base64_str, delimiter)
    example_file_field_opts = \
        [{"label": None, "value": None}] \
        + [{"label": e, "value": e} for e in example_file_fields]

    form = get_create_config_modal_form(example_file_field_opts)

    return form, "primary", example_file_field_opts


@app.callback(
    Output({"type": "create-config-modal-help-alert", "index": MATCH},
           "is_open"),
    Input({"type": "create-config-modal-help-btn", "index": MATCH},
          "n_clicks"),
    State({"type": "create-config-modal-help-alert", "index": MATCH},
          "is_open"),
    prevent_initial_call=True
)
def toggle_create_config_modal_help_alert(_, is_already_open):
    """TODO"""
    return not is_already_open


@app.callback(
    Output({"type": "expandable-create-config-form-col", "index": MATCH},
           "children"),
    Input({"type": "expandable-create-config-form-btn", "index": MATCH},
          "n_clicks"),
    State({"type": "expandable-create-config-form-col", "index": MATCH},
          "children"),
    State({"type": "expandable-create-config-form-col", "index": MATCH},
          "id"),
    State("example-file-field-opts", "data"),
    prevent_initial_call=True
)
def expand_create_config_modal_form(_, existing_divs, col_id,
                                    example_file_field_opts):
    """TODO"""
    col_index = col_id["index"]
    nested_select_fields = ["all-eq-fields", "all-neq-fields", "any-eq-fields"]

    if not len(existing_divs):
        most_recent_index = None
    else:
        most_recent_index = existing_divs[-1]["props"]["id"]["index"]

    if col_index == "link-config":
        unique_index = 1 if most_recent_index is None else most_recent_index+1
        new_input_div = get_duplicating_link_section(example_file_field_opts,
                                                     unique_index)
    elif col_index.startswith("attr-filter-fields"):
        prefix = col_index.split("-")[-1]
        if most_recent_index is None:
            unique_index = prefix + "-1"
        else:
            suffix = most_recent_index.split("-")[-1]
            unique_index = prefix + "-" + str(int(suffix) + 1)
        new_input_div = \
            get_duplicating_attr_filter_section(example_file_field_opts,
                                                unique_index)
    elif any([col_index.startswith(e) for e in nested_select_fields]):
        if col_index.startswith("all_eq_fields"):
            type_ = "all-eq-select"
        elif col_index.startswith("all_neq_fields"):
            type_ = "all-neq-select"
        else:
            type_ = "any-eq-select"

        prefix = col_index.split("-")[-1]
        if most_recent_index is None:
            unique_index = prefix + "-1"
        else:
            suffix = most_recent_index.split("-")[-1]
            unique_index = prefix + "-" + str(int(suffix) + 1)
        new_input_div = \
            get_duplicating_select_field(example_file_field_opts,
                                         type_,
                                         unique_index)
    else:
        unique_index = 1 if most_recent_index is None else most_recent_index+1
        new_input_div = get_duplicating_select_field(example_file_field_opts,
                                                     col_index,
                                                     unique_index)

    new_div = Div(
        [
            dbc.Row(
                dbc.Col(
                    dbc.Button("Delete",
                               id={
                                   "type": "contractable-create-config-form"
                                           "-btn",
                                   "expandable-col-index": col_index,
                                   "index": unique_index
                               },
                               color="danger",
                               size="sm",
                               className="p-0"),
                    className="text-right",
                    width={"offset": 10, "size": 2}
                ),
                className="mb-1"
            ),
            new_input_div
        ],
        id={"type": "contractable-create-config-form-div",
            "expandable-col-index": col_index,
            "index": unique_index}
    )

    return existing_divs + [new_div]


@app.callback(
    Output({"type": "contractable-create-config-form-div",
            "expandable-col-index": MATCH,
            "index": MATCH},
           "children"),
    Input({"type": "contractable-create-config-form-btn",
            "expandable-col-index": MATCH,
            "index": MATCH},
          "n_clicks"),
    prevent_initial_call=True
)
def contract_create_config_modal_form(_):
    """TODO"""
    return None


@app.callback(
    Output("config-file-generation-started", "data"),
    Input("generate-config-file-btn", "n_clicks"),
    State("generate-config-file-btn", "color"),
    prevent_initial_call=True
)
def start_config_file_generation(_, btn_color):
    """TODO"""
    if btn_color != "primary":
        raise PreventUpdate

    return True

@app.callback(
    Output("config-error-msg-label", "children"),
    Output("config-error-msg-col", "style"),
    Output("date-field-select", "invalid"),
    Output("date-input-format-input", "invalid"),
    Output("date-output-format-input", "invalid"),
    Output({"type": "y-axis-fields", "index": 0}, "invalid"),
    Input("config-file-generation-started", "data"),
    State("date-field-select", "value"),
    State("date-input-format-input", "value"),
    State("date-output-format-input", "value"),
    State("links-across-primary-y-checkbox", "checked"),
    State("max-day-range-input", "value"),
    State("empty-strings-are-null-checkbox", "checked"),
    State("null-vals-textarea", "value"),
    State({"type": "y-axis-fields", "index": 0}, "value"),
    State({"type": "y-axis-fields", "index": ALL}, "value"),
    State({"type": "node-label-fields", "index": ALL}, "value"),
    State({"type": "node-color-fields", "index": ALL}, "value"),
    State({"type": "node-symbol-fields", "index": ALL}, "value"),
    State({"type": "link-label", "index": ALL}, "id"),
    State({"type": "link-label", "index": ALL}, "value"),
    State({"type": "link-minimize-loops", "index": ALL}, "id"),
    State({"type": "link-minimize-loops", "index": ALL}, "checked"),
    State({"type": "link-arrowheads", "index": ALL}, "id"),
    State({"type": "link-arrowheads", "index": ALL}, "checked"),
    State({"type": "link-weight-exp", "index": ALL}, "id"),
    State({"type": "link-weight-exp", "index": ALL}, "value"),
    State({"type": "link-weight-lt", "index": ALL}, "id"),
    State({"type": "link-weight-lt", "index": ALL}, "value"),
    State({"type": "link-weight-gt", "index": ALL}, "id"),
    State({"type": "link-weight-gt", "index": ALL}, "value"),
    State({"type": "link-weight-neq", "index": ALL}, "id"),
    State({"type": "link-weight-neq", "index": ALL}, "value"),
    State({"type": "link-attr-filter-select", "index": ALL}, "id"),
    State({"type": "link-attr-filter-select", "index": ALL}, "value"),
    State({"type": "link-attr-filter-textarea", "index": ALL}, "value"),
    State({"type": "link-all-eq-select", "index": ALL}, "id"),
    State({"type": "link-all-eq-select", "index": ALL}, "value"),
    State({"type": "link-all-neq-select", "index": ALL}, "id"),
    State({"type": "link-all-neq-select", "index": ALL}, "value"),
    State({"type": "link-any-eq-select", "index": ALL}, "id"),
    State({"type": "link-any-eq-select", "index": ALL}, "value"),
    prevent_initial_call=True
)
def continue_config_file_generation(started, date_field, date_input_format,
                                    date_output_format, links_across_primary_y,
                                    max_day_range, empty_strings_are_null,
                                    null_vals_textarea, first_y_axis_field,
                                    y_axis_fields, node_label_fields,
                                    node_color_fields, node_symbol_fields,
                                    link_label_ids, link_label_vals,
                                    link_min_loop_ids, link_min_loop_vals,
                                    link_arrowhead_ids, link_arrowhead_vals,
                                    link_weight_exp_ids, link_weight_exp_vals,
                                    link_weight_lt_ids, link_weight_lt_vals,
                                    link_weight_gt_ids, link_weight_gt_vals,
                                    link_weight_neq_ids, link_weight_neq_vals,
                                    link_attr_filter_ids,
                                    link_attr_filter_select_vals,
                                    link_attr_filter_textarea_vals,
                                    link_all_eq_ids, link_all_eq_vals,
                                    link_all_neq_ids, link_all_neq_vals,
                                    link_any_eq_ids, link_any_eq_vals,):
    """TODO"""
    if not started:
        raise PreventUpdate

    mandatory_fields = [date_field,
                        date_input_format,
                        date_output_format,
                        first_y_axis_field]
    field_invalidity_list = \
        [True if e is None or e == "" else False for e in mandatory_fields]
    if any(field_invalidity_list):
        return "Missing required values", \
               {"visibility": "visible"}, \
               *field_invalidity_list

    if max_day_range is None:
        max_day_range = maxsize
    elif max_day_range < 0:
        return "Invalid number in highlighted input", \
               {"visibility": "visible"}, \
               *field_invalidity_list

    null_vals = []
    if empty_strings_are_null:
        null_vals.append("")
    if null_vals_textarea is not None and null_vals_textarea != "":
        null_vals += null_vals_textarea.split(";")

    return None, {"visibility": "hidden"}, *field_invalidity_list


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
