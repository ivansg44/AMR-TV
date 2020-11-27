from django.db import connection

from amr_tv.isolate.models import Isolate


def get_organism_groups_list(date_range):
    """TODO: ..."""
    isolates_qs = Isolate.objects.all().filter(create_date__range=date_range)
    return \
        list(isolates_qs.values_list('organism_group', flat=True).distinct())


def get_node_color_map(organism_groups_list):
    """TODO: ..."""
    # https://colorbrewer2.org/?type=qualitative&scheme=Set1&n=9
    colour_scheme = [
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33",
        "#a65628", "#f781bf", "#999999"
    ]

    acc = 0
    color_map = {}
    for organism_group in organism_groups_list:
        color_map[organism_group] = colour_scheme[acc % len(colour_scheme)]
        acc += 1

    return color_map


def run_transmission_events_query(date_range):
    """TODO: ..."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT a.amr_genotypes, a.organism_group, a.min_date, "
                       "b.amr_genotypes, b.organism_group, b.min_date "
                       "FROM ("
                       "SELECT organism_group, min(create_date) min_date, "
                       "amr_genotypes, array_agg(isolate) isolates "
                       "FROM isolate_isolate "
                       "WHERE create_date BETWEEN %s AND %s "
                       "GROUP BY organism_group, amr_genotypes"
                       ") a INNER JOIN ("
                       "SELECT organism_group, min(create_date) min_date, "
                       "amr_genotypes, array_agg(isolate) isolates "
                       "FROM isolate_isolate "
                       "WHERE create_date BETWEEN %s AND %s "
                       "GROUP BY organism_group, amr_genotypes"
                       ") b ON a.min_date < b.min_date "
                       "AND a.amr_genotypes <@ b.amr_genotypes "
                       "AND a.amr_genotypes <> b.amr_genotypes",
                       [date_range[0], date_range[1],
                        date_range[0], date_range[1]])
        rows = cursor.fetchall()

    return rows
