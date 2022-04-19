"""Fns for generating main fig in viz."""

import plotly.graph_objects as go


def get_main_fig_nodes(app_data):
    """Get plotly scatter obj of nodes in main fig.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter obj of nodes in main fig
    :rtype: go.Scatter
    """
    nodes = go.Scatter(
        x=app_data["main_fig_nodes_x"],
        y=app_data["main_fig_nodes_y"],
        mode="markers+text",
        marker={
            "color": app_data["main_fig_nodes_marker_color"],
            "line": {
                "color": "black",
                "width": 1
            },
            "size": 24,
            "symbol": app_data["main_fig_nodes_marker_symbol"],
            "opacity": app_data["main_fig_nodes_marker_opacity"]
        },
        text=app_data["main_fig_nodes_text"],
        textfont={
            "color": app_data["main_fig_nodes_textfont_color"],
            "size": 16
        }
    )
    return nodes


def get_main_fig_base_link_graphs(app_data):
    """TODO"""
    opaque_x = app_data["main_fig_base_links_dict"]["opaque"]["x"]
    opaque_y = app_data["main_fig_base_links_dict"]["opaque"]["y"]
    transparent_x = app_data["main_fig_base_links_dict"]["transparent"]["x"]
    transparent_y = app_data["main_fig_base_links_dict"]["transparent"]["y"]
    opaque_graph = go.Scatter(
        x=[x if x else None for x in opaque_x],
        y=[y if y else None for y in opaque_y],
        mode="lines",
        line={
            "width": 3,
            "color": "black"
        }
    )
    transparent_graph = go.Scatter(
        x=[x if x else None for x in transparent_x],
        y=[y if y else None for y in transparent_y],
        mode="lines",
        line={
            "width": 3,
            "color": "lightgrey"
        }
    )
    return [opaque_graph, transparent_graph]


def get_main_fig_attr_link_graphs(app_data):
    """TODO"""
    ret = []
    for attr in app_data["main_fig_attr_links_dict"]:
        opaque_x = \
            app_data["main_fig_attr_links_dict"][attr]["opaque"]["x"]
        opaque_y = \
            app_data["main_fig_attr_links_dict"][attr]["opaque"]["y"]
        transparent_x = \
            app_data["main_fig_attr_links_dict"][attr]["transparent"]["x"]
        transparent_y = \
            app_data["main_fig_attr_links_dict"][attr]["transparent"]["y"]

        opaque_graph = go.Scatter(
            x=[x if x else None for x in opaque_x],
            y=[y if y else None for y in opaque_y],
            mode="lines",
            line={
                "width": 2,
                "color": "red"
            }
        )
        transparent_graph = go.Scatter(
            x=[x if x else None for x in transparent_x],
            y=[y if y else None for y in transparent_y],
            mode="lines",
            line={
                "width": 2,
                "color": "white"
            }
        )
        ret += [opaque_graph, transparent_graph]

    return ret


def get_main_fig_link_graphs(app_data):
    """Get plotly scatter objs of different links in main fig.

    Basically, a list of different scatter objs that draw the links.
    One scatter obj per link type.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: List of plotly scatter obj used to draw links in main fig
    :rtype: list[go.Scatter]
    """
    # link_graphs = []
    # for attr in app_data["sample_links_dict"]:
    #     opaque_link_dict = app_data["sample_links_dict"][attr]["opaque"]
    #     (r, g, b) = opaque_link_dict["color"]
    #     link_graphs.append(
    #         go.Scatter(
    #             x=[x if x else None for x in opaque_link_dict["x"]],
    #             y=[y if y else None for y in opaque_link_dict["y"]],
    #             mode="lines",
    #             line={
    #                 "width": 3,
    #                 "color": "rgb(%s, %s, %s)" % (r, g, b),
    #                 "dash": opaque_link_dict["dash"]
    #             }
    #         )
    #     )
    # 
    #     transparent_link_dict = \
    #         app_data["sample_links_dict"][attr]["transparent"]
    #     (r, g, b) = transparent_link_dict["color"]
    #     link_graphs.append(
    #         go.Scatter(
    #             x=[x if x else None for x in transparent_link_dict["x"]],
    #             y=[y if y else None for y in transparent_link_dict["y"]],
    #             mode="lines",
    #             line={
    #                 "width": 3,
    #                 "color": "rgba(%s, %s, %s, 0.01)" % (r, g, b),
    #                 "dash": opaque_link_dict["dash"]
    #             }
    #         )
    #     )
    # return link_graphs
    return []


def get_main_fig_facet_lines(app_data):
    """Get plotly scatter obj of facet lines in main fig.

    These are the lines that split the main graph into tracks.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter obj used to draw facet lines in main fig
    :rtype: go.Scatter
    """
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
    """Get main fig in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure object that shows main fig in viz
    :rtype: go.Figure
    """
    main_fig_base_link_graphs = get_main_fig_base_link_graphs(app_data)
    main_fig_attr_link_graphs = get_main_fig_attr_link_graphs(app_data)
    # main_fig_link_graphs = get_main_fig_link_graphs(app_data)
    fig = go.Figure(
        data=main_fig_base_link_graphs + main_fig_attr_link_graphs + [
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
