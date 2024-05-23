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
         	cursor(SELECT * FROM python_ser WHERE key = 'yolo_paddle'),  -- Data to infer(predict) X target data
         	cursor(SELECT * FROM python_ser WHERE key = 'yolo_paddle'),  -- Model Serialized Table Record
            'SELECT 1.0 ClusterNo, 1.0 Homogeneity, TO_CLOB(NULL) IMAGE, CAST(''A'' AS   VARCHAR2(40)) OCR FROM dual',
           'YOLOv8:predict_with_model'))
```
