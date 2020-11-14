from django.shortcuts import render
from plotly import express as px
from plotly.offline import plot

from amr_tv.isolate.models import Isolate


def adjacency_matrix_view(request):
    """wip"""
    # TODO: May not need to use viewsets???
    queryset = Isolate.objects.all()
    queryset = queryset.filter(create_date__range=("2020-10-29", "2020-10-31"))
    organism_groups_list = \
        list(queryset.values_list('organism_group', flat=True).distinct())
    fig = px.imshow([[1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20],
                     [20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1],
                     [30, 60, 1, 30, 60, 1, 30, 60, 1, 30, 60, 1, 30, 60],
                     [1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20],
                     [20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1],
                     [30, 60, 1, 30, 60, 1, 30, 60, 1, 30, 60, 1, 30, 60],
                     [1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20],
                     [20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1],
                     [30, 60, 1, 30, 60, 1, 30, 60, 1, 30, 60, 1, 30, 60],
                     [1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20],
                     [20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1],
                     [30, 60, 1, 30, 60, 1, 30, 60, 1, 30, 60, 1, 30, 60],
                     [1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20, 30, 1, 20],
                     [20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1, 60, 20, 1],
                     ],
                    x=organism_groups_list,
                    y=organism_groups_list
                    )
    fig.update_xaxes(side="top")
    plt_div = plot(fig, output_type='div')
    return render(request, "base.html", {"foo": plt_div})
