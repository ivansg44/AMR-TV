import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

from django.shortcuts import HttpResponse

from amr_tv.isolate.models import Isolate


def node_detail_table_view(request):
    """TODO: ..."""
    headers = []
    for field in Isolate._meta.get_fields():
        if field.name != "organism_group" and field.name != "amr_genotypes":
            headers.append(field.name)

    query_params = dict(request.GET)
    organism_group = query_params["organism_group"][0]
    amr_genotypes = query_params["amr_genotypes[]"]
    node_detail_qs = Isolate.objects.filter(
        create_date__range=request.session["date_range"],
        organism_group=organism_group,
        amr_genotypes=amr_genotypes
    )

    df = pd.DataFrame(list(node_detail_qs.values_list(*headers)), columns=headers)

    fig = go.Figure(data=[go.Table(
        header=dict(values=headers,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[header] for header in headers],
                   fill_color='lavender',
                   align='left'))
    ])

    plot_div = plot(fig, output_type="div")

    return HttpResponse(plot_div)
