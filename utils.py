import json
import plotly
import plotly.express as px

"""
Fichier contenant des fonctions utiles au projet
"""


def create_graph(data, title, xaxis_title, yaxis_title, legend_title):
    figure = px.bar(data)
    figure.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title
    )
    graph = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
    return graph
