"""Parses sample file for data used in viz."""

from base64 import b64decode
from collections import Counter
import csv
from datetime import datetime
from io import StringIO
from json import loads
from math import sqrt
from re import compile

from expression_evaluator import eval_expr


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
                                            config_file_dict["date_input"],
                                            config_file_dict["date_output"],
                                            config_file_dict["null_vals"])
    enumerated_samples = enumerate(sample_data_dict)
    selected_samples = \
        {k for i, k in enumerated_samples if str(i) in selected_nodes}

    date_list =\
        [v[config_file_dict["date_attr"]] for v in sample_data_dict.values()]
    datetime_list =\
        [v["datetime_obj"] for v in sample_data_dict.values()]
    date_x_vals_dict = get_date_x_vals_dict(date_list=date_list,
                                            datetime_list=datetime_list)
    main_fig_nodes_x_dict = \
        get_main_fig_nodes_x_dict(sample_data_dict,
                                  date_attr=config_file_dict["date_attr"],
                                  date_list=date_list,
                                  date_x_vals_dict=date_x_vals_dict)

    track_list = \
        get_unsorted_track_list(sample_data_dict, config_file_dict["y_axes"])
    track_date_node_count_dict = Counter(zip(track_list, date_list))
    max_node_count_at_track_dict = \
        get_max_node_count_at_track_dict(track_date_node_count_dict)
    track_y_vals_dict = get_track_y_vals_dict(max_node_count_at_track_dict)
    main_fig_nodes_y_dict = get_main_fig_nodes_y_dict(
        sample_data_dict,
        date_attr=config_file_dict["date_attr"],
        track_date_node_count_dict=track_date_node_count_dict,
        max_node_count_at_track_dict=max_node_count_at_track_dict,
        y_axes=config_file_dict["y_axes"],
        track_y_vals_dict=track_y_vals_dict
    )

    num_of_primary_facets = \
        len({k[0] for k in max_node_count_at_track_dict}) - 1
    num_of_secondary_facets = len(max_node_count_at_track_dict.keys()) - 1

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
    default_yaxis_range = [0.5, sum(max_node_count_at_track_dict.values())+0.5]
    if not xaxis_range:
        xaxis_range = default_xaxis_range
    if not yaxis_range:
        yaxis_range = default_yaxis_range

    main_fig_height = get_main_fig_height(max_node_count_at_track_dict)
    main_fig_width = len(date_x_vals_dict) * 144

    link_parallel_translation = \
        get_link_parallel_translation(default_yaxis_range, yaxis_range)

    sample_links_dict = get_sample_links_dict(
        sample_data_dict=sample_data_dict,
        attr_link_list=config_file_dict["attr_link_list"],
        primary_y=config_file_dict["y_axes"][0],
        links_across_primary_y=config_file_dict["links_across_primary_y"],
        max_day_range=config_file_dict["max_day_range"],
        null_vals=config_file_dict["null_vals"],
        weights=config_file_dict["weights"],
        weight_filters=config_file_dict["weight_filters"],
        attr_val_filters=config_file_dict["attr_val_filters"]
    )

    attr_color_dash_dict = get_attr_color_dash_dict(sample_links_dict)

    main_fig_attr_links_dict = get_main_fig_attr_links_dict(
        sample_links_dict=sample_links_dict,
        main_fig_nodes_x_dict=main_fig_nodes_x_dict,
        main_fig_nodes_y_dict=main_fig_nodes_y_dict,
        selected_samples=selected_samples,
        main_fig_height=main_fig_height,
        main_fig_width=main_fig_width,
        link_parallel_translation=link_parallel_translation
    )

    main_fig_attr_link_labels_dict = get_main_fig_attr_link_labels_dict(
        sample_links_dict=sample_links_dict,
        main_fig_nodes_x_dict=main_fig_nodes_x_dict,
        main_fig_nodes_y_dict=main_fig_nodes_y_dict,
        selected_samples=selected_samples,
        main_fig_height=main_fig_height,
        main_fig_width=main_fig_width,
        link_parallel_translation=link_parallel_translation,
        weights=config_file_dict["weights"]
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

    main_fig_yaxis_ticktext = \
        ["<br>".join(["null" if e is None else e for e in k])
         for k in track_y_vals_dict]

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
            list(track_y_vals_dict.values()),
        "main_fig_yaxis_ticktext":
            main_fig_yaxis_ticktext,
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
        "main_fig_attr_link_labels_dict": main_fig_attr_link_labels_dict,
        "attr_color_dash_dict": attr_color_dash_dict,
        "main_fig_attr_link_tips_dict": main_fig_attr_link_tips_dict,
        "main_fig_primary_facet_x":
            get_main_fig_primary_facet_x(default_xaxis_range,
                                         num_of_primary_facets),
        "main_fig_primary_facet_y":
            get_main_fig_primary_facet_y(max_node_count_at_track_dict),
        "main_fig_secondary_facet_x":
            get_main_fig_secondary_facet_x(default_xaxis_range,
                                           num_of_secondary_facets),
        "main_fig_secondary_facet_y":
            get_main_fig_secondary_facet_y(max_node_count_at_track_dict),
        "main_fig_height": main_fig_height,
        "main_fig_width": main_fig_width
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
    """Convert each val in a track to a tuple.

    The necessity of this is due to columns potentially having both int
    and str vals. Inspiration from:
    https://stackoverflow.com/a/34757358/11472358

    We sort as follows:

    * None comes first
    * Sort ints next
    * Sort strs last

    :param track: List of attr vals found in a track
    :type track: tuple[int|str]
    :return: List of tuples mapped to each attr val in track
    :rtype: list[tuple]
    """
    ret = []
    for attr_val in track:
        try:
            ret.append((
                attr_val is None,
                0,
                int(attr_val)
             ))
        except (TypeError, ValueError):
            ret.append((
                attr_val is None,
                1,
                attr_val
             ))
    return ret


def get_sample_data_dict(sample_file_str, delimiter, node_id, date,
                         date_input, date_output, null_vals):
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
    :param date_input: 1989 C format code used when parsing date attr
        from sample data.
    :type date_input: str
    :param date_output: 1989 C format code sample data dates are
        converted to (useful for binning dates if needed).
    :type date_input: str
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
        if row[date] in null_vals:
            continue
        row = {k: (None if row[k] in null_vals else row[k]) for k in row}

        row["datetime_obj"] = datetime.strptime(row[date], date_input)
        row[date] = row["datetime_obj"].strftime(date_output)

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
                          links_across_primary_y, max_day_range, null_vals,
                          weights, weight_filters, attr_val_filters):
    """Get a dict of all links to viz in main graph.

    The keys in the dict are different attrs. The values are a nested
    dict. The keys in the nested dict are tuples containing two samples
    with a shared val for the attr key in the outer dict. The values in
    the nested dict are weights assigned to that link.

    We filter out certain links using ``weight_filters`` and
    ``attr_val_filters``.

    :param sample_data_dict: ``get_sample_data_dict`` ret val
    :type sample_data_dict: dict
    :param attr_link_list: list of attrs to include in ret dict
    :type attr_link_list: list[str]
    :param primary_y: attr encoded as one part of a track along y-axis
    :type primary_y: str
    :param links_across_primary_y: Whether we consider links across
        different primary y vals.
    :type links_across_primary_y: bool
    :param max_day_range: Maximum day range to still consider links
    :type max_day_range: int
    :param null_vals: List of null vals in sample data
    :type null_vals: list
    :param weights: Dictionary of expressions used to assign weights to
        specific attr links
    :type weights: dict
    :param attr_val_filters: Dictionary of vals to ignore for certain
        attrs, when generating links.
    :type attr_val_filters: dict
    :return: Dict detailing links to viz in main graph
    :rtype: dict
    """
    sample_links_dict = {k: {} for k in attr_link_list}
    sample_list = list(sample_data_dict.keys())
    regex_obj = compile("!.*?!|@.*?@")

    for attr in attr_link_list:
        attr_list = []
        disjoint_match_list = []
        for attr_list_val in attr.split(";"):
            if attr_list_val[0] == "~":
                disjoint_match_list.append(True)
                attr_list.append(attr_list_val[1:])
            else:
                disjoint_match_list.append(False)
                attr_list.append(attr_list_val)

        for i in range(len(sample_list)):
            sample = sample_list[i]

            sample_attr_list = \
                [sample_data_dict[sample][v] for v in attr_list]
            if any(v in null_vals for v in sample_attr_list):
                continue
            # Bit of a complex comprehension. Basically, we remove any
            # values in sample_attr_list that are belong to a val
            # specified for the attr in attr_val_filters.
            sample_attr_list = \
                [y for x, y in zip(attr_list, sample_attr_list)
                 if
                 x not in attr_val_filters or y not in attr_val_filters[x]]
            if not sample_attr_list:
                continue

            for j in range(i+1, len(sample_list)):
                other_sample = sample_list[j]

                sample_primary_y = sample_data_dict[sample][primary_y]
                sample_datetime = sample_data_dict[sample]["datetime_obj"]
                other_primary_y = sample_data_dict[other_sample][primary_y]
                other_datetime = sample_data_dict[other_sample]["datetime_obj"]

                if not links_across_primary_y:
                    if sample_primary_y != other_primary_y:
                        continue

                day_range_datetime = other_datetime - sample_datetime
                day_range = abs(day_range_datetime.days)
                if max_day_range < day_range:
                    continue

                other_sample_attr_list = \
                    [sample_data_dict[other_sample][v] for v in attr_list]
                # See sample_attr_list comment
                other_sample_attr_list = \
                    [y for x, y in zip(attr_list, other_sample_attr_list)
                     if
                     x not in attr_val_filters or y not in attr_val_filters[x]]

                an_iterator = zip(sample_attr_list,
                                  other_sample_attr_list,
                                  disjoint_match_list)
                is_a_link = True
                for sample_val, other_val, disjoint in an_iterator:
                    if disjoint and sample_val == other_val:
                        is_a_link = False
                        break
                    elif not disjoint and sample_val != other_val:
                        is_a_link = False
                        break

                if is_a_link:
                    if attr in weights:
                        def repl_fn(match_obj):
                            match = match_obj.group(0)
                            if match[0] == "!":
                                exp_attr = match.strip("!")
                                return sample_data_dict[sample][exp_attr]
                            elif match[0] == "@":
                                exp_attr = match.strip("@")
                                return sample_data_dict[other_sample][exp_attr]
                            else:
                                msg = "Unexpected regex match obj when " \
                                      "parsing weight expression: " + match
                                raise RuntimeError(msg)

                        weight_exp = weights[attr]
                        subbed_exp = regex_obj.sub(repl_fn, weight_exp)
                        link_weight = eval_expr(subbed_exp)

                        if attr in weight_filters["not_equal"]:
                            neq = weight_filters["not_equal"][attr]
                            if link_weight == neq:
                                continue
                        if attr in weight_filters["less_than"]:
                            le = weight_filters["less_than"][attr]
                            if link_weight < le:
                                continue
                        if attr in weight_filters["greater_than"]:
                            ge = weight_filters["greater_than"][attr]
                            if link_weight > ge:
                                continue
                    else:
                        link_weight = 0

                    if other_datetime > sample_datetime:
                        sample_links_dict[attr][(sample, other_sample)] = \
                            link_weight
                    else:
                        sample_links_dict[attr][(sample, other_sample)] = \
                            link_weight

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


