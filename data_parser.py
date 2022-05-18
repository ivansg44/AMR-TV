"""Parses sample file for data used in viz."""

from base64 import b64decode
from collections import Counter
import csv
from datetime import datetime
from io import StringIO
from json import loads
from math import sqrt


def get_app_data(sample_file_base64_str, config_file_base64_str,
                 selected_nodes=None, xaxis_range=None, yaxis_range=None):
    """Get data from uploaded file that is used to generate viz.

    :param sample_file_base64_str: Base64 encoded str corresponding to
        contents of user uploaded sample file.
    :type sample_file_base64_str: str
    :param config_file_base64_str: Base64 encoded str corresponding to
        contents of user uploaded config file.
    :type config_file_base64_str: str
    :param selected_nodes: Nodes selected by user
    :type selected_nodes: dict
    :param xaxis_range: Main graph x-axis min and max val
    :type xaxis_range: list
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Data derived from sample data, used to generate viz
    :rtype: dict
    """
    if selected_nodes is None:
        selected_nodes = {}

    sample_file_str = b64decode(sample_file_base64_str).decode("utf-8")

    config_file_str = b64decode(config_file_base64_str).decode("utf-8")
    config_file_dict = loads(config_file_str)

    sample_data_dict = get_sample_data_dict(sample_file_str,
                                            config_file_dict["delimiter"],
                                            config_file_dict["node_id"],
                                            config_file_dict["date_attr"],
                                            config_file_dict["date_format"],
                                            config_file_dict["null_vals"])
    enumerated_samples = enumerate(sample_data_dict)
    selected_samples = \
        {k for i, k in enumerated_samples if str(i) in selected_nodes}

    date_list =\
        [v[config_file_dict["date_attr"]] for v in sample_data_dict.values()]
    date_x_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted(date_list)))
    }
    main_fig_nodes_x_dict = \
        get_main_fig_nodes_x_dict(sample_data_dict,
                                  date_attr=config_file_dict["date_attr"],
                                  date_list=date_list,
                                  date_x_vals_dict=date_x_vals_dict)

    primary_y_list = \
        [v[config_file_dict["y_axes"][0]] for v in sample_data_dict.values()]
    track_list = \
        get_unsorted_track_list(sample_data_dict, config_file_dict["y_axes"])
    sorted_track_list = sorted(track_list, key=sorting_key)
    track_y_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted_track_list))
    }

    main_fig_nodes_y_dict = \
        get_main_fig_nodes_y_dict(sample_data_dict,
                                  date_attr=config_file_dict["date_attr"],
                                  date_list=date_list,
                                  y_axes=config_file_dict["y_axes"],
                                  track_list=track_list,
                                  track_y_vals_dict=track_y_vals_dict)

    node_symbol_attr = config_file_dict["node_symbol_attr"]
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

    node_range = range(len(sample_data_dict))
    if selected_nodes:
        main_fig_nodes_marker_opacity = \
            [1 if str(e) in selected_nodes else 0.5 for e in node_range]
    else:
        main_fig_nodes_marker_opacity = 1

    node_color_attr = config_file_dict["node_color_attr"]
    if node_color_attr:
        node_color_attr_list = \
            [v[node_color_attr] for v in sample_data_dict.values()]
        node_color_attr_dict = get_node_color_attr_dict(node_color_attr_list)
        main_fig_nodes_marker_color = \
            [node_color_attr_dict[v] for v in node_color_attr_list]
    else:
        node_color_attr_dict = {}
        main_fig_nodes_marker_color = "lightgrey"

    default_xaxis_range = [0.5, len(date_x_vals_dict) + 0.5]
    default_yaxis_range = [0.5, len(track_y_vals_dict) + 0.5]
    if not xaxis_range:
        xaxis_range = default_xaxis_range
    if not yaxis_range:
        yaxis_range = default_yaxis_range

    sample_links_dict = get_sample_links_dict(
        sample_data_dict=sample_data_dict,
        attr_link_list=config_file_dict["attr_link_list"],
        primary_y=config_file_dict["y_axes"][0],
        links_across_y=config_file_dict["links_across_y"],
        max_day_range=config_file_dict["max_day_range"],
        null_vals=config_file_dict["null_vals"]
    )

    attr_color_dash_dict = get_attr_color_dash_dict(sample_links_dict)

    main_fig_attr_links_dict = get_main_fig_attr_links_dict(
        sample_links_dict=sample_links_dict,
        main_fig_nodes_x_dict=main_fig_nodes_x_dict,
        main_fig_nodes_y_dict=main_fig_nodes_y_dict,
        selected_samples=selected_samples,
        yaxis_range=yaxis_range
    )

    main_fig_attr_link_tips_dict = \
        get_main_fig_attr_link_tips_dict(main_fig_attr_links_dict)

    label_attr = config_file_dict["label_attr"]
    main_fig_nodes_text = \
        ["<b>%s</b>" % v[label_attr] for v in sample_data_dict.values()]

    if selected_samples:
        ss = selected_samples
        main_fig_nodes_textfont_color = \
            ["black" if k in ss else "grey" for k in sample_data_dict]
    else:
        main_fig_nodes_textfont_color = "black"

    app_data = {
        "node_shape_legend_fig_nodes_y":
            list(range(len(node_symbol_attr_dict))),
        "node_shape_legend_fig_nodes_marker_symbol":
            list(node_symbol_attr_dict.values()),
        "node_shape_legend_fig_nodes_text":
            ["<b>%s</b>" % k for k in node_symbol_attr_dict.keys()],
        "main_fig_xaxis_range":
            xaxis_range,
        "main_fig_yaxis_range":
            yaxis_range,
        "main_fig_xaxis_tickvals":
            list(range(1, len(date_x_vals_dict) + 1)),
        "main_fig_xaxis_ticktext":
            list(date_x_vals_dict.keys()),
        "main_fig_yaxis_tickvals":
            list(range(1, len(track_y_vals_dict) + 1)),
        "main_fig_yaxis_ticktext":
            ["<br>".join(k) for k in track_y_vals_dict],
        "main_fig_nodes_x":
            [main_fig_nodes_x_dict[k] for k in sample_data_dict],
        "main_fig_nodes_y":
            [main_fig_nodes_y_dict[k] for k in sample_data_dict],
        "main_fig_nodes_marker_symbol":
            main_fig_nodes_marker_symbol,
        "main_fig_nodes_marker_color":
            main_fig_nodes_marker_color,
        "main_fig_nodes_marker_opacity":
            main_fig_nodes_marker_opacity,
        "main_fig_nodes_text":
            main_fig_nodes_text,
        "main_fig_nodes_textfont_color":
            main_fig_nodes_textfont_color,
        "node_color_attr_dict": node_color_attr_dict,
        "main_fig_attr_links_dict": main_fig_attr_links_dict,
        "attr_color_dash_dict": attr_color_dash_dict,
        "main_fig_attr_link_tips_dict": main_fig_attr_link_tips_dict,
        "main_fig_facet_x":
            get_main_fig_facet_x(default_xaxis_range, primary_y_list),
        "main_fig_facet_y": get_main_fig_facet_y(track_y_vals_dict)
    }

    return app_data


