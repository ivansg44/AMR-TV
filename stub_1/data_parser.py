from collections import Counter
import csv
from datetime import datetime


def get_app_data(sample_file_path, delimiter, node_id, track, date_attr,
                 date_format, label_attr, attr_link_list, links_across_y,
                 max_day_range, null_vals, node_symbol_attr=None,
                 node_color_attr=None, y_key=None, selected_points=None):
    if selected_points is None:
        selected_points = {}

    sample_data_dict = get_sample_data_dict(sample_file_path,
                                            delimiter,
                                            node_id,
                                            date_attr,
                                            date_format,
                                            null_vals)
    enumerated_samples = enumerate(sample_data_dict)
    selected_samples = \
        {k: None for i, k in enumerated_samples if str(i) in selected_points}

    date_list = [v[date_attr] for v in sample_data_dict.values()]
    date_x_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(date_list)))
    }

    track_list = [v[track] for v in sample_data_dict.values()]
    sorted_track_list = get_sorted_track_list(track_list, y_key=y_key)
    track_y_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted_track_list))
    }

    main_fig_nodes_y_dict = \
        get_main_fig_nodes_y_dict(sample_data_dict,
                                  date_attr=date_attr,
                                  date_list=date_list,
                                  track=track,
                                  track_list=track_list,
                                  track_y_vals_dict=track_y_vals_dict)

    if node_symbol_attr:
        node_symbol_attr_list = \
            [v[node_symbol_attr] for v in sample_data_dict.values()]
        node_symbol_attr_dict = \
            get_node_symbol_attr_dict(node_symbol_attr_list)
        main_fig_nodes_marker_symbol = \
            [node_symbol_attr_dict[v] for v in node_symbol_attr_list]
    else:
        node_symbol_attr_dict = {}
        main_fig_nodes_marker_symbol = "square"

    point_range = range(len(sample_data_dict))
    if selected_points:
        main_fig_nodes_marker_opacity = \
            [1 if str(e) in selected_points else 0.5 for e in point_range]
    else:
        main_fig_nodes_marker_opacity = 1

    if node_color_attr:
        node_color_attr_list = \
            [v[node_color_attr] for v in sample_data_dict.values()]
        node_color_attr_dict = get_node_color_attr_dict(node_color_attr_list)
        main_fig_nodes_marker_color = \
            [node_color_attr_dict[v] for v in node_color_attr_list]
    else:
        node_color_attr_dict = {}
        main_fig_nodes_marker_color = "lightgrey"

    sample_links_dict = \
        get_sample_links_dict(attr_link_list=attr_link_list,
                              sample_data_dict=sample_data_dict,
                              track=track,
                              links_across_y=links_across_y,
                              max_day_range=max_day_range,
                              date_x_vals_dict=date_x_vals_dict,
                              main_fig_nodes_y_dict=main_fig_nodes_y_dict,
                              null_vals=null_vals,
                              date_attr=date_attr,
                              selected_samples=selected_samples)

    app_data = {
        "node_shape_legend_fig_nodes_y":
            list(range(len(node_symbol_attr_dict))),
        "node_shape_legend_fig_nodes_marker_symbol":
            list(node_symbol_attr_dict.values()),
        "node_shape_legend_fig_nodes_text":
            ["<b>%s</b>" % k for k in node_symbol_attr_dict.keys()],
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
            main_fig_nodes_marker_symbol,
        "main_fig_nodes_marker_color":
            main_fig_nodes_marker_color,
        "main_fig_nodes_marker_opacity":
            main_fig_nodes_marker_opacity,
        "main_fig_nodes_text":
            ["<b>%s</b>" % v[label_attr] for v in sample_data_dict.values()],
        "sample_links_dict": sample_links_dict,
        "node_color_attr_dict": node_color_attr_dict
    }

    num_of_facets = len(app_data["main_fig_yaxis_tickvals"]) - 1
    app_data["main_fig_facet_y"] =\
        get_main_fig_facet_y(num_of_facets)
    app_data["main_fig_facet_x"] =\
        get_main_fig_facet_x(app_data["main_fig_xaxis_range"], num_of_facets)

    return app_data


def get_sorted_track_list(track_list, y_key=None):
    if y_key == "int":
        y_key = int
    elif y_key is not None:
        msg = 'Currently only accept "int" as a y_key, or its default arg ' \
              '``None``.'
        raise ValueError(msg)

    return sorted(track_list, key=y_key)


def get_sample_data_dict(sample_file_path, delimiter, node_id, date,
                         date_format, null_vals):
    sample_data_dict = {}
    with open(sample_file_path) as fp:
        reader = csv.DictReader(fp, delimiter=delimiter)
        for row in reader:
            sample_id = row[node_id]
            if sample_id in null_vals:
                continue

            row["datetime_obj"] = datetime.strptime(row[date], date_format)
            row[date] = row["datetime_obj"].strftime("%Y-%m-%d")

            sample_data_dict[sample_id] = row
    return sample_data_dict


def get_node_symbol_attr_dict(node_symbol_attr_list):
    node_symbol_attr_dict = {}
    node_symbol_attr_table = dict.fromkeys(node_symbol_attr_list)

    available_plotly_symbols = [
        "circle", "square", "diamond", "cross", "x", "triangle-up"
    ]
    next_index_in_symbol_list = 0

    if len(node_symbol_attr_table) > len(available_plotly_symbols):
        msg = "Not enough unique symbols for specified node attribute"
        raise IndexError(msg)

    for node_symbol_attr in node_symbol_attr_table:
        node_symbol_attr_dict[node_symbol_attr] =\
            available_plotly_symbols[next_index_in_symbol_list]
        next_index_in_symbol_list += 1
    return node_symbol_attr_dict


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

    if len(node_color_attr_table) > len(available_colors):
        msg = "Not enough unique colors for specified node attribute"
        raise IndexError(msg)

    for node_color_attr in node_color_attr_table:
        node_color_attr_dict[node_color_attr] = \
            available_colors[next_index_in_color_list]
        next_index_in_color_list += 1

    return node_color_attr_dict


