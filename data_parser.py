"""Parses sample file for data used in viz."""

from base64 import b64decode
from collections import Counter
import csv
from datetime import datetime
from io import StringIO
from json import loads


def get_app_data(sample_file_base64_str, config_file_base64_str,
                 selected_nodes=None, xaxis_range=None, yaxis_range=None):
    """Get data from sample file that is used to generate viz. TODO

    :param sample_file_base64_str: Path to sample file TODO
    :type sample_file_base64_str: str
    :param config_file_base64_str: TODO
    :type config_file_base64_str: TODO
    :param delimiter: Delimiter in sample file
    :type delimiter: str
    :param node_id: Sample file attr encoded by presence of different
        nodes.
    :type node_id: str
    :param track: Sample file attr encoded by y-axis
    :type track: str
    :param date_attr: Sample file attr encoded by sample date/x-axis
    :type date_attr: str
    :param date_format: 1989 C format code used when parsing date attr
    :type date_format: str
    :param label_attr: Sample file attr encoded by node labels
    :type label_attr: str
    :param attr_link_list: Sample file attrs encoded by different link
        types.
    :type attr_link_list: list[str]
    :param links_across_y: Whether to viz links across tracks
    :type links_across_y: bool
    :param max_day_range: Max number of days allowed b/w sample dates
        for two nodes when drawing links.
    :type max_day_range: int
    :param null_vals: Vals to treat as null in sample data
    :type null_vals: list[str]
    :param node_symbol_attr: Sample date attr encoded by node symbol
    :type node_symbol_attr: str
    :param node_color_attr: Sample date attr encoded by node color
    :type node_color_attr: str
    :param y_key: Python-specific key used to sort vals along y-axis
    :type y_key: str
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
        {k: None for i, k in enumerated_samples if str(i) in selected_nodes}

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

    track_list = \
        [v[config_file_dict["track"]] for v in sample_data_dict.values()]
    sorted_track_list = \
        get_sorted_track_list(track_list, y_key=config_file_dict["y_key"])
    track_y_vals_dict = {
        e: i+1 for i, e in enumerate(dict.fromkeys(sorted_track_list))
    }

    main_fig_nodes_y_dict = \
        get_main_fig_nodes_y_dict(sample_data_dict,
                                  date_attr=config_file_dict["date_attr"],
                                  date_list=date_list,
                                  track=config_file_dict["track"],
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

    if not xaxis_range:
        xaxis_range = [0.5, len(date_x_vals_dict) + 0.5]
    if not yaxis_range:
        yaxis_range = [0.5, len(track_y_vals_dict) + 0.5]
    sample_links_dict = get_sample_links_dict(
        attr_link_list=config_file_dict["attr_link_list"],
        sample_data_dict=sample_data_dict,
        track=config_file_dict["track"],
        links_across_y=config_file_dict["links_across_y"],
        max_day_range=config_file_dict["max_day_range"],
        main_fig_nodes_x_dict=main_fig_nodes_x_dict,
        main_fig_nodes_y_dict=main_fig_nodes_y_dict,
        null_vals=config_file_dict["null_vals"],
        selected_samples=selected_samples,
        xaxis_range=xaxis_range,
        yaxis_range=yaxis_range
    )

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
            list(track_y_vals_dict.keys()),
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
    """Get a sorted list of tracks assigned across all nodes.

    :param track_list: List of tracks assigned across all nodes
    :type track_list: list[str]
    :param y_key: Python-specific key used to sort tracks
    :type y_key: str
    :return: Sorted list of tracks assigned across all nodes
    :rtype: list[str]
    """
    if y_key == "int":
        y_key = int
    elif y_key == "str":
        y_key = str
    else:
        msg = 'Currently only accept "int" or "str" as y_key values'
        raise ValueError(msg)

    return sorted(track_list, key=y_key)


def get_sample_data_dict(sample_file_str, delimiter, node_id, date,
                         date_format, null_vals):
    """Parse sample data file into dict obj.

    :param sample_file_str: Path to sample file TODO
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