def get_unsorted_track_list(sample_data_dict, y_axes):
    """Get an unsorted list of tracks assigned across all nodes.

    If the y axes selected are "ham", "spam", and "eggs", the tracks
    are (sample_1_ham, sample_1_spam, sample_1_eggs),
    (sample_2_ham, sample_2_spam, sample_2_eggs), ...

    :param sample_data_dict: ``get_sample_data_dict`` ret val
    :type sample_data_dict: dict
    :param y_axes: List of attrs to use as hierarchical y axes
    :type y_axes: list[str]
    :return: Unsorted list of tracks assigned across all nodes
    :rtype: list[tuple[str]]
    """
    lists_to_zip = []
    vals = sample_data_dict.values()
    for axis in y_axes:
        lists_to_zip.append([val[axis] for val in vals])
    ret = list(zip(*lists_to_zip))
    return ret


def sorting_key(track):
    """Call ``str`` or ``int`` on each val in track.

    This fn allows us to sort tracks in the main graph by the str and
    int vals of their attr vals.

    :param track: List of attr vals found in a track
    :type track: tuple[str]
    :return: List of attrs after calling str or int on them
    :rtype: list[str]
    """
    ret = []
    for attr_val in track:
        if attr_val is "n/a":
            continue
        try:
            ret.append(int(attr_val))
        except ValueError:
            ret.append(str(attr_val))
    return ret


