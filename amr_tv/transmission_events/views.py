import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

import amr_tv.transmission_events.utils as utils


def transmission_events_view(request):
    """TODO: ..."""
    date_range = json.loads(request.GET["date_range"])
    organism_groups_list = utils.get_organism_groups_list(date_range)
    request.session["organism_groups_list"] = \
        utils.get_organism_groups_list(date_range)

    raw_query_data = utils.run_transmission_events_query(date_range)
    request.session["transmission_events"] = \
        json.dumps(raw_query_data, cls=DjangoJSONEncoder)

    return JsonResponse({"organismGroupsArr": organism_groups_list})
