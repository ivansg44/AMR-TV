import json

from django.shortcuts import HttpResponse

import amr_tv.adjacency_matrix.utils as utils
from amr_tv.isolate.models import Isolate


def adjacency_matrix_view(request):
    """TODO: ..."""
    date_range = request.session["date_range"]
    isolates_qs = Isolate.objects.all().filter(create_date__range=date_range)
    organism_groups_list = \
        list(isolates_qs.values_list('organism_group', flat=True).distinct())

    transmission_events = json.loads(request.session["transmission_events"])

    data = utils.get_adjacency_matrix_data(transmission_events,
                                           organism_groups_list)
    plot_div = utils.get_adjacency_matrix_plot(data, organism_groups_list)
    return HttpResponse(plot_div)
