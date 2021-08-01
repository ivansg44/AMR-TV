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
            [mge_strain_combos_y_vals_dict[x] for x in mge_strain_combos_list],
        "main_fig_edges_x":
            get_main_fig_edges_x(transmissions_data_dict,
                                 samples_data_dict,
                                 sample_date_x_vals_dict),
        "main_fig_edges_y":
            get_main_fig_edges_y(transmissions_data_dict,
                                 samples_data_dict,
                                 mge_strain_combos_y_vals_dict),
        "main_fig_edge_labels_text":
            [v["notes"] for v in transmissions_data_dict.values()],
        "main_fig_facet_y":
            get_main_fig_facet_y(mge_strain_combos_y_vals_dict)
    }
    app_data["main_fig_facet_x"] = get_main_fig_facet_x(app_data)
    app_data["main_fig_edge_labels_x"] = get_main_fig_edge_labels_x(app_data)
    app_data["main_fig_edge_labels_y"] = get_main_fig_edge_labels_y(app_data)

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


def get_main_fig_edges_x(transmissions_data_dict, samples_data_dict,
                         sample_date_x_vals_dict):
    """TODO"""
    main_fig_edges_x = []
    for transmission_id in transmissions_data_dict:
        sample_one_id = \
            transmissions_data_dict[transmission_id]["sample_id_one"]
        sample_two_id = \
            transmissions_data_dict[transmission_id]["sample_id_two"]
        sample_one_date = samples_data_dict[sample_one_id]["sample_date"]
        sample_two_date = samples_data_dict[sample_two_id]["sample_date"]
        sample_one_x = sample_date_x_vals_dict[sample_one_date]
        sample_two_x = sample_date_x_vals_dict[sample_two_date]
        main_fig_edges_x += [sample_one_x, sample_two_x, None]
    return main_fig_edges_x


def get_main_fig_edges_y(transmissions_data_dict, samples_data_dict,
                         mge_strain_combos_y_vals_dict):
    """TODO"""
    main_fig_edges_y = []
    for transmission_id in transmissions_data_dict:
        sample_one_id = \
            transmissions_data_dict[transmission_id]["sample_id_one"]
        sample_two_id = \
            transmissions_data_dict[transmission_id]["sample_id_two"]
        sample_one_mge_strain_combo = \
            (samples_data_dict[sample_one_id]["mge"],
             samples_data_dict[sample_one_id]["strain"])
        sample_two_mge_strain_combo = \
            (samples_data_dict[sample_two_id]["mge"],
             samples_data_dict[sample_two_id]["strain"])
        sample_one_y = \
            mge_strain_combos_y_vals_dict[sample_one_mge_strain_combo]
        sample_two_y = \
            mge_strain_combos_y_vals_dict[sample_two_mge_strain_combo]
        main_fig_edges_y += [sample_one_y, sample_two_y, None]
    return main_fig_edges_y


def get_main_fig_facet_y(mge_strain_combos_y_vals_dict):
    """TODO"""
    last_mge_seen = None
    main_fig_facet_y = []
    for mge_strain_combo in mge_strain_combos_y_vals_dict:
        if last_mge_seen is not None and last_mge_seen != mge_strain_combo[0]:
            y_val = mge_strain_combos_y_vals_dict[mge_strain_combo] - 0.5
            main_fig_facet_y += [y_val, y_val, None]
        last_mge_seen = mge_strain_combo[0]
    return main_fig_facet_y


def get_main_fig_facet_x(app_data):
    """TODO"""
    main_fig_facet_x = []
    line_start = app_data["main_fig_nodes_x"][0] - 0.5
    line_end = app_data["main_fig_nodes_x"][-1] + 0.5
    for i in range(0, len(app_data["main_fig_facet_y"]), 3):
        main_fig_facet_x += [line_start, line_end, None]
    return main_fig_facet_x


def get_main_fig_edge_labels_x(app_data):
    """TODO"""
    main_fig_edge_labels_x = []
    for i in range(0, len(app_data["main_fig_edges_x"]), 3):
        line_start = app_data["main_fig_edges_x"][i]
        line_end = app_data["main_fig_edges_x"][i+1]
        main_fig_edge_labels_x.append((line_start + line_end) / 2)
    return main_fig_edge_labels_x


def get_main_fig_edge_labels_y(app_data):
    """TODO"""
    main_fig_edge_labels_y = []
    for i in range(0, len(app_data["main_fig_edges_y"]), 3):
        line_start = app_data["main_fig_edges_y"][i]
        line_end = app_data["main_fig_edges_y"][i+1]
        main_fig_edge_labels_y.append((line_start + line_end) / 2)
    return main_fig_edge_labels_y
