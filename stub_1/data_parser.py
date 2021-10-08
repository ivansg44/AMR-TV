from collections import Counter
import csv
from datetime import datetime


def get_app_data(sample_csv_path):
    sample_data_dict = get_sample_data_dict(sample_csv_path)

    date_list = [v["date"] for v in sample_data_dict.values()]
    date_x_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(date_list)))
    }

    location_list = [v["location"] for v in sample_data_dict.values()]
    location_y_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(location_list)))
    }

    organism_list = [v["organism"] for v in sample_data_dict.values()]
    organism_symbol_dict = get_organism_symbol_dict(organism_list)

    app_data = {
        "main_fig_xaxis_range":
            [0.5, len(date_x_vals_dict) + 0.5],
        "main_fig_yaxis_range":
            [0.5, len(location_y_vals_dict) + 0.5],
        "main_fig_xaxis_tickvals":
            list(range(1, len(date_x_vals_dict) + 1)),
        "main_fig_xaxis_ticktext":
            list(date_x_vals_dict.keys()),
        "main_fig_yaxis_tickvals":
            list(range(1, len(location_y_vals_dict) + 1)),
        "main_fig_yaxis_ticktext":
            list(location_y_vals_dict.keys()),
        "main_fig_nodes_x":
            [date_x_vals_dict[e] for e in date_list],
        "main_fig_nodes_y":
            get_main_fig_nodes_y(date_list,
                                 location_list,
                                 location_y_vals_dict),
        "main_fig_nodes_marker_symbol":
            [organism_symbol_dict[v] for v in organism_list],
        "main_fig_nodes_text":
            ["<b>%s</b>" % v["patient_id"] for v in sample_data_dict.values()]
    }

    num_of_facets = len(app_data["main_fig_yaxis_tickvals"]) - 1
    app_data["main_fig_facet_y"] =\
        get_main_fig_facet_y(num_of_facets)
    app_data["main_fig_facet_x"] =\
        get_main_fig_facet_x(app_data["main_fig_xaxis_range"], num_of_facets)

    return app_data


def get_sample_data_dict(sample_csv_path):
    sample_data_dict = {}
    with open(sample_csv_path) as fp:
        next(fp)
        reader = csv.DictReader(fp)
        for row in reader:
            sample_id = row["Sample ID / Isolate"]
            if not sample_id:
                continue

            datetime_obj =\
                datetime.strptime(row["Date of collection"], "%B %Y")
            datetime_iso_str = datetime_obj.strftime("%G-%m-%d")

            sample_data_dict[sample_id] = {
                "patient_id": row["Patient ID"],
                "location": row["Location"],
                "date": datetime_iso_str,
                "organism": row["Organism"],
                "mlst": row["F1: MLST type"],
                "gene": row["Resitance gene type"],
                "homozygous_snps": row["SNPs_homozygous"],
                "left_flanks": row["Left_flanks"],
                "right_flanks": row["Right_flanks"],
                "mash_neighbour_cluster": row["mash_neighbor_cluster"],
                "replicon_types": row["rep_type(s)"],
                "relaxase_types": row["relaxase_type(s)"],
                "predicted_mobility": row["PredictedMobility"]
            }
    return sample_data_dict


def get_organism_symbol_dict(organism_list):
    organism_symbol_dict = {}
    organism_table = dict.fromkeys(organism_list)

    available_plotly_symbols = [
        "circle", "square", "diamond", "cross", "x", "triangle-up"
    ]
    next_index_in_symbol_list = 0

    if len(organism_table) > len(available_plotly_symbols):
        raise IndexError("Not enough unique symbols for different organisms")

    for organism in organism_table:
        organism_symbol_dict[organism] =\
            available_plotly_symbols[next_index_in_symbol_list]
        next_index_in_symbol_list += 1
    return organism_symbol_dict


def get_main_fig_nodes_y(date_list, location_list, location_y_vals_dict):
    main_fig_nodes_y = []

    date_location_zip_list = list(zip(date_list, location_list))
    helper_obj = \
        {k: [1/(v+1), 1] for k, v in Counter(date_location_zip_list).items()}

    for combo in date_location_zip_list:
        unstaggered_y = location_y_vals_dict[combo[1]]
        lowest_y = unstaggered_y - 0.5
        staggered_y = lowest_y + (helper_obj[combo][0] * helper_obj[combo][1])
        helper_obj[combo][1] += 1
        main_fig_nodes_y.append(staggered_y)

    return main_fig_nodes_y


def get_main_fig_facet_x(main_fig_xaxis_range, num_of_facets):
    main_fig_facet_x = []
    [xmin, xmax] = main_fig_xaxis_range
    for i in range(0, num_of_facets):
        main_fig_facet_x += [xmin, xmax, None]
    return main_fig_facet_x


def get_main_fig_facet_y(num_of_facets):
    main_fig_facet_y = []
    for i in range(0, num_of_facets):
        main_fig_facet_y += [i+1.5, i+1.5, None]
    return main_fig_facet_y
