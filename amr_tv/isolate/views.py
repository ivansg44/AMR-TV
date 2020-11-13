from rest_framework.viewsets import ReadOnlyModelViewSet

from amr_tv.isolate.models import Isolate
from amr_tv.isolate.serializers import IsolateSerializer


class IsolateViewSet(ReadOnlyModelViewSet):
    serializer_class = IsolateSerializer
    lookup_value_regex = '[\w.]+'

    def get_queryset(self):
        """Optionally return isolates over time period."""
        queryset = Isolate.objects.all().order_by("-create_date")
        start_date = self.request.query_params.get("start_date", "0001-01-01")
        end_date = self.request.query_params.get("end_date", "9999-01-01")
        return queryset.filter(create_date__range=(start_date, end_date))
