import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

from django.shortcuts import HttpResponse


def node_detail_table_view(request):
    """TODO: ..."""
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
                   fill_color='lavender',
                   align='left'))
    ])

    plot_div = plot(fig, output_type="div")

    return HttpResponse(plot_div)
