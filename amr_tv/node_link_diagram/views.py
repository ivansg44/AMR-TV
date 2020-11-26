import json

from django.shortcuts import HttpResponse

import networkx as nx
import plotly.graph_objects as go
from plotly.offline import plot

import amr_tv.node_link_diagram.utils as utils


def node_link_diagram_view(request):
    """wip"""
    transmission_events = json.loads(request.session["transmission_events"])
    filtered_transmission_events = \
        utils.filter_transmission_events(request.GET, transmission_events)
    G = utils.get_transmission_network(filtered_transmission_events)
    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        organism_group = G.nodes[node]["organism_group"]
        min_date = G.nodes[node]["min_date"]
        node_text_vals = (organism_group, min_date)
        node_text.append("organism_group: %s, min_date: %s" % node_text_vals)

    node_trace = go.Scatter(
        x=node_x, y=node_y, text=node_text,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace])

    plot_div = plot(fig, output_type="div")
    return HttpResponse(plot_div)
