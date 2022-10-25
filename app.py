"""Point of entry for application.

Running this script launches the application.
"""

from json import dumps
from pathlib import Path
from sys import maxsize

import dash
from dash import Dash
from dash.dash import no_update
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
import plotly.graph_objects as go

from data_parser import get_app_data, parse_fields_from_example_file
from main_fig_generator import (get_main_fig,
                                get_zoomed_out_main_fig,
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
                                               "overflowY": "scroll"},
                                        width=2
                                    ),
                                    dbc.Col(
                                        dcc.Graph(
                                            figure={},
                                            id="main-graph",
                                            config={"displayModeBar": False,
                                                    "scrollZoom": True},
                                            style={"height": "100%",
                                                   "width": "100%"}
                                        ),
                                        id="main-graph-col",
                                        className="p-0",
                                        style={"height": "80vh",
                                               "width": "70vw",
                                               "overflow": "hidden"},
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
                                               "overflowX": "scroll"},
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
        dcc.Store("config-file-generation-started", data=False),
        dcc.Store("config-json-str", data=""),
        dcc.Download(id="download-config-json-str")
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
    Output("select-matrix-file-btn", "children"),
    Output("select-matrix-file-btn", "color"),
    Input("upload-matrix-file", "contents"),
    Input("upload-matrix-file", "filename"),
    prevent_initial_call=True
)
def edit_upload_data_modal_after_matrix_file_upload(_, filename):
    """TODO"""
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
    """Toggle create config modal.

    :param _: Create config file btn clicked
    :return: Whether modal is open or closed
    :rtype: bool
    :raise RuntimeError: Unexpected trigger trying to toggle modal
    """
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
    Input("upload-example-file", "contents"),
    Input("upload-example-file", "filename"),
    prevent_initial_call=True
)
def edit_create_config_modal_after_example_file_upload(_, filename):
    """Edit create config modal css after user uploads example file.

    Current changes:

    * Filename replaces content of upload example file btn
    * Upload example file btn color changes

    :param _: User uploaded example file
    :param filename: Example filename
    :type filename: str
    :return: Text inside upload example file btn, and btn color
    :rtype: (str, str)
    """
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
    """Add form to create config modal.

    This is called when the user uploads an example file OR selects a
    delimiter, but we only want to add the form if both actions have
    been completed.

    We also change the color of the btn at the bottom of the create
    config modal for actually generating the file, and we store the
    example file field select opts in a browser var.

    :param example_file_contents: User-uploaded example file contents
    :type example_file_contents: str
    :param delimiter: User-specified example file delimiter
    :type delimiter: str
    :return: Create config modal form, color of btn for actually
        generating config file, and example file fields select opts
        browser var.
    :rtype: (list[dbc.Row], str, list)
    """
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
    """Toggle a help alert in create config modal.

    :param _: User clicked help btn for an alert
    :param is_already_open: Is the alert already open?
    :type is_already_open: bool
    :return: Open status for alert specific to help btn user clicked
    :rtype: bool
    """
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
    """Add divs to create config modal form after user clicks add btn.

    :param _: User clicked add btn in create config modal section
    :param existing_divs: Existing divs in the section we plan to add
        another div to.
    :type existing_divs: list
    :param col_id: ID of section corresponding to add btn user clicked
    :type col_id: dict
    :param example_file_field_opts: Example file fields select opts
        browser var.
    :type example_file_field_opts: list
    :return: New div to add to section of form corresponding to add btn
        user clicked.
    :rtype: Div
    """
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
        if col_index.startswith("all-eq-fields"):
            type_ = "link-all-eq-select"
        elif col_index.startswith("all-neq-fields"):
            type_ = "link-all-neq-select"
        else:
            type_ = "link-any-eq-select"

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
    """Del divs from create config modal after user clicks del btn.

    Basically we just empty the outer div, so we will have an empty div
    left on the page.

    :param _: User clicked del btn in create config modal section
    :return: Content of outer div containing div user wants to remove
    :rtype: None
    """
    return None


