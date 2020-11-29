import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

from django.http import JsonResponse

from amr_tv.isolate.models import Isolate
import amr_tv.node_detail_table.utils as utils

_headers = utils.get_headers()


def node_detail_table_view(request):
    """TODO: ..."""
    query_params = dict(request.GET)
    organism_group = query_params["organism_group"][0]
    amr_genotypes = query_params["amr_genotypes[]"]
    node_detail_qs = Isolate.objects.filter(
        create_date__range=request.session["date_range"],
        organism_group=organism_group,
        amr_genotypes=amr_genotypes
    )

    df = pd.DataFrame(list(node_detail_qs.values_list(*_headers)), columns=_headers)

    fig = go.Figure(
        data=[go.Table(
            header=dict(values=_headers,
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df[header] for header in _headers],
                       fill_color='lavender',
                       align='left',
                       height=24,
                       ))],
        layout={
            "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
            "font": {"size": 14}
        }
    )

    plot_div = plot(fig, output_type="div")

    return JsonResponse({
        "organismGroup": organism_group,
        "amrGenotypes": amr_genotypes,
        "plotDiv": plot_div
    })
