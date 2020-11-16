from django.shortcuts import render
import numpy as np
from plotly import express as px
from plotly.offline import plot

from amr_tv.adjacency_matrix.utils import foo


def adjacency_matrix_view(request):
    """wip"""
    # TODO: May not need to use viewsets???
    foo_ret = foo()
    organism_groups_list = list(foo_ret.keys())
    organism_groups_count = len(organism_groups_list)
    data = np.zeros((organism_groups_count, organism_groups_count))
    for i in range(organism_groups_count):
        for j in range(organism_groups_count):
            first_organism_group = organism_groups_list[i]
            second_organism_group = organism_groups_list[j]
            data[i][j] = foo_ret[first_organism_group][second_organism_group]
    fig = px.imshow(data,
                    x=organism_groups_list,
                    y=organism_groups_list,
                    color_continuous_scale="Greens"
                    )
    fig.update_xaxes(side="top")
    fig.update_layout(width=1000,
                      height=1000)
    plt_div = plot(fig, output_type='div', config={"responsive": True})
    return render(request, "base.html", {"foo": plt_div})
