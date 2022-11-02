"""Parses sample file for data used in viz."""

from base64 import b64decode
from collections import Counter
import csv
from datetime import datetime
from io import StringIO
from itertools import groupby
from json import loads
from math import atan, degrees, radians, sqrt, tan
from re import compile

import networkx as nx
import pandas as pd

from adaptagrams.cola import adaptagrams as ag
from expression_evaluator import eval_expr


def parse_fields_from_example_file(example_file_base64_str, delimiter):
    """Return list of fields from example file.

    This is a list corresponding to values in the top row of example
    file.

    :param example_file_base64_str: Base64 encoded str corresponding to
        contents of user uploaded example file.
    :type example_file_base64_str: str
    :param delimiter: Delimiter in example file
    :type delimiter: str
    """
    example_file_str = b64decode(example_file_base64_str).decode("utf-8")
    reader = csv.reader(StringIO(example_file_str), delimiter=delimiter)
    for row in reader:
        return row
    return []


def get_app_data(sample_file_base64_str, config_file_base64_str,
                 matrix_file_base64_str=None, selected_nodes=None, vpsc=False):
    """Get data from uploaded file that is used to generate viz.

    :param sample_file_base64_str: Base64 encoded str corresponding to
        contents of user uploaded sample file.
    :type sample_file_base64_str: str
    :param config_file_base64_str: Base64 encoded str corresponding to
        contents of user uploaded config file.
    :type config_file_base64_str: str
    :param matrix_file_base64_str: Base64 encoded str corresponding to
        contents of user uploaded matrix file.
    :type matrix_file_base64_str: str
    :param selected_nodes: Nodes selected by user
    :type selected_nodes: dict
    :param vpsc: Run vpsc nodal overlap removal algorithm
    :type vpsc: bool
    :return: Data derived from sample data, used to generate viz
    :rtype: dict
    """
    if selected_nodes is None:
        selected_nodes = {}

    sample_file_str = b64decode(sample_file_base64_str).decode("utf-8")

    config_file_str = b64decode(config_file_base64_str).decode("utf-8")
    config_file_dict = loads(config_file_str)

    if matrix_file_base64_str:
        matrix_file_str = b64decode(matrix_file_base64_str).decode("utf-8")
        matrix_file_df = pd.read_csv(StringIO(matrix_file_str),
                                     sep="\t",
                                     index_col=0)
    else:
        matrix_file_df = None

    sample_data_dict = get_sample_data_dict(sample_file_str,
                                            config_file_dict["sample_id"],
                                            config_file_dict["delimiter"],
                                            config_file_dict["date_attr"],
                                            config_file_dict["date_input"],
                                            config_file_dict["date_output"],
                                            config_file_dict["null_vals"])
    sample_data_vals = sample_data_dict.values()
    enumerated_samples = enumerate(sample_data_dict)
    selected_samples = \
        {k for i, k in enumerated_samples if str(i) in selected_nodes}

    date_list = [v[config_file_dict["date_attr"]] for v in sample_data_vals]
    datetime_list = [v["datetime_obj"] for v in sample_data_vals]
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

    num_of_primary_facets = \
        len({k[0] for k in max_node_count_at_track_dict}) - 1
    num_of_secondary_facets = len(max_node_count_at_track_dict.keys()) - 1

    node_symbol_attr = config_file_dict["node_symbol_attr"]
    if node_symbol_attr:
        # Use tuples instead of lists for hashing
        node_symbol_attr_list = \
            [tuple([v[e] for e in node_symbol_attr]) for v in sample_data_vals]
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
        # Use tuples instead of lists for hashing
        node_color_attr_list = \
            [tuple([v[e] for e in node_color_attr]) for v in sample_data_vals]
        node_color_attr_dict = get_node_color_attr_dict(node_color_attr_list)
        main_fig_nodes_marker_color = \
            [node_color_attr_dict[v] for v in node_color_attr_list]
    else:
        node_color_attr_dict = {}
        main_fig_nodes_marker_color = "lightgrey"

    label_attr = config_file_dict["label_attr"]
    main_fig_nodes_text = \
        ["<br>".join(["<b>%s</b>" % v[e] for e in label_attr])
         for v in sample_data_vals]

    main_fig_nodes_hovertext = [k for k in sample_data_dict]

    xaxis_range = [0.5, len(date_x_vals_dict) + 0.5]
    yaxis_range = [0.5, sum(max_node_count_at_track_dict.values())+0.5]

    main_fig_height = get_main_fig_height(max_node_count_at_track_dict)
    main_fig_width = len(date_x_vals_dict) * 144

    sample_links_dict = get_sample_links_dict(
        sample_data_dict=sample_data_dict,
        links_config=config_file_dict["links_config"],
        primary_y=config_file_dict["y_axes"][0],
        links_across_primary_y=config_file_dict["links_across_primary_y"],
        max_day_range=config_file_dict["max_day_range"],
        matrix_file_df=matrix_file_df
    )

    main_fig_nodes_y_dict = get_main_fig_nodes_y_dict(
        sample_data_dict=sample_data_dict,
        sample_links_dict=sample_links_dict,
        date_attr=config_file_dict["date_attr"],
        track_list=track_list,
        track_date_node_count_dict=track_date_node_count_dict,
        max_node_count_at_track_dict=max_node_count_at_track_dict,
        track_y_vals_dict=track_y_vals_dict
    )

    if vpsc:
        node_overlap_dict = \
            remove_node_overlap(main_fig_nodes_x_dict,
                                main_fig_nodes_y_dict,
                                xaxis_range,
                                yaxis_range)
        main_fig_nodes_x_dict = node_overlap_dict["main_fig_nodes_x_dict"]
        main_fig_nodes_y_dict = node_overlap_dict["main_fig_nodes_y_dict"]

    zoomed_out_main_fig_x_axis_dict = \
        get_zoomed_out_main_fig_x_axis_dict(datetime_list,
                                            main_fig_nodes_x_dict)

    sample_links_dict = \
        filter_link_loops(sample_links_dict=sample_links_dict,
                          links_config=config_file_dict["links_config"],
                          main_fig_nodes_x_dict=main_fig_nodes_x_dict,
                          main_fig_nodes_y_dict=main_fig_nodes_y_dict,
                          matrix_file_df=matrix_file_df)

    link_color_dict = get_link_color_dict(sample_links_dict)

    main_fig_links_dict = get_main_fig_links_dict(
        sample_links_dict=sample_links_dict,
        main_fig_nodes_x_dict=main_fig_nodes_x_dict,
        main_fig_nodes_y_dict=main_fig_nodes_y_dict,
        selected_samples=selected_samples,
        main_fig_height=main_fig_height,
        main_fig_width=main_fig_width,
        xaxis_range=xaxis_range,
        yaxis_range=yaxis_range
    )

    main_fig_arcs_dict = get_main_fig_arcs_dict(
        sample_links_dict=sample_links_dict,
        main_fig_nodes_x_dict=main_fig_nodes_x_dict,
        main_fig_nodes_y_dict=main_fig_nodes_y_dict,
        selected_samples=selected_samples,
        main_fig_height=main_fig_height,
        main_fig_width=main_fig_width,
        xaxis_range=xaxis_range,
        yaxis_range=yaxis_range
    )

    main_fig_link_arrowheads_dict = get_main_fig_link_arrowheads_dict(
        main_fig_links_dict=main_fig_links_dict,
        links_config=config_file_dict["links_config"],
        main_fig_height=main_fig_height,
        yaxis_range=yaxis_range
    )

    main_fig_link_labels_dict = get_main_fig_link_labels_dict(
        sample_links_dict=sample_links_dict,
        main_fig_links_dict=main_fig_links_dict,
        main_fig_nodes_x_dict=main_fig_nodes_x_dict,
        selected_samples=selected_samples,
        main_fig_height=main_fig_height,
        main_fig_width=main_fig_width,
        xaxis_range=xaxis_range,
        yaxis_range=yaxis_range
    )

    if selected_samples:
        ss = selected_samples
        main_fig_nodes_textfont_color = \
            ["black" if k in ss else "grey" for k in sample_data_dict]
    else:
        main_fig_nodes_textfont_color = "black"

    main_fig_yaxis_ticktext = get_main_fig_yaxis_ticktext(track_y_vals_dict)
    zoomed_out_main_fig_yaxis_tickvals = \
        get_zoomed_out_main_fig_yaxis_tickvals(track_y_vals_dict)
    zoomed_out_main_fig_yaxis_ticktext = list(dict.fromkeys(
        [";".join("null" if j is None else j for j in i[0])
         for i in track_y_vals_dict]
    ))

    if vpsc:
        xaxis_range = node_overlap_dict["xaxis_range"]
        yaxis_range = node_overlap_dict["yaxis_range"]

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
            [main_fig_nodes_x_dict["staggered"][k] for k in sample_data_dict],
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
        "main_fig_nodes_hovertext":
            main_fig_nodes_hovertext,
        "node_color_attr_dict": node_color_attr_dict,
        "main_fig_links_dict": main_fig_links_dict,
        "main_fig_arcs_dict": main_fig_arcs_dict,
        "main_fig_link_arrowheads_dict": main_fig_link_arrowheads_dict,
        "main_fig_link_labels_dict": main_fig_link_labels_dict,
        "link_color_dict": link_color_dict,
        "main_fig_primary_facet_x":
            get_main_fig_primary_facet_x(xaxis_range, num_of_primary_facets),
        "main_fig_primary_facet_y":
            get_main_fig_primary_facet_y(max_node_count_at_track_dict),
        "main_fig_secondary_facet_x":
            get_main_fig_secondary_facet_x(xaxis_range,
                                           num_of_secondary_facets),
        "main_fig_secondary_facet_y":
            get_main_fig_secondary_facet_y(max_node_count_at_track_dict),
        "main_fig_height": main_fig_height,
        "main_fig_width": main_fig_width,
        "zoomed_out_main_fig_xaxis_tickvals":
            list(zoomed_out_main_fig_x_axis_dict.values()),
        "zoomed_out_main_fig_xaxis_ticktext":
            list(zoomed_out_main_fig_x_axis_dict.keys()),
        "zoomed_out_main_fig_yaxis_tickvals":
            zoomed_out_main_fig_yaxis_tickvals,
        "zoomed_out_main_fig_yaxis_ticktext":
            zoomed_out_main_fig_yaxis_ticktext
    }

    return app_data


