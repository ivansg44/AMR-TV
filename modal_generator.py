"""Fns for generating modals."""

from sys import maxsize

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_html_components import A, B, Br, Hr, I, P, H5


def get_upload_data_modal():
    """Get modal for uploading data.

    :return: Modal for uploading data
    :rtype: dbc.Modal
    """
    ret = dbc.Modal(
        [
            dbc.ModalHeader("Upload tabular data"),
            dbc.ModalBody([
                dcc.Upload(
                    dbc.Button("Select tabular data file",
                               id="select-sample-file-btn"),
                    id="upload-sample-file"
                ),
                dcc.Upload(
                    dbc.Button("Optional matrix file",
                               id="select-matrix-file-btn",
                               color="light",
                               style={"display": "none"}),
                    id="upload-matrix-file",
                    className="mt-2"
                )
            ]),
            dbc.ModalHeader("Upload config file",
                            id="select-config-file-modal-header",
                            style={"display": "none"}),
            dbc.ModalBody(
                [
                    dcc.Upload(
                        dbc.Button("Select config file",
                                   id="select-config-file-btn"),
                        id="upload-config-file"
                    ),
                    dbc.Button(
                        "...or click here to create one from scratch",
                        id="create-config-file-btn",
                        color="link"
                    )
                ],
                id="select-config-file-modal-body",
                style={"display": "none"}
            ),
            dbc.ModalFooter(
                dbc.Button("Visualize", id="viz-btn")
            )
        ],
        id="upload-data-modal"
    )
    return ret


def get_create_config_file_modal():
    """Get modal for creating config file.

    This does not contain the entire form the user ultimately sees.

    :return: Modal for creating config file
    :rtype: dbc.Modal
    """
    ret = dbc.Modal(
        [
            dbc.ModalHeader("Create config file"),
            dbc.ModalBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Upload(
                                    dbc.Button("Upload sample/example tabular "
                                               "file",
                                               id="select-example-file-btn"),
                                    id="upload-example-file"
                                ),
                                width=8
                            ),
                            dbc.Col(
                                dbc.Select(
                                    id="delimiter-select",
                                    placeholder="Delimiter?",
                                    options=[
                                        {"label": "Tab", "value": "\t"},
                                        {"label": "Comma", "value": ","}
                                    ]
                                )
                            )
                        ]
                    ),
                    Hr()
                ],
                className="pb-0"
            ),
            dbc.ModalBody(
                P(
                    "Upload a delimited data file containing the fields you "
                    "want to generate a config file for, and specify the "
                    "delimiter."
                ),
                id="create-config-file-modal-form",
                style={"height": "60vh", "overflowY": "scroll"}
            ),
            dbc.ModalFooter(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label(None,
                                      id="config-error-msg-label",
                                      color="danger",
                                      className="mb-0"),
                            id="config-error-msg-col",
                            className="text-right my-auto",
                            style={"visibility": "hidden"}
                        ),
                        dbc.Col(
                            dbc.Button("Generate config file",
                                       id="generate-config-file-btn"),
                            className="text-right my-auto",
                            width=6
                        )
                    ],
                    style={"width": "100%"}
                )
            )
        ],
        id="create-config-file-modal"
    )
    return ret


