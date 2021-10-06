"""Parse data used by application for generating viz.

Currently using stub data in convenient format.
"""

import csv


def get_app_data(samples_tsv_path, transmissions_tsv_path):
    """Parse sample and transmission data to be vized.

    The philosophy of this fn is to provide data that is ready to be
    "plugged in". i.e., we parse and format the data in such way that
    the amount of data manipulation required downstream by modules
    dedicated to generating the actual viz is minimized. This means the
    object returned by this fn may not be easily understood by humans
    if you exported it as a stand-alone JSON file.

    The format of files specified by ``samples_tsv_path`` and
    ``transmissions_tsv_path`` is not described in this docstring,
    because we have not decided on the final data format to be fed into
    this application.

    :param samples_tsv_path: Path to tsv file describing sample data
    :type samples_tsv_path: str
    :param transmissions_tsv_path: Path to tsv file describing
        transmission data.
    :type transmissions_tsv_path: str
    :return: Sample and transmission data used to generate app viz
    :rtype: dict
    """
    samples_data_dict = \
        get_samples_data_dict(samples_tsv_path)
    transmissions_data_dict = \
        get_transmission_data_dict(transmissions_tsv_path)

    sample_dates_list = \
        [v["sample_date"] for v in samples_data_dict.values()]
    # Sort, and delete duplicates while maintaining new order
    sorted_sample_dates_tbl = dict.fromkeys(sorted(sample_dates_list))
    # Assign positive int x-vals to unique sample dates
    sample_date_x_vals_dict = {
        e: i+1 for i, e in enumerate(sorted_sample_dates_tbl)
    }

    # MGE and strain of each sample
    mge_strain_combos_list = \
        [(v["mge"], v["strain"]) for v in samples_data_dict.values()]
    # Sort, and delete duplicates while maintaining new order
    sorted_mge_strain_combos_tbl = \
        dict.fromkeys(sorted(mge_strain_combos_list))
    # Assign positive int y-vals to unique mge strain combos
    mge_strain_combos_y_vals_dict = {
        e: i+1 for i, e in enumerate(sorted_mge_strain_combos_tbl)
    }
    # Highest y-val for each mge across all its mge strain combos
    mge_highest_y_vals_dict = {
        mge: v for (mge, _), v in mge_strain_combos_y_vals_dict.items()
    }

    sample_species_list = [v["species"] for v in samples_data_dict.values()]
    species_color_dict = get_species_color_dict(sample_species_list)

    app_data = {
        "species_color_dict": species_color_dict,
        "main_fig_xaxis_range":
            [0.5, len(sample_date_x_vals_dict)+0.5],
        "main_fig_xaxis_tickvals":
            list(range(1, len(sample_date_x_vals_dict) + 1)),
        "main_fig_xaxis_ticktext":
            list(sample_date_x_vals_dict.keys()),
        "main_fig_yaxis_tickvals":
            get_main_fig_yaxis_tickvals(mge_highest_y_vals_dict),
        "main_fig_yaxis_ticktext":
            [mge for mge in mge_highest_y_vals_dict],
        "main_fig_nodes_x":
            [sample_date_x_vals_dict[x] for x in sample_dates_list],
        "main_fig_nodes_y":
            [mge_strain_combos_y_vals_dict[x] for x in mge_strain_combos_list],
        "main_fig_nodes_text": [
            v["strain"]+"<br>"+v["notes"] for v in samples_data_dict.values()
        ],
        "main_fig_nodes_marker_color":
            [species_color_dict[x] for x in sample_species_list],
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
            get_main_fig_facet_y(mge_highest_y_vals_dict)
    }
    app_data["main_fig_facet_x"] = \
        get_main_fig_facet_x(app_data["main_fig_xaxis_range"],
                             app_data["main_fig_facet_y"])
    app_data["main_fig_edge_labels_x"] = \
        get_main_fig_edge_labels_x(app_data["main_fig_edges_x"])
    app_data["main_fig_edge_labels_y"] = \
        get_main_fig_edge_labels_y(app_data["main_fig_edges_y"])
    app_data["main_fig_edge_labels_textposition"] = \
        get_main_fig_edge_labels_textposition(app_data["main_fig_edges_x"],
                                              app_data["main_fig_edges_y"])

    return app_data


