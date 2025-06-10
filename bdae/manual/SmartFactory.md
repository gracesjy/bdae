### Smart Factory Example

설비 유의차
```
import os
import sys
import urllib
import base64
import pandas as pd
import plotly.express as px
import plotly.offline as py

def display(df):
    fig = px.box(df, x="MACHINE_ID", y="YIELD", color='MACHINE_ID',
             notched=True, # used notched shape
             title="Yield Machine Significant",
             hover_data=["DAY"] # add day column to hover data
            )
    total = py.offline.plot(fig, output_type='div')
    return total
```

SQL
```
SELECT *
FROM table(apTableEval(
   CURSOR(SELECT
          MACHINE_ID, OUT_QTY AS YIELD, 
          TO_CHAR(TKIN_TIME, 'yyyy-mm-dd') DAY 
          FROM lot_sum WHERE MACHINE_ID like '24%'),
   NULL,
   'XML',
   'EquipSignifi:display'))
```
