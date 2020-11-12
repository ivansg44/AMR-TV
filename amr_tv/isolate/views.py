from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from amr_tv.isolate.models import Isolate
from amr_tv.isolate.serializers import IsolateSerializer


class IsolateViewSet(ReadOnlyModelViewSet):
    """wip"""
    queryset = Isolate.objects.all().order_by("-create_date")
    serializer_class = IsolateSerializer
    lookup_value_regex = '[\w.]+'

    def list(self, request):
        """Lists all isolates over optionally supplied time period.

        Overrides superclass method.

        :param request: May contain query parameters start_date and
        end_date.
        """
        start_date = request.query_params.get("start_date", "0001-01-01")
        end_date = request.query_params.get("end_date", "9999-01-01")
        queryset = self.get_queryset()
        queryset = queryset.filter(create_date__range=(start_date, end_date))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
