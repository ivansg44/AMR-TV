from collections import Counter
import csv
from datetime import datetime


def get_app_data(sample_csv_path, links_across_y):
    sample_data_dict = get_sample_data_dict(sample_csv_path)

    date_list = [v["date"] for v in sample_data_dict.values()]
    date_x_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(date_list)))
    }

    location_list = [v["location"] for v in sample_data_dict.values()]
    location_y_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(location_list)))
    }

    main_fig_nodes_y_dict = get_main_fig_nodes_y_dict(sample_data_dict,
                                                      date_list,
                                                      location_list,
                                                      location_y_vals_dict)

    organism_list = [v["organism"] for v in sample_data_dict.values()]
    organism_symbol_dict = get_organism_symbol_dict(organism_list)

    mobility_list = \
        [v["predicted_mobility"] for v in sample_data_dict.values()]
    mobility_marker_dict = {"Conjugative": "#a6cee3",
                            "Non-mobilizable": "#b2df8a"}

    some_args = {"sample_data_dict": sample_data_dict,
                 "link_across_y": links_across_y}
    mlst_links = get_link_list(**{**some_args, **{"attr": "mlst"}})
    gene_links = get_link_list(**{**some_args, **{"attr": "gene"}})
    homozygous_snps_links = \
        get_link_list(**{**some_args, **{"attr": "homozygous_snps"}})
    flanks_links = get_link_list(**{**some_args, **{"attr": "flanks"}})
    mash_neighbour_cluster_links =\
        get_link_list(**{**some_args, **{"attr": "mash_neighbour_cluster"}})
    replicon_types_links = \
        get_link_list(**{**some_args, **{"attr": "replicon_types"}})

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
            [main_fig_nodes_y_dict[k] for k in sample_data_dict],
        "main_fig_nodes_marker_symbol":
            [organism_symbol_dict[v] for v in organism_list],
        "main_fig_nodes_marker_color":
            [mobility_marker_dict[v] for v in mobility_list],
        "main_fig_nodes_text":
            ["<b>%s</b>" % v["patient_id"] for v in sample_data_dict.values()],
        "main_fig_mlst_links_x":
            get_link_list_x(mlst_links, date_x_vals_dict, sample_data_dict),
        "main_fig_mlst_links_y":
            get_link_list_y(mlst_links, main_fig_nodes_y_dict),
        "main_fig_gene_links_x":
            get_link_list_x(gene_links, date_x_vals_dict, sample_data_dict),
        "main_fig_gene_links_y":
            get_link_list_y(gene_links, main_fig_nodes_y_dict),
        "main_fig_homozygous_snps_links_x":
            get_link_list_x(homozygous_snps_links,
                            date_x_vals_dict,
                            sample_data_dict),
        "main_fig_homozygous_snps_links_y":
            get_link_list_y(homozygous_snps_links, main_fig_nodes_y_dict),
        "main_fig_flanks_links_x":
            get_link_list_x(flanks_links, date_x_vals_dict, sample_data_dict),
        "main_fig_flanks_links_y":
            get_link_list_y(flanks_links, main_fig_nodes_y_dict),
        "main_fig_mash_neighbour_cluster_links_x":
            get_link_list_x(mash_neighbour_cluster_links,
                            date_x_vals_dict,
                            sample_data_dict),
        "main_fig_mash_neighbour_cluster_links_y":
            get_link_list_y(mash_neighbour_cluster_links,
                            main_fig_nodes_y_dict),
        "main_fig_replicon_types_links_x":
            get_link_list_x(replicon_types_links,
                            date_x_vals_dict,
                            sample_data_dict),
        "main_fig_replicon_types_links_y":
            get_link_list_y(replicon_types_links, main_fig_nodes_y_dict),
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
                "flanks": row["Left_flanks"] + row["Right_flanks"],
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


def get_link_list(sample_data_dict, attr, link_across_y):
    link_list = []
    sample_list = list(sample_data_dict.keys())
    for i in range(len(sample_list)):
        sample = sample_list[i]
        for j in range(i+1, len(sample_list)):
            other_sample = sample_list[j]

            sample_location = sample_data_dict[sample]["location"]
            other_location = sample_data_dict[other_sample]["location"]
            if not link_across_y and sample_location != other_location:
                continue

            sample_val = sample_data_dict[sample][attr]
            other_sample_val = sample_data_dict[other_sample][attr]
            if sample_val == other_sample_val:
                link_list.append((sample, other_sample))
    return link_list


def get_link_list_x(link_list, date_x_vals_dict, sample_data_dict):
    link_list_x = []
    for (sample, other_sample) in link_list:
        date = sample_data_dict[sample]["date"]
        other_date = sample_data_dict[other_sample]["date"]
        link_list_x += [
            date_x_vals_dict[date],
            date_x_vals_dict[other_date],
            None
        ]
    return link_list_x


def get_link_list_y(link_list, main_fig_nodes_y_dict):
    link_list_y = []
    for (sample, other_sample) in link_list:
        main_fig_node_y = main_fig_nodes_y_dict[sample]
        other_main_fig_node_y = main_fig_nodes_y_dict[other_sample]
        link_list_y += [main_fig_node_y, other_main_fig_node_y, None]
    return link_list_y


def get_main_fig_nodes_y_dict(sample_data_dict, date_list, location_list,
                              location_y_vals_dict):
    date_location_zip_list = list(zip(date_list, location_list))
    helper_obj = \
        {k: [1/(v+1), 1] for k, v in Counter(date_location_zip_list).items()}

    main_fig_nodes_y_dict = {}
    for sample in sample_data_dict:
        sample_date = sample_data_dict[sample]["date"]
        sample_location = sample_data_dict[sample]["location"]
        [stagger, multiplier] = helper_obj[(sample_date, sample_location)]

        unstaggered_y = location_y_vals_dict[sample_location]
        lowest_y = unstaggered_y - 0.5
        staggered_y = lowest_y + (stagger * multiplier)

        main_fig_nodes_y_dict[sample] = staggered_y
        helper_obj[(sample_date, sample_location)][1] += 1

    return main_fig_nodes_y_dict


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
