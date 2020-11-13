from rest_framework.viewsets import ReadOnlyModelViewSet

from amr_tv.amr_genotype.models import AMRGenotype
from amr_tv.amr_genotype.serializers import AMRGenotypeSerializer


class AMRGenotypeViewSet(ReadOnlyModelViewSet):
    queryset = AMRGenotype.objects.all().order_by("amr_genotype")
    serializer_class = AMRGenotypeSerializer