def get_samples_data_dict(samples_tsv_path):
    """Parse tsv file describing sample data into dict.

    :param samples_tsv_path: Path to tsv file describing sample data
    :type samples_tsv_path: str
    :return: Dict describing sample data
    :rtype: dict
    """
    samples_data_dict = {}
    with open(samples_tsv_path) as fp:
        reader = csv.DictReader(fp, delimiter="\t")
        for row in reader:
            samples_data_dict[row.pop("sample_id")] = row
    return samples_data_dict


def get_transmission_data_dict(transmissions_tsv_path):
    """Parse tsv file describing transmission data into dict.

    :param transmissions_tsv_path: Path to tsv file describing
        transmission data.
    :type transmissions_tsv_path: str
    :return: Dict describing transmission data
    :rtype: dict
    """
    transmissions_data_dict = {}
    with open(transmissions_tsv_path) as fp:
        reader = csv.DictReader(fp, delimiter="\t")
        for row in reader:
            transmissions_data_dict[row.pop("transmission_id")] = row
    return transmissions_data_dict


def get_species_color_dict(sample_species_list):
    """Assign colors to species.

    The colors assigned are unique for up to 12 species. After 12, the
    colors are repeated.

    :param sample_species_list: Species to assign colors to
    :type sample_species_list: list
    :return: Dict of format {species: color}
    :rtype: dict
    """
    color_opts = ["#8dd3c7",
                  "#ffffb3",
                  "#bebada",
                  "#fb8072",
                  "#80b1d3",
                  "#fdb462",
                  "#b3de69",
                  "#fccde5",
                  "#d9d9d9",
                  "#bc80bd",
                  "#ccebc5",
                  "#ffed6f"]
    species_tbl = dict.fromkeys(sample_species_list)
    species_color_dict = \
        {species: color for species, color in zip(species_tbl, color_opts)}
    return species_color_dict


def get_main_fig_yaxis_tickvals(mge_highest_y_vals_dict):
    """Assign tick vals for displaying mge labels in main fig.

    Each tick val for an mge should be in the middle of the y-axis
    segment corresponding to its associated markers.

    :param mge_highest_y_vals_dict: Highest y-val for each mge across
        all its mge strain combos.
    :type mge_highest_y_vals_dict: dict
    :return: mge label tick vals in the format required by a Plotly
        linear axis.
    :rtype: list[int]
    """
    main_fig_yaxis_tickvals = []
    lowest_y = 1
    for highest_y in mge_highest_y_vals_dict.values():
        main_fig_yaxis_tickvals.append((highest_y + lowest_y) / 2)
        lowest_y = highest_y + 1
    return main_fig_yaxis_tickvals


def get_main_fig_edges_x(transmissions_data_dict, samples_data_dict,
                         sample_date_x_vals_dict):
    """Assign x vals for displaying edges between main fig markers.

    These edges represent transmission events. The edges are generated
    downstream by Plotly as a Scatter obj.

    :param transmissions_data_dict: See ``get_transmission_data_dict``
    :type transmissions_data_dict: dict
    :param samples_data_dict: See ``get_samples_data_dict``
    :type samples_data_dict: dict
    :param sample_date_x_vals_dict: Dict with positive int x-vals
        assigned to unique sample dates.
    :type sample_date_x_vals_dict: dict
    :return: Edge x vals in the format required by a Plotly Scatter obj
    :rtype: list[int]
    """
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
    """Assign y vals for displaying edges between main fig markers.

    These edges represent transmission events. The edges are generated
    downstream by Plotly as a Scatter obj.

    :param transmissions_data_dict: See ``get_transmission_data_dict``
    :type transmissions_data_dict: dict
    :param samples_data_dict: See ``get_samples_data_dict``
    :type samples_data_dict: dict
    :param mge_strain_combos_y_vals_dict: Dict with positive int y-vals
        assigned to unique mge-strain combos.
    :type mge_strain_combos_y_vals_dict: dict
    :return: Edge y vals in the format required by a Plotly Scatter obj
    :rtype: list[int]
    """
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


