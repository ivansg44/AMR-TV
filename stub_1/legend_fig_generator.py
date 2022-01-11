import plotly.graph_objects as go


def get_node_symbol_legend_fig_nodes(app_data):
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
        },
        hoverinfo="skip"
    )
    return nodes


def get_node_symbol_legend_fig(app_data):
    fig = go.Figure(
        data=[get_node_symbol_legend_fig_nodes(app_data)],
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "xaxis": {
                "visible": False,
                "fixedrange": True
            },
            "yaxis": {
                "visible": False,
                "fixedrange": True
            },
            "showlegend": False,
            "plot_bgcolor": "white"
        },
    )
    return fig


def get_link_legend_fig_links(app_data):
    links = []
    for i, attr in enumerate(app_data["sample_links_dict"]):
        link_dict = app_data["sample_links_dict"][attr]["opaque"]
        links.append(
            go.Scatter(
                x=[0, 1],
                y=[i, i],
                mode="lines+text",
                line={
                    "width": 3,
                    "color": "rgb(%s, %s, %s)" % link_dict["color"],
                    "dash": link_dict["dash"]
                },
                text=["<b>%s</b>" % attr, None],
                textfont={
                    "color": "black",
                    "size": 16
                },
                textposition="top right",
                hoverinfo="skip"
            )
        )
    return links


def get_link_legend_fig(app_data):
    fig = go.Figure(
        data=get_link_legend_fig_links(app_data),
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0, "pad": 0
            },
            "xaxis": {
                "visible": False,
                "fixedrange": True
            },
            "yaxis": {
                "visible": False,
                "fixedrange": True,
                "range": [-0.5, len(app_data["sample_links_dict"])]
            },
            "showlegend": False,
            "plot_bgcolor": "white"
        }
    )
    return fig


def get_node_color_legend_fig_nodes(app_data):
    node_color_attr_dict = app_data["node_color_attr_dict"]

    if not node_color_attr_dict:
        return {}

    nodes = go.Scatter(
        x=[1 for _ in node_color_attr_dict],
        y=list(range(len(node_color_attr_dict))),
        mode="markers+text",
        marker={
            "color": list(node_color_attr_dict.values()),
            "line": {
                "color": "black",
                "width": 1
            },
            "size": 24,
            "symbol": "circle"
        },
        text=["<b>%s</b>" % e for e in node_color_attr_dict.keys()],
        textfont={
            "color": "black",
            "size": 16
        },
        textposition="middle right",
        hoverinfo="skip"
    )
    return nodes


def get_node_color_legend_fig(app_data):
    fig = go.Figure(
        data=[get_node_color_legend_fig_nodes(app_data)],
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "xaxis": {
                "visible": False,
                "fixedrange": True,
                "range": [0.5, 5]
            },
            "yaxis": {
                "visible": False,
                "fixedrange": True
            },
            "showlegend": False,
            "plot_bgcolor": "white"
        },
    )
    return fig