def get_link_parallel_translation(default_yaxis_range, yaxis_range):
    """Get min distance 2 links b/w same nodes are parallel shifted.

    We want the min distance when the main graph is not zoomed in to be
    0.05 wrt the scale of the y-axis. As the fig is zoomed in, we want
    the distance to remain the same on the computer screen, so we
    adjust accordingly.

    :param default_yaxis_range: y-axis range when main graph first
        loads.
    :type default_yaxis_range: list
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Min parallel translation distance b/w two links connecting
        the same nodes.
    :rtype: float
    """
    default_yaxis_range_len = default_yaxis_range[1] - default_yaxis_range[0]

    # a is a variable we will multiply by zoomed in y-axis range lens
    # to get a zoomed in min distance.
    a = 0.05 / default_yaxis_range_len

    yaxis_range_len = yaxis_range[1] - yaxis_range[0]
    ret = yaxis_range_len * a

    return ret


def get_main_fig_attr_links_dict(sample_links_dict, main_fig_nodes_x_dict,
                                 main_fig_nodes_y_dict, selected_samples,
                                 main_fig_height, main_fig_width,
                                 link_parallel_translation):
    """Get dict with info used by Plotly to viz links in main graph.

    :param sample_links_dict: ``get_sample_links_dict`` ret val
    :type sample_links_dict: dict
    :param main_fig_nodes_x_dict: ``get_main_fig_nodes_x_dict`` ret val
    :type main_fig_nodes_x_dict: dict
    :param main_fig_nodes_y_dict: ``get_main_fig_nodes_y_dict`` ret val
    :type main_fig_nodes_y_dict: dict
    :param selected_samples: Samples selected by users
    :type selected_samples: set[str]
    :param main_fig_height: Height for main fig
    :type main_fig_height: int
    :param main_fig_width: Width for main fig
    :type main_fig_width: int
    :param link_parallel_translation: Min distance links between the
        same nodes must be parallel translated.
    :type link_parallel_translation: float
    :return: Dict with info used by Plotly to viz links in main graph
    :rtype: dict
    """
    ret = {}
    translation_dict = {}
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

            total_translation = multiplier * link_parallel_translation

            x0 = main_fig_nodes_x_dict[sample]
            y0 = main_fig_nodes_y_dict[sample]
            x1 = main_fig_nodes_x_dict[other_sample]
            y1 = main_fig_nodes_y_dict[other_sample]

            if (x1 - x0) == 0:
                x0 += total_translation * (main_fig_height / main_fig_width)
                x1 += total_translation * (main_fig_height / main_fig_width)
            elif (y1 - y0) == 0:
                y0 += total_translation
                y1 += total_translation
            else:
                inverse_perpendicular_slope = (x1 - x0) / (y1 - y0)
                numerator = total_translation ** 2
                denominator = 1 + inverse_perpendicular_slope**2
                x_translation = sqrt(numerator/denominator)
                if total_translation < 0:
                    x_translation *= -1
                x0 += x_translation * (main_fig_height / main_fig_width)
                x1 += x_translation * (main_fig_height / main_fig_width)
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


