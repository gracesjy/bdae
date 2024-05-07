import os
import sys
import urllib
import base64
import pandas as pd
import plotly.express as px
import plotly.offline as py

def make_plot(df):
   dfx = df.query("CONTINENT == 'Europe'")

   dfx.loc[dfx['POP'] < 2.e6, 'COUNTRY'] = 'Other countries' # Represent only large countries
   fig = px.pie(df, values='POP', names='COUNTRY', title='Population of European continent')
   total = py.offline.plot(fig, output_type='div')
   f = open('/tmp/python_plotly.txt','w',encoding='utf8')
   f.write(total)
   f.close()
   return (total)
