import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import HttpResponse

import amr_tv.transmission_events.utils as utils


def transmission_events_view(request):
    """TODO: ..."""
    # Stub date range
    request.session["date_range"] = ["2020-10-01", "2020-10-31"]
    request.session["organism_groups_list"] = \
        utils.get_organism_groups_list(request.session["date_range"])

    raw_query_data = \
        utils.run_transmission_events_query(request.session["date_range"])

    request.session["transmission_events"] = \
        json.dumps(raw_query_data, cls=DjangoJSONEncoder)

    return HttpResponse("Transmission data added to session")
