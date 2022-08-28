"""Fns for generating modals."""

from sys import maxsize

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_html_components import Div, Hr, P, H5


def get_upload_data_modal():
    """TODO"""
    ret = dbc.Modal(
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
    )
    return ret


def get_create_config_file_modal():
    """TODO"""
    ret = dbc.Modal(
        [
            dbc.ModalHeader("Create config file"),
            dbc.ModalBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Upload(
                                    dbc.Button("Upload sample/example data "
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
    """TODO"""
    ret = [
        get_create_config_help_btn("date-fields"),
        get_create_config_help_alert(
            "date-fields",
            [P("Hello world!")]
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
            [P("Hello world!")]
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
            [P("Hello world!")]
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
            [P("Hello world!")]
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
            [P("Hello world!")]
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
            [P("Hello world!")]
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
            [P("Hello world!")]
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
            [P("Hello world!")]
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
            [P("Hello world!")]
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
            {"type": "link-config", "index": 0},
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
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "link-config"},
                           color="primary")
            ),
            className="mb-3"
        ),
    ]
    return ret


def get_duplicating_select_field(example_file_field_opts, type_, index):
    """TODO"""
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
    """TODO"""
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
                    [P("Hello world!")]
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
                    [P("Hello world!")]
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
                    [P("Hello world!")]
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
                    [P("Hello world!")]
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
                    [P("Hello world!")]
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
                    [P("Hello world!")]
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
                    [P("Hello world!")]
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
                    [P("Hello world!")]
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
            ]
        ),
        id={"type": "link-config", "index": index},
        className="mb-3"
    )
    return ret


def get_duplicating_attr_filter_section(example_file_field_opts, index):
    """TODO"""
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
    """TODO"""
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
    """TODO"""
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