def get_sample_data_dict(sample_file_str, delimiter, node_id, date,
                         date_format, null_vals):
    """Parse sample data file into dict obj.

    :param sample_file_str: Str corresponding to contents of user
        uploaded sample file.
    :type sample_file_str: str
    :param delimiter: Delimiter in sample file
    :type delimiter: str
    :param node_id: Sample file attr encoded by presence of different
        nodes.
    :type node_id: str
    :param date: Sample file attr encoded by sample date/x-axis
    :type date: str
    :param date_format: 1989 C format code used when parsing date attr
    :type date_format: str
    :param null_vals: Vals to treat as null in sample data
    :type null_vals: list[str]
    :return: Sample file data parsed into dict obj
    :rtype: dict
    """
    sample_data_dict = {}
    reader = csv.DictReader(StringIO(sample_file_str),
                            delimiter=delimiter)
    for row in reader:
        sample_id = row[node_id]
        if sample_id in null_vals:
            continue
        row = {k: ("n/a" if row[k] in null_vals else row[k]) for k in row}

        row["datetime_obj"] = datetime.strptime(row[date], date_format)
        row[date] = row["datetime_obj"].strftime("%Y-%m-%d")

        sample_data_dict[sample_id] = row
    return sample_data_dict


def get_node_symbol_attr_dict(node_symbol_attr_list):
    """Get a dict mapping node symbol attr vals to symbols.

    :param node_symbol_attr_list: List of node symbol attr vals across
        all nodes.
    :type node_symbol_attr_list: list[str]
    :return: dict with unique node symbol attr vals as keys, and actual
        symbols as vals.
    :rtype: dict
    """
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
    """Get a dict mapping node color attr vals to symbols.

    :param node_color_attr_list: List of node color attr vals across
        all nodes.
    :type node_color_attr_list: list[str]
    :return: dict with unique node color attr vals as keys, and actual
        colors as vals.
    :rtype: dict
    """
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


def get_sample_links_dict(sample_data_dict, attr_link_list, primary_y,
                          links_across_y, max_day_range, null_vals):
    """Get a dict of all links to viz in main graph.

    The keys in the dict are different attrs. The values are a list of
    tuples containing two samples with a shared val for that attr.

    :param sample_data_dict: ``get_sample_data_dict`` ret val
    :type sample_data_dict: dict
    :param attr_link_list: list of attrs to include in ret dict
    :type attr_link_list: list[str]
    :param primary_y: attr encoded as one part of a track along y-axis
    :type primary_y: str
    :param links_across_y: Whether we consider links across different
        tracks.
    :type links_across_y: bool
    :param max_day_range: Maximum day range to still consider links
    :type max_day_range: int
    :param null_vals: List of null vals in sample data
    :type null_vals: list
    :return: Dict detailing links to viz in main graph
    :rtype: dict
    """
    sample_links_dict = {k: [] for k in attr_link_list}
    sample_list = list(sample_data_dict.keys())

    for attr in attr_link_list:
        attr_list = attr.split(";")

        for i in range(len(sample_list)):
            sample = sample_list[i]

            sample_attr_list = \
                [sample_data_dict[sample][v] for v in attr_list]
            if any(v in null_vals for v in sample_attr_list):
                continue

            for j in range(i+1, len(sample_list)):
                other_sample = sample_list[j]

                sample_primary_y = sample_data_dict[sample][primary_y]
                sample_datetime = sample_data_dict[sample]["datetime_obj"]
                other_primary_y = sample_data_dict[other_sample][primary_y]
                other_datetime = sample_data_dict[other_sample]["datetime_obj"]

                if not links_across_y and sample_primary_y != other_primary_y:
                    continue

                day_range_datetime = other_datetime - sample_datetime
                day_range = abs(day_range_datetime.days)
                if max_day_range < day_range:
                    continue

                other_sample_attr_list = \
                    [sample_data_dict[other_sample][v] for v in attr_list]

                if sample_attr_list == other_sample_attr_list:
                    if other_datetime > sample_datetime:
                        sample_links_dict[attr].append((sample, other_sample))
                    else:
                        sample_links_dict[attr].append((other_sample, sample))

    return sample_links_dict


