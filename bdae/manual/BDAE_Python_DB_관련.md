### BDAE Python

예측 관련 예제
```
SELECT *
FROM table(apTableEval(
   cursor(SELECT '/home/oracle/DeepLearning/Aquarium_Combined.v2-raw-1024.yolov8/test/images' AS DATA FROM dual),
   cursor(SELECT MODEL_NAME AS KEY, 
                 MODEL_DATA AS RAWDATA, 
                 APPLY_YN AS YN 
          FROM MODEL_SAVING_TBL
          WHERE MODEL_NAME='yolov8_aqua_model'),
   'SELECT CAST(''A'' AS VARCHAR2(120)) FileName, TO_CLOB(NULL) Image FROM dual',
   'YOLOv8:predict_aqua'))
```
YOLOv8:predict_aqua
```
import numpy as np
import pandas as pd
import matplotlib
import gc
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from matplotlib import style
import os
import sys
import urllib
import base64
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os
import subprocess
import cv2
import sys
import urllib
import base64
import pandas as pd
import _pickle as cPickle
import tempfile
import logging
from StreamToLogger import StreamToLogger
import logging, logging.handlers
   
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION']='python'

def image_to_html():
    tmp_file_name = tempfile.NamedTemporaryFile().name + '.png'
    plt.savefig(tmp_file_name)
    image = open(tmp_file_name, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)
    uri = '<img src="data:img/png;base64,' + image_64_encode.decode() + '">'
    html_str = "<html><body>" + uri + "</body></html>"
    if os.path.exists(tmp_file_name):
        os.remove(tmp_file_name)
    return html_str

def make_output(df, key, data):
    df[key] = data
    return df

def predict_aqua(df_data, df_model):
    logger = logging.getLogger('YOLOv8:predict_aqua')
    logger.setLevel(logging.DEBUG)

    socketHandler = logging.handlers.SocketHandler('localhost',
                   logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    
    logger.addHandler(socketHandler)
     
    sys.stdout = StreamToLogger(logger,logging.INFO)
    sys.stderr = StreamToLogger(logger,logging.ERROR)   
    
    print('--- columns ----'  + str(df_model.columns))
    print(str(df_model.head()))
    print(str(df_data.head()))
    
    model_binary = df_model['RAWDATA'][0]
    tmp_file_name = tempfile.NamedTemporaryFile().name + '.pt'
    print('file_name : ' + tmp_file_name)
    with open(tmp_file_name, "wb") as f:
        f.write(model_binary)
        f.close()
        
    print('before loading model')   
    model = YOLO(tmp_file_name)
    print('before test data location ....' )  
    source_data = df_data['DATA'][0]
    print('after test data location ....' + source_data )  
    results = model.predict(source=source_data, save=True)
    print('after prediction ...')
    base64_list = []
    filelist = []
    for result in results:
        filename = os.path.basename(result.path).split('/')[-1]
        fullpathfilename = os.getcwd() + '/' + result.save_dir + '/' + filename
        image = open(fullpathfilename, 'rb')
        image_read = image.read()
        image_64_encode = base64.b64encode(image_read)
        uri = '<img src="data:img/png;base64,' + image_64_encode.decode() + '">'
        total = "<html><body>" + uri + "</body></html>"
        base64_list.append(total)
        filelist.append(filename)

    print(str(filelist))
    tupleStart = {'file name': filelist, 'images': base64_list }
    pdf = pd.DataFrame(tupleStart)   
    return pdf

```
