from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
import random
from matplotlib import style
import os
import sys
import urllib
import base64
import pandas as pd
import _pickle as cPickle
import tempfile

def display(df):
   # Raw Data from Database's Table (BLOB)
   # y_train, y_train_pred compressed by cPickle.dumps, inserted into BLOB columns
   
   y_train_data = df['Y']
   y_train_pred_data = df['Y_PRED']

   # uncompressed ..
   y_train = cPickle.loads(y_train_data[0])
   y_train_pred = cPickle.loads(y_train_pred_data[0])

   # Output - ConfusionMatrix
   fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
   plt.rc('font', size=9)
   ConfusionMatrixDisplay.from_predictions(y_train, y_train_pred, ax=axs[0])
   axs[0].set_title("Confusion matrix")
   plt.rc('font', size=10)
   ConfusionMatrixDisplay.from_predictions(y_train, y_train_pred, ax=axs[1],
                                        normalize="true", values_format=".0%")
   axs[1].set_title("CM normalized by row")

   tmp_file_name = tempfile.NamedTemporaryFile().name + '.png'
   plt.savefig(tmp_file_name)
   image = open(tmp_file_name, 'rb')
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   uri = '<img src="data:img/png;base64,' + image_64_encode.decode() + '">'
   html_str = "<html><body>" + uri + "</body></html>"
   datax ={'IMG' : [html_str]}
   pdf = pd.DataFrame(datax)

   if os.path.exists(tmp_file_name):
      os.remove(tmp_file_name)
   return pdf
