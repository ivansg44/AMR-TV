"""Fns for generating modals."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_html_components import Div


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
            dbc.ModalBody([
                dbc.Row(
                    [
                        dbc.Col(
                            Div(
                                dcc.Upload(
                                    dbc.Button("Upload sample/example data "
                                               "file",
                                               id="select-example-file-btn"),
                                    id="upload-example-file"
                                ),
                                id="select-example-file-tooltip-target"
                            ),
                            width=8
                        ),
                        dbc.Col(
                            Div(
                                dbc.Select(
                                    id="delimiter-select",
                                    placeholder="Delimiter?",
                                    options=[
                                        {"label": "Tab", "value": "\t"},
                                        {"label": "Comma", "value": ","}
                                    ]
                                ),
                                id="delimiter-select-tooltip-target"
                            )
                        )
                    ]
                ),
                dbc.Tooltip("foo",
                            delay={"show": 0, "hide": 0},
                            placement="left",
                            target="select-example-file-tooltip-target"),
                dbc.Tooltip("bar",
                            delay={"show": 0, "hide": 0},
                            placement="right",
                            target="delimiter-select-tooltip-target")
            ]),
            dbc.ModalBody(None, id="create-config-file-modal-form")
        ],
        id="create-config-file-modal"
    )
    return ret


def get_create_config_modal_form(example_file_fields):
    """TODO"""
    example_file_fields_select_opts = \
        [{"label": None, "value": None}] \
        + [{"label": e, "value": e} for e in example_file_fields]
    ret = [
        dbc.Row(
            dbc.Col(
                Div(
                    [
                        dbc.Label("Date field:", html_for="date-field-select"),
                        dbc.Select(
                            id="date-field-select",
                            options=example_file_fields_select_opts
                        )
                    ],
                    id="date-field-select-tooltip-target"
                )
            ),
            className="mb-3"
        ),
        # TODO this isn't right
        dbc.Row(
            dbc.Col(
                Div(
                    [
                        dbc.Label("Node label field:",
                                  html_for="node-label-field-select"),
                        dbc.Select(
                            id="node-label-field-select",
                            options=example_file_fields_select_opts
                        )
                    ],
                    id="node-label-field-select-target"
                )
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                Div(
                    [
                        dbc.Row([
                            dbc.Col(
                                dbc.Checkbox(
                                    id="links-across-primary-y-checkbox",
                                    checked=False
                                ),
                                width=1
                            ),
                            dbc.Col(
                                dbc.Label("Draw links b/w nodes w/ different "
                                          "primary y-axis values?",
                                          html_for="links-across-primary-y-"
                                                   "checkbox")
                            )
                        ])
                    ],
                    id="links-across-primary-y-checkbox-target"
                )
            ),
            className="mb-3"
        ),
        dbc.Tooltip("bar",
                    delay={"show": 0, "hide": 0},
                    placement="right",
                    target="date-field-select-tooltip-target"),
        dbc.Tooltip("bar",
                    delay={"show": 0, "hide": 0},
                    placement="right",
                    target="node-label-field-select-target"),
        dbc.Tooltip("bar",
                    delay={"show": 0, "hide": 0},
                    placement="right",
                    target="links-across-primary-y-checkbox-target")
    ]
    return ret