def get_main_fig_attr_link_labels_dict(sample_links_dict,
                                       main_fig_nodes_x_dict,
                                       main_fig_nodes_y_dict, selected_samples,
                                       main_fig_height, main_fig_width,
                                       link_parallel_translation, weights):
    """Get dict with info used by Plotly to viz link labels.

    TODO: there may be a better way to do this. Certainly, the code
          used to calculate the midpoints does not need to be repeated
          each loop. We'll keep it there in case we decide to translate
          different labels parallel-wise later.

    Current logic:
    * Put labels parallel to midpoint of centermost line between nodes
    * Multiple labels occupy the same vertical plane--offsetted along
      x-axis only

    :param sample_links_dict: ``get_sample_links_dict`` ret val
    :type sample_links_dict: dict
    :param main_fig_nodes_x_dict: ``get_main_fig_nodes_x_dict`` ret val
    :type main_fig_nodes_x_dict: dict
    :param main_fig_nodes_y_dict: ``get_main_fig_nodes_y_dict`` ret val
    :type main_fig_nodes_y_dict: dict
    :param selected_samples: Samples selected by users
    :type selected_samples: set[str]
    :param main_fig_height: Height for main fig
    :type main_fig_height: int
    :param main_fig_width: Width for main fig
    :type main_fig_width: int
    :param link_parallel_translation: Min distance links between the
        same nodes must be parallel translated.
    :type link_parallel_translation: float
    :param weights: Dictionary of expressions used to assign weights to
        specific attr links
    :type weights: dict
    :return: Dict with info used by Plotly to viz links in main graph
    :rtype: dict
    """
    ret = {}
    label_count_dict = {}
    min_multiplier = len(sample_links_dict)/2 + 1
    total_translation = min_multiplier * link_parallel_translation
    for attr in sample_links_dict:
        if attr not in weights:
            continue

        ret[attr] = {
            "opaque": {"x": [], "y": [], "text": []},
            "transparent": {"x": [], "y": [], "text": []}
        }

        for (sample, other_sample) in sample_links_dict[attr]:
            if (sample, other_sample) in label_count_dict:
                label_count_dict[(sample, other_sample)] += 1
                label_count = label_count_dict[(sample, other_sample)]
            else:
                label_count = 1
                label_count_dict[(sample, other_sample)] = label_count

            x0 = main_fig_nodes_x_dict[sample]
            y0 = main_fig_nodes_y_dict[sample]
            x1 = main_fig_nodes_x_dict[other_sample]
            y1 = main_fig_nodes_y_dict[other_sample]

            if (x1 - x0) == 0:
                x0 += total_translation * (main_fig_height / main_fig_width)
                x1 += total_translation * (main_fig_height / main_fig_width)
            elif (y1 - y0) == 0:
                y0 += total_translation
                y1 += total_translation
            else:
                inverse_perpendicular_slope = (x1 - x0) / (y1 - y0)
                numerator = total_translation ** 2
                denominator = 1 + inverse_perpendicular_slope**2
                x_translation = sqrt(numerator/denominator)
                if total_translation < 0:
                    x_translation *= -1
                x0 += x_translation * (main_fig_height / main_fig_width)
                x1 += x_translation * (main_fig_height / main_fig_width)
                y0 += -inverse_perpendicular_slope * x_translation
                y1 += -inverse_perpendicular_slope * x_translation

            xmid = (x0 + x1) / 2 + \
                   (label_count - 1) * 3 * link_parallel_translation
            ymid = (y0 + y1) / 2
            weight = sample_links_dict[attr][(sample, other_sample)]

            selected_link = \
                sample in selected_samples or other_sample in selected_samples
            if selected_samples and not selected_link:
                ret[attr]["transparent"]["x"].append(xmid)
                ret[attr]["transparent"]["y"].append(ymid)
                ret[attr]["transparent"]["text"].append(weight)
            else:
                ret[attr]["opaque"]["x"].append(xmid)
                ret[attr]["opaque"]["y"].append(ymid)
                ret[attr]["opaque"]["text"].append(weight)

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


