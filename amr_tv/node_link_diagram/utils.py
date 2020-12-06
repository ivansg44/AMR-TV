import networkx as nx
import plotly.graph_objects as go


def filter_transmission_events(selected_events, transmission_events):
    """Filter transmission_events for node-links of interest.

    :param selected_events: Specified organism_group-organism_group
    relationships inside nested dictionary.
    :type selected_events: dict[str, dict[str, None]]
    :param transmission_events: See run_transmission_events_query
    return value.
    :type transmission_events: list[list]
    :return: Filtered version of run_transmission_events_query return
    value.
    :rtype: list[list]
    """
    ret = []

    for event in transmission_events:
        organism_group_one = event[1]
        organism_group_two = event[4]
        if organism_group_one in selected_events:
            if organism_group_two in selected_events[organism_group_one]:
                ret.append(event)

    return ret


def get_transmission_network(transmission_events):
    """Create a networkX graph encoding transmission_events.

    :param transmission_events: See run_transmission_events_query
    return value.
    :type transmission_events: list[list]
    :return: networkX graph
    :rtype: nx.Graph
    """
    node_indices_dict = \
        get_transmission_network_node_indices_dict(transmission_events)
    graph = nx.Graph()
    for event in transmission_events:
        node_index_one = node_indices_dict[str(event[0:3])]
        node_index_two = node_indices_dict[str(event[3:])]
        graph.add_node(node_index_one,
                       organism_group=event[1],
                       min_date=event[2],
                       amr_genotypes=event[0])
        graph.add_node(node_index_two,
                       organism_group=event[4],
                       min_date=event[5],
                       amr_genotypes=event[3])
        graph.add_edge(node_index_one, node_index_two)
    return graph


def get_transmission_network_node_indices_dict(transmission_events):
    """Assigns an index to each unique node in transmission_events.

    This is useful when making the networkX graph, as
    transmission_events details every one-to-one relationship, so
    nodes may appear twice.

    :param transmission_events: See run_transmission_events_query
    return value.
    :type transmission_events: list[list]
    :return: Concatenated and stringified amr_genotypes, min_date, and 
    organism_groups of unique nodes, and an assigned index.
    :rtype: dict[str, int]
    """
    node_indices_dict = {}
    count = 0
    for event in transmission_events:
        str_node_one = str(event[0:3])
        str_node_two = str(event[3:])
        if str_node_one not in node_indices_dict:
            node_indices_dict[str_node_one] = count
            count += 1
        if str_node_two not in node_indices_dict:
            node_indices_dict[str_node_two] = count
            count += 1
    return node_indices_dict


def get_node_color_map(selected_events):
    """Generate color map for all organism groups in selected_events.

    This is done dynamically for each node-link diagram, because it 
    minimizes collisions.

    :param selected_events: Specified organism_group-organism_group
    relationships inside nested dictionary.
    :type selected_events: dict[str, dict[str, None]]
    :return: organism_group and their assigned hex codes.
    :rtype: dict[str, str]
    """
    # https://colorbrewer2.org/?type=qualitative&scheme=Set1&n=9
    colour_scheme = [
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33",
        "#a65628", "#f781bf", "#999999"
    ]

    acc = 0
    color_map = {}
    for organism_group in selected_events:
        if len(selected_events[organism_group]):
            color_map[organism_group] = colour_scheme[acc % len(colour_scheme)]
            acc += 1

    return color_map


def get_node_traces(graph, positions, color_map):
    """Generate scatter traces from graph.

    One scatter trace is generated for every organism_group.

    :param graph: See get_transmission_network return value.
    :type graph: nx.Graph
    :param positions: x and y positions of every node in graph.
    :type positions: dict[int, list[int, int]]
    :param color_map: See get_node_color_map return value.
    :type color_map: dict[str, str]
    :return: NetworkX scatter traces for every organism group in graph.
    :rtype: list[go.Scatter]
    """
    traces_dict = {}
    for node in graph.nodes():
        organism_group = graph.nodes[node]["organism_group"]
        if organism_group not in traces_dict:
            traces_dict[organism_group] = {
                "x_list": [],
                "y_list": [],
                "custom_data_list": [],
                "text_list": [],
                "color": color_map[organism_group]
            }

        trace_dict = traces_dict[organism_group]
        trace_dict["x_list"].append(positions[node][0])
        trace_dict["y_list"].append(positions[node][1])

        min_date = graph.nodes[node]["min_date"]
        amr_genotypes = graph.nodes[node]["amr_genotypes"]
        trace_dict["custom_data_list"].append({
            "organism_group": organism_group,
            "amr_genotypes": amr_genotypes
        })

        trace_dict["text_list"].append("min_date: " + min_date)

    ret = []
    for organism_group in traces_dict:
        trace_dict = traces_dict[organism_group]
        trace = go.Scatter(
            x=trace_dict["x_list"],
            y=trace_dict["y_list"],
            text=trace_dict["text_list"],
            mode='markers',
            hoverinfo='text',
            customdata=trace_dict["custom_data_list"],
            marker={
                "showscale": False,
                "color": trace_dict["color"],
                "size": 10,
                "line_width": 2
            },
            name=organism_group
        )
        ret.append(trace)

    return ret


def get_graph_layout(graph, positions):
    """Get layout data for node-link diagram plotly figure.

    :param graph: See get_transmission_network return value.
    :type graph: nx.Graph
    :param positions: x and y positions of every node in graph.
    :type positions: dict[int, list[int, int]]
    :return: Layout data for node-link diagram plotly figure.
    :rtype: dict
    """
    axis = {
        "showline": False,
        "zeroline": False,
        "showgrid": False,
        "showticklabels": False,
        "ticklen": 0
    }

    # Plotly does not support built-in arrows for some idiotic reason.
    # Here's a hackey solution from:
    # https://stackoverflow.com/questions/57482878/
    # plotting-a-directed-graph-with-dash-through-matplotlib
    annotations = []
    for edge in graph.edges():
        # NetworkX re-orders edges by node index
        # TODO: less hackey way to do this?
        node_0 = graph.nodes[edge[0]]
        node_1 = graph.nodes[edge[1]]
        if len(node_0["amr_genotypes"]) < len(node_1["amr_genotypes"]):
            edge_0 = edge[0]
            edge_1 = edge[1]
        else:
            edge_0 = edge[1]
            edge_1 = edge[0]

        annotations.append({
            "showarrow": True,
            "arrowsize": 2,
            "arrowwidth": 1,
            "arrowhead": 1,
            "standoff": 3,
            "startstandoff": 1,
            "ax": positions[edge_0][0],
            "ay": positions[edge_0][1],
            "axref": "x",
            "ayref": "y",
            "x": positions[edge_1][0],
            "y": positions[edge_1][1],
            "xref": "x",
            "yref": "y",
        })

    return {
        "width": 700,
        "height": 700,
        "margin": {
            "l": 0, "r": 0, "t": 0, "b": 0
        },
        "showlegend": True,
        "xaxis": axis,
        "yaxis": axis,
        "annotations": annotations
    }
