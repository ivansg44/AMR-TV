from amr_tv.isolate.models import Isolate


def foo():
    """wip"""
    # TODO: May not need to use viewsets???
    queryset = Isolate.objects.all()
    queryset = queryset.filter(create_date__range=("2020-10-29", "2020-10-31"))
    organism_groups_list = \
        list(queryset.values_list('organism_group', flat=True).distinct())
    ret = {organism_group: 0 for organism_group in organism_groups_list}
    return ret
