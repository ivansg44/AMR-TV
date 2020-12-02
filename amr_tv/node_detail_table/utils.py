from amr_tv.isolate.models import Isolate


def get_headers():
    """Get column headers for node-detail table.

    This means getting every field from Isolate that isn't
    organism_group and amr_genotypes. This function should only be
    called once, and then assigned to a global variable.

    :return: Node-detail table column headers.
    :rtype: list[str]
    """
    headers = []
    for field in Isolate._meta.get_fields():
        if field.name != "organism_group" and field.name != "amr_genotypes":
            headers.append(field.name)
    return headers
