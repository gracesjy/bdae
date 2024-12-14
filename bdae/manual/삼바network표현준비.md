### 네트워크 다이어그램으로 표현하는 연습 준비

```
import pandas as pd
filename = r'G:\DeepLearning\networkx.xlsx'
df = pd.read_excel(filename, 'Sheet2')

import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly
big = ['Ignite','General','Storage']


G = nx.Graph()
for _, row in df.iterrows():
  G.add_edge(row['Step'], row['Parameters'], label=row['Relation'])

pos = nx.fruchterman_reingold_layout(G, k=0.5)

edge_traces = []
for edge in G.edges():
    print('print edge : ' + str(edge))
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
text_node1 = []

x2 = []
y2 = []
text_node2 = []
for node in G.nodes:
    print(node)
    if node in big:
        text_node1.append(node)
        if pos[node][0] not in x1:
            x1.append(pos[node][0])
        if pos[node][1] not in y1:
            y1.append(pos[node][1])
    else:
        text_node2.append(node)
        if pos[node][0] not in x2:
            x2.append(pos[node][0])
        if pos[node][1] not in y2:
            y2.append(pos[node][1])
    

x = [pos[node][0] for node in G.nodes()]
y = [pos[node][1] for node in G.nodes()]
print('x : ' + str(x))
print('x1 : ' + str(x1))
print('x2 : ' + str(x2))

print('y : ' + str(y))
print('y1 : ' + str(y1))
print('y2 : ' + str(y2))

node_trace = go.Scatter(
    #x=[pos[node][0] for node in G.nodes()],
    #y=[pos[node][1] for node in G.nodes()],
    x = x2,
    y = y2,
    mode='markers+text',
    marker=dict(size=10, color='lightblue'),
    #text=[node for node in G.nodes()],
    text=text_node2,
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
    #text=[node for node in G.nodes()],
    text=text_node1,
    textposition='top center',
    hoverinfo='text',
    textfont=dict(size=14) #
)

# Create edge label trace

label_x1 = []
label_y1 = []
label_x2 = []
label_y2 = []

label_text1= []
label_text2 = []


for edge in G.edges():
    xx = G[edge[0]][edge[1]]['label']
    print('label : ' + str(xx))
    val = float(xx)
    if val >= 0.2:
        label_x1.append((pos[edge[0]][0] + pos[edge[1]][0]) / 2)
        label_y1.append((pos[edge[0]][1] + pos[edge[1]][1]) / 2)
        label_text1.append(xx)
    else:
        label_x2.append((pos[edge[0]][0] + pos[edge[1]][0]) / 2)
        label_y2.append((pos[edge[0]][1] + pos[edge[1]][1]) / 2)
        label_text2.append(xx)
    
    
edge_label_trace = go.Scatter(
    #x=[(pos[edge[0]][0] + pos[edge[1]][0]) / 2 for edge in G.edges()],
    #y=[(pos[edge[0]][1] + pos[edge[1]][1]) / 2 for edge in G.edges()],
    x = label_x1,
    y = label_y1,
    mode='text',
    #text=[G[edge[0]][edge[1]]['label'] for edge in G.edges()],
    text = label_text1,
    textposition='middle center',
    hoverinfo='none',
    textfont=dict(size=10, color='red')
)

edge_label_trace2 = go.Scatter(
    #x=[(pos[edge[0]][0] + pos[edge[1]][0]) / 2 for edge in G.edges()],
    #y=[(pos[edge[0]][1] + pos[edge[1]][1]) / 2 for edge in G.edges()],
    x = label_x2,
    y = label_y2,
    mode='text',
    #text=[G[edge[0]][edge[1]]['label'] for edge in G.edges()],
    text=label_text2,
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
#fig = go.Figure(data=edge_traces + [node_trace, edge_label_trace], layout=layout)
print('node_trace : ' + str(node_trace))

fig = go.Figure(data=edge_traces + [node_trace, node_trace2, edge_label_trace,edge_label_trace2], layout=layout)
# Show the interactive plot
fig.show()

```
