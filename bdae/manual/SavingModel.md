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
