"""TODO"""

from dash import Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import data_parser

app = Dash(external_stylesheets=[dbc.themes.UNITED],
           # Fixes bug with debugger in Pycharm. See
           # https://bit.ly/3j86GL1.
           name="foo")


def get_main_fig_nodes(app_data, marker_size=60):
    """TODO"""
    nodes = go.Scatter(
        x=app_data["main_fig_nodes_x"],
        y=app_data["main_fig_nodes_y"],
        mode="markers+text",
        marker={
            "size": marker_size,
            "symbol": ["square" for _ in app_data["main_fig_nodes_x"]],
            "color": app_data["main_fig_nodes_marker_color"],
            "line": {
                "width": 2,
                "color": "black"
            }
        },
        text=app_data["main_fig_nodes_text"],
        textfont={
            "size": 16
        }
    )
    return nodes


def get_main_fig_edges(app_data):
    """TODO"""
    edges = go.Scatter(
        x=app_data["main_fig_edges_x"],
        y=app_data["main_fig_edges_y"],
        mode="lines",
        line={
            "width": 1,
            "color": "grey"
        }
    )
    return edges


def get_main_fig_edge_labels(app_data):
    """TODO"""
    edges = go.Scatter(
        x=app_data["main_fig_edge_labels_x"],
        y=app_data["main_fig_edge_labels_y"],
        mode="text",
        text=app_data["main_fig_edge_labels_text"],
        textposition=app_data["main_fig_edge_labels_textposition"],
        textfont={
            "size": 16
        },
    )
    return edges


def get_main_fig_facet_lines(app_data):
    """TODO"""
    lines = go.Scatter(
        x=app_data["main_fig_facet_x"],
        y=app_data["main_fig_facet_y"],
        mode="lines",
        line={
            "color": "grey"
        }
    )
    return lines


def get_main_fig(app_data):
    """TODO"""
    fig = go.Figure(
        data=[get_main_fig_edges(app_data),
              get_main_fig_edge_labels(app_data),
              get_main_fig_nodes(app_data),
              get_main_fig_facet_lines(app_data)],
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "showlegend": False,
            "xaxis": {
                "range": app_data["main_fig_xaxis_range"],
                "fixedrange": True,
                "tickmode": "array",
                "tickvals": app_data["main_fig_xaxis_tickvals"],
                "ticktext": app_data["main_fig_xaxis_ticktext"],
                "tickfont": {
                    "size": 16
                },
                "linecolor": "black"
            },
            "yaxis": {
                "fixedrange": True,
                "tickmode": "array",
                "tickvals": app_data["main_fig_yaxis_tickvals"],
                "ticktext": app_data["main_fig_yaxis_ticktext"],
                "tickfont": {
                    "size": 16
                },
                "linecolor": "black"
            },
            "plot_bgcolor": "white"
        },
    )
    return fig


def get_main_fig_legend_cols(sample_species_dict):
    """TODO"""
    main_fig_legend_cols = []
    for species, color in sample_species_dict.items():
        main_fig_legend_cols.append(
            dbc.Col(
                html.I(species),
                style={
                    "backgroundColor": color,
                    "textAlign": "center"
                }
            )
        )
    return main_fig_legend_cols


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
    """TODO"""
    app_data = data_parser.get_app_data("stub_sample_data.tsv",
                                        "stub_transmission_data.tsv")
    return [
        dbc.Row(
            children=get_main_fig_legend_cols(app_data["species_color_dict"])
        ),
        dbc.Row(
            children=dbc.Col(
                children=dcc.Graph(
                    figure=get_main_fig(app_data),
                    id="main-graph",
                    config={"displayModeBar": False},
                    style={"height": "90vh"}
                ),
                id="main-col"
            ),
            id="main-row"
        ),
        dcc.Store(id="app_data", data=app_data)
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
