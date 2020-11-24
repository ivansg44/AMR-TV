import networkx as nx


def filter_transmission_events(query_params, transmission_events):
    """TODO: ..."""
    ret = []
    # Less of a headache
    dict_params = dict(query_params)

    for event in transmission_events:
        # "[]" added to end of query_dict keys
        organism_group_one = event[1] + "[]"
        organism_group_two = event[4]
        if organism_group_one in dict_params:
            if organism_group_two in dict_params[organism_group_one]:
                ret.append(event)
        continue

    return ret


def get_transmission_network(transmission_events):
    """TODO: ..."""
    node_indices_dict = \
        get_transmission_network_node_indices_dict(transmission_events)
    graph = nx.Graph()
    for event in transmission_events:
        node_index_one = node_indices_dict[str(event[0:3])]
        node_index_two = node_indices_dict[str(event[3:])]
        graph.add_node(node_index_one)
        graph.add_node(node_index_two)
        graph.add_edge(node_index_one, node_index_two)
    return graph


def get_transmission_network_node_indices_dict(transmission_events):
    """TODO: ..."""
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
