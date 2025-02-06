"""Fns for generating legend figs in viz."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
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


def get_link_legend_fig_graph_objs(link_type, link_color, is_filtered):
    """Get Plotly scatter/bar objs that render one link in link legend.

    The link legend has multiple links in it. This only draws one.

    The scatter obj draws the link. An invisible bar obj allows easier
    registration of click events.

    :param link_type: ``data_parser.get_app_data`` ret val
    :type link_type: str
    :param link_color: RGB color val of link
    :type link_color: tuple[int, int, int]
    :param is_filtered: Whether link is filtered or not
    :type is_filtered: bool
    :return: Plotly scatter/bar obj used to draw a link in link legend
    :rtype: list[go.Scatter, go.Bar]
    """
    (r, g, b) = link_color
    a = "0.5" if is_filtered else "1"
    scatter_obj = go.Scatter(
        x=[0, 1],
        y=[1, 1],
        mode="lines+text",
        line={
            "width": 3,
            "color": "rgba(%s, %s, %s, %s)" % (r, g, b, a),
        },
        text=["<b>%s</b>" % link_type, None],
        textfont={
            "color": "grey" if is_filtered else "black",
            "size": 16
        },
        textposition="top right",
        hoverinfo="skip"
    )
    # Invisible bar chart underneath to register clicks
    bar_obj = go.Bar(
        x=[1],
        y=[1],
        hoverinfo="none",
        orientation="h",
        width=1,
        opacity=0
    )
    return [scatter_obj, bar_obj]


def get_link_legend_fig(link_type, link_color, is_filtered):
    """Get Plotly fig that renders one link in link legend.

    The link legend has multiple links in it. This only draws one.

    :param link_type: ``data_parser.get_app_data`` ret val
    :type link_type: str
    :param link_color: RGB color val of link
    :type link_color: tuple[int, int, int]
    :param is_filtered: Whether link is filtered or not
    :type is_filtered: bool
    :return: Plotly fig obj used to draw one link in link legend
    :rtype: go.Figure
    """
    graph_objs = \
        get_link_legend_fig_graph_objs(link_type, link_color, is_filtered)
    fig = go.Figure(
        data=graph_objs,
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
            },
            "showlegend": False,
            "plot_bgcolor": "white",
            "height": 75,
        }
    )
    return fig


def get_link_legend_col(app_data, link_filter_collapse_states_dict):
    """Get link legend col in viz.TODO

    This is a list of graphs, one per link type, and sliders/filter
    btns if a link type is visible and has weights.

    :param app_data: ``data_parser.get_app_data`` ret val
    :type app_data: dict
    :param link_filter_form_collapse_states: List of whether link
        filter forms are open, in the order they appear on the legend.
    :type link_filter_form_collapse_states: list[bool]
    :return: Graphs, sliders, and filter btns constituting link legend
        in viz.
    :rtype: list[dcc.Graph|dcc.RangeSlider|dbc.Button]
    """
    children = []
    for attr in app_data["main_fig_links_dict"]:
        link_color = app_data["link_color_dict"][attr]
        is_filtered = attr in app_data["filtered_link_types"]

        link_legend_fig = get_link_legend_fig(attr, link_color, is_filtered)
        children.append(
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=link_legend_fig,
                              id={"type": "link-legend-fig", "index": attr},
                              config={"displayModeBar": False})
                )
            )
        )

        if attr not in app_data["weight_slider_info_dict"]:
            continue
        min_weight = app_data["weight_slider_info_dict"][attr]["min"]
        max_weight = app_data["weight_slider_info_dict"][attr]["max"]
        val = app_data["weight_slider_info_dict"][attr]["value"]
        marks = app_data["weight_slider_info_dict"][attr]["marks"]
        children.append(
            dbc.Row(
                children = [
                    dbc.Col(
                        dcc.RangeSlider(id={"type": "link-legend-slider",
                                            "index": attr},
                                        className="pt-2",
                                        min=min_weight,
                                        max=max_weight,
                                        value=val,
                                        step=None,
                                        marks=marks,
                                        allowCross=False,
                                        tooltip={})
                    ),
                    dbc.Col(
                        dbc.Button(
                            html.I(className="bi-funnel-fill",
                                   style={"font-size": 16}),
                            id={"type": "link-legend-filter-btn",
                                "index": attr},
                            className="px-0 pt-1",
                            color="link",
                            size="sm"
                        ),
                        width="auto"
                    )
                ],
                no_gutters=True
            )
        )

        if attr not in app_data["weight_filter_form_dict"]:
            continue
        # Assemble form for dealing with neq conditions
        checklist = dbc.Checklist(
            options=app_data["weight_filter_form_dict"][attr]["options"],
            value=app_data["weight_filter_form_dict"][attr]["value"],
            id={"type": "link-legend-filter-form", "index": attr}
        )
        if attr not in link_filter_collapse_states_dict:
            # Forms are collapsed by default
            is_open = False
        else:
            is_open = link_filter_collapse_states_dict[attr]
        children.append(
            dbc.Row(
                dbc.Col(
                    dbc.Collapse(
                        checklist,
                        id={"type": "link-legend-filter-collapse",
                            "index": attr},
                        is_open=is_open
                    )
                )
            )
        )
    return children


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
