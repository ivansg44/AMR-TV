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
            ])
        ],
        id="create-config-file-modal"
    )
    return ret
