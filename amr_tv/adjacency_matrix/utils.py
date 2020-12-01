from math import log10

from numpy import zeros
from plotly import express as px


def get_adjacency_matrix_fig(data, organism_groups_list):
    """Get plotly figure of adjacency matrix.

    Really, it's a heatmap.

    :param data: See get_adjacency_matrix_data return value.
    :type data: Numpy.array
    :param organism_groups_list: List of organism groups encoding axes
    values.
    :type organism_groups_list: list[str]
    :return: Plotly figure of adjacency matrix.
    :rtype: plotly.graph_objects.Figure
    """
    fig = px.imshow(data,
                    x=organism_groups_list,
                    y=organism_groups_list,
                    color_continuous_scale="Greys"
                    )
    fig.update_xaxes(side="top")
    fig.update_layout(width=850,
                      height=850)
    return fig


def get_adjacency_matrix_data(transmission_events, organism_groups_list):
    """Get data that goes into rendered adjacency matrix.

    :param transmission_events: See run_transmission_events_query
    return value.
    :type transmission_events: list[list]
    :param organism_groups_list: List of organism groups encoding axes
    values.
    :type organism_groups_list: list[str]
    :return: Matrix storing number of log10 transmission events
    between different organism groups.
    :rtype: Numpy.array
    """
    organism_groups_count = len(organism_groups_list)
    data = zeros((organism_groups_count, organism_groups_count))
    organism_groups_list_indices = \
        {k: v for v, k in enumerate(organism_groups_list)}
    for row in transmission_events:
        x = organism_groups_list_indices[row[1]]
        y = organism_groups_list_indices[row[4]]
        data[x][y] += 1
        data[y][x] += 1

    for i in range(organism_groups_count):
        for j in range(organism_groups_count):
            if data[i][j] > 0:
                data[i][j] = log10(data[i][j])

    return data


def get_highlighted_adjacency_matrix_fig(fig, selected_cells):
    """Add highlights to fig.

    :param fig: See get_adjacency_matrix_fig return value.
    :type fig: plotly.graph_objects.Figure
    :param selected_events: Specified organism_group-organism_group
    relationships inside nested dictionary.
    :type selected_events: dict[str, dict[str, None]]
    :return: Fig with some yellow and transparent rectangles added to
    it.
    :rtype: plotly.graph_objects.Figure
    """
    for organism_group in selected_cells:
        if not len(selected_cells[organism_group]):
            continue
        nested_organism_groups = selected_cells[organism_group]
        for group in nested_organism_groups:
            x = nested_organism_groups[group][0]
            y = nested_organism_groups[group][1]
            fig.add_shape(
                type="rect",
                x0=x-0.5,
                x1=x+0.5,
                y0=y-0.5,
                y1=y+0.5,
                line={
                    "color": "orange",
                    "width": 3
                },
                fillcolor="rgba(240,255,0,0.2)"
            )

    return fig
