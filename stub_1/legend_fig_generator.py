import plotly.graph_objects as go


def get_node_shape_legend_fig_nodes(app_data):
    nodes = go.Scatter(
        x=[1 for _ in app_data["node_shape_legend_fig_nodes_y"]],
        y=app_data["node_shape_legend_fig_nodes_y"],
        mode="markers+text",
        marker={
            "color": "lightgrey",
            "line": {
                "color": "black",
                "width": 1
            },
            "size": 24,
            "symbol": app_data["node_shape_legend_fig_nodes_marker_symbol"]
        },
        text=app_data["node_shape_legend_fig_nodes_text"],
        textfont={
            "color": "black",
            "size": 16
        }
    )
    return nodes


def get_node_shape_legend_fig(app_data):
    fig = go.Figure(
        data=[get_node_shape_legend_fig_nodes(app_data)],
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "xaxis": {
                "visible": False,
            },
            "yaxis": {
                "visible": False,
            },
            "showlegend": False,
            "plot_bgcolor": "white"
        },
    )
    return fig
