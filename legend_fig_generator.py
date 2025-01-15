"""Fns for generating legend figs in viz."""

import plotly.graph_objects as go


def get_node_symbol_legend_fig_nodes(app_data):
    """Get plotly objs in node symbol legend.

    Basically, a scatter obj that draws nodes you see in the legend.
    Also, invisible bar obj for easier registration of click events.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly obj in node symbol legend
    :rtype: list[go.Scatter|go.Bar]
    """
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
            "symbol": app_data["node_shape_legend_fig_nodes_marker_symbol"],
            "opacity": app_data["node_shape_legend_fig_nodes_marker_opacity"]
        },
        text=app_data["node_shape_legend_fig_nodes_text"],
        textfont={
            "color": app_data["node_shape_legend_fig_nodes_textfont_color"],
            "size": 16
        },
        hoverinfo="skip"
    )
    easier_clicking = go.Bar(
        x=[2 for _ in app_data["node_shape_legend_fig_nodes_y"]],
        y=app_data["node_shape_legend_fig_nodes_y"],
        hoverinfo="none",
        orientation="h",
        width=1,
        opacity=0,
        customdata=app_data["node_shape_legend_fig_nodes_marker_symbol"]
    )
    return [nodes, easier_clicking]


def get_node_symbol_legend_fig(app_data):
    """Get node symbol legend fig in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure object that shows node symbol legend in viz
    :rtype: go.Figure
    """
    graph = get_node_symbol_legend_fig_nodes(app_data)
    fig = go.Figure(
        data=graph,
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
            "plot_bgcolor": "white",
            "height": len(graph[0]["y"]) * 50
        },
    )
    return fig


def get_link_legend_fig_links(app_data):
    """Get plotly objs of different links in link legend fig.

    Basically, a list of different scatter objs that draw one of each
    link you see in the legend. Also, invisible bar objs to allow
    easier registration of click events.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: List of plotly scatter/bar obj used to draw links in link
        legend fig.
    :rtype: list[go.Scatter|go.Bar]
    """
    links = []
    for i, attr in enumerate(app_data["main_fig_links_dict"]):
        filtered_link = attr in app_data["filtered_link_types"]
        (r, g, b) = app_data["link_color_dict"][attr]
        a = "0.5" if filtered_link else "1"
        links.append(
            go.Scatter(
                x=[0, 1],
                y=[i, i],
                mode="lines+text",
                line={
                    "width": 3,
                    "color": "rgba(%s, %s, %s, %s)" % (r, g, b, a),
                },
                text=["<b>%s</b>" % attr, None],
                textfont={
                    "color": "grey" if filtered_link else "black",
                    "size": 16
                },
                textposition="top right",
                hoverinfo="skip"
            )
        )
        # Invisible bar chart underneath to register clicks
        links.append(
            go.Bar(
                x=[1],
                y=[i],
                hoverinfo="none",
                orientation="h",
                width=1,
                opacity=0,
                customdata=[attr]
            )
        )
    return links


def get_link_legend_fig(app_data):
    """Get link legend fig in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure object that shows link legend in viz
    :rtype: go.Figure
    """
    graph = get_link_legend_fig_links(app_data)
    fig = go.Figure(
        data=graph,
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
                "range": [len(app_data["main_fig_links_dict"])-0.5, -0.5]
            },
            "showlegend": False,
            "plot_bgcolor": "white",
            "height": len(graph)/2 * 75,
        }
    )
    return fig


def get_node_color_legend_fig_nodes(app_data):
    """Get plotly objs in node color legend.

    Basically, a scatter obj that draws nodes you see in the legend.
    Also, invisible bar obj for easier registration of click events.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly obj in node color legend
    :rtype: list[go.Scatter|go.Bar]
    """
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
            "symbol": "circle",
            "opacity": app_data["node_color_legend_fig_nodes_marker_opacity"],
        },
        text=["<b>%s</b>" % e for e in node_color_attr_dict.keys()],
        textfont={
            "color": app_data["node_color_legend_fig_nodes_textfont_color"],
            "size": 16
        },
        textposition="middle right",
        hoverinfo="skip"
    )
    easier_clicking = go.Bar(
        x=[5 for _ in node_color_attr_dict],
        y=list(range(len(node_color_attr_dict))),
        hoverinfo="none",
        orientation="h",
        width=1,
        opacity=0,
        customdata=list(node_color_attr_dict.values())
    )
    return [nodes, easier_clicking]


def get_node_color_legend_fig(app_data):
    """Get node color legend fig in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure object that shows node color legend in viz
    :rtype: go.Figure
    """
    graph = get_node_color_legend_fig_nodes(app_data)
    fig = go.Figure(
        data=graph,
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
            "plot_bgcolor": "white",
        },
    )
    if graph:
        fig.update_layout(height=len(graph[0]["y"] * 50))
    return fig
