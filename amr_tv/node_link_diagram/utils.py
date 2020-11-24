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
    graph = nx.Graph()
    count = 1
    for event in transmission_events:
        graph.add_node(count)
        graph.add_node(count + 1)
        graph.add_edge(count, count + 1)
        count += 2
    return graph
