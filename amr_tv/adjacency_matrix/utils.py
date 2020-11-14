import pandas as pd

from amr_tv.isolate.models import Isolate


def foo():
    """wip"""
    # TODO: May not need to use viewsets???
    isolate_qs = Isolate.objects.all()
    isolate_qs = \
        isolate_qs.filter(create_date__range=("2020-10-29", "2020-10-31"))
    df = pd.DataFrame.from_records(isolate_qs.values())

    df_organism_groups = df.groupby(by="organism_group").groups

    ret = {organism_group: 0 for organism_group in df_organism_groups}
    return ret
