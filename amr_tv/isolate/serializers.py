from rest_framework import serializers

from amr_tv.isolate.models import Isolate


class IsolateSerializer(serializers.HyperlinkedModelSerializer):
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


class IsolateLinkSerializer(serializers.Serializer):
    """wip"""
    isolate_1 = serializers.CharField()
    isolate_2 = serializers.CharField()
    amr_genotypes_1 = serializers.ListField(child=serializers.CharField())
    amr_genotypes_2 = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
