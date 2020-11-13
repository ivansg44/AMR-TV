from rest_framework.serializers import HyperlinkedModelSerializer

from amr_tv.amr_genotype.models import AMRGenotype


class AMRGenotypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AMRGenotype
        fields = [
            "amr_genotype",
            "isolates"
        ]
