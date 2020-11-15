from math import factorial

from django.db.models import Count

from amr_tv.isolate.models import Isolate, IsolateGenotype


def foo():
    """wip"""
    # TODO: May not need to use viewsets???
    date_range = ("2020-10-29", "2020-10-31")
    isolates_qs = Isolate.objects.all().filter(create_date__range=date_range)
    organism_groups_list = \
        isolates_qs.values_list('organism_group', flat=True).distinct()
    ret_val = {organism_group: 0 for organism_group in organism_groups_list}
    ret = {organism_group: ret_val for organism_group in organism_groups_list}

    isolate_genotypes_qs = \
        IsolateGenotype.objects.all().filter(create_date__range=date_range)
    total_num_edges = count_edges(isolate_genotypes_qs)

    return ret


def count_edges(isolate_genotypes_qs, organism_group=None):
    """wip"""
    genotypes_qs = isolate_genotypes_qs.values("amr_genotype")
    shared_genotype_counts_qs = \
        genotypes_qs.annotate(total=Count("amr_genotype"))
    shared_genotype_counts_list = \
        shared_genotype_counts_qs.values_list("total", flat=True)
    edge_counts_list = \
        [count_unique_pairs(count) for count in shared_genotype_counts_list]
    return sum(edge_counts_list)


def count_unique_pairs(num_items):
    """wip"""
    if num_items < 2:
        return 0

    return factorial(num_items) // factorial(2) // factorial(num_items-2)
