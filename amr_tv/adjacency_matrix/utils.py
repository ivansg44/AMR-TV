from math import log10

from numpy import zeros
from plotly import express as px
from plotly.offline import plot


def get_adjacency_matrix_plot(data, organism_groups_list):
    """TODO: ..."""
    fig = px.imshow(data,
                    x=organism_groups_list,
                    y=organism_groups_list,
                    color_continuous_scale="Greys"
                    )
    fig.update_xaxes(side="top")
    fig.update_layout(width=1000,
                      height=1000)
    return plot(fig, output_type="div", config={"responsive": True})


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
