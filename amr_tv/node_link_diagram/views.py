import json

from django.shortcuts import HttpResponse

import networkx as nx
import plotly.graph_objects as go
from plotly.offline import plot

import amr_tv.node_link_diagram.utils as utils


def node_link_diagram_view(request):
    """TODO: ..."""
    transmission_events = json.loads(request.session["transmission_events"])
    selected_events = json.loads(request.GET["selected_events"])
    filtered_transmission_events = \
        utils.filter_transmission_events(selected_events, transmission_events)
    graph = utils.get_transmission_network(filtered_transmission_events)
    positions = nx.spring_layout(graph)

    color_map = utils.get_node_color_map(selected_events)
    node_traces = utils.get_node_traces(graph, positions, color_map)

    graph_layout = utils.get_graph_layout(graph, positions)

    fig = go.Figure(data=node_traces, layout=graph_layout)
    plot_div = plot(fig, output_type="div")

    return HttpResponse(plot_div)