def get_sample_links_dict(attr_link_list, sample_data_dict, track,
                          links_across_y, max_day_range, main_fig_nodes_x_dict,
                          main_fig_nodes_y_dict, null_vals, selected_samples,
                          xaxis_range, yaxis_range):
    """Get nested dict containing info on links b/w samples.

    This includes whether the links are opaque or transparent.

    :param attr_link_list: Sample file attrs encoded by different link
        types.
    :type attr_link_list: list[str]
    :param sample_data_dict: Sample file data parsed into dict obj
    :rtype: dict
    :param track: Sample file attr encoded by y-axis
    :type track: str
    :param links_across_y: Whether to viz links across tracks
    :type links_across_y: bool
    :param max_day_range: Max number of days allowed b/w sample dates
        for two nodes when drawing links.
    :type max_day_range: int
    :param main_fig_nodes_x_dict: Dict mapping nodes to x vals
    :type main_fig_nodes_x_dict: dict
    :param main_fig_nodes_y_dict: Dict mapping nodes to y vals
    :type main_fig_nodes_y_dict: dict
    :param null_vals: Vals to treat as null in sample data
    :type null_vals: list[str]
    :param selected_samples: User-selected samples
    :type selected_samples: dict
    :param xaxis_range: Main graph x-axis min and max val
    :type xaxis_range: list
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Nested dict containing info on links b/w samples
    :rtype: dict
    """
    available_link_color_dash_combos = [
        ((27, 158, 119), "solid"), ((217, 95, 2), "solid"),
        ((117, 112, 179), "solid"), ((27, 158, 119), "dot"),
        ((217, 95, 2), "dot"), ((117, 112, 179), "dot"),
    ]
    next_index_in_color_dash_list = 0
    if len(attr_link_list) > len(available_link_color_dash_combos):
        msg = "Not enough unique edge patterns for different attributes"
        raise IndexError(msg)

    x_offset_interval = (xaxis_range[1] - xaxis_range[0]) / 300
    x_offset = 0 - (len(attr_link_list) * (x_offset_interval / 2))
    y_offset_interval = (yaxis_range[1] - yaxis_range[0]) / 300
    y_offset = 0 - (len(attr_link_list) * (y_offset_interval / 2))

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
                            main_fig_nodes_x_dict=main_fig_nodes_x_dict)
        opaque_link_list_y = \
            get_link_list_y(link_list=opaque_sample_links_list,
                            main_fig_nodes_y_dict=main_fig_nodes_y_dict)
        for i in range(0, len(opaque_link_list_y), 3):
            [y1, y2] = opaque_link_list_y[i:i+2]
            if y1 == y2:
                opaque_link_list_y[i] += y_offset
                opaque_link_list_y[i+1] += y_offset
            if y1 != y2:
                opaque_link_list_x[i] += x_offset
                opaque_link_list_x[i+1] += x_offset
        sample_links_dict[attr]["opaque"]["x"] = opaque_link_list_x
        sample_links_dict[attr]["opaque"]["y"] = opaque_link_list_y
        sample_links_dict[attr]["opaque"]["color"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][0]
        sample_links_dict[attr]["opaque"]["dash"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][1]

        transparent_link_list_x = \
            get_link_list_x(link_list=transparent_sample_links_list,
                            main_fig_nodes_x_dict=main_fig_nodes_x_dict)
        transparent_link_list_y = \
            get_link_list_y(link_list=transparent_sample_links_list,
                            main_fig_nodes_y_dict=main_fig_nodes_y_dict)
        for i in range(0, len(transparent_link_list_y), 3):
            [y1, y2] = transparent_link_list_y[i:i+2]
            if y1 == y2:
                transparent_link_list_y[i] += y_offset
                transparent_link_list_y[i+1] += y_offset
            if y1 != y2:
                transparent_link_list_x[i] += x_offset
                transparent_link_list_x[i+1] += x_offset
        sample_links_dict[attr]["transparent"]["x"] = transparent_link_list_x
        sample_links_dict[attr]["transparent"]["y"] = transparent_link_list_y
        sample_links_dict[attr]["transparent"]["color"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][0]
        sample_links_dict[attr]["transparent"]["dash"] = \
            available_link_color_dash_combos[next_index_in_color_dash_list][1]

        x_offset += x_offset_interval
        y_offset += y_offset_interval
        next_index_in_color_dash_list += 1

    return sample_links_dict


def get_sample_links_list(sample_data_dict, track, attr, links_across_y,
                          max_day_range, null_vals):
    """Get a list of all links for a particular attr b/w samples.

    This is a barebone list of tuples.

    :param sample_data_dict: Sample file data parsed into dict obj
    :rtype: dict
    :param track: Sample file attr encoded by y-axis
    :type track: str
    :param attr: Specific attr we are parsing links for
    :type attr: str
    :param links_across_y: Whether to viz links across tracks
    :type links_across_y: bool
    :param max_day_range: Max number of days allowed b/w sample dates
        for two nodes when drawing links.
    :type max_day_range: int
    :param null_vals: Vals to treat as null in sample data
    :type null_vals: list[str]
    :return: List of links b/w all samples for a particular attr
    :rtype: list[tuple]
    """
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


