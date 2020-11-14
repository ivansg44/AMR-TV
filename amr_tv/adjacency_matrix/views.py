from django.shortcuts import render
from plotly import express as px
from plotly.offline import plot


def adjacency_matrix_view(request):
    fig = px.imshow([[1, 20, 30],
                     [20, 1, 60],
                     [30, 60, 1]])
    plt_div = plot(fig, output_type='div')
    return render(request, "base.html", {"foo": plt_div})
