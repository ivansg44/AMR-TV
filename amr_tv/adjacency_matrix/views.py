from django.shortcuts import render

import amr_tv.adjacency_matrix.utils as utils
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
        utils.get_adjacency_matrix_data(isolate_genotypes_qs,
                                        organism_groups_list)
    plot_div = utils.get_adjacency_matrix_plot(data, organism_groups_list)
    return render(request, "base.html", {"adjacency_matrix": plot_div})
