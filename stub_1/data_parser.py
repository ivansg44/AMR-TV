from collections import Counter
import csv
from datetime import datetime


def get_app_data(sample_csv_path, track, attr_link_list,
                 links_across_y, max_day_range, node_color_attr=None):
    sample_data_dict = get_sample_data_dict(sample_csv_path)

    date_list = [v["date"] for v in sample_data_dict.values()]
    date_x_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(date_list)))
    }

    track_list = [v[track] for v in sample_data_dict.values()]
    track_y_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(track_list)))
    }

    main_fig_nodes_y_dict = get_main_fig_nodes_y_dict(sample_data_dict,
                                                      track,
                                                      date_list,
                                                      track_list,
                                                      track_y_vals_dict)

    organism_list = [v["organism"] for v in sample_data_dict.values()]
    organism_symbol_dict = get_organism_symbol_dict(organism_list)

    if node_color_attr:
        node_color_attr_list = \
            [v[node_color_attr] for v in sample_data_dict.values()]
        node_color_attr_dict = get_node_color_attr_dict(node_color_attr_list)
        main_fig_nodes_marker_color = \
            [node_color_attr_dict[v] for v in node_color_attr_list]
    else:
        node_color_attr_dict = None
        main_fig_nodes_marker_color = "lightgrey"

    sample_links_dict = \
        get_sample_links_dict(attr_link_list=attr_link_list,
                              sample_data_dict=sample_data_dict,
                              track=track,
                              links_across_y=links_across_y,
                              max_day_range=max_day_range,
                              date_x_vals_dict=date_x_vals_dict,
                              main_fig_nodes_y_dict=main_fig_nodes_y_dict)

    app_data = {
        "node_shape_legend_fig_nodes_y":
            list(range(len(organism_symbol_dict))),
        "node_shape_legend_fig_nodes_marker_symbol":
            list(organism_symbol_dict.values()),
        "node_shape_legend_fig_nodes_text":
            ["<b>%s</b>" % k for k in organism_symbol_dict.keys()],
        "main_fig_xaxis_range":
            [0.5, len(date_x_vals_dict) + 0.5],
        "main_fig_yaxis_range":
            [0.5, len(track_y_vals_dict) + 0.5],
        "main_fig_xaxis_tickvals":
            list(range(1, len(date_x_vals_dict) + 1)),
        "main_fig_xaxis_ticktext":
            list(date_x_vals_dict.keys()),
        "main_fig_yaxis_tickvals":
            list(range(1, len(track_y_vals_dict) + 1)),
        "main_fig_yaxis_ticktext":
            list(track_y_vals_dict.keys()),
        "main_fig_nodes_x":
            [date_x_vals_dict[e] for e in date_list],
        "main_fig_nodes_y":
            [main_fig_nodes_y_dict[k] for k in sample_data_dict],
        "main_fig_nodes_marker_symbol":
            [organism_symbol_dict[v] for v in organism_list],
        "main_fig_nodes_marker_color":
            main_fig_nodes_marker_color,
        "main_fig_nodes_text":
            ["<b>%s</b>" % v["patient_id"] for v in sample_data_dict.values()],
        "sample_links_dict": sample_links_dict,
        "node_color_attr_dict": node_color_attr_dict
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
                "datetime_obj": datetime_obj,
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


def get_node_color_attr_dict(node_color_attr_list):
    node_color_attr_dict = {}
    node_color_attr_table = dict.fromkeys(node_color_attr_list)

    # TODO make color blind safe by using color + pattern
    available_colors = [
        "#8dd3c7",
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
        "#ffed6f"
    ]
    next_index_in_color_list = 0

    if len(node_color_attr_table) > len(node_color_attr_table):
        msg = "Not enough unique colors for specified node attribute"
        raise IndexError(msg)


    for node_color_attr in node_color_attr_table:
        node_color_attr_dict[node_color_attr] = \
            available_colors[next_index_in_color_list]
        next_index_in_color_list += 1

    return node_color_attr_dict


def get_sample_links_dict(attr_link_list, sample_data_dict, track,
                          links_across_y, max_day_range, date_x_vals_dict,
                          main_fig_nodes_y_dict):
    available_link_color_dash_combos = [
        ("#1b9e77", "solid"), ("#d95f02", "solid"), ("#7570b3", "solid"),
        ("#1b9e77", "dot"), ("#d95f02", "dot"), ("#7570b3", "dot"),
    ]
    next_index_in_color_dash_list = 0
    if len(attr_link_list) > len(available_link_color_dash_combos):
        msg = "Not enough unique edge patterns for different attributes"
        raise IndexError(msg)

    offset = 0 - (len(attr_link_list) / 200)

    sample_links_dict = {}
    for attr in attr_link_list:
        attr_link_list = get_link_list(sample_data_dict=sample_data_dict,
                                       track=track,
                                       attr=attr,
                                       links_across_y=links_across_y,
                                       max_day_range=max_day_range)
        link_list_x = get_link_list_x(link_list=attr_link_list,
                                      sample_data_dict=sample_data_dict,
                                      date_x_vals_dict=date_x_vals_dict)
        link_list_y = \
            get_link_list_y(link_list=attr_link_list,
                            main_fig_nodes_y_dict=main_fig_nodes_y_dict)

        sample_links_dict[attr] = {}
        sample_links_dict[attr]["x"] = \
            [e+offset if e else e for e in link_list_x]
        sample_links_dict[attr]["y"] = \
            [e+offset if e else e for e in link_list_y]
        sample_links_dict[attr]["color"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][0]
        sample_links_dict[attr]["dash"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][1]

        offset += 0.01
        next_index_in_color_dash_list += 1

    return sample_links_dict


def get_link_list(sample_data_dict, track, attr, links_across_y,
                  max_day_range):
    link_list = []
    sample_list = list(sample_data_dict.keys())
    for i in range(len(sample_list)):
        sample = sample_list[i]

        if sample_data_dict[sample][attr] == "-":
            continue

        for j in range(i+1, len(sample_list)):
            other_sample = sample_list[j]

            sample_track = sample_data_dict[sample][track]
            other_track = sample_data_dict[other_sample][track]
            if not links_across_y and sample_track != other_track:
                continue

            sample_datetime = sample_data_dict[sample]["datetime_obj"]
            other_datetime = sample_data_dict[other_sample]["datetime_obj"]
            day_range_datetime = other_datetime - sample_datetime
            day_range = abs(day_range_datetime.days)
            if max_day_range < day_range:
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


def get_main_fig_nodes_y_dict(sample_data_dict, track, date_list, track_list,
                              track_y_vals_dict):
    date_track_zip_list = list(zip(date_list, track_list))
    helper_obj = \
        {k: [1/(v+1), 1] for k, v in Counter(date_track_zip_list).items()}

    main_fig_nodes_y_dict = {}
    for sample in sample_data_dict:
        sample_date = sample_data_dict[sample]["date"]
        sample_track = sample_data_dict[sample][track]
        [stagger, multiplier] = helper_obj[(sample_date, sample_track)]

        unstaggered_y = track_y_vals_dict[sample_track]
        lowest_y = unstaggered_y - 0.5
        staggered_y = lowest_y + (stagger * multiplier)

        main_fig_nodes_y_dict[sample] = staggered_y
        helper_obj[(sample_date, sample_track)][1] += 1

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
