from django.db.models import F
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from amr_tv.isolate.models import Isolate
from amr_tv.isolate.serializers import IsolateSerializer, IsolateLinkSerializer


class IsolateViewSet(ReadOnlyModelViewSet):
    """wip"""
    queryset = Isolate.objects.all().order_by("-create_date")
    serializer_class = IsolateSerializer
    lookup_value_regex = '[\w.]+'

    def list(self, request):
        """Lists all isolates over optionally supplied time period.

        Overrides superclass method. If end_date is supplied,
        end_date-1 is used.

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

    @action(detail=False)
    def links(self, request):
        """wip"""
        queryset = self.get_queryset().annotate(isolate_1=F("isolate"), isolate_2=F("isolate"), amr_genotypes_1=F("amr_genotypes"), amr_genotypes_2=F("amr_genotypes"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = IsolateLinkSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = IsolateLinkSerializer(queryset, many=True)
        return Response(serializer.data)
