from django.contrib.postgres.fields import ArrayField
from django.db import models


class Isolate(models.Model):
    """Samples from NCBI Isolates Browser."""
    organism_group = models.TextField()
    isolate = models.TextField(primary_key=True)
    create_date = models.DateTimeField()
    location = models.TextField()
    isolation_source = models.TextField()
    host = models.TextField()
    amr_genotypes = ArrayField(models.TextField())


class IsolateGenotype(models.Model):
    """Similar to isolate, but with unnested genotypes.

    Useful for counting and finding shared genotypes. Better to
    populate this once, than every time at runtime.
    """
    isolate = models.TextField()
    amr_genotype = models.TextField()
    create_date = models.DateTimeField()
    organism_group = models.TextField()
