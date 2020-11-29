from amr_tv.isolate.models import Isolate


def get_headers():
    """TODO: ..."""
    headers = []
    for field in Isolate._meta.get_fields():
        if field.name != "organism_group" and field.name != "amr_genotypes":
            headers.append(field.name)
    return headers