def get_attr_color_dash_dict(sample_links_dict):
    """Get dict assigning color/dash combo to attrs vized as links.

    :param sample_links_dict: ``get_sample_links_dict`` ret val
    :type sample_links_dict: dict
    :return: Dict with attrs vized as links as keys,
        and a unique color/dash combo as vals.
    :rtype: dict
    """
    available_link_color_dash_combos = [
        ((27, 158, 119), "solid"), ((217, 95, 2), "solid"),
        ((117, 112, 179), "solid"), ((27, 158, 119), "dot"),
        ((217, 95, 2), "dot"), ((117, 112, 179), "dot"),
    ]
    if len(sample_links_dict) > len(available_link_color_dash_combos):
        msg = "Not enough unique edge patterns for different attributes"
        raise IndexError(msg)
    zip_obj = zip(sample_links_dict.keys(), available_link_color_dash_combos)
    ret = {k: v for (k, v) in zip_obj}
    return ret


def get_main_fig_attr_links_dict(sample_links_dict, main_fig_nodes_x_dict,
                                 main_fig_nodes_y_dict, selected_samples,
                                 yaxis_range):
    """Get dict with info used by Plotly to viz links in main graph.

    :param sample_links_dict: ``get_sample_links_dict`` ret val
    :type sample_links_dict: dict
    :param main_fig_nodes_x_dict: ``get_main_fig_nodes_x_dict`` ret val
    :type main_fig_nodes_x_dict: dict
    :param main_fig_nodes_y_dict: ``get_main_fig_nodes_y_dict`` ret val
    :type main_fig_nodes_y_dict: dict
    :param selected_samples: Samples selected by users
    :type selected_samples: set[str]
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Dict with info used by Plotly to viz links in main graph
    :rtype: dict
    """
    ret = {}
    translation_dict = {}
    unit_parallel_translation = (yaxis_range[1] - yaxis_range[0]) / 200
    for attr in sample_links_dict:
        ret[attr] = {
            "opaque": {"x": [], "y": []},
            "transparent": {"x": [], "y": []}
        }

        for (sample, other_sample) in sample_links_dict[attr]:
            if (sample, other_sample) in translation_dict:
                old_multiplier = translation_dict[(sample, other_sample)]
                if old_multiplier == 0:
                    translation_dict[(sample, other_sample)] = 1
                elif old_multiplier > 0:
                    translation_dict[(sample, other_sample)] *= -1
                else:
                    translation_dict[(sample, other_sample)] *= -1
                    translation_dict[(sample, other_sample)] += 1
                multiplier = translation_dict[(sample, other_sample)]
            else:
                multiplier = 0
                translation_dict[(sample, other_sample)] = multiplier

            parallel_translation = multiplier * unit_parallel_translation

            x0 = main_fig_nodes_x_dict[sample]
            y0 = main_fig_nodes_y_dict[sample]
            x1 = main_fig_nodes_x_dict[other_sample]
            y1 = main_fig_nodes_y_dict[other_sample]

            if (x1 - x0) == 0:
                x0 += parallel_translation
                x1 += parallel_translation
            elif (y1 - y0) == 0:
                y0 += parallel_translation
                y1 += parallel_translation
            else:
                inverse_perpendicular_slope = (x1 - x0) / (y1 - y0)
                numerator = parallel_translation**2
                denominator = 1 + inverse_perpendicular_slope**2
                x_translation = sqrt(numerator/denominator)
                if parallel_translation < 0:
                    x_translation *= -1
                x0 += x_translation
                x1 += x_translation
                y0 += -inverse_perpendicular_slope * x_translation
                y1 += -inverse_perpendicular_slope * x_translation

            selected_link = \
                sample in selected_samples or other_sample in selected_samples
            if selected_samples and not selected_link:
                ret[attr]["transparent"]["x"] += [x0, x1, None]
                ret[attr]["transparent"]["y"] += [y0, y1, None]
            else:
                ret[attr]["opaque"]["x"] += [x0, x1, None]
                ret[attr]["opaque"]["y"] += [y0, y1, None]

    return ret


