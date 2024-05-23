## How to infer(predict) with stored model information

for example, make your table like

```
Table Name : PYTHON_SER 
Name    Null? Type         
------- ----- ------------ 
KEY           VARCHAR2(40) 
RAWDATA       BLOB          ....... Model Binary Data   
YN            VARCHAR2(40)
------- ----- ------------ 
```

SQL
```
SELECT * 
      FROM table(apTableEval(
         	cursor(SELECT '/home/oracle/yolo/car_2.jpg' AS DATA
                   FROM dual), -- Data to infer(predict) X target data

         	cursor(SELECT * FROM python_ser WHERE key = 'yolo_paddle'),  -- Model Serialized Table Record

            'SELECT 1.0 ClusterNo, 1.0 Homogeneity, TO_CLOB(NULL) IMAGE, CAST(''A'' AS   VARCHAR2(40)) OCR FROM dual',
            'YOLOv8:predict_with_model') -- Python Module and Function
          )
```

Python Module

```
def predict_with_model(df_data, df_model):
   
   model_binary = df_model['RAWDATA'].values
   fh.close()
   logger.removeHandler(fh)
   
   #logging.info('type : {}'.format(str(type(model_binary)))
   with open("/home/oracle/yolo/yolo_paddle_test.pt", "wb") as f:
      f.write(model_binary[0])
      f.close()
      
      
   os.chdir('/home/oracle/yolo')
   model = YOLO('yolo_paddle_test.pt')
   img = cv2.imread(df_data['DATA'])
   results = model.predict(img, save=False, conf=0.5)
   color1 = (155, 200, 230)
   img_crop = None
   for result in results:
      boxes = result.boxes.cpu().numpy()  # Get boxes on CPU in numpy format
      for box in boxes:
         r = box.xyxy[0].astype(int)
         class_id = int(box.cls[0])  # Get class ID
         class_name = model.names[class_id]  # Get class name using the class ID
         cv2.rectangle(img, r[:2], r[2:], (0, 255, 0), 2)  # Draw boxes on the image
         cv2.putText(img, class_name, (r[0], r[1]), 1, 2, color1, 2, cv2.LINE_AA)
         img_crop = img[r[:2], r[2:]].copy()
   plt.imshow(img)
   plt.savefig('/tmp/result.png')
   img_crop =  img[r[1]:r[3], r[0]:r[2]].copy()  
   ocr = PaddleOCR(lang="korean")
   result = ocr.ocr(img_crop, cls=False)
   ocr_result = result[0]
   license_x = ''
   for rectObj in ocr_result:
      for rect in rectObj:
         if isinstance(rect, list):
            pt1 = tuple([int(s) for s in rect[0]])
            pt2 = (int(rect[1][0]), int(rect[3][1]))
         if isinstance(rect, tuple):
            license_x = license_x + rect[0]
            
   image = open('/tmp/result.png', 'rb')
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   print(type(image_64_encode))

   uri = '<img src="data:img/png;base64,' + image_64_encode.decode() + '">'
   total = "<html><body>" + uri + "</body></html>"

   color1 = (155, 200, 230)
   list_data1 = [1]
   list_data2 = [2]
   list_data3 = [total]
   list_data4 = [license_x]
   #list_data4 = [license_x]
   datax ={'Estimate No. Clusters': list_data1, 'Homogeneity': list_data2, 'IMG' : list_data3, 'OCR': list_data4}
   pdf = pd.DataFrame(datax)
   return (pdf)
```

Result

![ModelUnSerialize.png](../../images/ModelUnSerialize.png)
