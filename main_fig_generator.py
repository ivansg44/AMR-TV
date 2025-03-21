"""Fns for generating main fig in viz."""

import plotly.graph_objects as go


def get_main_fig_nodes(app_data):
    """Get plotly scatter obj of nodes in main fig.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter obj of nodes in main fig
    :rtype: go.Scatter
    """
    opacity = app_data["main_fig_nodes_marker_opacity"]
    text = app_data["main_fig_nodes_text"]
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
            "opacity": opacity
        },
        # There is a bug, where if you use "", it will not change later
        text=[text[i] if e else " " for i, e in enumerate(opacity)],
        textfont={
            "color": app_data["main_fig_nodes_textfont_color"],
            "size": 16
        },
        hoverinfo=["text" if e else "skip" for e in opacity],
        hovertext=app_data["main_fig_nodes_hovertext"],
        name="main_fig_nodes_trace",
        customdata=opacity
    )
    return nodes


def get_main_fig_link_graphs(app_data):
    """Get plotly scatter objs of links in main fig.

    This is basically a list of different scatter objs--one for each
    link.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly scatter objs of links in main fig
    :rtype: list[go.Scatter]
    """
    ret = []
    for link in app_data["main_fig_links_dict"]:
        link_x = app_data["main_fig_links_dict"][link]["x"]
        link_y = app_data["main_fig_links_dict"][link]["y"]
        (r, g, b) = app_data["link_color_dict"][link]

        link_graph = go.Scatter(
            x=[x if x else None for x in link_x],
            y=[y if y else None for y in link_y],
            mode="lines",
            line={
                "width": 3,
                "color": "rgb(%s,%s,%s)" % (r, g, b)
            }
        )
        ret += [link_graph]

    return ret


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


def get_main_fig(app_data):
    """Get main fig in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure obj showing main fig in viz
    :rtype: go.Figure
    """
    nodes_graph = get_main_fig_nodes(app_data)
    link_graphs = get_main_fig_link_graphs(app_data)
    primary_facet_lines_graph = get_main_fig_primary_facet_lines(app_data)
    secondary_facet_lines_graph = get_main_fig_secondary_facet_lines(app_data)

    ret = go.Figure(
        data=link_graphs + [
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
                "visible": False
            },
            "yaxis": {
                "range": app_data["main_fig_yaxis_range"],
                "visible": False
            },
            "plot_bgcolor": "white",
            "dragmode": "pan"
        },
    )

    main_fig_annotations = get_link_arrowhead_annotations(app_data,
                                                          arrow_width=3,
                                                          arrow_size=0.6)
    main_fig_annotations += get_arc_arrowhead_annotations(app_data,
                                                          arrow_width=3,
                                                          arrow_size=0.6)
    main_fig_annotations += get_link_label_annotations(app_data)
    main_fig_annotations += get_arc_label_annotations(app_data)
    main_fig_shapes = get_arc_shapes(app_data, line_width=3)
    ret.update_layout(annotations=main_fig_annotations,
                      shapes=main_fig_shapes)

    return ret


def get_zoomed_out_main_fig(app_data):
    """Get zoomed out main fig in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure obj showing zoomed-out main fig in viz
    :rtype: go.Figure
    """
    nodes_graph = get_main_fig_nodes(app_data)
    link_graphs = get_main_fig_link_graphs(app_data)
    primary_facet_lines_graph = get_main_fig_primary_facet_lines(app_data)

    ret = go.Figure(
        data=link_graphs + [nodes_graph, primary_facet_lines_graph],
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "showlegend": False,
            "xaxis": {
                "range": app_data["main_fig_xaxis_range"],
                "fixedrange": True,
                "tickmode": "array",
                "tickvals": app_data["zoomed_out_main_fig_xaxis_tickvals"],
                "ticktext": app_data["zoomed_out_main_fig_xaxis_ticktext"],
                "tickangle": -90,
                "linecolor": "black"
            },
            "yaxis": {
                "range": app_data["main_fig_yaxis_range"],
                "fixedrange": True,
                "tickmode": "array",
                "tickvals": app_data["zoomed_out_main_fig_yaxis_tickvals"],
                "ticktext": app_data["zoomed_out_main_fig_yaxis_ticktext"],
                "linecolor": "black"
            },
            "plot_bgcolor": "white"
        },
    )

    ret.update_traces(marker_size=8)
    ret.update_traces(mode="markers",
                      selector={"mode": "markers+text"})
    ret.update_traces(line_width=1)

    zoomed_out_main_fig_annotations = \
        get_link_arrowhead_annotations(app_data, arrow_width=1, arrow_size=1)
    zoomed_out_main_fig_annotations +=\
        get_arc_arrowhead_annotations(app_data, arrow_width=1, arrow_size=1)
    zoomed_out_main_fig_shapes = get_arc_shapes(app_data, line_width=1)
    ret.update_layout(
        annotations=zoomed_out_main_fig_annotations,
        shapes=zoomed_out_main_fig_shapes
    )

    return ret