def get_unsorted_track_list(sample_data_dict, y_axes):
    """Get an unsorted list of tracks assigned across all nodes.

    A track for a node (N) consists of:

    * 1 tuple (A)
    * >=1 tuples inside A (B)
    * >=1 attribute values from a node N inside B

    This maps to the y axes specified in the config file, which
    consists of:

    * 1 list (A)
    * >=1 lists inside A (B)
    * >=1 attributes to collect from nodes

    e.g., If the y axes selected are ["ham"], ["spam", "foo"], and
    ["eggs"], the tracks are ((sample_1_ham,),
    (sample_1_spam, sample_1_foo,), (sample_1_eggs),),
    ((sample_2_ham,), (sample_2_spam, sample_2_foo,),
    (sample_2_eggs,),), ...

    We use tuples because they are hashable, which is useful to us in
    downstream code.

    :param sample_data_dict: ``get_sample_data_dict`` ret val
    :type sample_data_dict: dict
    :param y_axes: List of lists, with inner lists populated by
        attributes to collect from nodes when calculating their
        position along the y axis.
    :type y_axes: list[list[str]]
    :return: Unsorted list of tracks assigned across all nodes
    :rtype: list[tuple[tuple[str]]]
    """
    lists_to_zip = []
    vals = sample_data_dict.values()
    for axis_list in y_axes:
        lists_to_zip.append([tuple([i[j] for j in axis_list]) for i in vals])
    ret = list(zip(*lists_to_zip))
    return ret


