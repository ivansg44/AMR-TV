"""TODO"""

from dash import Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go

import data_parser

app = Dash(external_stylesheets=[dbc.themes.UNITED])


def get_main_fig_nodes(marker_size):
    """TODO"""
    x = [1, 2, 3, 4, 5, 5, 5, 6, 7]
    y = [7, 7, 5, 3, 5, 4, 1, 4, 3]
    nodes = go.Scatter(
        x=x,
        y=y,
        mode="markers+text",
        marker={
            "size": marker_size,
            "symbol": "square",
            "color": "white",
            "line": {
                "width": 2,
                "color": "black"
            }
        },
        text="ST1846<br>ST1846",
        textfont={
            "size": 16
        }
    )
    return nodes


def get_main_fig_edges():
    """TODO"""
    x = [1, 2, None,
         3, 4, None,
         3, 5, None,
         3, 5, None,
         4, 7, None,
         5, 5, None,
         5, 6, None]
    y = [7, 7, None,
         5, 3, None,
         5, 5, None,
         5, 4, None,
         3, 3, None,
         5, 4, None,
         4, 4, None]
    edges = go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line={
            "width": 1,
            "color": "grey"
        }
    )
    return edges


def get_main_fig_edge_labels():
    """TODO"""
    x = [1.5, 3.5, 4, 4, 5.5, 5, 5.5]
    y = [7, 4, 5, 4.5, 3, 4.5, 4]
    edges = go.Scatter(
        x=x,
        y=y,
        mode="text",
        text=[
            "4 SNVs",
            "pRFLPA1",
            "3 SNVs",
            "OR",
            "6 SNVs<br>pRFLPA1",
            "pRFLPA1",
            "38 SNVs<br>pRFLPA1"
        ],
        textposition=[
            "top center",
            "top right",
            "top center",
            "top right",
            "top center",
            "middle right",
            "top center",
        ],
        textfont={
            "size": 16
        },
    )
    return edges


def get_main_fig_y_axis_facet_lines():
    """TODO"""
    lines = go.Scatter(
        x=[0.5, 7.5, None,
           0.5, 7.5, None],
        y=[2, 2, None,
           6, 6, None],
        mode="lines",
        line={
            "color": "grey"
        }
    )
    return lines


def get_main_fig():
    """TODO"""
    fig = go.Figure(
        data=[get_main_fig_edges(),
              get_main_fig_edge_labels(),
              get_main_fig_nodes(60),
              get_main_fig_y_axis_facet_lines()],
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "showlegend": False,
            "xaxis": {
                "range": [0.5, 7.5],
                "tickmode": "array",
                "tickvals": list(range(1, 8)),
                # TODO use dates with days so no x values are shared
                "ticktext": [
                    "Oct 2011",
                    "Sep 2012",
                    "Jun 2012",
                    "Jul 2012",
                    "Nov 2014",
                    "Dec 2014",
                    "Jan 2015"
                ],
                "tickfont": {
                    "size": 16
                },
                "linecolor": "black"
            },
            "yaxis": {
                "tickmode": "array",
                "tickvals": [1, 4, 7],
                "ticktext": [
                    "Tn4401<br>Tn4401b-1<br>IncP,L/M",
                    "Tn4401<br>Tn4401b-2<br>IncN",
                    "Tn4401<br>Tn4401a-1<br>IncFll(k)"
                ],
                "tickfont": {
                    "size": 16
                },
                "linecolor": "black"
            },
            "plot_bgcolor": "white"
        },
    )
    return fig


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
            children=dbc.Col(
                children=dcc.Graph(
                    figure=get_main_fig(),
                    id="main-graph",
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