def get_create_config_modal_form(example_file_field_opts):
    """Get full form user sees in create config modal.

    :param example_file_field_opts: Select opts from example file
    :type example_file_field_opts: list
    :return: List of divs containing create config modal form
    :rtype: list
    """
    ret = [
        get_create_config_help_btn("sample-id-fields"),
        get_create_config_help_alert(
            "sample-id-fields",
            [
                P([
                    B("Sample ID field"),
                    " is the field from your data that contains your sample "
                    "identifiers. Hovering over a node will display the "
                    "Sample ID value corresponding to that node. If you "
                    "upload a matrix, the row and column headers must "
                    "correspond to this Sample ID field."
                ])
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Sample ID field:",
                              html_for="sample-field-select"),
                    dbc.Select(
                        id="sample-field-select",
                        options=example_file_field_opts
                    )
                ]
            ),
            className="mb-3"
        ),
        get_create_config_help_btn("date-fields"),
        get_create_config_help_alert(
            "date-fields",
            [
                P([
                    B("Date field"),
                    " is the field from your data that contains sample dates, "
                    "and is ultimately encoded along the x-axis. ",
                    B("Date input format"),
                    " is the format the dates are recorded in your data, and ",
                    B("Date output format"),
                    " is the format you want the dates encoded along the "
                    "x-axis in the resulting visualization."
                ]),
                P([
                    "The format must be entered using the 1989 C standard "
                    "format codes. ",
                    A("Click here for details.",
                      href="https://bit.ly/3wApxGf",
                      target="_blank",
                      rel="noopener noreferrer")
                ]),
                P([
                    I("e.g., "),
                    "July 1, 2021 uses the format %B %d, %Y"
                ])
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Date field:", html_for="date-field-select"),
                    dbc.Select(
                        id="date-field-select",
                        options=example_file_field_opts
                    )
                ]
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Date input format:",
                              html_for="date-input-format-input"),
                    dbc.Input(id="date-input-format-input")
                ]
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Date output format:",
                              html_for="date-output-format-input"),
                    dbc.Input(id="date-output-format-input")
                ]
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("link-across-primary-y-field"),
        get_create_config_help_alert(
            "link-across-primary-y-field",
            [
                P([
                    "The primary y-axis value is the first selected value "
                    "under ",
                    B("y-axis fields"),
                    ". Nodes in the resulting visualization with differing "
                    "primary y-axis values are separated by solid lines. "
                    "Check this box if you do not want to draw links across "
                    "these solid lines, or in other words, between nodes of "
                    "differing primary y-axis values."
                ])
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Checkbox(
                        id="links-across-primary-y-checkbox",
                        checked=False
                    ),
                    width=1
                ),
                dbc.Col(
                    dbc.Label("Draw links b/w nodes w/ different "
                              "primary y-axis values?")
                )
            ],
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("max-day-range-field"),
        get_create_config_help_alert(
            "max-day-range-field",
            [P("Links will not be drawn between nodes that were sampled more "
               "than this many days apart.")]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Do not draw links b/w nodes that are this "
                              "many days apart:",
                              html_for="max-day-range-input"),
                    dbc.Input(
                        id="max-day-range-input",
                        type="number",
                        min=0,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("null-val-fields"),
        get_create_config_help_alert(
            "null-val-fields",
            [
                P([
                    "Use these inputs to specify the values in your data that "
                    "are considered \"null\". ",
                    I("e.g., "),
                    "null;n/a;none"
                ]),
                P([
                    "The visualization will ignore these values when drawing "
                    "links between nodes."
                ])
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(
                            P("Which values in your data should be treated as "
                              "null?")
                        )
                    ),
                    dbc.Row([
                        dbc.Col(
                            dbc.Label("Empty strings?:"),
                            width={"offset": 1}
                        ),
                        dbc.Col(
                            dbc.Checkbox(
                                id="empty-strings-are-null-checkbox",
                                checked=False
                            ),
                            width=1
                        )
                    ]),
                    dbc.Row(
                        dbc.Col(
                            P("Other (please specify):"),
                            width={"offset": 1}
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.Textarea(
                                id="null-vals-textarea",
                                placeholder="Separate multiple values "
                                            "with a semicolon"
                            ),
                            className="p-0",
                            width={"size": 10, "offset": 1}
                        )
                    )
                ]
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("y-axis-fields"),
        get_create_config_help_alert(
            "y-axis-fields",
            [
                P([
                    "These are the fields from your data that will be encoded "
                    "along the y-axis of the visualization. You must select "
                    "at least one field. If you specify more than one field, "
                    "each unique combination of values across the specified "
                    "y-axis fields will occupy one track along the y-axis."
                ]),
                P([
                    I("e.g., "),
                    "if you specify two fields \"fruits\" and \"vegetables\", "
                    "and the possible values for both fields are "
                    "apple/banana and carrot/celery respectively, then there "
                    "will be four tracks along the y-axis:"
                ]),
                P(["apple", Br(), "carrot"]),
                P(["apple", Br(), "celery"]),
                P(["banana", Br(), "carrot"]),
                P(["banana", Br(), "celery"])
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("y-axis field(s):",
                              html_for={"type": "y-axis-fields", "index": 0}),
                    dbc.Select(
                        id={"type": "y-axis-fields", "index": 0},
                        options=example_file_field_opts
                    )
                ]
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": "y-axis-fields"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "y-axis-fields"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("node-label-fields"),
        get_create_config_help_alert(
            "node-label-fields",
            [
                P([
                    "These are the fields from your data that will be used to "
                    "assign a label to each node. If you specify one field, "
                    "each node will be given a label corresponding to their "
                    "value for that particular field. If you specify more "
                    "than one field, the nodes will receive one label for "
                    "each field, with each label separated by a newline "
                    "character."
                ]),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Node label field(s):",
                              html_for={"type": "node-label-fields",
                                        "index": 0}
                              ),
                    dbc.Select(
                        id={"type": "node-label-fields", "index": 0},
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": "node-label-fields"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "node-label-fields"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("node-color-fields"),
        get_create_config_help_alert(
            "node-color-fields",
            [
                P([
                    "These are the fields from your data that will be used to "
                    "assign a color to each node. If you specify one field, "
                    "each unique value from that field will be assigned a "
                    "unique color. If you specify more than one field, each "
                    "unique combination of values across the specified fields "
                    "will be assigned a color."
                ]),
                P([
                    I("e.g., "),
                    "if you specify two fields \"birds\" and \"mammals\", "
                    "and the possible values for both fields are "
                    "eagle/sparrow and dog/monkey respectively, then there "
                    "will be four unique node colors encoding the following "
                    "combination of values:"
                ]),
                P(["eagle", Br(), "dog"]),
                P(["eagle", Br(), "monkey"]),
                P(["sparrow", Br(), "dog"]),
                P(["sparrow", Br(), "monkey"]),
                dbc.Alert("The number of available colors is limited. The "
                          "visualization will not work if there are more than "
                          "12 unique values or combinations to encode.",
                          color="warning")
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Node color field(s):",
                              html_for={"type": "node-color-fields",
                                        "index": 0}),
                    dbc.Select(
                        id={"type": "node-color-fields", "index": 0},
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": "node-color-fields"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "node-color-fields"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("node-symbol-fields"),
        get_create_config_help_alert(
            "node-symbol-fields",
            [
                P([
                    "These are the fields from your data that will be used to "
                    "assign a shape/symbol to each node. If you specify one "
                    "field, each unique value from that field will be "
                    "assigned a unique symbol. If you specify more than one "
                    "field, each unique combination of values across the "
                    "specified fields will be assigned a symbol."
                ]),
                P([
                    I("e.g., "),
                    "if you specify two fields \"utensils\" and \"metals\", "
                    "and the possible values for both fields are "
                    "spoon/fork and steel/silver respectively, then there "
                    "will be four unique node colors encoding the following "
                    "combination of values:"
                ]),
                P(["spoon", Br(), "steel"]),
                P(["spoon", Br(), "silver"]),
                P(["fork", Br(), "steel"]),
                P(["fork", Br(), "silver"]),
                dbc.Alert("The number of available symbols is limited. The "
                          "visualization will not work if there are more than "
                          "6 unique values or combinations to encode.",
                          color="warning")
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Node symbol field(s):",
                              html_for={"type": "node-symbol-fields",
                                        "index": 0}),
                    dbc.Select(
                        id={"type": "node-symbol-fields", "index": 0},
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": "node-symbol-fields"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "node-symbol-fields"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("link-config"),
        get_create_config_help_alert(
            "link-config",
            [
                P([
                    "This section enables you to set the criteria for drawing "
                    "links between nodes. If you click the ",
                    B("Add link config section"),
                    " button at the very bottom, you can add duplicate the "
                    "section below, and set criteria for multiple links."
                ]),
                P([
                   "You do not have to define any links, but if you begin to "
                   "partially complete a link configuration without "
                   "specifying the link label, you will encounter an error "
                   "when generating the config file."
                ]),
                dbc.Alert("The number of available link colors is limited. "
                          "The visualization will not work if you define more "
                          "than 5 link types.",
                          color="warning")
            ]
        ),
        dbc.Row(
            dbc.Col(
                H5("Link configuration")
            )
        ),
        Hr(),
        dbc.Row(
            dbc.Col(
                get_duplicating_link_section(example_file_field_opts,
                                             0,
                                             alerts=True)
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": "link-config"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add link config section",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "link-config"},
                           color="primary")
            ),
            className="mb-3"
        )
    ]
    return ret


def get_duplicating_select_field(example_file_field_opts, type_, index):
    """Get generic select field for create config form.

    :param example_file_field_opts: Select opts from example file
    :type example_file_field_opts: list
    :param type_: Type to assign to select field ID
    :type type_: str
    :param index: Index to assign to select field ID
    :type index: int | str
    :return: Generic select field
    :rtype: dbc.Row
    """
    ret = dbc.Row(
        dbc.Col(
            dbc.Select(
                id={"type": type_, "index": index},
                options=example_file_field_opts,
                placeholder="Optional"
            )
        ),
        className="mb-3"
    )
    return ret


def get_duplicating_link_section(example_file_field_opts, index, alerts=False):
    """Get link config section for create config form.

    :param example_file_field_opts: Select opts from example file
    :type example_file_field_opts: list
    :param index: Index to assign to link config section
    :type index: int | str
    :param alert: Whether to display help alerts
    :type alert: bool
    :return: Link config section for create config form
    :rtype: dbc.Row
    """
    ret = dbc.Row(
        dbc.Col(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Label("Link label:",
                                      html_for={"type": "link-label",
                                                "index": index}),
                            dbc.Input(
                                id={"type": "link-label", "index": index}
                            )
                        ]
                    ),
                    className="mb-3"
                ),
                get_create_config_help_btn("min-loops") if alerts else None,
                get_create_config_help_alert(
                    "min-loops",
                    [
                        P([
                            "If you check this box, each ",
                            A("connected component",
                              href="https://bit.ly/3CFBKNJ",
                              target="_blank",
                              rel="noopener noreferrer"),
                            " will be converted into a ",
                            A("minimum spanning tree (MST)",
                              href="https://bit.ly/2VxWqSp",
                              target="_blank",
                              rel="noopener noreferrer"),
                            ". If an optional matrix file was provided, the "
                            "weight assigned to each link or edge when "
                            "generating MSTs is equal to the corresponding "
                            "matrix cell value encoding the two nodes "
                            "connected by said link. If an optional matrix "
                            "file was not provided, the difference in "
                            "graphical distance on the plot between the two "
                            "nodes connected by the link is used."
                        ]),
                        P([
                            A("Kruskal's algorithm",
                              href="https://bit.ly/3wEZuNW",
                              target="_blank",
                              rel="noopener noreferrer"),
                            " is used to generate MSTs."
                        ])
                    ]
                ) if alerts else None,
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Checkbox(
                                id={"type": "link-minimize-loops",
                                    "index": index},
                                checked=False
                            ),
                            width=1
                        ),
                        dbc.Col(
                            dbc.Label("Minimize loops? (generate MST for each "
                                      "group of connected nodes)")
                        )
                    ],
                    className="mb-3"
                ),
                get_create_config_help_btn("arrowheads") if alerts else None,
                get_create_config_help_alert(
                    "arrowheads",
                    [P("If you check this box, the links will have "
                       "arrowheads. This is really just a stylistic choice, "
                       "as directionality is already implied through the "
                       "x-axis encoding sampling date.")]
                ) if alerts else None,
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Checkbox(
                                id={"type": "link-arrowheads", "index": index},
                                checked=False
                            ),
                            width=1
                        ),
                        dbc.Col(
                            dbc.Label("Show arrowheads?")
                        )
                    ],
                    className="mb-3"
                ),
                get_create_config_help_btn("weight-exp") if alerts else None,
                get_create_config_help_alert(
                    "weight-exp",
                    [
                        P("Enter the equation for calculating link weights. "
                          "This is optional, but if specified, the link "
                          "weights will be overlaid on top of the links in "
                          "the visualization."),
                        P([
                            "The equation expects a specific syntax. You can "
                            "add (+), subtract (-), multiply (*), and divide "
                            "(/). You can specify negative numbers. You can "
                            "also specify absolute values with ",
                            B("abs()"),
                            "."
                        ]),
                        P("You can also reference data values from the two "
                          "nodes connected by the link with the following "
                          "notation:"),
                        P([
                            B("!some_field!"),
                            " for the data value from the node with an "
                            "earlier sampling date",
                        ]),
                        P([
                            B("@some_field@"),
                            " for the data value from the node with a later "
                            "sampling date",
                        ]),
                        P([
                            I("e.g., "),
                            "If we have a field called \"mass\", we can "
                            "calculate the absolute difference in mass "
                            "between the nodes connected by each link with: ",
                            B("abs(@mass@ - !mass!)")
                        ]),
                        P([
                            "If you upload a matrix, you can also reference "
                            "the pairwise matrix value for the two nodes "
                            "with ",
                            B("{{matrix}}")
                        ])
                    ],
                ) if alerts else None,
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Label("Weight expression:",
                                      html_for={"type": "link-weight-exp",
                                                "index": index}),
                            dbc.Input(
                                id={"type": "link-weight-exp", "index": index},
                                placeholder="Optional"
                            )
                        ]
                    ),
                    className="mb-3"
                ),
                get_create_config_help_btn("weight-fltrs") if alerts else None,
                get_create_config_help_alert(
                    "weight-fltrs",
                    [P("Filter out links with a weight less than or greater "
                       "than a certain value. You can also filter out links "
                       "that are equal to specific values.")]
                ) if alerts else None,
                dbc.Row(
                    dbc.Col(
                        dbc.Label("Weight filters:")
                    ),
                    className="mb-3"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label("Less than:",
                                      html_for={"type": "link-weight-lt",
                                                "index": index}),
                            width={"offset": 1, "size": 4}
                        ),
                        dbc.Col(
                            dbc.Input(
                                id={"type": "link-weight-lt", "index": index},
                                type="number",
                                max=maxsize,
                                placeholder="Optional"
                            ),
                            width=4
                        )
                    ],
                    className="mb-1"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label("Greater than:",
                                      html_for={"type": "link-weight-gt",
                                                "index": index}),
                            width={"offset": 1, "size": 4}
                        ),
                        dbc.Col(
                            dbc.Input(
                                id={"type": "link-weight-gt", "index": index},
                                type="number",
                                max=maxsize,
                                placeholder="Optional"
                            ),
                            width=4
                        )
                    ],
                    className="mb-1"
                ),
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Label("Not equal to:",
                                      html_for={"type": "link-weight-neq",
                                                "index": index}),
                            dbc.Textarea(
                                id={"type": "link-weight-neq", "index": index},
                                placeholder="Separate multiple values with a "
                                            "semicolon"
                            )
                        ],
                        width={"offset": 1, "size": 8}
                    ),
                    className="mb-1"
                ),
                get_create_config_help_btn("attr-filters") if alerts else None,
                get_create_config_help_alert(
                    "attr-filters",
                    [
                        P([
                            "Specify values you want to ignore from certain "
                            "fields when comparing data between nodes for "
                            "link-drawing purposes. This can be useful when "
                            "you only want to consider outlier data for "
                            "specific fields in your criteria when drawing "
                            "links."
                        ]),
                        P([
                            I("e.g., "),
                            "if you want to draw links between nodes that "
                            "have the same value for \"HIV positive\", but "
                            "the majority of your data is for patients who "
                            "are HIV negative, you can select the "
                            "\"HIV positive\" field, and enter the value "
                            "\"negative\" in the textbox, to only draw links "
                            "between nodes representing HIV positive patients"
                        ])
                    ]
                ) if alerts else None,
                dbc.Row(
                    dbc.Col(
                        dbc.Label("Field value filters:")
                    ),
                    className="mb-1"
                ),
                dbc.Row(
                    dbc.Col(
                        get_duplicating_attr_filter_section(
                            example_file_field_opts,
                            str(index) + "-0"
                        )
                    ),
                    className="mb-3"
                ),
                dbc.Row(
                    dbc.Col(
                        [],
                        id={"type": "expandable-create-config-form-col",
                            "index": "attr-filter-fields-" + str(index)}
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Button("Add",
                                   id={"type": "expandable-create-config-form"
                                               "-btn",
                                       "index": "attr-filter-fields-"
                                                + str(index)},
                                   color="primary")
                    ),
                    className="mb-3"
                ),
                get_create_config_help_btn("all-eq") if alerts else None,
                get_create_config_help_alert(
                    "all-eq",
                    [P("In order to draw a link between any two nodes, they "
                       "must have the same values for all the fields you "
                       "specify in this section.")]
                ) if alerts else None,
                dbc.Row(
                    dbc.Col(
                        dbc.Label("ALL of these fields must be equal:")
                    ),
                    className="mb-1"
                ),
                dbc.Row(
                    dbc.Col(
                        get_duplicating_select_field(
                            example_file_field_opts,
                            "link-all-eq-select",
                            str(index) + "-0"
                        )
                    ),
                    className="mb-3"
                ),
                dbc.Row(
                    dbc.Col(
                        [],
                        id={"type": "expandable-create-config-form-col",
                            "index": "all-eq-fields-" + str(index)}
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Button("Add",
                                   id={"type": "expandable-create-config-form"
                                               "-btn",
                                       "index": "all-eq-fields-" + str(index)},
                                   color="primary")
                    ),
                    className="mb-3"
                ),
                get_create_config_help_btn("all-neq") if alerts else None,
                get_create_config_help_alert(
                    "all-neq",
                    [P("In order to draw a link between any two nodes, they "
                       "must have different values for all the fields you "
                       "specify in this section.")]
                ) if alerts else None,
                dbc.Row(
                    dbc.Col(
                        dbc.Label("ALL of these fields must NOT be equal:")
                    ),
                    className="mb-1"
                ),
                dbc.Row(
                    dbc.Col(
                        get_duplicating_select_field(
                            example_file_field_opts,
                            "link-all-neq-select",
                            str(index) + "-0"
                        )
                    ),
                    className="mb-3"
                ),
                dbc.Row(
                    dbc.Col(
                        [],
                        id={"type": "expandable-create-config-form-col",
                            "index": "all-neq-fields-" + str(index)}
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Button("Add",
                                   id={"type": "expandable-create-config-form"
                                               "-btn",
                                       "index": "all-neq-fields-"
                                                + str(index)},
                                   color="primary")
                    ),
                    className="mb-3"
                ),
                get_create_config_help_btn("any-eq") if alerts else None,
                get_create_config_help_alert(
                    "any-eq",
                    [P("In order to draw a link between any two nodes, they "
                       "must have at least one matching value across all the "
                       "fields you specify in this section.")]
                ) if alerts else None,
                dbc.Row(
                    dbc.Col(
                        dbc.Label("ANY of these fields must be equal:")
                    ),
                    className="mb-1"
                ),
                dbc.Row(
                    dbc.Col(
                        get_duplicating_select_field(
                            example_file_field_opts,
                            "link-any-eq-select",
                            str(index) + "-0"
                        )
                    ),
                    className="mb-3"
                ),
                dbc.Row(
                    dbc.Col(
                        [],
                        id={"type": "expandable-create-config-form-col",
                            "index": "any-eq-fields-" + str(index)}
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Button("Add",
                                   id={"type": "expandable-create-config-form"
                                               "-btn",
                                       "index": "any-eq-fields-" + str(index)},
                                   color="primary")
                    ),
                    className="mb-3"
                ),
                Hr()
            ]
        ),
        id={"type": "link-config", "index": index},
        className="mb-3"
    )
    return ret