def get_link_list_x(link_list, main_fig_nodes_x_dict):
    """Get x values for a list of sample links.

    Basically, for Plotly to do what we want, we need a list that looks
    like this: [x1, x2, None, x3, x4, None, ...]

    Where (x1, x2) and (x3, x4) are separate links.

    :param link_list: See ``get_sample_links_list`` ret val
    :type link_list: list[tuple]
    :param main_fig_nodes_x_dict: Dict mapping nodes to x vals
    :type main_fig_nodes_x_dict: dict
    :return: List of x vals Plotly needs to draw links for a single
        attr.
    :rtype: list
    """
    link_list_x = []
    for (sample, other_sample) in link_list:
        main_fig_node_x = main_fig_nodes_x_dict[sample]
        other_main_fig_node_x = main_fig_nodes_x_dict[other_sample]
        link_list_x += [main_fig_node_x, other_main_fig_node_x, None]
    return link_list_x


def get_link_list_y(link_list, main_fig_nodes_y_dict):
    """Get y values for a list of sample links.

    Basically, for Plotly to do what we want, we need a list that looks
    like this: [y1, y2, None, y3, y4, None, ...]

    Where (y1, y2) and (y3, y4) are separate links.

    :param link_list: See ``get_sample_links_list`` ret val
    :type link_list: list[tuple]
    :param main_fig_nodes_y_dict: Dict mapping nodes to y vals
    :type main_fig_nodes_y_dict: dict
    :return: List of y vals Plotly needs to draw links for a single
        attr.
    :rtype: list
    """
    link_list_y = []
    for (sample, other_sample) in link_list:
        main_fig_node_y = main_fig_nodes_y_dict[sample]
        other_main_fig_node_y = main_fig_nodes_y_dict[other_sample]
        link_list_y += [main_fig_node_y, other_main_fig_node_y, None]
    return link_list_y


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


def get_main_fig_nodes_y_dict(sample_data_dict, date_attr, date_list, track,
                              track_list, track_y_vals_dict):
    """Get dict mapping nodes to y vals.

    :param sample_data_dict: Sample file data parsed into dict obj
    :rtype: dict
    :param date_attr: Sample file attr encoded by sample date/x-axis
    :type date_attr: str
    :param date_list: List of sample dates wrt all nodes
    :type date_list: list
    :param track: Sample file attr encoded by y-axis
    :type track: str
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
        sample_track = sample_data_dict[sample][track]
        [stagger, multiplier] = helper_obj[(sample_date, sample_track)]

        unstaggered_y = track_y_vals_dict[sample_track]
        lowest_y = unstaggered_y - 0.5
        staggered_y = lowest_y + (stagger * multiplier)

        main_fig_nodes_y_dict[sample] = staggered_y
        helper_obj[(sample_date, sample_track)][1] += 1

    return main_fig_nodes_y_dict


def get_main_fig_facet_x(main_fig_xaxis_range, num_of_facets):
    """Get x vals for lines used to split main graph by tracks.

    :param main_fig_xaxis_range: Main graph x-axis min and max val
    :type main_fig_xaxis_range: list
    :param num_of_facets: Number of lines to draw (number of tracks-1)
    :type num_of_facets: int
    :return: List of x vals Plotly needs to draw lines splitting main
        graph by tracks.
    :rtype: list
    """
    main_fig_facet_x = []
    [xmin, xmax] = main_fig_xaxis_range
    for i in range(0, num_of_facets):
        main_fig_facet_x += [xmin, xmax, None]
    return main_fig_facet_x


def get_main_fig_facet_y(num_of_facets):
    """Get y vals for lines used to split main graph by tracks.

    :param num_of_facets: Number of lines to draw (number of tracks-1)
    :type num_of_facets: int
    :return: List of y vals Plotly needs to draw lines splitting main
        graph by tracks.
    :rtype: list
    """
    main_fig_facet_y = []
    for i in range(0, num_of_facets):
        main_fig_facet_y += [i+1.5, i+1.5, None]
    return main_fig_facet_y