def get_date_x_vals_dict(date_list, datetime_list):
    """Get dict mapping dates to numerical x vals.

    :param date_list: List of sample dates wrt all nodes
    :type date_list: list
    :param datetime_list: List of sample datetime objs wrt all nodes
    :type datetime_list: list
    :return: Dict mapping dates to numerical x vals
    :rtype: dict
    """
    date_datetime_zip_list = zip(datetime_list, date_list)
    sorted_date_list = [date for (_, date) in sorted(date_datetime_zip_list)]
    sorted_date_table = dict.fromkeys(sorted_date_list)
    ret = {e: i+1 for i, e in enumerate(sorted_date_table)}
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


def get_max_node_count_at_track_dict(track_date_node_count_dict):
    """Get the max number of nodes at one date in every track.

    :param track_date_node_count_dict: Number of nodes at each track
        and date combination.
    :type track_date_node_count_dict: dict
    :return: Maximum number of nodes at a single date within each track
    :rtype: dict
    """
    unsorted_ret = {}
    for (track, date) in track_date_node_count_dict:
        node_count = track_date_node_count_dict[(track, date)]
        if track in unsorted_ret:
            old_count = unsorted_ret[track]
            if node_count > old_count:
                unsorted_ret[track] = node_count
        else:
            unsorted_ret[track] = node_count
    ret = {k: unsorted_ret[k] for k in sorted(unsorted_ret, key=sorting_key)}
    return ret


