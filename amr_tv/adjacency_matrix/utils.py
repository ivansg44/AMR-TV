from math import log10

from django.db import connection
from numpy import zeros
from plotly import express as px
from plotly.offline import plot


def get_links(date_range):
    """TODO: ..."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT a.amr_genotypes, a.organism_group, a.min_date, "
                       "b.amr_genotypes, b.organism_group, b.min_date "
                       "FROM ("
                       "SELECT organism_group, min(create_date) min_date, "
                       "amr_genotypes, array_agg(isolate) isolates "
                       "FROM isolate_isolate "
                       "WHERE create_date BETWEEN %s AND %s "
                       "GROUP BY organism_group, amr_genotypes"
                       ") a INNER JOIN ("
                       "SELECT organism_group, min(create_date) min_date, "
                       "amr_genotypes, array_agg(isolate) isolates "
                       "FROM isolate_isolate "
                       "WHERE create_date BETWEEN %s AND %s "
                       "GROUP BY organism_group, amr_genotypes"
                       ") b ON a.min_date < b.min_date "
                       "AND a.amr_genotypes <@ b.amr_genotypes "
                       "AND a.amr_genotypes <> b.amr_genotypes",
                       [date_range[0], date_range[1],
                        date_range[0], date_range[1]])
        rows = cursor.fetchall()

    return rows


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


def get_adjacency_matrix_data(links, organism_groups_list):
    """TODO: ..."""
    organism_groups_count = len(organism_groups_list)
    data = zeros((organism_groups_count, organism_groups_count))
    organism_groups_list_indices = \
        {k: v for v, k in enumerate(organism_groups_list)}
    for link in links:
        x = organism_groups_list_indices[link[1]]
        y = organism_groups_list_indices[link[4]]
        data[x][y] += 1

    for i in range(organism_groups_count):
        for j in range(organism_groups_count):
            if data[i][j] > 0:
                data[i][j] = log10(data[i][j])

    return data
