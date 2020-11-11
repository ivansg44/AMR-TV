from rest_framework.viewsets import ReadOnlyModelViewSet

from amr_tv.isolate.models import Isolate
from amr_tv.isolate.serializers import IsolateSerializer


class IsolateViewSet(ReadOnlyModelViewSet):
    """wip"""
    queryset = Isolate.objects.all().order_by("-create_date")
    serializer_class = IsolateSerializer
