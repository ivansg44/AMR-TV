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
        },
        hoverinfo="text",
        hovertext=app_data["main_fig_nodes_hovertext"]
    )
    return nodes


def get_main_fig_attr_link_graphs(app_data):
    """Get plotly scatter objs of links in main fig.

    This is basically a list of different scatter objs--one for each
    attr.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter objs of links in main fig
    :rtype: list[go.Scatter]
    """
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
        (r, g, b) = app_data["attr_link_color_dict"][attr]

        opaque_graph = go.Scatter(
            x=[x if x else None for x in opaque_x],
            y=[y if y else None for y in opaque_y],
            mode="lines",
            line={
                "width": 3,
                "color": "rgb(%s,%s,%s)" % (r, g, b)
            }
        )
        transparent_graph = go.Scatter(
            x=[x if x else None for x in transparent_x],
            y=[y if y else None for y in transparent_y],
            mode="lines",
            line={
                "width": 3,
                "color": "rgba(%s,%s,%s, 0.5)" % (r, g, b)
            }
        )
        ret += [opaque_graph, transparent_graph]

    return ret


def get_main_fig_attr_link_label_graphs(app_data):
    """Get plotly scatter objs of links labels in main fig.

    This is basically a list of different scatter objs--one for each
    attr label type.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter objs of link labels in main fig
    :rtype: list[go.Scatter]
    """
    ret = []
    for attr in app_data["main_fig_attr_link_labels_dict"]:
        opaque_dict = \
            app_data["main_fig_attr_link_labels_dict"][attr]["opaque"]
        opaque_x = opaque_dict["x"]
        opaque_y = opaque_dict["y"]
        opaque_text = opaque_dict["text"]
        transparent_dict = \
            app_data["main_fig_attr_link_labels_dict"][attr]["transparent"]
        transparent_x = transparent_dict["x"]
        transparent_y = transparent_dict["y"]
        transparent_text = transparent_dict["text"]
        (r, g, b) = app_data["attr_link_color_dict"][attr]

        opaque_graph = go.Scatter(
            x=opaque_x,
            y=opaque_y,
            text=opaque_text,
            mode="text",
            textfont={
                "color": "rgb(%s,%s,%s)" % (r, g, b),
                "size": 16
            }
        )

        transparent_graph = go.Scatter(
            x=transparent_x,
            y=transparent_y,
            text=transparent_text,
            mode="text"
        )

        ret += [opaque_graph, transparent_graph]

    return ret


def get_main_fig_attr_link_tip_graphs(app_data):
    """Get plotly scatter objs of lin tips in main fig.

    This is basically a list of different scatter objs--one for each
    attr.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter objs of link tips in main fig
    :rtype: list[go.Scatter]
    """
    opaque_x = \
        app_data["main_fig_attr_link_tips_dict"]["opaque"]["x"]
    opaque_y = \
        app_data["main_fig_attr_link_tips_dict"]["opaque"]["y"]
    transparent_x = \
        app_data["main_fig_attr_link_tips_dict"]["transparent"]["x"]
    transparent_y = \
        app_data["main_fig_attr_link_tips_dict"]["transparent"]["y"]

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


def get_main_fig_primary_facet_lines(app_data):
    """Get plotly scatter obj of primary facet lines in main fig.

    These are the lines that split the main graph by the first
    (primary) val in each track.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter obj used to draw primary facet lines in
        main fig.
    :rtype: go.Scatter
    """
    lines = go.Scatter(
        x=app_data["main_fig_primary_facet_x"],
        y=app_data["main_fig_primary_facet_y"],
        mode="lines",
        line={
            "color": "grey"
        }
    )
    return lines


def get_main_fig_secondary_facet_lines(app_data):
    """Get plotly scatter obj of secondary facet lines in main fig.

    These are the lines that split the main graph into tracks.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter obj used to draw secondary facet lines in
        main fig.
    :rtype: go.Scatter
    """
    lines = go.Scatter(
        x=app_data["main_fig_secondary_facet_x"],
        y=app_data["main_fig_secondary_facet_y"],
        mode="lines",
        line={
            "color": "grey",
            "dash": "dot",
            "width": 1
        }
    )
    return lines


def get_main_fig(app_data, nodes_graph, attr_link_graphs,
                 attr_link_label_graphs, primary_facet_lines_graph,
                 secondary_facet_lines_graph):
    """Get main fig in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :param nodes_graph: Plotly scatter obj of nodes in main fig
    :type nodes_graph: go.Scatter
    :param attr_link_graphs: Plotly scatter objs of links in main fig
    :type attr_link_graphs: list[go.Scatter]
    :param attr_link_label_graphs: Plotly scatter objs of link labels in main
        fig.
    :type attr_link_label_graphs: list[go.Scatter]
    :param primary_facet_lines_graph: Plotly scatter obj used to draw primary
        facet lines in main fig.
    :type primary_facet_lines_graph: go.Scatter
    :param secondary_facet_lines_graph: Plotly scatter obj used to draw
        secondary facet lines in main fig.
    :type secondary_facet_lines_graph: go.Scatter
    :return: Plotly figure obj showing main fig in viz
    :rtype: go.Figure
    """
    ret = go.Figure(
        data=attr_link_graphs + attr_link_label_graphs + [
              nodes_graph,
              secondary_facet_lines_graph,
              primary_facet_lines_graph
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
    return ret


def get_zoomed_out_main_fig(app_data, nodes_graph, attr_link_graphs):
    """Get zoomed out main fig in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :param nodes_graph: Plotly scatter obj of nodes in main fig
    :type nodes_graph: go.Scatter
    :param attr_link_graphs: Plotly scatter objs of links in main fig
    :type attr_link_graphs: list[go.Scatter]
    :return: Plotly figure obj showing zoomed-out main fig in viz
    :rtype: go.Figure
    """
    ret = go.Figure(
        data=attr_link_graphs + [nodes_graph],
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
                "visible": False
            },
            "yaxis": {
                "range": app_data["main_fig_yaxis_range"],
                "fixedrange": True,
                "tickmode": "array",
                "tickvals": app_data["main_fig_yaxis_tickvals"],
                "visible": False
            },
            "plot_bgcolor": "white"
        },
    )

    ret.update_traces(marker_size=8)
    ret.update_traces(mode="markers",
                      selector={"mode": "markers+text"})
    ret.update_traces(line_width=1)

    return ret


def get_main_figs(app_data):
    """Get main and zoomed-out main figs in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure objects that show main and zoomed-out main
        figs in viz.
    :rtype: tuple[go.Figure, go.Figure]
    """
    nodes_graph = get_main_fig_nodes(app_data)
    attr_link_graphs = get_main_fig_attr_link_graphs(app_data)
    attr_link_label_graphs = get_main_fig_attr_link_label_graphs(app_data)
    primary_facet_lines_graph = get_main_fig_primary_facet_lines(app_data)
    secondary_facet_lines_graph = get_main_fig_secondary_facet_lines(app_data)

    main_fig = get_main_fig(app_data,
                            nodes_graph,
                            attr_link_graphs,
                            attr_link_label_graphs,
                            primary_facet_lines_graph,
                            secondary_facet_lines_graph)
    zoomed_out_main_fig = get_zoomed_out_main_fig(app_data,
                                                  nodes_graph,
                                                  attr_link_graphs)

    return main_fig, zoomed_out_main_fig
