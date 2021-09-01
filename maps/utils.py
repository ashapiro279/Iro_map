from io import BytesIO
import matplotlib.pyplot as plt
import base64
import plotly.express as px
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(df, cat):
    plt.switch_backend('AGG')
    plt.figure(figsize=(12,5))
    fig = plt.figure()
    fig.patch.set_facecolor('purple')
    plt.title(cat)
    plt.plot(df['datetime'], df[cat])
    graph = get_graph
    return graph


def get_plotly_graph(df):
    return (plot(px.line(df, x='datetime', y=key, title=f'Showing data for {key}'),
                output_type='div') for key in df.keys() if key != 'datetime')