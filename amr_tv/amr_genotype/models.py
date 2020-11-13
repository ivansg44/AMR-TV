from django.contrib.postgres.fields import ArrayField
from django.db import models


class AMRGenotype(models.Model):
    """Distinct AMR genotypes NCBI Isolates Browser."""
    amr_genotype = models.TextField(primary_key=True)
    isolates = ArrayField(models.TextField())
