"""Fns for generating modals."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc


def get_upload_modal():
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
