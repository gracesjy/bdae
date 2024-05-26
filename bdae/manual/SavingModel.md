## Saving Model

Just Example ...

```
import pandas as pd
import logging

def serialize(df):
   logger.info(df['FILENAME'][0])
   f = open(df['FILENAME'][0], mode="rb")
   data = f.read()
   pdf = pd.DataFrame(data={'KEY': ['yolo_license_plate'], 'RAWDATA' : [data], 'YN': ['for test'] })
   return (pdf)
```

SQL to run
```
SELECT *
FROM table(apEval(
   cursor(SELECT '/tmp/yolo_license_plate.pt' FILENAME FROM dual),
   'PYTHON_SER',
   'MODEL_SERIAL:serialize'))
```

Insert into PYTHON_SER table ..
```
INSERT INTO PYTHON_SER
SELECT *
FROM table(apEval(
   cursor(SELECT '/tmp/yolo_license_plate.pt' FILENAME FROM dual),
   'PYTHON_SER',
   'MODEL_SERIAL:serialize'))
   ;
```


