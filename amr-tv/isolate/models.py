from django.db import models


class Isolate(models.Model):
    """Samples from NCBI Isolates Browser."""
    organism_group = models.TextField()
    isolate = models.TextField(primary_key=True)
    create_date = models.DateTimeField
    location = models.TextField()
    isolation_source = models.TextField()
    host = models.TextField()
    amr_genotypes = models.JSONField()