def get_main_fig_facet_y(mge_highest_y_vals_dict):
    """Assign y vals for facet lines dividing plot by mge.

    These lines are generated downstream by Plotly as a Scatter obj.

    :param mge_highest_y_vals_dict: Dict with highest marker y-val for
        each mge.
    :type mge_highest_y_vals_dict: dict
    :return: Facet line y vals in the format required by a Plotly
        Scatter obj.
    :rtype: list[int]
    """
    main_fig_facet_y = []
    for facet_y in [y + 0.5 for y in mge_highest_y_vals_dict.values()][:-1]:
        main_fig_facet_y += [facet_y, facet_y, None]
    return main_fig_facet_y


def get_main_fig_facet_x(main_fig_xaxis_range, main_fig_facet_y):
    """Assign x vals for facet lines dividing plot by mge.

    These lines are generated downstream by Plotly as a Scatter obj.

    :param main_fig_xaxis_range: Main fig x-axis range as specified for
        Plotly graph objs.
    :type main_fig_xaxis_range: list[int]
    :param main_fig_facet_y: See ``get_main_fig_facet_y``
    :type main_fig_facet_y: list[int]
    :return: Facet line x vals in the format required by a Plotly
        Scatter obj.
    :rtype: list[int]
    """
    main_fig_facet_x = []
    line_start = main_fig_xaxis_range[0]
    line_end = main_fig_xaxis_range[1]
    for i in range(0, len(main_fig_facet_y), 3):
        main_fig_facet_x += [line_start, line_end, None]
    return main_fig_facet_x


def get_main_fig_edge_labels_x(main_fig_edges_x):
    """Assign x vals for displaying labels over edges.

    The edge labels are generated downstream by Plotly as a Scatter obj.

    :param main_fig_edges_x: See ``get_main_fig_edges_x``
    :type main_fig_edges_x: list[int]
    :return: Edge label x vals in the format required by a Plotly
        Scatter obj.
    :rtype: list[int]
    """
    main_fig_edge_labels_x = []
    for i in range(0, len(main_fig_edges_x), 3):
        line_start = main_fig_edges_x[i]
        line_end = main_fig_edges_x[i+1]
        main_fig_edge_labels_x.append((line_start + line_end) / 2)
    return main_fig_edge_labels_x


def get_main_fig_edge_labels_y(main_fig_edges_y):
    """Assign y vals for displaying labels over edges.

    The edge labels are generated downstream by Plotly as a Scatter obj.

    :param main_fig_edges_y: See ``get_main_fig_edges_y``
    :type main_fig_edges_y: list[int]
    :return: Edge label y vals in the format required by a Plotly
        Scatter obj.
    :rtype: list[int]
    """
    main_fig_edge_labels_y = []
    for i in range(0, len(main_fig_edges_y), 3):
        line_start = main_fig_edges_y[i]
        line_end = main_fig_edges_y[i+1]
        main_fig_edge_labels_y.append((line_start + line_end) / 2)
    return main_fig_edge_labels_y


def get_main_fig_edge_labels_textposition(main_fig_edges_x, main_fig_edges_y):
    """Assign Plotly text positions to edge labels.

    The best text position will depend on the angle of the edge, which
    we can determine using the x and y values of the start and end
    positions belonging to each edge.

    :param main_fig_edges_x: See ``get_main_fig_edges_x``
    :type main_fig_edges_x: list[int]
    :param main_fig_edges_y: See ``get_main_fig_edges_y``
    :type main_fig_edges_y: list[int]
    :return: Edge label text positions in the format required by a Plotly
        Scatter obj with text markers.
    :rtype: list[str]
    """
    main_fig_edge_labels_text_pos = []
    for i in range(0, len(main_fig_edges_x), 3):
        x_line_diff = \
            main_fig_edges_x[i] - main_fig_edges_x[i+1]
        y_line_diff = \
            main_fig_edges_y[i] - main_fig_edges_y[i+1]
        if x_line_diff and y_line_diff < 0:
            main_fig_edge_labels_text_pos.append("bottom right")
        if x_line_diff and y_line_diff > 0:
            main_fig_edge_labels_text_pos.append("top right")
        elif x_line_diff and not y_line_diff:
            main_fig_edge_labels_text_pos.append("top center")
        elif not x_line_diff and y_line_diff:
            main_fig_edge_labels_text_pos.append("middle right")
    return main_fig_edge_labels_text_pos
