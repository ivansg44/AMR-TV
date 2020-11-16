from functools import reduce
from itertools import combinations
from operator import mul

from django.db.models import Count
from numpy import zeros
from plotly import express as px
from plotly.offline import plot


def get_adjacency_matrix_plot(data, organism_groups_list):
    """wip"""
    fig = px.imshow(data,
                    x=organism_groups_list,
                    y=organism_groups_list,
                    color_continuous_scale="Greys"
                    )
    fig.update_xaxes(side="top")
    fig.update_layout(width=1000,
                      height=1000)
    return plot(fig, output_type='div', config={"responsive": True})


def get_adjacency_matrix_data(isolate_genotypes_qs, organism_groups_list):
    """wip"""
    organism_groups_count = len(organism_groups_list)
    data = zeros((organism_groups_count, organism_groups_count))

    shared_genotypes_qs = \
        isolate_genotypes_qs.values("amr_genotype", "organism_group")
    shared_genotype_counts_qs = \
        shared_genotypes_qs.annotate(count=Count("amr_genotype"))

    count_acc = 0
    amr_genotype_acc = ""
    organism_groups_acc = set()
    organism_groups_list_indices = \
        {k: v for v, k in enumerate(organism_groups_list)}
    for entry in shared_genotype_counts_qs.order_by("amr_genotype"):
        if entry["amr_genotype"] != amr_genotype_acc:
            edge_count = ncr(count_acc, 2)
            for organism_group in organism_groups_acc:
                x = organism_groups_list_indices[organism_group]
                data[x][x] += edge_count
            for pair in combinations(organism_groups_acc, 2):
                x = organism_groups_list_indices[pair[0]]
                y = organism_groups_list_indices[pair[1]]
                data[x][y] += edge_count
                data[y][x] += edge_count
            count_acc = 0
            amr_genotype_acc = entry["amr_genotype"]
            organism_groups_acc = set()
        count_acc += entry["count"]
        organism_groups_acc.add(entry["organism_group"])

    return data


def ncr(n, r):
    """wip https://stackoverflow.com/a/4941932"""
    r = min(r, n-r)
    numer = reduce(mul, range(n, n-r, -1), 1)
    denom = reduce(mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2
