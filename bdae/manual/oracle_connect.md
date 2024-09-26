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
data = pd.read_sql_query("select machine_id, out_qty as yield, TO_CHAR(TKIN_TIME, 'yyyy-mm-dd') day FROM lot_sum where machine_id like '24%'", conn)
```
