import plotly.graph_objects as go


def get_main_fig_nodes(app_data):
    nodes = go.Scatter(
        x=app_data["main_fig_nodes_x"],
        y=app_data["main_fig_nodes_y"],
        mode="markers+text",
        marker={
            "color": "lightgrey",
            "line": {
                "color": "black",
                "width": 1
            },
            "size": 24,
            "symbol": app_data["main_fig_nodes_marker_symbol"]
        },
        text=app_data["main_fig_nodes_text"],
        textfont={
            "color": "black",
            "size": 16
        }
    )
    return nodes


def get_main_fig_mlst_links(app_data):
    mlst_links = go.Scatter(
        x=app_data["main_fig_mlst_links_x"],
        y=app_data["main_fig_mlst_links_y"],
        mode="lines",
        line={
            "width": 1,
            "color": "#a6cee3"
        }
    )
    return mlst_links


def get_main_fig_facet_lines(app_data):
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
    fig = go.Figure(
        data=[
            get_main_fig_mlst_links(app_data),
            get_main_fig_nodes(app_data),
            get_main_fig_facet_lines(app_data)
        ],
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
                "range": app_data["main_fig_yaxis_range"],
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
