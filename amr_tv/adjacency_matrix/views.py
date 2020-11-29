import json

from django.shortcuts import HttpResponse

import amr_tv.adjacency_matrix.utils as utils


def adjacency_matrix_view(request):
    """TODO: ..."""
    organism_groups_list = json.loads(request.GET["data"])

    transmission_events = json.loads(request.session["transmission_events"])

    data = utils.get_adjacency_matrix_data(transmission_events,
                                           organism_groups_list)
    plot_div = utils.get_adjacency_matrix_plot(data, organism_groups_list)
    return HttpResponse(plot_div)