def get_link_arrowhead_annotations(app_data, arrow_width, arrow_size):
    """Get annotations to be added as link arrowheads to main fig.

    Plotly does not allow you to add arrowheads to line traces, so a
    separate fn was built for this as a workaround. We add annotations,
    which do allow arrowheads.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :param arrow_width: Width of links
    :type arrow_width: int
    :param arrow_size: Size of arrowhead; must be greater than 0.3
    :type arrow_size: float
    :return: list of annotations to be added as arrowheads
    :rtype: list
    """
    annotations = []
    for link in app_data["main_fig_link_arrowheads_dict"]:
        arrowhead_dict = app_data["main_fig_link_arrowheads_dict"][link]
        arrowhead_color = app_data["link_color_dict"][link]
        for i in range(len(arrowhead_dict["x"])):
            annotations.append({
                "x": arrowhead_dict["x"][i][1],
                "y": arrowhead_dict["y"][i][1],
                "ax": arrowhead_dict["x"][i][0],
                "ay": arrowhead_dict["y"][i][0],
                "xref": "x",
                "yref": "y",
                "axref": "x",
                "ayref": "y",
                "showarrow": True,
                "arrowcolor": "rgb(%s, %s, %s)" % arrowhead_color,
                "arrowhead": 1,
                "arrowwidth": arrow_width,
                "arrowsize": arrow_size
            })

    return annotations


def get_arc_arrowhead_annotations(app_data, arrow_width, arrow_size):
    """Get annotations to be added as arc arrowheads to main fig.

    Plotly does not allow you to add arrowheads to line traces, so a
    separate fn was built for this as a workaround. We add annotations,
    which do allow arrowheads.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :param arrow_width: Width of links
    :type arrow_width: int
    :param arrow_size: Size of arrowhead; must be greater than 0.3
    :type arrow_size: float
    :return: list of annotations to be added as arrowheads
    :rtype: list
    """
    annotations = []
    for link in app_data["main_fig_arc_arrowheads_dict"]:
        arrowhead_dict = app_data["main_fig_arc_arrowheads_dict"][link]
        arrowhead_color = app_data["link_color_dict"][link]
        for i in range(len(arrowhead_dict["x"])):
            annotations.append({
                "x": arrowhead_dict["x"][i][1],
                "y": arrowhead_dict["y"][i][1],
                "ax": arrowhead_dict["x"][i][0],
                "ay": arrowhead_dict["y"][i][0],
                "xref": "x",
                "yref": "y",
                "axref": "x",
                "ayref": "y",
                "showarrow": True,
                "arrowcolor": "rgb(%s, %s, %s)" % arrowhead_color,
                "arrowhead": 1,
                "arrowwidth": arrow_width,
                "arrowsize": arrow_size
            })

    return annotations


