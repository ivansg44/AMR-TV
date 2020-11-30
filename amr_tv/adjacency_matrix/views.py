import json

from django.shortcuts import HttpResponse
import plotly.graph_objects as go
from plotly.offline import plot

import amr_tv.adjacency_matrix.utils as utils

# For faster rendering in highlighted view
_base_fig = None


def adjacency_matrix_view(request):
    """TODO: ..."""
    organism_groups_list = json.loads(request.GET["data"])
    transmission_events = json.loads(request.session["transmission_events"])
    data = utils.get_adjacency_matrix_data(transmission_events,
                                           organism_groups_list)

    global _base_fig
    _base_fig = utils.get_adjacency_matrix_fig(data, organism_groups_list)
    plot_div = plot(_base_fig, output_type="div")

    return HttpResponse(plot_div)


def highlighted_adjacency_matrix_view(request):
    """TODO: ..."""
    # Copy global variable
    fig = go.Figure(_base_fig)
    if not fig:
        return HttpResponse(fig)

    selected_cells = json.loads(request.GET["data"])
    highlighted_fig = \
        utils.get_highlighted_adjacency_matrix_fig(fig, selected_cells)
    plot_div = plot(highlighted_fig, output_type="div")

    return HttpResponse(plot_div)
