"""TODO"""

import csv


def get_app_data(samples_tsv_path, transmissions_tsv_path):
    """TODO"""
    samples_data_dict = \
        get_samples_data_dict(samples_tsv_path)
    transmissions_data_dict = \
        get_transmission_data_dict(transmissions_tsv_path)

    sample_dates_list = \
        [v["sample_date"] for v in samples_data_dict.values()]
    sorted_sample_dates_tbl = \
        dict.fromkeys(sorted(sample_dates_list))
    sample_date_x_vals_dict = {
        e: i+1 for i, e in enumerate(sorted_sample_dates_tbl)
    }

    mge_strain_combos_list = \
        [(v["mge"], v["strain"]) for v in samples_data_dict.values()]
    sorted_mge_strain_combos_tbl = \
        dict.fromkeys(sorted(mge_strain_combos_list))
    mge_strain_combos_y_vals_dict = {
        e: i+1 for i, e in enumerate(sorted_mge_strain_combos_tbl)
    }

    app_data = {
        "main_fig_nodes_x":
            [sample_date_x_vals_dict[x] for x in sample_dates_list],
        "main_fig_nodes_y":
            [mge_strain_combos_y_vals_dict[x] for x in mge_strain_combos_list]
    }
    return app_data


def get_samples_data_dict(samples_tsv_path):
    """TODO"""
    samples_data_dict = {}
    with open(samples_tsv_path) as fp:
        reader = csv.DictReader(fp, delimiter="\t")
        for row in reader:
            samples_data_dict[row.pop("sample_id")] = row
    return samples_data_dict


def get_transmission_data_dict(transmissions_tsv_path):
    """TODO"""
    transmissions_data_dict = {}
    with open(transmissions_tsv_path) as fp:
        reader = csv.DictReader(fp, delimiter="\t")
        for row in reader:
            transmissions_data_dict[row.pop("transmission_id")] = row
    return transmissions_data_dict
