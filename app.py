# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objs as go
import plotly
import pandas as pd
from data_fetch import DataFetch
from dash.dependencies import Input, Output
import datetime

app = Dash(__name__)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# data = DataFetch('basement_pi_sensor_002', 100)
# fig2 = go.Figure(data=[go.Scatter(
#         x=data.return_data('time'), 
#         y=data.return_data('temperature')
#     )])

# dcc.Graph(figure=fig2)

app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 10000,
            n_intervals = 0
        ),
    ]
)
  
@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)
  
def update_graph_scatter(n):
    data = DataFetch('basement_pi_sensor_002', 50)
    x=data.return_data('time')
    y=data.return_data('temperature')
    
  
    data = plotly.graph_objs.Scatter(
            x=x,
            y=y,
            name='Scatter',
            mode= 'lines+markers'
    )

    date_time_obj = datetime.datetime.strptime(max(x), '%Y-%m-%d %H:%M:%S.%f')
    new_time = date_time_obj + datetime.timedelta(seconds=10)
    new_time = new_time.strftime('%Y-%m-%d %H:%M:%S.%f')
  
    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(x),new_time]),yaxis = dict(range = [32,33]),)}
    
    # fig2 = go.Figure(data=[go.Scatter(
    #     x=x, 
    #     y=y
    # )])

    # return fig2

if __name__ == '__main__':
    app.run_server(debug=True)
	
