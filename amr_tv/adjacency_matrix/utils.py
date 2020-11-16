from copy import deepcopy
from functools import reduce
from operator import mul

from django.db.models import Count

from amr_tv.isolate.models import Isolate, IsolateGenotype


def foo():
    """wip"""
    # TODO: May not need to use viewsets???
    date_range = ("2020-10-01", "2020-10-31")
    isolates_qs = Isolate.objects.all().filter(create_date__range=date_range)
    organism_groups_list = \
        isolates_qs.values_list('organism_group', flat=True).distinct()
    ret_val = {organism_group: 0 for organism_group in organism_groups_list}
    ret = {organism_group: deepcopy(ret_val) for organism_group in organism_groups_list}

    isolate_genotypes_qs = \
        IsolateGenotype.objects.all().filter(create_date__range=date_range)
    shared_genotypes_qs = \
        isolate_genotypes_qs.values("amr_genotype", "organism_group")
    shared_genotype_counts_qs = \
        shared_genotypes_qs.annotate(count=Count("amr_genotype"))

    count_acc = 0
    amr_genotype_acc = ""
    organism_groups_acc = set()
    for e in shared_genotype_counts_qs.order_by("amr_genotype"):
        if e["amr_genotype"] != amr_genotype_acc:
            edge_count = ncr(count_acc, 2)
            for organism_group in organism_groups_acc:
                for second_organism_group in organism_groups_acc:
                    ret[organism_group][second_organism_group] += edge_count
            count_acc = 0
            amr_genotype_acc = e["amr_genotype"]
            organism_groups_acc = set()
        count_acc += e["count"]
        organism_groups_acc.add(e["organism_group"])

    return ret


def ncr(n, r):
    """wip https://stackoverflow.com/a/4941932"""
    r = min(r, n-r)
    numer = reduce(mul, range(n, n-r, -1), 1)
    denom = reduce(mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2