def get_main_fig_attr_link_tips_dict(main_fig_attr_links_dict):
    """Get dict used to draw black tips on links in main viz.

    :param main_fig_attr_links_dict: ``get_main_fig_attr_links_dict``
        ret val.
    :type main_fig_attr_links_dict: dict
    :return: Dict with info used by plotly to draw black tips on main
        viz.
    :rtype: dict
    """
    ret = {
        "opaque": {
            "x": [],
            "y": []
        },
        "transparent": {
            "x": [],
            "y": []
        },
    }
    shortest_link = 100000
    for attr in main_fig_attr_links_dict:
        opaque_dict = main_fig_attr_links_dict[attr]["opaque"]
        for i in range(0, len(opaque_dict["x"]), 3):
            [x0, x1] = opaque_dict["x"][i:i+2]
            [y0, y1] = opaque_dict["y"][i:i+2]
            shortest_link = min(shortest_link,
                                sqrt((x1 - x0)**2 + (y1 - y0)**2))
    dt = shortest_link * 0.25

    for attr in main_fig_attr_links_dict:
        opaque_dict = main_fig_attr_links_dict[attr]["opaque"]
        for i in range(0, len(opaque_dict["x"]), 3):
            [x0, x1] = opaque_dict["x"][i:i+2]
            [y0, y1] = opaque_dict["y"][i:i+2]

            # https://math.stackexchange.com/a/1630886
            d = sqrt((x1 - x0)**2 + (y1 - y0)**2)
            t = dt / d
            xt0 = (1 - t)*x0 + t*x1
            yt0 = (1 - t)*y0 + t*y1
            xt1 = (1 - t)*x1 + t*x0
            yt1 = (1 - t)*y1 + t*y0
            ret["opaque"]["x"] += \
                [x0, xt0, None, xt1, x1, None]
            ret["opaque"]["y"] += \
                [y0, yt0, None, yt1, y1, None]

        transparent_dict = main_fig_attr_links_dict[attr]["transparent"]
        for i in range(0, len(transparent_dict["x"]), 3):
            [x1, x2] = transparent_dict["x"][i:i+2]
            [y1, y2] = transparent_dict["y"][i:i+2]
            x_diff = x2 - x1
            y_diff = y2 - y1
            ret["transparent"]["x"] += \
                [x1, x1+(x_diff*0.1), None, x2-(x_diff*0.1), x2, None]
            ret["transparent"]["y"] += \
                [y1, y1+(y_diff*0.1), None, y2-(y_diff*0.1), y2, None]
    return ret


