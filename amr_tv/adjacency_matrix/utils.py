from math import log10

from numpy import zeros
from plotly import express as px


def get_adjacency_matrix_fig(data, organism_groups_list):
    """TODO: ..."""
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
    """TODO: ..."""
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
    """TODO: ..."""
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