def get_track_y_vals_dict(max_node_count_at_track_dict):
    """Get the y val at the center of each track on the main graph.

    :param max_node_count_at_track_dict: Maximum number of nodes at a
        single date within each track.
    :type max_node_count_at_track_dict: dict
    :return: Dict mapping tracks to numerical y vals
    :rtype: dict
    """
    ret = {}
    last_track_top_boundary = 0
    for track in max_node_count_at_track_dict:
        node_count = max_node_count_at_track_dict[track]
        ret[track] = last_track_top_boundary + 1 + (node_count - 1)/2
        last_track_top_boundary += node_count
    return ret


def get_main_fig_nodes_y_dict(sample_data_dict, date_attr,
                              track_date_node_count_dict,
                              max_node_count_at_track_dict, y_axes,
                              track_y_vals_dict):
    """Get dict mapping nodes to y vals.

    :param sample_data_dict: Sample file data parsed into dict obj
    :rtype: dict
    :param date_attr: Sample file attr encoded by sample date/x-axis
    :type date_attr: str
    :param track_date_node_count_dict: Number of nodes at each track
        and date combination.
    :type track_date_node_count_dict: dict
    :param max_node_count_at_track_dict: Maximum number of nodes at a
        single date within each track.
    :type max_node_count_at_track_dict: dict
    :param y_axes: List of attrs to use as hierarchical y axes
    :type y_axes: list[str]
    :param track_y_vals_dict: Dict mapping tracks to numerical y vals
    :type track_y_vals_dict: dict
    :return: Dict mapping nodes to y vals
    :rtype: dict
    """
    helper_obj = {k: [max_node_count_at_track_dict[k[0]]/(v+1), 1]
                  for k, v in track_date_node_count_dict.items()}

    main_fig_nodes_y_dict = {}
    for sample in sample_data_dict:
        sample_date = sample_data_dict[sample][date_attr]
        sample_track = \
            tuple((sample_data_dict[sample][axis] for axis in y_axes))
        [stagger, multiplier] = helper_obj[(sample_track, sample_date)]

        unstaggered_y = track_y_vals_dict[sample_track]
        lowest_y = unstaggered_y - max_node_count_at_track_dict[sample_track]/2
        staggered_y = lowest_y + (stagger * multiplier)

        main_fig_nodes_y_dict[sample] = staggered_y
        helper_obj[(sample_track, sample_date)][1] += 1

    return main_fig_nodes_y_dict