def get_first_link_config_section(example_file_field_opts):
    """TODO"""
    ret = [
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Link label:",
                              html_for="first-link-config-label-input"),
                    dbc.Input(
                        id="first-link-config-label-input"
                    )
                ]
            ),
            className="mb-3"
        ),
        get_create_config_help_btn("first-link-config-minimize-loops"),
        get_create_config_help_alert(
            "first-link-config-minimize-loops",
            [P("Hello world!")]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Checkbox(
                        id="first-link-config-minimize-loops-checkbox",
                        checked=False
                    ),
                    width=1
                ),
                dbc.Col(
                    dbc.Label("Minimize loops? (generate MST for each group "
                              "of connected nodes)")
                )
            ],
            className="mb-3"
        ),
        get_create_config_help_btn("first-link-config-show-arrowheads"),
        get_create_config_help_alert(
            "first-link-config-show-arrowheads",
            [P("Hello world!")]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Checkbox(
                        id="first-link-config-show-arrowheads-checkbox",
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
        get_create_config_help_btn("first-link-config-weight-exp"),
        get_create_config_help_alert(
            "first-link-config-weight-exp",
            [P("Hello world!")]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Weight expression:",
                              html_for="first-link-config-weight-exp-input"),
                    dbc.Input(
                        id="first-link-config-weight-exp-input",
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        get_create_config_help_btn("first-link-config-weight-filters"),
        get_create_config_help_alert(
            "first-link-config-weight-filters",
            [P("Hello world!")]
        ),
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
                              html_for="weight-filter-less-than-input"),
                    width={"offset": 1, "size": 4}
                ),
                dbc.Col(
                    dbc.Input(
                        id="weight-filter-less-than-input",
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
                              html_for="weight-filter-less-than-input"),
                    width={"offset": 1, "size": 4}
                ),
                dbc.Col(
                    dbc.Input(
                        id="weight-filter-greater-than-input",
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
                              html_for="weight-filter-not-equal-input"),
                    dbc.Textarea(
                        id="weight-filter-not-equal-input",
                        placeholder="Separate multiple values with a semicolon"
                    )
                ],
                width={"offset": 1, "size": 8}
            ),
            className="mb-1"
        ),
        get_create_config_help_btn("first-link-config-attr-filters"),
        get_create_config_help_alert(
            "first-link-config-attr-filters",
            [P("Hello world!")]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Label("Field value filters:")
            ),
            className="mb-1"
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Select(
                        id="first-link-config-attr-filter-select",
                        options=example_file_field_opts,
                        placeholder="Optional"
                    ),
                    dbc.Textarea(
                        id="first-link-config-attr-filter-textarea",
                        placeholder="Separate multiple values with a semicolon"
                    )
                ]
            ),
            className="mb-3"
        ),
        Div(
            dbc.Row(
                dbc.Col(
                [
                    dbc.Select(
                        options=example_file_field_opts,
                        placeholder="Optional"
                    ),
                    dbc.Textarea(
                        placeholder="Separate multiple values with a semicolon"
                    )
                ]
                ),
                className="mb-3"
            ),
            id={"type": "expandable-create-config-form-template",
                "index": "first-link-config-attr-filter"},
            style={"display": "none"}
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": "first-link-config-attr-filter"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "first-link-config-attr-filter"},
                           color="primary")
            ),
            className="mb-3"
        ),
        get_create_config_help_btn("first-link-config-all-equal"),
        get_create_config_help_alert(
            "first-link-config-all-equal",
            [P("Hello world!")]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("ALL of these fields must be equal:",
                              html_for="first-link-config-all-equal-select"),
                    dbc.Select(
                        id="first-link-config-all-equal-select",
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        Div(
            dbc.Row(
                dbc.Col(
                    dbc.Select(
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ),
                className="mb-3"
            ),
            id={"type": "expandable-create-config-form-template",
                "index": "first-link-config-all-equal"},
            style={"display": "none"}
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": "first-link-config-all-equal"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "first-link-config-all-equal"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("first-link-config-all-not-equal"),
        get_create_config_help_alert(
            "first-link-config-all-not-equal",
            [P("Hello world!")]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("ALL of these fields must be NOT equal:",
                              html_for="first-link-config-all-not-equal"
                                       "-select"),
                    dbc.Select(
                        id="first-link-config-all-not-equal-select",
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        Div(
            dbc.Row(
                dbc.Col(
                    dbc.Select(
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ),
                className="mb-3"
            ),
            id={"type": "expandable-create-config-form-template",
                "index": "first-link-config-all-not-equal"},
            style={"display": "none"}
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": "first-link-config-all-not-equal"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "first-link-config-all-not-equal"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr(),
        get_create_config_help_btn("first-link-config-any-equal"),
        get_create_config_help_alert(
            "first-link-config-any-equal",
            [P("Hello world!")]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("ANY of these fields may be equal:",
                              html_for="first-link-config-any-equal-select"),
                    dbc.Select(
                        id="first-link-config-any-equal-select",
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
                    "index": "first-link-config-any-equal"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": "first-link-config-any-equal"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr()
    ]
    return ret


def get_extra_link_config_section(example_file_field_opts, index_prefix):
    """TODO"""
    ret = [
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Link label:",
                              html_for=index_prefix+"-label-input"),
                    dbc.Input(
                        id=index_prefix+"-label-input"
                    )
                ]
            ),
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Checkbox(
                        id=index_prefix+"-minimize-loops-checkbox",
                        checked=False
                    ),
                    width=1
                ),
                dbc.Col(
                    dbc.Label("Minimize loops? (generate MST for each group "
                              "of connected nodes)")
                )
            ],
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Checkbox(
                        id=index_prefix+"-show-arrowheads-checkbox",
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
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Weight expression:",
                              html_for=index_prefix+"-weight-exp-input"),
                    dbc.Input(
                        id=index_prefix+"-weight-exp-input",
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
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
                              html_for="weight-filter-less-than-input"),
                    width={"offset": 1, "size": 4}
                ),
                dbc.Col(
                    dbc.Input(
                        id="weight-filter-less-than-input",
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
                              html_for="weight-filter-less-than-input"),
                    width={"offset": 1, "size": 4}
                ),
                dbc.Col(
                    dbc.Input(
                        id="weight-filter-greater-than-input",
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
                              html_for="weight-filter-not-equal-input"),
                    dbc.Textarea(
                        id="weight-filter-not-equal-input",
                        placeholder="Separate multiple values with a semicolon"
                    )
                ],
                width={"offset": 1, "size": 8}
            ),
            className="mb-1"
        ),
        dbc.Row(
            dbc.Col(
                dbc.Label("Field value filters:")
            ),
            className="mb-1"
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Select(
                        id=index_prefix+"-attr-filter-select",
                        options=example_file_field_opts,
                        placeholder="Optional"
                    ),
                    dbc.Textarea(
                        id=index_prefix+"-attr-filter-textarea",
                        placeholder="Separate multiple values with a semicolon"
                    )
                ]
            ),
            className="mb-3"
        ),
        Div(
            dbc.Row(
                dbc.Col(
                [
                    dbc.Select(
                        options=example_file_field_opts,
                        placeholder="Optional"
                    ),
                    dbc.Textarea(
                        placeholder="Separate multiple values with a semicolon"
                    )
                ]
                ),
                className="mb-3"
            ),
            id={"type": "expandable-create-config-form-template",
                "index": index_prefix+"-attr-filter"},
            style={"display": "none"}
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": index_prefix+"-attr-filter"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": index_prefix+"-attr-filter"},
                           color="primary")
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("ALL of these fields must be equal:",
                              html_for=index_prefix+"-all-equal-select"),
                    dbc.Select(
                        id=index_prefix+"-all-equal-select",
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        Div(
            dbc.Row(
                dbc.Col(
                    dbc.Select(
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ),
                className="mb-3"
            ),
            id={"type": "expandable-create-config-form-template",
                "index": index_prefix+"-all-equal"},
            style={"display": "none"}
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": index_prefix+"-all-equal"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": index_prefix+"-all-equal"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr(),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("ALL of these fields must be NOT equal:",
                              html_for=index_prefix+"-all-not-equal-select"),
                    dbc.Select(
                        id=index_prefix+"-all-not-equal-select",
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        Div(
            dbc.Row(
                dbc.Col(
                    dbc.Select(
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ),
                className="mb-3"
            ),
            id={"type": "expandable-create-config-form-template",
                "index": index_prefix+"-all-not-equal"},
            style={"display": "none"}
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": index_prefix+"-all-not-equal"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": index_prefix+"-all-not-equal"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr(),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("ANY of these fields may be equal:",
                              html_for=index_prefix+"-any-equal-select"),
                    dbc.Select(
                        id=index_prefix+"-any-equal-select",
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ]
            ),
            className="mb-3"
        ),
        Div(
            dbc.Row(
                dbc.Col(
                    dbc.Select(
                        options=example_file_field_opts,
                        placeholder="Optional"
                    )
                ),
                className="mb-3"
            ),
            id={"type": "expandable-create-config-form-template",
                "index": index_prefix+"-any-equal"},
            style={"display": "none"}
        ),
        dbc.Row(
            dbc.Col(
                [],
                id={"type": "expandable-create-config-form-col",
                    "index": index_prefix+"-any-equal"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Add",
                           id={"type": "expandable-create-config-form-btn",
                               "index": index_prefix+"-any-equal"},
                           color="primary")
            ),
            className="mb-3"
        ),
        Hr()
    ]
    return ret
