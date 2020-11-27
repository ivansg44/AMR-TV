import json

from django.shortcuts import HttpResponse

import networkx as nx
import plotly.graph_objects as go
from plotly.offline import plot

import amr_tv.node_link_diagram.utils as utils


def node_link_diagram_view(request):
    """TODO: ..."""
    transmission_events = json.loads(request.session["transmission_events"])
    filtered_transmission_events = \
        utils.filter_transmission_events(request.GET, transmission_events)
    graph = utils.get_transmission_network(filtered_transmission_events)
    positions = nx.spring_layout(graph)

    color_map = utils.get_node_color_map(request.GET)
    node_trace = utils.get_node_trace(graph, positions, color_map)

    graph_layout = utils.get_graph_layout(graph, positions)

    fig = go.Figure(data=[node_trace], layout=graph_layout)
    plot_div = plot(fig, output_type="div")

    return HttpResponse(plot_div)
