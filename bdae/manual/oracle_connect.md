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
