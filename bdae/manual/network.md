### network

```
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly

# Define the heads, relations, and tails
head = ['E2BC01','E2BC02','E2BC03', 'E2BC01-1']
relation = ['0.56', '0.67', '0.36', '1.0']
tail = ['E2BC01-1', 'E2BC02-1','E2BC03-1', 'E2BC01-1-1']

big = ['E2BC01','E2BC02']

# Create a dataframe
df = pd.DataFrame({'head': head, 'relation': relation, 'tail': tail})

# Create a graph
G = nx.Graph()
for _, row in df.iterrows():
  G.add_edge(row['head'], row['tail'], label=row['relation'])

pos = nx.fruchterman_reingold_layout(G, k=0.5)
edge_traces = []
for edge in G.edges():
    print(edge)
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace = go.Scatter(
        x=[x0, x1, None],
        y=[y0, y1, None],
        mode='lines',
        line=dict(width=0.5, color='gray'),
        hoverinfo='none'
     )
    edge_traces.append(edge_trace)

# Create node trace
x1 = []
y1 = []

x2 = []
y2 = []
for node in G.nodes:
    print(node)
    if node in big:
        if pos[node][0] not in x1:
            x1.append(pos[node][0])
        if pos[node][1] not in y1:
            y1.append(pos[node][1])
    else:
        x2.append(pos[node][0])
        y2.append(pos[node][1])
    


node_trace = go.Scatter(
    x=[pos[node][0] for node in G.nodes()],
    y=[pos[node][1] for node in G.nodes()],
    #x = x2,
    #y = y2,
    mode='markers+text',
    marker=dict(size=10, color='lightblue'),
    text=[node for node in G.nodes()],
    textposition='top center',
    hoverinfo='text',
    textfont=dict(size=10) #
)

node_trace2 = go.Scatter(
    #x=[pos[node][0] for node in G.nodes()],
    #y=[pos[node][1] for node in G.nodes()],
    x = x1,
    y = y1,
    mode='markers+text',
    marker=dict(size=10, color='blue'),
    text=[node for node in G.nodes()],
    textposition='top center',
    hoverinfo='text',
    textfont=dict(size=14) #
)

# Create edge label trace
edge_label_trace = go.Scatter(
    x=[(pos[edge[0]][0] + pos[edge[1]][0]) / 2 for edge in G.edges()],
    y=[(pos[edge[0]][1] + pos[edge[1]][1]) / 2 for edge in G.edges()],
    mode='text',
    text=[G[edge[0]][edge[1]]['label'] for edge in G.edges()],
    textposition='middle center',
    hoverinfo='none',
    textfont=dict(size=7)
)

# Create layout
layout = go.Layout(
    title='Knowledge Graph',
    titlefont_size=16,
    title_x=0.5,
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20, l=5, r=5, t=40),
    xaxis_visible=False,
    yaxis_visible=False
)

# Create Plotly figure
fig = go.Figure(data=edge_traces + [node_trace, edge_label_trace], layout=layout)

# Show the interactive plot
fig.show()
fig.write_html('G:/atlas.html')
```
