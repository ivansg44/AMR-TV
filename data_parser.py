"""TODO"""

import csv


def get_app_data(samples_tsv_path, transmissions_tsv_path):
    """TODO"""
    samples_data_dict = {}
    with open(samples_tsv_path) as fp:
        reader = csv.DictReader(fp, delimiter="\t")
        for row in reader:
            samples_data_dict[row.pop("sample_id")] = row
    transmissions_data_dict = {}
    with open(transmissions_tsv_path) as fp:
        reader = csv.DictReader(fp, delimiter="\t")
        for row in reader:
            transmissions_data_dict[row.pop("transmission_id")] = row
    app_data = {
        "main_fig_nodes_x": get_main_fig_nodes_x(samples_data_dict),
        "main_fig_nodes_y": get_main_fig_nodes_y(samples_data_dict)
    }
    return app_data


def get_main_fig_nodes_x(samples_data_dict):
    """TODO"""
    sample_dates_list = [v["sample_date"] for v in samples_data_dict.values()]
    sorted_sample_dates_list = sorted(sample_dates_list)
    sample_date_x_vals_dict = \
        {e: i+1 for i, e in enumerate(dict.fromkeys(sorted_sample_dates_list))}
    main_fig_nodes_x = [sample_date_x_vals_dict[x] for x in sample_dates_list]
    return main_fig_nodes_x


def get_main_fig_nodes_y(samples_data_dict):
    """TODO"""
    mge_strain_combos_list = \
        [(v["mge"], v["strain"]) for v in samples_data_dict.values()]
    mge_strain_combos_y_vals_dict = \
        {e: i+1 for i, e in enumerate(dict.fromkeys(mge_strain_combos_list))}
    main_fig_nodes_y = \
        [mge_strain_combos_y_vals_dict[x] for x in mge_strain_combos_list]
    return main_fig_nodes_y
