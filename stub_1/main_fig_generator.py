import plotly.graph_objects as go


def get_main_fig_nodes(app_data, node_size):
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
            "size": node_size,
            "symbol": app_data["main_fig_nodes_marker_symbol"],
            "opacity": app_data["main_fig_nodes_marker_opacity"]
        },
        text=app_data["main_fig_nodes_text"],
        textfont={
            "color": "black",
            "size": 16
        }
    )
    return nodes


def get_main_fig_link_graphs(app_data):
    link_graphs = []
    for attr in app_data["sample_links_dict"]:
        opaque_link_dict = app_data["sample_links_dict"][attr]["opaque"]
        (r, g, b) = opaque_link_dict["color"]
        link_graphs.append(
            go.Scatter(
                x=[x if x else None for x in opaque_link_dict["x"]],
                y=[y if y else None for y in opaque_link_dict["y"]],
                mode="lines",
                line={
                    "width": 3,
                    "color": "rgb(%s, %s, %s)" % (r, g, b),
                    "dash": opaque_link_dict["dash"]
                }
            )
        )

        transparent_link_dict = \
            app_data["sample_links_dict"][attr]["transparent"]
        (r, g, b) = transparent_link_dict["color"]
        link_graphs.append(
            go.Scatter(
                x=[x if x else None for x in transparent_link_dict["x"]],
                y=[y if y else None for y in transparent_link_dict["y"]],
                mode="lines",
                line={
                    "width": 3,
                    "color": "rgba(%s, %s, %s, 0.01)" % (r, g, b),
                    "dash": opaque_link_dict["dash"]
                }
            )
        )
    return link_graphs


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


def get_main_fig(app_data, node_size, xaxis_range, yaxis_range):
    main_fig_link_graphs = get_main_fig_link_graphs(app_data)
    fig = go.Figure(
        data=main_fig_link_graphs + [
            get_main_fig_nodes(app_data, node_size),
            get_main_fig_facet_lines(app_data)
        ],
        layout={
            "margin": {
                "l": 0, "r": 0, "t": 0, "b": 0
            },
            "showlegend": False,
            "xaxis": {
                "range": xaxis_range,
                "tickmode": "array",
                "tickvals": app_data["main_fig_xaxis_tickvals"],
                "ticktext": app_data["main_fig_xaxis_ticktext"],
                "tickfont": {
                    "size": 16
                },
                "linecolor": "black"
            },
            "yaxis": {
                "range": yaxis_range,
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
