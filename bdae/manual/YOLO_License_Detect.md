## YOLO + Paddle

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
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION']='python'
from paddleocr import PaddleOCR
import logging
import tempfile
import io
from StreamToLogger import StreamToLogger
import logging, logging.handlers

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


def predict_with_model(df_data, df_model):
    
    logger = logging.getLogger('ArrayPreprocessing:describe')
    logger.setLevel(logging.DEBUG)
    
    socketHandler = logging.handlers.SocketHandler('localhost',
                   logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    
    logger.addHandler(socketHandler)
    
    sys.stdout = StreamToLogger(logger,logging.INFO)
    sys.stderr = StreamToLogger(logger,logging.ERROR)
    
    print('----- YOLOv8:predict_with_model ------')
    logger.info('--- Normal Logging Info -----')
    logger.error('--- Error Logging Test -----')
    model_binary = df_model['RAWDATA'][0]
    
    tmp_file_name = tempfile.NamedTemporaryFile().name + '.pt'
    with open(tmp_file_name, "wb") as f:
        #f.write(model_binary[0])
        f.write(model_binary)
        f.close()
    
    model = YOLO(tmp_file_name)
    if os.path.exists(tmp_file_name):
        os.remove(tmp_file_name)
    
    img_f = cv2.imread(df_data['DATA'][0])
    img = cv2.cvtColor(img_f, cv2.COLOR_BGR2RGB)
    results = model.predict(img, save=False, conf=0.5)
    color1 = (155, 200, 230)
    img_crop = None
    for result in results:
        boxes = result.boxes.cpu().numpy()  # Get boxes on CPU in numpy format
        for box in boxes:
            r = box.xyxy[0].astype(int)
            class_id = int(box.cls[0])  # Get class ID
            class_name = model.names[class_id]  # Get class name using the class ID
            cv2.rectangle(img, r[:2], r[2:], (255, 0, 0), 5)  # Draw boxes on the image
            cv2.putText(img, class_name, (r[0], r[1]), 1, 2, color1, 2, cv2.LINE_AA)
            img_crop = img[r[:2], r[2:]].copy()
    plt.imshow(img)
    
    img2html_org = image_to_html()

    img_crop =  img[r[1]:r[3], r[0]:r[2]].copy()  
    ocr = PaddleOCR(lang="korean")
    result = ocr.ocr(img_crop, cls=False)
    ocr_result = result[0]
    license_ocr = ''

    color = (255, 0, 0)
    license_x = ''

    box_data = []
    license_data = []
    min_x = 9999999
    max_x = 0
    min_y = 9999999
    max_y = 0

    min_x_for_order = 999999

    for rectObj in ocr_result:
        for rect in rectObj:
            if isinstance(rect, list):
                for xx in rect:
                    x = xx[0]
                    y = xx[1]
                    if max_x < x:
                        max_x = x
                    if max_y < y:
                        max_y = y
                    if min_x > x:
                        min_x = x
                    if min_y > y:
                        min_y = y

                pt1 = (int(min_x), int(min_y))
                pt2 = (int(max_x), int(max_y))

                if min_x_for_order > min_x:
                    min_x_for_order = min_x
                
                box_data.append(min_x_for_order)
                min_x = 9999999
                max_x = 0
                min_y = 9999999
                max_y = 0
                cv2.rectangle(img_crop, pt1, pt2, color, 5)

            if isinstance(rect, tuple):
                license_x = license_x + rect[0] 
                license_data.append(rect)

    np_arr = np.array(box_data)
    indexes = np.argsort(np_arr).tolist()
    license_ocr = ''
    for i in range(len(indexes)):
        license_ocr = license_ocr + license_data[indexes[i]][0]

    plt.imshow(img_crop)
    img2html_final = image_to_html()
    color1 = (155, 200, 230)
    #list_data1 = [df_model['KEY'][0]]
    #list_data2 = [total]
    #list_data3 = [license_x]
    dataDict ={'Model': [df_model['KEY'][0]], 'IMG' : [img2html_org], 'IMG2': [img2html_final], 'OCR': [license_ocr]}
    pdf = pd.DataFrame(dataDict)

    return (pdf)

```

SQL
```
SELECT * 
      FROM table(apTableEval(
            cursor(SELECT '/home/oracle/Downloads/20240428_175815.jpg' AS DATA FROM dual),
         	cursor(select * from python_ser where key = 'yolo_license_plate'),
            'SELECT CAST(''A'' AS VARCHAR2(40)) MODEL_TYPE, TO_CLOB(NULL) YOLO_Detect_Object, 
                     TO_CLOB(NULL) PADDLE_OCR,
                   CAST(''A'' AS   VARCHAR2(40)) OCR FROM dual',
           'YOLOv8:predict_with_model'))
```
