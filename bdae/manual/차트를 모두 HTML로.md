### 차트를 모두 HTML

```
import plotly.express as px

def figures_to_html(figs, filename="dashboard.html"):
    with open(filename, 'w',encoding='utf-8') as dashboard:
        dashboard.write("<html><head></head><body>" + "\n")
        for fig in figs:
            inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
            dashboard.write(inner_html)
        dashboard.write("</body></html>" + "\n")

import plotly.express as px
df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig1 = px.pie(df, values='pop', names='country', title='Population of European continent')

import plotly.express as px
df = px.data.tips()
fig2 = px.box(df, y="total_bill")
fig2.show()

figs = [fig1,fig2]
figures_to_html(figs, 'atlas.html')
```

### 테이블을 이동 가능하게
```
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
               fill_color='lavender',
               align='left'))
])

fig.show()
```
