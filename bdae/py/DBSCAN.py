import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib
import gc
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from matplotlib import style
import os
import sys
import urllib
import base64

def dbscan():
   centers = [[1, 1], [-1, -1], [1, -1]]
   X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                    random_state=0)

   X = StandardScaler().fit_transform(X)

   db = DBSCAN(eps=0.3, min_samples=10).fit(X)
   core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
   core_samples_mask[db.core_sample_indices_] = True
   labels = db.labels_

   n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


   unique_labels = set(labels)
   colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
   for k, col in zip(unique_labels, colors):
       if k == -1:
           col = [0, 0, 0, 1]
       class_member_mask = (labels == k)
       xy = X[class_member_mask & core_samples_mask]
       plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                markeredgecolor='k', markersize=14)

       xy = X[class_member_mask & ~core_samples_mask]
       plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                markeredgecolor='k', markersize=6)

   plt.title('Estimated number of clusters: %d' % n_clusters_)
   plt.savefig('/tmp/kmeans.png')

   image = open('/tmp/kmeans.png', 'rb')
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   print(type(image_64_encode))

   uri = '<img src="data:img/png;base64,' + image_64_encode.decode() + '">'
   total = "<html><body>" + uri + "</body></html>"

   f = open("/tmp/james02.html", "w")
   f.write(total)
   f.close()
   list_data1 = [n_clusters_]
   list_data2 = [metrics.homogeneity_score(labels_true, labels)]
   list_data3 = [total]

   datax ={'Estimate No. Clusters': list_data1, 'Homogeneity': list_data2, 'IMG' : list_data3}
   pdf = pd.DataFrame(datax)
   del X
   del db
   del image_64_encode
   del uri
   gc.collect()
   return (pdf)
