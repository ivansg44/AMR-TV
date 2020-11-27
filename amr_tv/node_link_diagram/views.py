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
    G = utils.get_transmission_network(filtered_transmission_events)
    pos = nx.spring_layout(G)

    node_trace = \
        utils.get_node_trace(G, pos, request.session["node_color_map"])

    edges = []
    for edge in G.edges():
        edges.append((edge[0], edge[1]))

    # Plotly does not support built-in arrows for some idiotic reason.
    # Here's a hackey solution from:
    # https://stackoverflow.com/questions/57482878/
    # plotting-a-directed-graph-with-dash-through-matplotlib
    x_axis = dict(showline=False, zeroline=False, showgrid=False,
                  showticklabels=False,
                  mirror='allticks', ticks='inside', ticklen=5,
                  tickfont=dict(size=14),
                  title='')

    y_axis = dict(showline=False, zeroline=False, showgrid=False,
                  showticklabels=False,
                  mirror='allticks', ticks='inside', ticklen=5,
                  tickfont=dict(size=14),
                  title='')
    annotations = [
        dict(showarrow=True, arrowsize=2, arrowwidth=1, arrowhead=1,
             standoff=3, startstandoff=1,
             ax=pos[arrow[0]][0], ay=pos[arrow[0]][1], axref='x', ayref='y',
             x=pos[arrow[1]][0], y=pos[arrow[1]][1], xref='x', yref='y'
             ) for arrow in edges]
    layout = dict(width=800, height=600,
                  showlegend=False,
                  xaxis=x_axis,
                  yaxis=y_axis,
                  hovermode='closest',
                  plot_bgcolor='#E5ECF6',
                  annotations=annotations,  # arrows
                  )

    fig = go.Figure(data=[node_trace], layout=layout)

    plot_div = plot(fig, output_type="div")
    return HttpResponse(plot_div)
