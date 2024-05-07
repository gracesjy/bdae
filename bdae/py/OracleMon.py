import pandas as pd           
import matplotlib.pyplot as plt  
import numpy as np        
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import urllib, base64                        

def make_mon(df):
    pdf = df.pivot(index='SAMPLE_TIME', columns='WAITCLASS', values='DB_TIME')
    pdf.plot(kind='area', stacked=True, title='DB Time over the last hour',
             color=['red', 'green', 'orange', 'darkred', 'brown', 'brown', 'pink',
                    'lightgreen', 'cyan', 'blue'])

    plt.title("Oracle Database Monitoring Example")
    plt.savefig("/tmp/oracle_mon.png")

    image = open('/tmp/oracle_mon.png', 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)

    uri = '<img src="data:img/png;base64,' + image_64_encode.decode() + '">'
    total = "<html><body>" + uri + "</body></html>"

    list_cols = ['data']
    list_data = [total]
    datax = {'Python Fig': list_cols, 'data': list_data}
    df_ret = pd.DataFrame(datax)
    return (df_ret)