@app.callback(
    Output("config-file-generation-started", "data"),
    Input("generate-config-file-btn", "n_clicks"),
    State("generate-config-file-btn", "color"),
    prevent_initial_call=True
)
def start_config_file_generation(_, btn_color):
    """Start generating the config file.

    We populate the config file generation started browser var, which
    starts the next phase. We do not proceed if the btn is not the
    right color yet.

    :param _: User clicked btn for generating config file
    :param btn_color: Color of btn for generating config file when user
        clicked it.
    :type btn_color: str
    :return: Config file generation started browser var
    :rtype: bool
    """
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
    Output({"type": "link-label", "index": ALL}, "invalid"),
    Output("config-json-str", "data"),
    Input("config-file-generation-started", "data"),
    State("delimiter-select", "value"),
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
    State({"type": "link-config", "index": ALL}, "id"),
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
def continue_config_file_generation(started, delimiter,
                                    date_field, date_input_format,
                                    date_output_format, links_across_primary_y,
                                    max_day_range, empty_strings_are_null,
                                    null_vals_textarea, first_y_axis_field,
                                    y_axis_fields, node_label_fields,
                                    node_color_fields, node_symbol_fields,
                                    link_config_ids,
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
    """Continue generating the config file.

    We populate the config json str browser var, which proceeds to the
    next phase of download.

    :param started: Config file generation started browser var
    :type started: bool
    :param delimiter: User-specified example file delimiter
    :type delimiter: str
    :param date_field: User-specified date field
    :type date_field: str
    :param date_input_format: User-specified date input format
    :type date_input_format: str
    :param date_output_format: User-specified date output format
    :type date_output_format: str
    :param links_across_primary_y: Whether we draw links across primary
        y vals.
    :type links_across_primary_y: bool
    :param max_day_range: Maximum day range over which we draw links
    :type max_day_range: int | None
    :param empty_strings_are_null: Whether empty strs are null vals
    :type empty_strings_are_null: bool
    :param null_vals_textarea: Semicolon delimited null vals
    :type null_vals_textarea: str | None
    :param first_y_axis_field: Primary y-axis field
    :type first_y_axis_field: str
    :param y_axis_fields: All y-axis fields
    :type y_axis_fields: list[str]
    :param node_label_fields: Node label fields
    :type node_label_fields: list[str]
    :param node_color_fields: Node color fields
    :type node_color_fields: list[str]
    :param node_symbol_fields: Node symbol fields
    :type node_symbol_fields: list[str]
    :param link_config_ids: IDs of link config sections
    :type link_config_ids: list[dict]
    :param link_label_ids: IDs of link label inputs
    :type link_label_ids: list[dict]
    :param link_label_vals: Vals of link label inputs
    :type link_label_vals: list[str]
    :param link_min_loop_ids: IDs of link min loop checkboxes
    :type link_min_loop_ids: list[dict]
    :param link_min_loop_vals: Vals of link min loop checkboxes
    :type link_min_loop_vals: list[bool]
    :param link_arrowhead_ids: IDs of link arrowhead checkboxes
    :type link_arrowhead_ids: list[dict]
    :param link_arrowhead_vals: Vals of link arrowhead checkboxes
    :type link_arrowhead_vals: list[bool]
    :param link_weight_exp_ids: IDs of link weight exp inputs
    :type link_weight_exp_ids: list[dict]
    :param link_weight_exp_vals: Vals of link weight exp inputs
    :type link_weight_exp_vals: list[str]
    :param link_weight_lt_ids: IDs of link weight less than filters
    :type link_weight_lt_ids: list[dict]
    :param link_weight_lt_vals: Vals of link weight less than filters
    :type link_weight_lt_vals: list[int]
    :param link_weight_gt_ids: IDs of link weight greater than filters
    :type link_weight_gt_ids: list[dict]
    :param link_weight_gt_vals: Vals of link weight greater than
        filters.
    :type link_weight_gt_vals: list[int]
    :param link_weight_neq_ids: IDs of link weight not equal filters
    :type link_weight_neq_ids: list[dict]
    :param link_weight_neq_vals: Semicolon-delimited vals of link
        weight not equal filters.
    :type link_weight_neq_vals: list[str]
    :param link_attr_filter_ids: IDs of link attr filters
    :type link_attr_filter_ids: list[dict]
    :param link_attr_filter_select_vals: Attr filter select vals
    :type link_attr_filter_select_vals: list[list[str]]
    :param link_attr_filter_textarea_vals: Attr filter textarea
        semicolon-delimited vals.
    :type link_attr_filter_textarea_vals: list[str]
    :param link_all_eq_ids: IDs of link all eq inputs
    :type link_all_eq_ids: list[dict]
    :param link_all_eq_vals: Vals of link all eq inputs
    :type link_all_eq_vals: list[list]
    :param link_all_neq_ids: IDs of link all neq inputs
    :type link_all_neq_ids: list[dict]
    :param link_all_neq_vals: Vals of link all neq inputs
    :type link_all_neq_vals: list[list]
    :param link_any_eq_ids: IDs of link any eq inputs
    :type link_any_eq_ids: list[dict]
    :param link_any_eq_vals: Vals of link any eq inputs
    :type link_any_eq_vals: list[list]
    :return: Error message label and style (if there is one), and the
        invalid values for some fields, and the config json str var.
    :rtype: tuple[str, dict, tuple[bool], list[bool]]
    """
    if not started:
        raise PreventUpdate

    mandatory_non_link_fields = [date_field,
                                 date_input_format,
                                 date_output_format,
                                 first_y_axis_field]
    non_link_field_invalidity_list = [True if e is None or e == "" else False
                                      for e in mandatory_non_link_fields]
    # Say all the link labels are valid for now
    stub_link_label_invalidity_list = [False for _ in link_label_ids]

    if any(non_link_field_invalidity_list):
        return "Missing required values", \
               {"visibility": "visible"}, \
               *non_link_field_invalidity_list, \
               stub_link_label_invalidity_list, \
               ""

    if max_day_range is None:
        max_day_range = maxsize
    elif max_day_range < 0:
        return "Invalid number in highlighted input", \
               {"visibility": "visible"}, \
               *non_link_field_invalidity_list, \
               stub_link_label_invalidity_list, \
               ""

    null_vals = []
    if empty_strings_are_null:
        null_vals.append("")
    if null_vals_textarea is not None and null_vals_textarea != "":
        null_vals += null_vals_textarea.split(";")

    link_dict = \
        {link_config_id["index"]: {"all_eq": [],
                                   "all_neq": [],
                                   "any_eq": [],
                                   "weight_exp": "",
                                   "weight_filters": {},
                                   "attr_filters": {}}
         for link_config_id in link_config_ids}
    for id_, val in zip(link_label_ids, link_label_vals):
        if val is not None and val != "":
            link_dict[id_["index"]]["label"] = val
    for id_, val in zip(link_min_loop_ids, link_min_loop_vals):
        link_dict[id_["index"]]["minimize_loops"] = int(val)
    for id_, val in zip(link_arrowhead_ids, link_arrowhead_vals):
        link_dict[id_["index"]]["show_arrowheads"] = int(val)
    for id_, val in zip(link_weight_exp_ids, link_weight_exp_vals):
        if val is None:
            val = ""
        link_dict[id_["index"]]["weight_exp"] = val
    for id_, val in zip(link_weight_lt_ids, link_weight_lt_vals):
        if val is not None and val != "":
            link_dict[id_["index"]]["weight_filters"]["less_than"] = val
    for id_, val in zip(link_weight_gt_ids, link_weight_gt_vals):
        if val is not None and val != "":
            link_dict[id_["index"]]["weight_filters"]["greater_than"] = val
    for id_, val in zip(link_weight_neq_ids, link_weight_neq_vals):
        if val is not None and val != "":
            val_list = val.split(";")
            link_dict[id_["index"]]["weight_filters"]["not_equal"] = val_list
    for id_, select_val, textarea_val in zip(link_attr_filter_ids,
                                             link_attr_filter_select_vals,
                                             link_attr_filter_textarea_vals):
        link_index = int(id_["index"].split("-")[0])
        cond = select_val is not None and select_val != ""
        cond &= textarea_val is not None and textarea_val != ""
        if cond:
            textarea_val_list = textarea_val.split(";")
            link_dict[link_index]["attr_filters"][select_val] = \
                textarea_val_list
    for id_, val in zip(link_all_eq_ids, link_all_eq_vals):
        link_index = int(id_["index"].split("-")[0])
        if val is not None and val != "":
            link_dict[link_index]["all_eq"].append(val)
    for id_, val in zip(link_all_neq_ids, link_all_neq_vals):
        link_index = int(id_["index"].split("-")[0])
        if val is not None and val != "":
            link_dict[link_index]["all_neq"].append(val)
    for id_, val in zip(link_any_eq_ids, link_any_eq_vals):
        link_index = int(id_["index"].split("-")[0])
        if val is not None and val != "":
            link_dict[link_index]["any_eq"].append(val)

    links_config = {}
    link_label_invalidity_list = []
    for link_config_index in link_dict:
        link_config_vals = link_dict[link_config_index]
        if "label" not in link_config_vals:
            partially_filled = (
                len(link_config_vals["all_eq"])
                or len(link_config_vals["all_neq"])
                or len(link_config_vals["any_eq"])
                or link_config_vals["show_arrowheads"]
                or link_config_vals["minimize_loops"]
                or link_config_vals["weight_exp"]
                or link_config_vals["weight_filters"]
                or link_config_vals["attr_filters"]
            )
            if partially_filled:
                link_label_invalidity_list.append(True)
            else:
                link_label_invalidity_list.append(False)
        else:
            label = link_config_vals.pop("label")
            links_config[label] = link_config_vals
            link_label_invalidity_list.append(False)
    if any(link_label_invalidity_list):
        return "Missing link labels", \
               {"visibility": "visible"}, \
               *non_link_field_invalidity_list, \
               link_label_invalidity_list, \
               ""

    config_dict = {
        "delimiter": delimiter,
        "date_attr": date_field,
        "date_input": date_input_format,
        "date_output": date_output_format,
        "links_across_primary_y": int(links_across_primary_y),
        "max_day_range": max_day_range,
        "null_vals": null_vals,
        "y_axes": [[e] for e in y_axis_fields
                   if e is not None or ""],
        "label_attr": [e for e in node_label_fields
                       if e is not None or ""],
        "node_color_attr": [e for e in node_color_fields
                            if e is not None or ""],
        "node_symbol_attr": [e for e in node_symbol_fields
                             if e is not None or ""],
        "links_config": links_config
    }
    config_json_str = dumps(config_dict, indent=2)

    return None, \
           {"visibility": "hidden"}, \
           *non_link_field_invalidity_list, \
           stub_link_label_invalidity_list, \
           config_json_str


@app.callback(
    Output("download-config-json-str", "data"),
    Input("config-json-str", "data"),
    State("upload-example-file", "filename"),
    prevent_initial_call=True
)
def download_config_file(config_json_str, filename):
    """Launch download of generated config file.

    :param config_json_str: In-browser config json str var
    :type config_json_str: str
    :param filename: Uploaded example file filename
    :type filename: str
    :return: New contents for in-browser var that triggers download
    :rtype: dict
    """
    if config_json_str == "":
        raise PreventUpdate
    json_filename = Path(filename).stem + ".json"
    return {"content": config_json_str, "filename": json_filename}


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
        Input("viz-btn", "n_clicks"),
        Input("main-graph", "relayoutData")
    ],
    state=[
        State("upload-sample-file", "contents"),
        State("upload-config-file", "contents"),
        State("upload-matrix-file", "contents"),
        State("main-graph", "figure"),
        State("main-graph-x-axis", "figure"),
        State("main-graph-y-axis", "figure")
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
def update_main_viz(selected_nodes, _, relayout_data, sample_file_contents,
                    config_file_contents, matrix_file_contents, old_main_fig,
                    old_main_fig_x_axis, old_main_fig_y_axis):
    """Update main graph, axes, zoomed-out main graph, and legends.TODO

    Current triggers:

    * User clicks viz btn (after uploading data)
    * User selects node in main graph

    :param selected_nodes: Currently selected nodes
    :type selected_nodes: dict
    :param _: User clicked viz btn
    :param relayout_data: Information on main graph relayout event
    :type relayout_data: dict
    :param sample_file_contents: Contents of uploaded sample file
    :type sample_file_contents: str
    :param config_file_contents: Contents of uploaded config file
    :type config_file_contents: str
    :param old_main_fig: Current main fig
    :type old_main_fig: go.Figure
    :param old_main_fig_x_axis: Current main x-axis fig
    :type old_main_fig_x_axis: go.Figure
    :param old_main_fig_y_axis: Current main y-axis fig
    :type old_main_fig_y_axis: go.Figure
    :return: New main graphs, axes, and legends
    :rtype: tuple[go.Figure]
    """
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"]

    if None in [sample_file_contents, config_file_contents]:
        raise PreventUpdate

    sample_file_base64_str = sample_file_contents.split(",")[1]
    config_file_base64_str = config_file_contents.split(",")[1]
    matrix_file_base64_str = \
        matrix_file_contents.split(",")[1] if matrix_file_contents else None

    if trigger == "selected-nodes.data":
        app_data = get_app_data(sample_file_base64_str,
                                config_file_base64_str,
                                matrix_file_base64_str=matrix_file_base64_str,
                                selected_nodes=selected_nodes)
        zoomed_out_app_data = \
            get_app_data(sample_file_base64_str,
                         config_file_base64_str,
                         matrix_file_base64_str=matrix_file_base64_str,
                         selected_nodes=selected_nodes,
                         vpsc=True)
        main_fig = get_main_fig(app_data)
        zoomed_out_main_fig = get_zoomed_out_main_fig(zoomed_out_app_data)
    elif trigger == "viz-btn.n_clicks":
        app_data = get_app_data(sample_file_base64_str,
                                config_file_base64_str,
                                matrix_file_base64_str=matrix_file_base64_str)
        zoomed_out_app_data = \
            get_app_data(sample_file_base64_str,
                         config_file_base64_str,
                         matrix_file_base64_str=matrix_file_base64_str,
                         vpsc=True)
        main_fig = get_main_fig(app_data)
        zoomed_out_main_fig = get_zoomed_out_main_fig(zoomed_out_app_data)
    elif trigger == "main-graph.relayoutData":
        zoom_keys = ["xaxis.range[0]",
                     "xaxis.range[1]",
                     "yaxis.range[0]",
                     "yaxis.range[1]"]
        autorange_keys = ["xaxis.autorange",
                          "yaxis.autorange"]
        zoom_event = all([e in relayout_data for e in zoom_keys])
        autorange_event = all([e in relayout_data for e in autorange_keys])
        if not zoom_event and not autorange_event:
            raise PreventUpdate

        main_fig = go.Figure(old_main_fig)
        main_fig_x_axis = go.Figure(old_main_fig_x_axis)
        main_fig_y_axis = go.Figure(old_main_fig_y_axis)

        first_x_axis_range = old_main_fig_x_axis["data"][0]["customdata"]
        first_y_axis_range = old_main_fig_y_axis["data"][0]["customdata"]
        old_x_axis_range = old_main_fig_x_axis["layout"]["xaxis"]["range"]

        if zoom_event:
            new_x_axis_range = old_main_fig["layout"]["xaxis"]["range"]
            new_y_axis_range = old_main_fig["layout"]["yaxis"]["range"]
        else:
            new_x_axis_range = first_x_axis_range
            new_y_axis_range = first_y_axis_range

        # Should be about equal across x and y
        change_in_range = new_x_axis_range[1] - new_x_axis_range[0]
        change_in_range /= (first_x_axis_range[1] - first_x_axis_range[0])

        # TODO do not used hardcoded values
        main_fig_nodes_trace = \
            [e for e in old_main_fig["data"]
             if "name" in e and e["name"] == "main_fig_nodes_trace"][0]
        old_marker_size = main_fig_nodes_trace["marker"]["size"]
        new_marker_size = max(1, 24/change_in_range)
        old_textfont_size = main_fig_nodes_trace["textfont"]["size"]
        new_textfont_size = max(1, 16/change_in_range)

        main_fig.update_traces(marker={"size": new_marker_size},
                               textfont={"size": new_textfont_size},
                               selector={"name": "main_fig_nodes_trace"})
        main_fig_x_axis.update_traces(textfont={"size": new_textfont_size},
                                      selector={
                                          "name": "main_fig_x_axis_trace"
                                      })
        main_fig_y_axis.update_traces(textfont={"size": new_textfont_size},
                                      selector={
                                          "name": "main_fig_y_axis_trace"
                                      })

        main_fig.update_layout(xaxis={"range": new_x_axis_range,
                                      "autorange": False},
                               yaxis={"range": new_y_axis_range,
                                      "autorange": False})
        main_fig_x_axis.update_layout(xaxis={"range": new_x_axis_range})
        main_fig_y_axis.update_layout(yaxis={"range": new_y_axis_range})

        return (main_fig,
                no_update,
                main_fig_x_axis,
                no_update,
                main_fig_y_axis,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update)
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