def get_sample_links_dict(attr_link_list, sample_data_dict, track,
                          links_across_y, max_day_range, date_x_vals_dict,
                          main_fig_nodes_y_dict, null_vals, date_attr,
                          selected_samples):
    available_link_color_dash_combos = [
        ((27, 158, 119), "solid"), ((217, 95, 2), "solid"),
        ((117, 112, 179), "solid"), ((217, 95, 2), "dot"),
        ((217, 95, 2), "dot"), ((117, 112, 179), "dot"),
    ]
    next_index_in_color_dash_list = 0
    if len(attr_link_list) > len(available_link_color_dash_combos):
        msg = "Not enough unique edge patterns for different attributes"
        raise IndexError(msg)

    offset = 0 - (len(attr_link_list) / 200)

    sample_links_dict = {}
    for attr in attr_link_list:
        sample_links_list = \
            get_sample_links_list(sample_data_dict=sample_data_dict,
                                  track=track,
                                  attr=attr,
                                  links_across_y=links_across_y,
                                  max_day_range=max_day_range,
                                  null_vals=null_vals)
        sample_links_dict[attr] = {
            "opaque": {},
            "transparent": {}
        }

        if selected_samples:
            opaque_sample_links_list = []
            transparent_sample_links_list = []
            for (x, y) in sample_links_list:
                if x in selected_samples or y in selected_samples:
                    opaque_sample_links_list.append((x, y))
                else:
                    transparent_sample_links_list.append((x, y))
        else:
            opaque_sample_links_list = sample_links_list
            transparent_sample_links_list = []

        opaque_link_list_x = \
            get_link_list_x(link_list=opaque_sample_links_list,
                            date_x_vals_dict=date_x_vals_dict,
                            sample_data_dict=sample_data_dict,
                            date_attr=date_attr)
        opaque_link_list_y = \
            get_link_list_y(link_list=opaque_sample_links_list,
                            main_fig_nodes_y_dict=main_fig_nodes_y_dict)
        for i in range(0, len(opaque_sample_links_list)*3, 3):
            [x1, x2] = opaque_link_list_x[i:i+2]
            [y1, y2] = opaque_link_list_y[i:i+2]
            if x1 != x2:
                opaque_link_list_y[i] += offset
                opaque_link_list_y[i+1] += offset
            if y1 != y2:
                opaque_link_list_x[i] += offset
                opaque_link_list_x[i+1] += offset
        sample_links_dict[attr]["opaque"]["x"] = opaque_link_list_x
        sample_links_dict[attr]["opaque"]["y"] = opaque_link_list_y
        sample_links_dict[attr]["opaque"]["color"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][0]
        sample_links_dict[attr]["opaque"]["dash"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][1]

        transparent_link_list_x = \
            get_link_list_x(link_list=transparent_sample_links_list,
                            date_x_vals_dict=date_x_vals_dict,
                            sample_data_dict=sample_data_dict,
                            date_attr=date_attr)
        transparent_link_list_y = \
            get_link_list_y(link_list=transparent_sample_links_list,
                            main_fig_nodes_y_dict=main_fig_nodes_y_dict)
        for i in range(0, len(transparent_sample_links_list)*3, 3):
            [x1, x2] = transparent_link_list_x[i:i+2]
            [y1, y2] = transparent_link_list_y[i:i+2]
            if x1 != x2:
                transparent_link_list_y[i] += offset
                transparent_link_list_y[i+1] += offset
            if y1 != y2:
                transparent_link_list_x[i] += offset
                transparent_link_list_x[i+1] += offset
        sample_links_dict[attr]["transparent"]["x"] = transparent_link_list_x
        sample_links_dict[attr]["transparent"]["y"] = transparent_link_list_y
        sample_links_dict[attr]["transparent"]["color"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][0]
        sample_links_dict[attr]["transparent"]["dash"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][1]

        offset += 0.01
        next_index_in_color_dash_list += 1

    return sample_links_dict


def get_sample_links_list(sample_data_dict, track, attr, links_across_y,
                          max_day_range, null_vals):
    attr_list = attr.split(";")
    link_list = []
    sample_list = list(sample_data_dict.keys())
    for i in range(len(sample_list)):
        sample = sample_list[i]
        sample_attr_list = [sample_data_dict[sample][v] for v in attr_list]

        if any(v in null_vals for v in sample_attr_list):
            continue

        for j in range(i+1, len(sample_list)):
            other_sample = sample_list[j]
            other_sample_attr_list = \
                [sample_data_dict[other_sample][v] for v in attr_list]

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

            if sample_attr_list == other_sample_attr_list:
                link_list.append((sample, other_sample))
    return link_list


def get_link_list_x(link_list, date_x_vals_dict, sample_data_dict, date_attr):
    link_list_x = []
    for (sample, other_sample) in link_list:
        date = sample_data_dict[sample][date_attr]
        other_date = sample_data_dict[other_sample][date_attr]
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


def get_main_fig_nodes_y_dict(sample_data_dict, date_attr, date_list, track,
                              track_list, track_y_vals_dict):
    date_track_zip_list = list(zip(date_list, track_list))
    helper_obj = \
        {k: [1/(v+1), 1] for k, v in Counter(date_track_zip_list).items()}

    main_fig_nodes_y_dict = {}
    for sample in sample_data_dict:
        sample_date = sample_data_dict[sample][date_attr]
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
