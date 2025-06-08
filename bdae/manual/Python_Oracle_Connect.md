### Smart Factory Example

```
import sqlalchemy
import pandas as pd
DATABASE = "oracle19c"
SCHEMA = "rquser"
PASSWORD = "nebula"

connstr = "oracle://{}:{}@{}".format(SCHEMA, PASSWORD, DATABASE)
engine = sqlalchemy.create_engine(connstr)
conn = engine.connect()
data = pd.read_sql_query("select machine_id, out_qty as yield, TO_CHAR(TKIN_TIME, 'yyyy-mm-dd')\
          day FROM lot_sum where machine_id like '24%'", conn)
```

Other one ..

```
import cx_Oracle
conn = cx_Oracle.connect('rquser', 'nebula', 'oracle19c')
cursor=conn.cursor()
binary_var = cursor.var(cx_Oracle.BLOB)

with open("/home/oracle/yolo/yolo_license_plate.pt", "rb") as f:
    data = f.read()
    print(len(data))
    binary_var.setvalue(0, data)


cursor.execute("INSERT INTO python_ser(KEY,RAWDATA,YN) VALUES(:1,:2,:3)", 
       ['yolo_paddle',binary_var,'yolov8+paddle_ocr'])
conn.commit()
```

```
import sqlalchemy
import pandas as pd
DATABASE = "oracle19c"
SCHEMA = "rquser"
PASSWORD = "nebula"

connstr = "oracle://{}:{}@{}".format(SCHEMA, PASSWORD, DATABASE)
engine = sqlalchemy.create_engine(connstr)
conn = engine.connect()

SQL = "SELECT EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID,VALUE \
        FROM fdc_trace \
        WHERE 1=1\
          AND EQP_ID='EQP-200'\
          AND UNIT_ID='UNIT-02'\
          AND LOT_ID='LOTB-101'\
          AND RECIPE='RECIPE-200'\
          AND PARAM_ID IN ('param_b-36') \
          ORDER BY EQP_ID, UNIT_ID, LOT_ID, RECIPE, PARAM_ID"

df = pd.read_sql_query(SQL, conn)

```

How to insert ...

```
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Float
from sqlalchemy import Integer

DATABASE = "oracle19c"
SCHEMA = "rquser"
PASSWORD = "nebula"

connstr = "oracle://{}:{}@{}".format(SCHEMA, PASSWORD, DATABASE)
engine = sqlalchemy.create_engine(connstr)
conn = engine.connect()

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Float
from sqlalchemy import Integer

sqlalchemy.types.NVARCHAR(length=255)
dtype = {"PassengerId" : sqlalchemy.types.INTEGER(),
         "Survived" : sqlalchemy.types.Float(precision=0, asdecimal=True),
         "Pclass": sqlalchemy.types.INTEGER(),
         "Name": sqlalchemy.types.NVARCHAR(100),
         "Sex": sqlalchemy.types.NVARCHAR(10),
         "Age": sqlalchemy.types.Float(precision=0, asdecimal=True),
         "SibSp" : sqlalchemy.types.INTEGER(),
         "Parch" : sqlalchemy.types.INTEGER(),
         "Ticket" : sqlalchemy.types.NVARCHAR(40),
         "Fare" : sqlalchemy.types.Float(precision=0, asdecimal=True),
         "Cabin": sqlalchemy.types.NVARCHAR(40),
         "Embarked": sqlalchemy.types.NVARCHAR(40),
         "TYPE": sqlalchemy.types.NVARCHAR(40)
        }

all_data.to_sql('TITANIC', conn, if_exists='replace', dtype=dtype)
```

바로 테스트 해 보도록 함

```
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Float
from sqlalchemy import Integer
import pandas as pd
import numpy as np

DATABASE = "FREE"
SCHEMA = "GPM"
PASSWORD = "GPM"

connstr = "oracle://{}:{}@{}".format(SCHEMA, PASSWORD, DATABASE)
engine = sqlalchemy.create_engine(connstr)
conn = engine.connect()

from openpyxl import load_workbook
excel_dir = r'G:\Downloads\Excel_Python_Test.xlsx'
df = pd.read_excel(excel_dir, sheet_name='Sheet1', header=0)

df.to_sql('TEST', conn, if_exists='replace')

```
