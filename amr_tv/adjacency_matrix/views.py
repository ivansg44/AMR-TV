from django.shortcuts import render
import numpy as np
from plotly import express as px
from plotly.offline import plot

from amr_tv.adjacency_matrix.utils import get_adjacency_matrix_data
from amr_tv.isolate.models import Isolate, IsolateGenotype


def adjacency_matrix_view(request):
    """wip"""
    # Stub date range
    date_range = ("2020-10-01", "2020-10-31")

    isolates_qs = Isolate.objects.all().filter(create_date__range=date_range)
    organism_groups_list = \
        list(isolates_qs.values_list('organism_group', flat=True).distinct())

    isolate_genotypes_qs = \
        IsolateGenotype.objects.all().filter(create_date__range=date_range)
    data = \
        get_adjacency_matrix_data(isolate_genotypes_qs, organism_groups_list)
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
