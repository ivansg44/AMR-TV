import json

from django.http import JsonResponse
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

from amr_tv.isolate.models import Isolate
import amr_tv.node_detail_table.utils as utils

_headers = utils.get_headers()


def node_detail_table_view(request):
    """TODO: ..."""
    query_params = json.loads(request.GET["data"])
    date_range = query_params["date_range"]
    organism_group = query_params["organism_group"]
    amr_genotypes = query_params["amr_genotypes"]

    node_detail_qs = Isolate.objects.filter(
        create_date__range=date_range,
        organism_group=organism_group,
        amr_genotypes=amr_genotypes
    )
    node_detail_values_list = list(node_detail_qs.values_list(*_headers))
    df = pd.DataFrame(node_detail_values_list, columns=_headers)

    header_dict = {"values": _headers, "align": "left"}
    cells_dict = {
        "values": [df[header] for header in _headers],
        "align": "left",
        "height": 24
    }
    table_trace = go.Table(header=header_dict, cells=cells_dict)

    fig = go.Figure(
        data=[table_trace],
        layout= {
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