def get_link_label_annotations(app_data):
    """Get annotations to be added as link labels to main fig.

    We add these as annotations, because that is the only way to
    implement angled text.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: list of annotations to be added as link labels
    :rtype: list
    """
    annotations = []
    for link in app_data["main_fig_link_labels_dict"]:
        link_label_dict = app_data["main_fig_link_labels_dict"][link]
        link_color = app_data["link_color_dict"][link]
        for i in range(len(link_label_dict["x"])):
            annotations.append({
                "x": link_label_dict["x"][i],
                "y": link_label_dict["y"][i],
                "text": link_label_dict["text"][i],
                "textangle": link_label_dict["textangle"][i],
                "showarrow": False,
                "font": {
                    "color": "rgb(%s, %s, %s)" % link_color,
                    "size": 12
                },
                "bgcolor": "white"
            })

    return annotations


def get_arc_shapes(app_data, line_width):
    """Get main graph arc annotations in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure object that shows the arc links on the main
        graph.
    :rtype: go.Figure
    """
    shapes = []
    for link in app_data["main_fig_arcs_dict"]:
        link_dict = app_data["main_fig_arcs_dict"][link]
        (r, g, b) = app_data["link_color_dict"][link]
        for i in range(len(link_dict["x"])):
            [x0, cx, x1] = link_dict["x"][i]
            [y0, cy, y1] = link_dict["y"][i]
            shapes.append({
                "type": "path",
                "path": "M %s,%s Q %s,%s %s,%s  " % (x0, y0, cx, cy, x1, y1),
                "line_color": "rgb(%s, %s, %s)" % (r, g, b),
                "line_width": line_width,
                "layer": "below"
            })
    return shapes


def get_arc_label_annotations(app_data):
    """Get annotations to be added as arc labels to main fig.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: list of annotations to be added as arc labels
    :rtype: list
    """
    annotations = []
    for link in app_data["main_fig_arc_labels_dict"]:
        link_label_dict = app_data["main_fig_arc_labels_dict"][link]
        link_color = app_data["link_color_dict"][link]
        for i in range(len(link_label_dict["x"])):
            annotations.append({
                "x": link_label_dict["x"][i],
                "y": link_label_dict["y"][i],
                "text": link_label_dict["text"][i],
                "showarrow": False,
                "font": {
                    "color": "rgb(%s, %s, %s)" % link_color,
                    "size": 12
                },
                "bgcolor": "white"
            })

    return annotations


def get_main_fig_x_axis(app_data):
    """Get main graph x-axis in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure object that shows the x-axis belonging to
        the main graph.
    :rtype: go.Figure
    """
    ret = go.Figure(
        go.Scatter(
            x=app_data["main_fig_xaxis_tickvals"],
            y=[0.5 for _ in app_data["main_fig_xaxis_tickvals"]],
            mode="text",
            text=app_data["main_fig_xaxis_ticktext"],
            textfont={
                "size": 16
            },
            hoverinfo="skip",
            name="main_fig_x_axis_trace",
            customdata=app_data["main_fig_xaxis_range"]
        ),
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "showlegend": False,
            "xaxis": {
                "range": app_data["main_fig_xaxis_range"],
                "fixedrange": True,
                "visible": False
            },
            "yaxis": {
                "range": [0, 1],
                "fixedrange": True,
                "visible": False
            },
            "plot_bgcolor": "white"
        },
    )
    return ret


def get_main_fig_y_axis(app_data):
    """Get main graph y-axis in viz.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :return: Plotly figure object that shows the y-axis belonging to
        the main graph.
    :rtype: go.Figure
    """
    ret = go.Figure(
        go.Scatter(
            x=[0.5 for _ in app_data["main_fig_yaxis_tickvals"]],
            y=app_data["main_fig_yaxis_tickvals"],
            mode="text",
            text=app_data["main_fig_yaxis_ticktext"],
            textfont={
                "size": 16
            },
            hoverinfo="skip",
            name="main_fig_y_axis_trace",
            customdata=app_data["main_fig_yaxis_range"]
        ),
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "showlegend": False,
            "xaxis": {
                "range": [0, 1],
                "fixedrange": True,
                "visible": False
            },
            "yaxis": {
                "range": app_data["main_fig_yaxis_range"],
                "fixedrange": True,
                "visible": False
            },
            "plot_bgcolor": "white"
        },
    )
    return ret
