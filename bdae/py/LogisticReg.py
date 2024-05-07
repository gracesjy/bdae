import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from matplotlib import style
import os
import sys
import urllib, base64


def logisticReg():

   cancer = load_breast_cancer()
   df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
   df['class'] = cancer.target
   sns.pairplot(df[['class'] + list(df.columns[:10])])
   
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

   sns.pairplot(df[['class'] + list(df.columns[20:30])])
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
   
   datax ={'Names': anames, 'IMG' : alist}
   df = pd.DataFrame(datax)
   return (df)
