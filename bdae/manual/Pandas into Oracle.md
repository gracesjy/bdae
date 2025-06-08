## Pandas DataFrame 을 Oracle 테이블로 넣기

```
import sqlalchemy
import pandas as pd
import pandas as pd
import cx_Oracle
import os
from sqlalchemy import create_engine

LOCATION = r"C:\Users\Admin\Downloads\instantclient-basic-windows.x64-23.8.0.25.04\instantclient_23_8"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}'
DATABASE = "FREE"
SCHEMA = "rquser"
PASSWORD = "nebula"

engine = create_engine(
    oracle_connection_string.format(
        username='rquser',
        password='nebula',
        hostname='177.175.54.97',
        port='1521',
        database='FREE',
    )
)

conn = engine.connect()

import seaborn as sns
df = sns.load_dataset('titanic')
df.columns
df.info()  # 대략적인 Type 을 확인한다.

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Float
from sqlalchemy import Integer

sqlalchemy.types.NVARCHAR(length=255)
dtype = {"survived" : sqlalchemy.types.INTEGER(),
         "pclass": sqlalchemy.types.INTEGER(),
         "sex": sqlalchemy.types.NVARCHAR(10),
         "age": sqlalchemy.types.Float(precision=0, asdecimal=True),
         "sibsp" : sqlalchemy.types.INTEGER(),
         "parch" : sqlalchemy.types.INTEGER(),
         "fare": sqlalchemy.types.INTEGER(),
         "embarked": sqlalchemy.types.NVARCHAR(40),
         "class": sqlalchemy.types.NVARCHAR(40),
         "who" : sqlalchemy.types.NVARCHAR(40),
         "adult_male" : sqlalchemy.types.INTEGER(),
         "deck": sqlalchemy.types.NVARCHAR(40),
         "embark_town": sqlalchemy.types.NVARCHAR(40),
         "alive": sqlalchemy.types.NVARCHAR(40),
         "alone": sqlalchemy.types.INTEGER()
        }

# 아래의 index=False 를 넣어야 index 컬럼이 생기지 않는다.  주의하자.
df.to_sql('TITANICX', conn, if_exists='replace', dtype=dtype, index=False)
```
