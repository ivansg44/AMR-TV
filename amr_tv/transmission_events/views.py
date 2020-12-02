import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import HttpResponse

import amr_tv.transmission_events.utils as utils


def transmission_events_view(request):
    """Stores all transmission events in session.

    A transmission event is defined as the amr_genotypes of an older
    node from the derived network being encapsulated by a newer node.

    :param request: Contains date_range value to specify which
    isolates to consider when deriving network.
    :return: Indication that all went well.
    :rtype: HttpResponse
    """
    date_range = json.loads(request.GET["date_range"])

    # We cached the events of Oct 2020
    if date_range[0] == "2020-10-01" and date_range[1] == "2020-10-31":
        json_path = settings.APPS_DIR.path("transmission_events",
                                           "stub_transmission_events.json")
        with open(json_path) as fp:
            request.session["transmission_events"] = json.load(fp)
    else:
        raw_query_data = utils.run_transmission_events_query(date_range)
        request.session["transmission_events"] = \
            json.dumps(raw_query_data, cls=DjangoJSONEncoder)

    return HttpResponse("Transmission events loaded successfully")
