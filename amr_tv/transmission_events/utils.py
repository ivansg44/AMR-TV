from django.db import connection


def run_transmission_events_query(date_range):
    """Runs SQL query to get transmission events.

    :param date_range: create_date range of isolates to derive network
    from.
    :type date_range: list[str, str]
    :return: Transmission events, detailing amr_genotypes,
    organism_group, and min_date for two nodes from derived network.
    :rtype: list[list]
    """
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
