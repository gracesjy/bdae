## SPC PLOTLY ...
This is not my codes, Others does.
I just tested with BDAE.

```
import os
import sys
import urllib
import base64
import pandas as pd
import plotly.express as px
import plotly.offline as py

from plotly.graph_objs import *


def basic():
    trace1 = {
      "uid": "cb8982", 
      "line": {
        "color": "rgb(0,116,217)", 
        "width": 2
      }, 
      "mode": "lines+markers", 
      "name": "Data", 
      "type": "scatter", 
      "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36], 
      "y": [-0.2625, -0.2925, -0.1425, -0.0875, -0.01, -0.045, -0.04, -0.0075, -0.0025, -0.1875, -0.21, -0.1725, -0.2025, -0.125, -0.14, -0.065, 0.0325, -0.13, -0.0925, 0.0825, 0.235, -0.0125, 0.065, 0.065, 0.215, 0.0975, 0.085, -0.235, -0.205, -0.27, -0.205, -0.1875, -0.1725, -0.185, -0.195, -0.105], 
      "xaxis": "x", 
      "yaxis": "y", 
      "marker": {
        "size": 8, 
        "color": "rgb(0,116,217)", 
        "symbol": "circle"
      }, 
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(0,116,217)", 
        "width": 1, 
        "thickness": 1
      }, 
      "visible": True, 
      "showlegend": True
    }
    trace2 = {
      "uid": "d7228d", 
      "line": {
        "color": "rgb(255,65,54)", 
        "width": 2
      }, 
      "mode": "markers", 
      "name": "Violation", 
      "type": "scatter", 
      #"x": [2, 21, 23, 24, 25, 26, 27], 
      "x": [2, 21, 25], 
      #"y": [-0.2925, 0.235, 0.065, 0.065, 0.215, 0.0975, 0.085], 
      "y": [-0.2925, 0.235, 0.215], 
      "xaxis": "x", 
      "yaxis": "y", 
      "marker": {
        "line": {"width": 3}, 
        "size": 12, 
        "color": "rgb(255,65,54)", 
        "symbol": "circle-open", 
        "opacity": 0.5
      }, 
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(255,65,54)", 
        "width": 1, 
        "thickness": 1
      }, 
      "visible": True, 
      "showlegend": True
    }
    trace3 = {
      "uid": "135942", 
      "line": {
        "color": "rgb(133,20,75)", 
        "width": 2
      }, 
      "mode": "lines", 
      "name": "Center", 
      "type": "scatter", 
      "x": [0.5, 36.5], 
      "y": [-0.086389, -0.086389], 
      "xaxis": "x", 
      "yaxis": "y", 
      "marker": {
        "size": 8, 
        "color": "rgb(133,20,75)", 
        "symbol": "circle"
      }, 
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(133,20,75)", 
        "width": 1, 
        "thickness": 1
      }, 
      "visible": True, 
      "showlegend": True
    }
    trace4 = {
      "uid": "df651f", 
      "line": {
        "color": "rgb(255,133,27)", 
        "width": 2
      }, 
      "mode": "lines", 
      "name": "LCL/UCL", 
      "type": "scatter", 
      "x": [0.5, 36.5, None, 0.5, 36.5], 
      "y": [-0.281712, -0.281712, None, 0.108934, 0.108934], 
      "xaxis": "x", 
      "yaxis": "y", 
      "marker": {
        "size": 8, 
        "color": "rgb(255,133,27)", 
        "symbol": "circle"
      }, 
      "error_x": {"copy_ystyle": True}, 
      "error_y": {
        "color": "rgb(255,133,27)", 
        "width": 1, 
        "thickness": 1
      }, 
      "visible": True, 
      "showlegend": True
    }
    data = Data([trace1, trace2, trace3, trace4])
    layout = {
      "title": "SPC Control Chart", 
      "width": 1600, 
      "xaxis": {
        "side": "bottom", 
        "type": "linear", 
        "range": [0.7986541837537402, 36.35240181528135], 
        "ticks": "inside", 
        "title": "Time (minutes)", 
        "anchor": "y", 
        "domain": [0.13, 0.746044], 
        "mirror": "allticks", 
        "showgrid": False, 
        "showline": True, 
        "zeroline": False, 
        "autorange": False, 
        "linecolor": "rgb(34,34,34)", 
        "linewidth": 1
      }, 
      "yaxis": {
        "side": "left", 
        "type": "linear", 
        "range": [-0.32885982596345953, 0.27135982596345953], 
        "ticks": "inside", 
        "title": "Deviation", 
        "anchor": "x", 
        "domain": [0.11, 0.925], 
        "mirror": "allticks", 
        "showgrid": False, 
        "showline": True, 
        "zeroline": False, 
        "autorange": True, 
        "linecolor": "rgb(34,34,34)", 
        "linewidth": 1
      }, 
      "height": 930, 
      "legend": {
        "x": 0.19141689373297002, 
        "y": 0.7684964200477327, 
        "xref": "paper", 
        "yref": "paper", 
        "bgcolor": "rgba(255, 255, 255, 0.5)", 
        "xanchor": "left", 
        "yanchor": "bottom"
      }, 
      "margin": {
        "b": 0, 
        "l": 0, 
        "r": 0, 
        "t": 60, 
        "pad": 0, 
        "autoexpand": True
      }, 
      "autosize": True, 
      "showlegend": True, 
      "annotations": [
        {
          "x": 0.438022, 
          "y": 0.935, 
          "text": "", 
          "xref": "paper", 
          "yref": "paper", 
          "align": "center", 
          "xanchor": "center", 
          "yanchor": "bottom", 
          "showarrow": False
        }
      ], 
      "plot_bgcolor": "white", 
      "paper_bgcolor": "white"
    }
    fig = Figure(data=data, layout=layout)
    total = py.offline.plot(fig, output_type='div')
    return total
```

SQL
```
SELECT *
FROM table(apEval(
   NULL,
   'XML',
   'SPC_Chart:basic'))
```

