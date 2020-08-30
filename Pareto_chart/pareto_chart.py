#Import libraries
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.tools import make_subplots

#Load sample data
data = pd.read_csv('sample_data.csv', index_col = 0, header = None, 
                   names = ['X'],
                   squeeze = True)

#Define Pareto chart function 
# For this function, we assume the data is passed as a pandas Series in which
# the index are the x-axis labels and the values are the total amounts for each
# label
def pareto(data, data_label):
    
    x_vals = data.value_counts().sort_index().index
    y_vals = data.value_counts().sort_index().values
    fig = make_subplots(rows = 1, 
                        cols = 1, 
                        print_grid = True, 
                        specs = [[{'secondary_y': True}]])
   
    #Bar trace
    fig.add_trace(go.Bar(x = x_vals, y = y_vals, name = data_label,
                         marker_color = 'rgb(100,150,250)',
                         hovertemplate = 'Category: %{x}' +
                                         '<br>Value: %{y}'
                         ), 
                  row = 1, 
                  col = 1, 
                  secondary_y = False)
    
    #Cumulative line trace
    fig.add_trace(go.Scatter(x = x_vals,
                             y = [100 * sum(y_vals[:i]) / sum(y_vals) 
                                  for i in range(len(y_vals))][1:] + [100],
                             mode = 'lines+markers',
                             name = 'Cumulative of ' + data_label,
                             marker = {'color': 'rgb(250,50,50)'},
                             hovertemplate = '%{y: 2.2f}%'
                             ), 
                  row = 1, 
                  col = 1, 
                  secondary_y = True)
   
    #80% line shape
    x_range = [min(x_vals) - 1, np.quantile(x_vals, 0.75)]
    y_range = [0, 1.1 * max(y_vals)]
    y_position = 0.8 * (y_range[1] - y_range[0])
    fig.add_shape(type = 'line',
                  x0 = x_range[0], y0 = y_position,
                  x1 = x_range[1], y1 = y_position,
                  line = {'width': 0.5,
                          'color': 'black',
                          'dash': 'dot'})

    fig.update_xaxes(range= x_range,
                     linecolor = 'black',
                     linewidth = 1,
                     mirror = True)
    fig.update_yaxes(range= y_range,
                     title= 'Amount', secondary_y=False,
                     showgrid = False, 
                     linecolor = 'black',
                     linewidth = 1)
    fig.update_yaxes(range = [0, 100],
                     showgrid = True,
                     title = 'Cumulative percentage',
                     secondary_y=True,
                     linecolor = 'black',
                     linewidth = 1);
    fig.update_layout(plot_bgcolor = 'white',
                      title = 'Pareto Chart Example',
                      width = 1000)
   
    return pyo.plot(fig)

#Create sample plot
pareto(data, 'Example')