def get_main_fig_primary_facet_x(default_xaxis_range, num_of_facets):
    """Get x vals for lines used to split main graph by primary y.

    The primary y is the first y attr used to generate tracks.

    :param default_xaxis_range: Main graph x-axis min and max val,
        without any zooming or panning.
    :type default_xaxis_range: list
    :param num_of_facets: Number of lines to draw
    :type num_of_facets: int
    :return: List of x vals Plotly needs to draw lines splitting main
        graph by primary y vals.
    :rtype: list
    """
    main_fig_facet_x = []
    [xmin, xmax] = default_xaxis_range
    for i in range(0, num_of_facets):
        main_fig_facet_x += [xmin, xmax, None]
    return main_fig_facet_x


def get_main_fig_primary_facet_y(max_node_count_at_track_dict):
    """Get y vals for lines used to split main graph by primary y.

    The primary y is the first y attr used to generate tracks.

    :param max_node_count_at_track_dict: Maximum number of nodes at a
        single date within each track.
    :type max_node_count_at_track_dict: dict
    :return: List of y vals Plotly needs to draw lines splitting main
        graph by primary y vals.
    :rtype: list
    """
    main_fig_facet_y = []
    last_primary_y_seen = None
    y_acc = 0
    for track in max_node_count_at_track_dict:
        primary_y = track[0]
        if last_primary_y_seen is None:
            last_primary_y_seen = primary_y
        elif primary_y != last_primary_y_seen:
            main_fig_facet_y += [y_acc+0.5, y_acc+0.5, None]
            last_primary_y_seen = primary_y
        y_acc += max_node_count_at_track_dict[track]
    return main_fig_facet_y


def get_main_fig_secondary_facet_x(default_xaxis_range, num_of_facets):
    """Get x vals for lines used to split main graph into tracks.

    :param default_xaxis_range: Main graph x-axis min and max val,
        without any zooming or panning.
    :type default_xaxis_range: list
    :param num_of_facets: Number of lines to draw
    :type num_of_facets: int
    :return: List of x vals Plotly needs to draw lines splitting main
        graph by tracks.
    :rtype: list
    """
    main_fig_facet_x = []
    [xmin, xmax] = default_xaxis_range
    for i in range(0, num_of_facets):
        main_fig_facet_x += [xmin, xmax, None]
    return main_fig_facet_x


def get_main_fig_secondary_facet_y(max_node_count_at_track_dict):
    """Get y vals for lines used to split main graph into tracks.

    :param max_node_count_at_track_dict: Maximum number of nodes at a
        single date within each track.
    :type max_node_count_at_track_dict: dict
    :return: List of y vals Plotly needs to draw lines splitting main
        graph by tracks.
    :rtype: list
    """
    main_fig_facet_y = []
    y_acc = 0
    for track in max_node_count_at_track_dict:
        y_acc += max_node_count_at_track_dict[track]
        main_fig_facet_y += [y_acc+0.5, y_acc+0.5, None]
    return main_fig_facet_y[:-3]


def get_main_fig_height(max_node_count_at_track_dict):
    """Return height for main fig.

    This is an absolute (not relative height). This takes into account
    the number of tracks you need to visualize, and also increases
    space per track if you are encoding more than 2 attrs along the
    y-axis.

    :param max_node_count_at_track_dict: Maximum number of nodes at a
        single date within each track.
    :type max_node_count_at_track_dict: dict
    :return: Height for main fig
    :rtype: int
    """
    num_of_rows = sum(max_node_count_at_track_dict.values())
    num_of_y_axis_attrs = len(next(iter(max_node_count_at_track_dict)))

    return num_of_rows * (72 + (num_of_y_axis_attrs - 2) * 24)
