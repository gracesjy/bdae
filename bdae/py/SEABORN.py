import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import os
import sys
import urllib, base64
import pandas as pd

def seaborn_plot():
   ''' Comments added '''
   tips = sns.load_dataset("tips")
    
   sns.relplot(x="total_bill", y="tip", hue="smoker", \
       style="smoker", data=tips)
        
   fig = plt.gcf()
   tmp_file = '/tmp/seaborn_plot01.png'
   fig.savefig(tmp_file)
    
   image = open(tmp_file, 'rb')
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   uri = 'data:image/png;base64,' + image_64_encode.decode()     
   total = "<html><body>\n"
   total = total +  "<img src = "
   total = total + uri
   total = total + " />\n</body></html>"
   
   os.remove(tmp_file)
   anames = []
   alist = []
   anames.append('Relplot')
   alist.append(total)
    
   plt.clf()
   sns.catplot(x="day", y="total_bill", hue="smoker",
            col="time", aspect=.6,
            kind="swarm", data=tips)
   fig = plt.gcf()
   fig.savefig(tmp_file)
   image = open(tmp_file, 'rb')
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   uri = 'data:image/png;base64,' + image_64_encode.decode()     
   total = "<html><body>\n"
   total = total +  "<img src = "
   total = total + uri
   total = total + " />\n</body></html>"
   
   anames.append('Catplot')
   alist.append(total)  
   os.remove(tmp_file)
   plt.clf()
   iris = sns.load_dataset("iris")
   sns.pairplot(iris)
   fig = plt.gcf()
   fig.savefig(tmp_file)
   image = open(tmp_file, 'rb')
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   uri = 'data:image/png;base64,' + image_64_encode.decode()     
   total = "<html><body>\n"
   total = total +  "<img src = "
   total = total + uri
   total = total + " />\n</body></html>"
   anames.append('Pairplot-1')
   alist.append(total)  
   os.remove(tmp_file)
   plt.clf()
   g = sns.PairGrid(iris)
   g.map_diag(sns.kdeplot)
   g.map_offdiag(sns.kdeplot, n_levels=6)
   fig = plt.gcf()
   fig.savefig(tmp_file)
   image = open(tmp_file, 'rb')
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   uri = 'data:image/png;base64,' + image_64_encode.decode()     
   total = "<html><body>\n"
   total = total +  "<img src = "
   total = total + uri
   total = total + " />\n</body></html>"
   anames.append('Pairplot-2')
   alist.append(total)  
   os.remove(tmp_file)
   datax ={'Names': anames, 'IMG' : alist}
   df = pd.DataFrame(datax)
   return (df)
