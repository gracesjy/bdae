## ${\textsf{\color{magenta}Model UnSerialize : BLOB Column}}$

This is a method of training a model, saving it as a file in a specific table, 
and reading it in real time to use it for inference.


BDAE can pass two pandas DataFrames as shown below. 
The first DataFrame (df_test_data) is Target Data to infer (predict),
and the second DataFrame is standard (reference) information. 
It conveys the model information stored at that level.

```
def doInference(df_test_data, df_model):
```

It will be easier to understand if you look at the corresponding SQL statement.
```
SELECT * 
  FROM table(apTableEval(
     cursor(SELECT '/home/oracle/yolo/car_2.jpg' AS DATA FROM dual),  -- matches df_test_data
     cursor(select * from python_ser where key = 'yolo_paddle'),      -- matches df_model
     'SELECT 1.0 ClusterNo, 1.0 Homogeneity, TO_CLOB(NULL) IMAGE, CAST(''A'' AS   VARCHAR2(40)) OCR FROM dual',
     'A-Model:doInference'))
```


Be careful because BDAE changes column names to all uppercase letters.

```
def doInference(df_test_data, df_model):
   # Model Binary stored Column - RAWDATA of Table (eg.)
   model_binary = df_model['RAWDATA'].values

   ...
   # target data to infer (predict)
   ... df_data['DATA'][0]

```
   