def get_duplicating_attr_filter_section(example_file_field_opts, index):
    """Get attr filter section for create config form.

    :param example_file_field_opts: Select opts from example file
    :type example_file_field_opts: list
    :param index: Index to assign to select and textarea inputs
    :type index: int | str
    :return: Attr filter section for create config form
    :rtype: dbc.Row
    """
    ret = dbc.Row(
        dbc.Col(
            [
                dbc.Select(
                    id={"type": "link-attr-filter-select",
                        "index": index},
                    options=example_file_field_opts,
                    placeholder="Optional"
                ),
                dbc.Textarea(
                    id={"type": "link-attr-filter-textarea",
                        "index": index},
                    placeholder="Separate multiple values with a semicolon"
                )
            ]
        ),
        className="mb-3"
    )
    return ret


def get_create_config_help_btn(index):
    """Get btn used to toggle alert in create config form.

    :param index: Index matching alert btn toggles
    :type index: str | int
    :return: Btn used to toggle alert in create config form
    :rtype: dbc.Row
    """
    return dbc.Row(
        dbc.Col(
            dbc.Button("Help",
                       id={"type": "create-config-modal-help-btn",
                           "index": index},
                       color="info",
                       size="sm",
                       className="p-0"),
            className="text-right",
            width={"offset": 10, "size": 2}
        )
    )


def get_create_config_help_alert(index, alert_children):
    """Get help alert in create config form.

    :param index: Index matching btn toggling alert
    :type index: str | int
    :return: Help lert in create config form
    :rtype: dbc.Row
    """
    return dbc.Row(
        dbc.Col(
            dbc.Alert(
                alert_children,
                id={"type": "create-config-modal-help-alert",
                    "index": index},
                dismissable=True,
                is_open=False,
                color="info"
            )
        ),
        className="mt-1"
    )