def get_main_fig_nodes_x_dict(sample_data_dict, date_attr, date_list,
                              date_x_vals_dict):
    """Get dict mapping nodes to x vals.

    :param sample_data_dict: Sample file data parsed into dict obj
    :rtype: dict
    :param date_attr: Sample file attr encoded by sample date/x-axis
    :type date_attr: str
    :param date_list: List of sample dates wrt all nodes
    :type date_list: list
    :param date_x_vals_dict: Dict mapping dates to numerical x vals
    :type date_x_vals_dict: dict
    :return: Dict mapping nodes to x vals
    :rtype: dict
    """
    date_counts_dict = Counter(date_list)
    helper_obj = {}
    for date in date_counts_dict:
        count = date_counts_dict[date]
        if count == 1:
            helper_obj[date] = [1/8, 1]
        else:
            helper_obj[date] = [1/(4 * (count - 1)), 0]

    main_fig_nodes_x_dict = {}
    for sample in sample_data_dict:
        sample_date = sample_data_dict[sample][date_attr]
        [stagger, multiplier] = helper_obj[sample_date]

        unstaggered_x = date_x_vals_dict[sample_date]
        lowest_x = unstaggered_x - (1/8)
        staggered_x = lowest_x + (stagger * multiplier)

        main_fig_nodes_x_dict[sample] = staggered_x
        helper_obj[sample_date][1] += 1

    return main_fig_nodes_x_dict


def get_main_fig_nodes_y_dict(sample_data_dict, date_attr, date_list,
                              y_axes, track_list, track_y_vals_dict):
    """Get dict mapping nodes to y vals.

    :param sample_data_dict: Sample file data parsed into dict obj
    :rtype: dict
    :param date_attr: Sample file attr encoded by sample date/x-axis
    :type date_attr: str
    :param date_list: List of sample dates wrt all nodes
    :type date_list: list
    :param y_axes: List of attrs to use as hierarchical y axes
    :type y_axes: list[str]
    :param track_list: List of track vals wrt all nodes
    :type track_list: list
    :param track_y_vals_dict: Dict mapping tracks to numerical y vals
    :type track_y_vals_dict: dict
    :return: Dict mapping nodes to y vals
    :rtype: dict
    """
    date_track_zip_list = list(zip(date_list, track_list))
    helper_obj = \
        {k: [1/(v+1), 1] for k, v in Counter(date_track_zip_list).items()}

    main_fig_nodes_y_dict = {}
    for sample in sample_data_dict:
        sample_date = sample_data_dict[sample][date_attr]
        sample_track = \
            tuple((sample_data_dict[sample][axis] for axis in y_axes))
        [stagger, multiplier] = helper_obj[(sample_date, sample_track)]

        unstaggered_y = track_y_vals_dict[sample_track]
        lowest_y = unstaggered_y - 0.5
        staggered_y = lowest_y + (stagger * multiplier)

        main_fig_nodes_y_dict[sample] = staggered_y
        helper_obj[(sample_date, sample_track)][1] += 1

    return main_fig_nodes_y_dict


def get_main_fig_facet_x(default_xaxis_range, primary_y_list):
    """Get x vals for lines used to split main graph by primary y.

    :param default_xaxis_range: Main graph x-axis min and max val,
        without any zooming or panning.
    :type default_xaxis_range: list
    :param primary_y_list: List of primary y vals for samples
    :type primary_y_list: list
    :return: List of x vals Plotly needs to draw lines splitting main
        graph by tracks.
    :rtype: list
    """
    main_fig_facet_x = []
    num_of_facets = len(set(primary_y_list)) - 1
    [xmin, xmax] = default_xaxis_range
    for i in range(0, num_of_facets):
        main_fig_facet_x += [xmin, xmax, None]
    return main_fig_facet_x


def get_main_fig_facet_y(track_y_vals_dict):
    """Get y vals for lines used to split main graph by primary y.

    :param track_y_vals_dict: Dict mapping tracks to numerical y vals
    :type track_y_vals_dict: dict
    :return: List of y vals Plotly needs to draw lines splitting main
        graph by tracks.
    :rtype: list
    """
    main_fig_facet_y = []
    last_primary_y = ""
    for i, ticktext in enumerate(track_y_vals_dict):
        if i == 0:
            last_primary_y = ticktext[0]
            continue
        if ticktext[0] != last_primary_y:
            main_fig_facet_y += [i+0.5, i+0.5, None]
            last_primary_y = ticktext[0]
    return main_fig_facet_y
