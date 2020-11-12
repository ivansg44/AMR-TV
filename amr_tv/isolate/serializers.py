from rest_framework.serializers import HyperlinkedModelSerializer

from amr_tv.isolate.models import Isolate


class IsolateSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Isolate
        fields = [
            "organism_group",
            "isolate",
            "create_date",
            "location",
            "isolation_source",
            "host",
            "amr_genotypes"
        ]