def sorting_key(track):
    """Map track to a unique structure for sorting purposes.

    Inspiration from:
    https://stackoverflow.com/a/34757358/11472358

    Basically, convert tracks back into a list of lists, and change the
    inner list values into a unique tuple structure that allows sorting
    of mixed types.

    We sort vals as follows:

    * None comes first
    * Sort ints next
    * Sort strs last

    :param track: Track value for a node
    :type track: tuple[tuple[str]]
    :return: List of tuples mapped to each attr val in track
    :rtype: list[list[tuple]]
    """
    ret = []
    for attr_tuple in track:
        inner_ret = []
        for attr in attr_tuple:
            try:
                inner_ret.append((
                    attr is None,
                    0,
                    int(attr)
                ))
            except (TypeError, ValueError):
                inner_ret.append((
                    attr is None,
                    1,
                    attr
                ))
        ret.append(inner_ret)
    return ret


def get_sample_data_dict(sample_file_str, sample_id_attr, delimiter, date,
                         date_input, date_output, null_vals):
    """Parse sample data file into dict obj.

    :param sample_file_str: Str corresponding to contents of user
        uploaded sample file.
    :type sample_file_str: str
    :param sample_id_attr: Sample file attr corresponding to sample ids
    :type sample_id_attr: str
    :param delimiter: Delimiter in sample file
    :type delimiter: str
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
    for i, row in enumerate(reader):
        if row[date] in null_vals:
            continue
        row = {k: (None if row[k] in null_vals else row[k]) for k in row}

        input_datetime_obj = datetime.strptime(row[date], date_input)
        row[date] = input_datetime_obj.strftime(date_output)
        # We want to keep track of the datetime obj using output format
        row["datetime_obj"] = datetime.strptime(row[date], date_output)

        sample_data_dict[row[sample_id_attr]] = row
    return sample_data_dict


def get_node_symbol_attr_dict(node_symbol_attr_list):
    """Get a dict mapping node symbol attr vals to symbols.

    :param node_symbol_attr_list: List of node symbol attr vals across
        all nodes.
    :type node_symbol_attr_list: list[tuple[str]]
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
    :type node_color_attr_list: list[tuple[str]]
    :return: dict with unique node color attr vals as keys, and actual
        colors as vals.
    :rtype: dict
    """
    node_color_attr_dict = {}
    node_color_attr_table = dict.fromkeys(node_color_attr_list)

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


def get_sample_links_dict(sample_data_dict, links_config, primary_y,
                          links_across_primary_y, max_day_range,
                          matrix_file_df):
    """Get a dict of all links to viz in main graph.

    The keys in the dict are different link labels. The values are a
    nested dict. The keys in the nested dict are tuples containing two
    samples that satisfy the criteria for that link b/w them. The
    values in the nested dict are weights assigned to the link b/w
    these nodes, or ``None`` if no weight is calculated.

    We filter out certain links using ``weight_filters`` and
    ``attr_val_filters``.

    :param sample_data_dict: ``get_sample_data_dict`` ret val
    :type sample_data_dict: dict
    :param links_config: dict of criteria for different user-specified
        links.
    :type links_config: dict
    :param primary_y: First list specified by user in y-axes
    :type primary_y: list[str]
    :param links_across_primary_y: Whether we consider links across
        different primary y vals.
    :type links_across_primary_y: bool
    :param max_day_range: Maximum day range to still consider links
    :type max_day_range: int
    :param matrix_file_df: Dataframe encoding user uploaded matrix
    :type matrix_file_df: pd.DataFrame | None
    :return: Dict detailing links to viz in main graph
    :rtype: dict
    """
    sample_links_dict = {k: {} for k in links_config}
    sample_list = list(sample_data_dict.keys())
    regex_obj = compile("!.*?!|@.*?@|{{matrix}}")

    def get_sample_attr_list(sample_data, link_config_list, filters):
        # Get the attr values for a sample, corresponding to one of the
        # lists that forms criteria for a link.
        return [None
                if (e in filters and sample_data[e] in filters[e])
                else sample_data[e]
                for e in link_config_list]

    for link in links_config:
        all_eq_list = links_config[link]["all_eq"]
        all_neq_list = links_config[link]["all_neq"]
        any_eq_list = links_config[link]["any_eq"]
        weight_exp = links_config[link]["weight_exp"]
        weight_filters = links_config[link]["weight_filters"]
        attr_filters = links_config[link]["attr_filters"]

        for i in range(len(sample_list)):
            sample_i = sample_list[i]
            sample_i_data = sample_data_dict[sample_i]
            sample_i_all_eq_list = get_sample_attr_list(sample_i_data,
                                                        all_eq_list,
                                                        attr_filters)
            sample_i_all_neq_list = get_sample_attr_list(sample_i_data,
                                                         all_neq_list,
                                                         attr_filters)
            sample_i_any_eq_list = get_sample_attr_list(sample_i_data,
                                                        any_eq_list,
                                                        attr_filters)

            for j in range(i + 1, len(sample_list)):
                sample_j = sample_list[j]
                sample_j_data = sample_data_dict[sample_j]

                sample_i_primary_y = [sample_i_data[e] for e in primary_y]
                sample_i_datetime = sample_i_data["datetime_obj"]
                sample_j_primary_y = [sample_j_data[e] for e in primary_y]
                sample_j_datetime = sample_j_data["datetime_obj"]

                if not links_across_primary_y:
                    if sample_i_primary_y != sample_j_primary_y:
                        continue

                day_range_datetime = sample_j_datetime - sample_i_datetime
                day_range = abs(day_range_datetime.days)
                if max_day_range < day_range:
                    continue

                sample_j_all_eq_list = get_sample_attr_list(sample_j_data,
                                                            all_eq_list,
                                                            attr_filters)
                sample_j_all_neq_list = get_sample_attr_list(sample_j_data,
                                                             all_neq_list,
                                                             attr_filters)
                sample_j_any_eq_list = get_sample_attr_list(sample_j_data,
                                                            any_eq_list,
                                                            attr_filters)

                all_eq_zip_obj = \
                    zip(sample_i_all_eq_list, sample_j_all_eq_list)
                all_neq_zip_obj = \
                    zip(sample_i_all_neq_list, sample_j_all_neq_list)
                any_eq_zip_obj = \
                    zip(sample_i_any_eq_list, sample_j_any_eq_list)

                all_eq = all(
                    [i == j and i is not None for (i, j) in all_eq_zip_obj]
                )
                all_neq = all(
                    [i != j and i is not None for (i, j) in all_neq_zip_obj]
                )

                # Unfortunately, any(empty list) returns False. So we
                # need an intermediate variable.
                any_eq_matches = \
                    [i == j and i is not None for (i, j) in any_eq_zip_obj]
                any_eq = any(any_eq_matches) if len(any_eq_matches) else True

                if all_eq and all_neq and any_eq:
                    if weight_exp:
                        def repl_fn(match_obj):
                            # Substitute the syntax used in weight
                            # expressions to reference node attr
                            # values, with the actual attr value.
                            match = match_obj.group(0)
                            if match[0] == "!":
                                exp_attr = match.strip("!")
                                return sample_i_data[exp_attr]
                            elif match[0] == "@":
                                exp_attr = match.strip("@")
                                return sample_j_data[exp_attr]
                            elif match == "{{matrix}}":
                                if matrix_file_df is None:
                                    msg = "Specified matrix in weight exp, " \
                                          "but no matrix file provided"
                                    raise RuntimeError(msg)
                                matrix_val = matrix_file_df[sample_i][sample_j]
                                return str(matrix_val)
                            else:
                                msg = "Unexpected regex match obj when " \
                                      "parsing weight expression: " + match
                                raise RuntimeError(msg)

                        subbed_exp = regex_obj.sub(repl_fn, weight_exp)
                        link_weight = eval_expr(subbed_exp)

                        if "not_equal" in weight_filters:
                            neq = weight_filters["not_equal"]
                            if link_weight in neq:
                                continue
                        if "less_than" in weight_filters:
                            le = weight_filters["less_than"]
                            if link_weight < le:
                                continue
                        if "greater_than" in weight_filters:
                            ge = weight_filters["greater_than"]
                            if link_weight > ge:
                                continue
                    else:
                        link_weight = None

                    if sample_i_datetime <= sample_j_datetime:
                        sample_links_dict[link][(sample_i, sample_j)] = \
                            link_weight
                    else:
                        sample_links_dict[link][(sample_j, sample_i)] = \
                            link_weight

    return sample_links_dict


def filter_link_loops(sample_links_dict, links_config, main_fig_nodes_x_dict,
                      main_fig_nodes_y_dict, matrix_file_df):
    """Remove links forming loops in a network.

    Every group of connected nodes is converted into a minimum spanning
    tree using Kruskal's algorithm. The weights assigned to each link
    for this algorithm are equal to the graphic distance b/w nodes in
    the plot.

    :param sample_links_dict: ``get_sample_links_dict`` ret val
    :type sample_links_dict: dict
    :param links_config: dict of criteria for different user-specified
        links.
    :type links_config: dict
    :param main_fig_nodes_x_dict: ``get_main_fig_nodes_x_dict`` ret val
    :type main_fig_nodes_x_dict: dict
    :param main_fig_nodes_y_dict: ``get_main_fig_nodes_y_dict`` ret val
    :type main_fig_nodes_y_dict: dict
    :param matrix_file_df: Dataframe encoding user uploaded matrix
    :type matrix_file_df: pd.DataFrame | None
    :return: ``sample_links_dict`` with certain links removed to
        prevent loops.
    :rtype: dict
    """
    for link in sample_links_dict:
        graph = nx.Graph()
        if not bool(links_config[link]["minimize_loops"]):
            continue
        for (sample, other_sample) in sample_links_dict[link]:
            # ``weight`` is a reserved keyword in ``add_edge``
            weight_ = sample_links_dict[link][(sample, other_sample)]

            if matrix_file_df is None:
                # nx will use the difference in graphic distance b/w nodes
                # in the plot as weight, for mst purposes.
                # TODO: allow users to specify own edge weight expressions
                x0 = main_fig_nodes_x_dict["staggered"][sample]
                x1 = main_fig_nodes_x_dict["staggered"][other_sample]
                y0 = main_fig_nodes_y_dict[sample]
                y1 = main_fig_nodes_y_dict[other_sample]
                weight = sqrt((x1-x0)**2 + (y1-y0)**2)
            else:
                weight = matrix_file_df[sample][other_sample]

            # Need to track original order because graph is undirected
            order = (sample, other_sample)

            graph.add_edge(sample,
                           other_sample,
                           weight=weight,
                           weight_=weight_,
                           order=order)

        disjoint_subgraphs = \
            [graph.subgraph(c).copy() for c in nx.connected_components(graph)]
        disjoint_mst_subgraphs = \
            [nx.minimum_spanning_tree(g) for g in disjoint_subgraphs]
        disjoint_mst_subgraph_edgeviews = \
            [g.edges(data=True) for g in disjoint_mst_subgraphs]

        new_link_dict = {}
        for edgeview in disjoint_mst_subgraph_edgeviews:
            for (sample, other_sample, data) in edgeview:
                weight_ = data["weight_"]
                order = data["order"]
                new_link_dict[order] = weight_
        sample_links_dict[link] = new_link_dict

    return sample_links_dict


def get_link_color_dict(sample_links_dict):
    """Get dict assigning color to each link.

    :param sample_links_dict: ``get_sample_links_dict`` ret val
    :type sample_links_dict: dict
    :return: Dict links as keys, and unique colors as vals.
    :rtype: dict
    """
    available_link_color_list = [
        (228, 26, 28),
        (55, 126, 184),
        (77, 175, 74),
        (152, 78, 163),
        (255, 127, 0)
    ]
    if len(sample_links_dict) > len(available_link_color_list):
        msg = "Not enough unique colors for different attributes"
        raise IndexError(msg)
    zip_obj = zip(sample_links_dict.keys(), available_link_color_list)
    ret = {k: v for (k, v) in zip_obj}
    return ret


def get_main_fig_links_dict(sample_links_dict, main_fig_nodes_x_dict,
                            main_fig_nodes_y_dict, selected_samples,
                            main_fig_height, main_fig_width, xaxis_range,
                            yaxis_range):
    """Get dict with info used by Plotly to viz links in main graph.

    These are straight links, so this does not include links b/w nodes
    w/ the same x-val, b/c we draw arcs b/w such nodes.

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
    :param xaxis_range: Main graph x-axis min and max val
    :type xaxis_range: list
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Dict with info used by Plotly to viz links in main graph
    :rtype: dict
    """
    ret = {}

    x_pixel_per_unit = main_fig_width / (xaxis_range[1] - xaxis_range[0])
    y_pixel_per_unit = main_fig_height / (yaxis_range[1] - yaxis_range[0])

    link_parallel_translation_dict = {}
    link_unit_parallel_translation = 5 / y_pixel_per_unit
    multiplier = 0
    for link in sample_links_dict:
        link_parallel_translation_dict[link] = \
            multiplier * link_unit_parallel_translation
        multiplier *= -1
        if multiplier >= 0:
            multiplier += 1

    for link in sample_links_dict:
        link_parallel_translation = link_parallel_translation_dict[link]
        ret[link] = {"x": [], "y": []}

        for (sample, other_sample) in sample_links_dict[link]:
            selected_link = \
                sample in selected_samples or other_sample in selected_samples
            if selected_samples and not selected_link:
                continue

            unstaggered_x0 = main_fig_nodes_x_dict["unstaggered"][sample]
            unstaggered_x1 = main_fig_nodes_x_dict["unstaggered"][other_sample]

            x0 = main_fig_nodes_x_dict["staggered"][sample]
            y0 = main_fig_nodes_y_dict[sample]
            x1 = main_fig_nodes_x_dict["staggered"][other_sample]
            y1 = main_fig_nodes_y_dict[other_sample]

            if (unstaggered_x1 - unstaggered_x0) == 0:
                continue
            elif (y1 - y0) == 0:
                y0 += link_parallel_translation
                y1 += link_parallel_translation
            elif link_parallel_translation != 0:
                # https://math.stackexchange.com/a/2870543
                dx = x1 - x0
                dy = y1 - y0
                length = sqrt(dx**2 + dy**2)
                x_translation = dy * link_parallel_translation/length
                x_translation *= y_pixel_per_unit / x_pixel_per_unit
                y_translation = -dx * link_parallel_translation/length
                x0 -= x_translation
                y0 -= y_translation
                x1 -= x_translation
                y1 -= y_translation

            ret[link]["x"] += [x0, x1, None]
            ret[link]["y"] += [y0, y1, None]

    return ret


def get_main_fig_arcs_dict(sample_links_dict, main_fig_nodes_x_dict,
                           main_fig_nodes_y_dict, selected_samples,
                           main_fig_height, main_fig_width, xaxis_range,
                           yaxis_range):
    """Get dict with info used by Plotly to viz arcs in main graph.

    These are arcs, so this does not include straight links b/w nodes
    w/ different x-vals, b/c we draw straight links b/w such nodes.

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
    :param xaxis_range: Main graph x-axis min and max val
    :type xaxis_range: list
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Dict with info used by Plotly to viz links in main graph
    :rtype: dict
    """
    ret = {}

    arc_degree_translation_dict = {}
    arc_unit_degree_translation = 10
    for i, link in enumerate(sample_links_dict):
        arc_degree_translation_dict[link] = i * arc_unit_degree_translation

    for link in sample_links_dict:
        arc_degree_translation = arc_degree_translation_dict[link]
        ret[link] = {"x": [], "y": []}

        for (sample, other_sample) in sample_links_dict[link]:
            selected_link = \
                sample in selected_samples or other_sample in selected_samples
            if selected_samples and not selected_link:
                continue

            unstaggered_x0 = main_fig_nodes_x_dict["unstaggered"][sample]
            unstaggered_x1 = main_fig_nodes_x_dict["unstaggered"][other_sample]

            x0 = main_fig_nodes_x_dict["staggered"][sample]
            y0 = main_fig_nodes_y_dict[sample]
            x1 = main_fig_nodes_x_dict["staggered"][other_sample]
            y1 = main_fig_nodes_y_dict[other_sample]

            if (unstaggered_x1 - unstaggered_x0) != 0:
                continue

            d = abs(y1 - y0) / 2
            e = d / (tan(radians(110+arc_degree_translation)))
            cx = unstaggered_x0 + e
            cy = (y0 + y1) / 2

            ret[link]["x"] += [[x0, cx, x1]]
            ret[link]["y"] += [[y0, cy, y1]]

    return ret


def get_main_fig_link_arrowheads_dict(main_fig_links_dict, links_config,
                                      main_fig_height, yaxis_range):
    """Get dict with info used by Plotly to add arrowheads to links.

    :param main_fig_links_dict: Dict with info used by Plotly to viz
        links in main graph.
    :type main_fig_links_dict: dict
    :param links_config: dict of criteria for different user-specified
        links.
    :type links_config: dict
    :param main_fig_height: Height for main fig
    :type main_fig_height: int
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Dict with info used by Plotly to add arrowheads to links
        in main graph.
    :rtype: dict
    """
    ret = {}

    y_pixel_per_unit = main_fig_height / (yaxis_range[1] - yaxis_range[0])

    for link in main_fig_links_dict:
        if not links_config[link]["show_arrowheads"]:
            continue

        ret[link] = {"x": [], "y": []}

        link_x = main_fig_links_dict[link]["x"]
        link_y = main_fig_links_dict[link]["y"]

        for i in range(0, len(link_x), 3):
            x0, x1 = link_x[i], link_x[i+1]
            y0, y1 = link_y[i], link_y[i+1]

            # https://math.stackexchange.com/a/1630886
            d = sqrt((x1-x0)**2 + (y1-y0)**2)

            dt0 = d - 20/y_pixel_per_unit
            t0 = dt0 / d
            xt0 = (1 - t0) * x0 + t0 * x1
            yt0 = (1 - t0) * y0 + t0 * y1

            dt1 = d - 10/y_pixel_per_unit
            t1 = dt1 / d
            xt1 = (1 - t1) * x0 + t1 * x1
            yt1 = (1 - t1) * y0 + t1 * y1

            ret[link]["x"] += [[xt0, xt1]]
            ret[link]["y"] += [[yt0, yt1]]

    return ret


def get_main_fig_link_labels_dict(sample_links_dict, main_fig_links_dict,
                                  main_fig_nodes_x_dict, selected_samples,
                                  main_fig_height, main_fig_width, xaxis_range,
                                  yaxis_range):
    """Get dict with info used by Plotly to viz link labels.

    :param sample_links_dict: ``get_sample_links_dict`` ret val
    :type sample_links_dict: dict
    :param main_fig_links_dict: Dict with info used by Plotly to viz
        links in main graph.
    :param main_fig_nodes_x_dict: ``get_main_fig_nodes_x_dict`` ret val
    :type main_fig_nodes_x_dict: dict
    :type main_fig_links_dict: dict
    :param selected_samples: Samples selected by users
    :type selected_samples: set[str]
    :param main_fig_height: Height for main fig
    :type main_fig_height: int
    :param main_fig_width: Width for main fig
    :type main_fig_width: int
    :param xaxis_range: Main graph x-axis min and max val
    :type xaxis_range: list
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Dict with info used by Plotly to viz links in main graph
    :rtype: dict
    """
    ret = {}

    x_pixel_per_unit = main_fig_width / (xaxis_range[1] - xaxis_range[0])
    y_pixel_per_unit = main_fig_height / (yaxis_range[1] - yaxis_range[0])

    for link in sample_links_dict:
        ret[link] = {"x": [], "y": [], "text": [], "textangle": []}

        # Keeping a local variable instead of using ``enumerate``,
        # because we do not want to increment i in certain cases.
        i = 0
        for (sample, other_sample) in sample_links_dict[link]:
            selected_link = \
                sample in selected_samples or other_sample in selected_samples
            if selected_samples and not selected_link:
                continue

            unstaggered_x0 = main_fig_nodes_x_dict["unstaggered"][sample]
            unstaggered_x1 = main_fig_nodes_x_dict["unstaggered"][other_sample]
            if (unstaggered_x1 - unstaggered_x0) == 0:
                continue

            weight = sample_links_dict[link][(sample, other_sample)]
            if weight is None:
                i += 1
                continue

            x0 = main_fig_links_dict[link]["x"][i*3]
            x1 = main_fig_links_dict[link]["x"][i*3 + 1]
            y0 = main_fig_links_dict[link]["y"][i*3]
            y1 = main_fig_links_dict[link]["y"][i*3 + 1]

            xmid = (x0 + x1)/2
            ymid = (y0 + y1)/2

            slope = ((y1-y0) * y_pixel_per_unit) / ((x1-x0) * x_pixel_per_unit)
            textangle = -degrees(atan(slope))

            ret[link]["x"].append(xmid)
            ret[link]["y"].append(ymid)
            ret[link]["text"].append(weight)
            ret[link]["textangle"].append(textangle)

            i += 1

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

    main_fig_nodes_x_dict = {
        "unstaggered": {},
        "staggered": {}
    }
    for sample in sample_data_dict:
        sample_date = sample_data_dict[sample][date_attr]
        [stagger, multiplier] = helper_obj[sample_date]

        unstaggered_x = date_x_vals_dict[sample_date]
        lowest_x = unstaggered_x - (1/8)
        staggered_x = lowest_x + (stagger * multiplier)

        main_fig_nodes_x_dict["unstaggered"][sample] = unstaggered_x
        main_fig_nodes_x_dict["staggered"][sample] = staggered_x
        helper_obj[sample_date][1] += 1

    return main_fig_nodes_x_dict


def get_zoomed_out_main_fig_x_axis_dict(datetime_list, main_fig_nodes_x_dict):
    """TODO"""
    date_bin_list = [e.year for e in datetime_list]
    just_one_year = len(set(date_bin_list)) == 1
    if just_one_year:
        date_bin_list = [e.month for e in datetime_list]

    x_dict_vals = main_fig_nodes_x_dict["staggered"].values()
    date_bin_x_zip_obj = zip(date_bin_list, x_dict_vals)
    ret = {}
    for k, group in groupby(sorted(date_bin_x_zip_obj),
                            lambda x: x[0]):
        if just_one_year:
            date = datetime.strptime(str(k), "%m").strftime("%B")
        else:
            date = k
        ret[date] = min(group, key=lambda x: x[1])[1]

    return ret


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


def get_main_fig_yaxis_ticktext(track_y_vals_dict):
    """Get the ticktext used by Plotly to label the y-axis.

    We map each track to a single str. We join the inner tuples with a
    linebreak, and the values inside each tuple with a semicolon.

    :param track_y_vals_dict: ``get_track_y_vals_dict`` ret val
    :type track_y_vals_dict: dict
    :return: Dict with label corresponding to each possible track
    :rtype: dict
    """
    ret = []
    for track in track_y_vals_dict:
        inner_ret = []
        for inner_track in track:
            inner_ret.append(
                "; ".join(["null" if e is None else e for e in inner_track])
            )
        ret.append("<br>".join(inner_ret))
    return ret


def get_zoomed_out_main_fig_yaxis_tickvals(track_y_vals_dict):
    """Get tickvals for zoomed out main fig.

    :param track_y_vals_dict: ``get_track_y_vals_dict`` ret val
    :type track_y_vals_dict: dict
    :return: Dict with label corresponding to each possible track
    :rtype: dict
    """
    ret = []
    for key, group in groupby(track_y_vals_dict.items(), lambda x: x[0][0]):
        group_list = list(group)
        ret.append(sum([e[1] for e in group_list])/len(group_list))
    return ret


def get_main_fig_nodes_y_dict(sample_data_dict, sample_links_dict, date_attr,
                              track_list, track_date_node_count_dict,
                              max_node_count_at_track_dict, track_y_vals_dict):
    """Get dict mapping nodes to y vals.

    We re-order nodes that occupy the same x and y position, to
    minimize the total length of arcs and links. We use a slightly
    modified version of the heuristic described here:

    https://doi.org/10.1109/TST.2012.6297585

    Our modification is that we only reorder within the x/y position.

    :param sample_data_dict: Sample file data parsed into dict obj
    :rtype: dict
    :param date_attr: Sample file attr encoded by sample date/x-axis
    :type date_attr: str
    :param track_list: List of sample tracks wrt all nodes
    :type track_list: list[tuple[tuple[str]]]
    :param track_date_node_count_dict: Number of nodes at each track
        and date combination.
    :type track_date_node_count_dict: dict
    :param max_node_count_at_track_dict: Maximum number of nodes at a
        single date within each track.
    :type max_node_count_at_track_dict: dict
    :param track_y_vals_dict: Dict mapping tracks to numerical y vals
    :type track_y_vals_dict: dict
    :return: Dict mapping nodes to y vals
    :rtype: dict
    """
    xy_ordered_nodes_dict = {}
    for i, sample in enumerate(sample_data_dict):
        sample_date = sample_data_dict[sample][date_attr]
        sample_track = track_list[i]
        xy = (sample_track, sample_date)
        if xy not in xy_ordered_nodes_dict:
            xy_ordered_nodes_dict[xy] = [sample]
        else:
            xy_ordered_nodes_dict[xy].append(sample)

    for xy in xy_ordered_nodes_dict:
        for i in range(3 * len(xy_ordered_nodes_dict[xy])):
            ordered_nodes = xy_ordered_nodes_dict[xy]
            average_neighbour_distance_dict = {}
            for j in range(0, len(ordered_nodes)):
                sum_of_neighbours = 0
                num_of_neighbours = 0
                for k in range(1, len(ordered_nodes)):
                    for link in sample_links_dict:
                        link_dict = sample_links_dict[link]
                        if (j, k) in link_dict or (k, j) in link_dict:
                            sum_of_neighbours += abs(k - j)
                            num_of_neighbours += 1
                if num_of_neighbours:
                    avg_distance = sum_of_neighbours / num_of_neighbours
                else:
                    avg_distance = 0
                average_neighbour_distance_dict[ordered_nodes[j]] = \
                    avg_distance
            xy_ordered_nodes_dict[xy] = \
                sorted(ordered_nodes,
                       key=lambda e: average_neighbour_distance_dict[e])

    helper_obj = {k: [max_node_count_at_track_dict[k[0]]/(v+1), 1]
                  for k, v in track_date_node_count_dict.items()}

    main_fig_nodes_y_dict = {}
    for (sample_track, sample_date) in xy_ordered_nodes_dict:
        for sample in xy_ordered_nodes_dict[(sample_track, sample_date)]:
            [stagger, multiplier] = helper_obj[(sample_track, sample_date)]

            unstaggered_y = track_y_vals_dict[sample_track]
            lowest_y = \
                unstaggered_y - max_node_count_at_track_dict[sample_track]/2
            staggered_y = lowest_y + (stagger * multiplier)

            main_fig_nodes_y_dict[sample] = staggered_y
            helper_obj[(sample_track, sample_date)][1] += 1

    return main_fig_nodes_y_dict


def get_main_fig_primary_facet_x(xaxis_range, num_of_facets):
    """Get x vals for lines used to split main graph by primary y.

    The primary y is the first y attr used to generate tracks.

    :param xaxis_range: Main graph x-axis min and max val
    :type xaxis_range: list
    :param num_of_facets: Number of lines to draw
    :type num_of_facets: int
    :return: List of x vals Plotly needs to draw lines splitting main
        graph by primary y vals.
    :rtype: list
    """
    main_fig_facet_x = []
    [xmin, xmax] = xaxis_range
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


def get_main_fig_secondary_facet_x(xaxis_range, num_of_facets):
    """Get x vals for lines used to split main graph into tracks.

    :param xaxis_range: Main graph x-axis min and max val
    :type xaxis_range: list
    :param num_of_facets: Number of lines to draw
    :type num_of_facets: int
    :return: List of x vals Plotly needs to draw lines splitting main
        graph by tracks.
    :rtype: list
    """
    main_fig_facet_x = []
    [xmin, xmax] = xaxis_range
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


def remove_node_overlap(main_fig_nodes_x_dict, main_fig_nodes_y_dict,
                        xaxis_range, yaxis_range):
    """Run VPSC node overlap removal algorithm.

    See details of algorithm here: https://doi.org/10.1007/11618058_15

    Will update node x and y positions, but also ranges.

    :param main_fig_nodes_x_dict: ``get_main_fig_nodes_x_dict`` ret val
    :type main_fig_nodes_x_dict: dict
    :param main_fig_nodes_y_dict: ``get_main_fig_nodes_y_dict`` ret val
    :type main_fig_nodes_y_dict: dict
    :param xaxis_range: Main graph x-axis min and max val
    :type xaxis_range: list
    :param yaxis_range: Main graph y-axis min and max val
    :type yaxis_range: list
    :return: Dict describing new x and y positions, and also ranges
    :rtype: dict
    """
    rectangles = []

    for k in main_fig_nodes_x_dict["unstaggered"]:
        x = main_fig_nodes_x_dict["staggered"][k]
        y = main_fig_nodes_y_dict[k]
        rectangles.append(ag.Rectangle(x-1, x+1, y-1, y+1))

    [x_min, x_max] = xaxis_range
    [y_min, y_max] = yaxis_range
    rectangle_ptrs = ag.RectanglePtrs(rectangles)
    ag.removeoverlaps(rectangle_ptrs)
    for k, ptr in zip(main_fig_nodes_x_dict["unstaggered"], rectangle_ptrs):
        x = ptr.getCentreX()
        y = ptr.getCentreY()
        main_fig_nodes_x_dict["staggered"][k] = x
        main_fig_nodes_y_dict[k] = y
        if x < x_min:
            x_min = x - 0.5
        elif x > x_max:
            x_max = x + 0.5
        if y < y_min:
            y_min = y - 0.5
        elif y > y_max:
            y_max = y + 0.5

    return {
        "main_fig_nodes_x_dict": main_fig_nodes_x_dict,
        "main_fig_nodes_y_dict": main_fig_nodes_y_dict,
        "xaxis_range": [x_min, x_max],
        "yaxis_range": [y_min, y_max]
    }
