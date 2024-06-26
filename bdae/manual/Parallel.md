## Using Oracle Parallel Processing for Massive Data

```
SELECT /*+ parallel(5) */
       *      
FROM table(APGROUPEVALPARALLEL( 
      CURSOR(SELECT * FROM FDC_TRACE), -- Driving Table (or Query) related Parallel Processing
      CURSOR(SELECT EQP_ID, UNIT_ID FROM FDC_TRACE WHERE ROWNUM < 1000001),  -- Sub Parameter Table (or Query)
      'SELECT CAST(''A'' AS VARCHAR2(40)) PARAM_NAME, 1.0 COUNTS FROM DUAL', -- Output Table or (View)
      'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID', -- Parallel related Columns
      'groupby_test:sumup')) -- Python Module and its Function to run
```

You can define below functions as you want.
```
create or replace  FUNCTION apGroupEvalParallel(
                          inp_cur IN fdc_tracePkg.cur, par_cur SYS_REFCURSOR,
                          out_qry VARCHAR2,  grp_col VARCHAR2, exp_nam VARCHAR2)
RETURN ANYDATASET PIPELINED PARALLEL_ENABLE (PARTITION inp_cur BY HASH(EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID))
CLUSTER inp_cur BY (EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID)
USING RQUSER.APGRPEVALIMPL;
```
You can define the package as you want
```
create or replace  PACKAGE  "FDC_TRACEPKG" AS
TYPE cur IS REF CURSOR RETURN fdc_trace%ROWTYPE;
END fdc_tracePkg;
```


Another example

```
SELECT /*+ parallel(5) */*
      FROM table(APGROUPEVALPARALLEL(
         	CURSOR(SELECT * FROM FDC_TRACE),
         	CURSOR(SELECT EQP_ID, UNIT_ID FROM FDC_TRACE WHERE ROWNUM < 1000001),
            'SELECT CAST(''A'' AS VARCHAR2(40)) EQP_ID, 
                    CAST(''A'' AS VARCHAR2(40)) UNIT_ID,
                    CAST(''A'' AS VARCHAR2(40)) LOT_ID,
                    CAST(''A'' AS VARCHAR2(40)) WAFER_ID,
                    CAST(''A'' AS VARCHAR2(40)) RECIPE,
                    CAST(''A'' AS VARCHAR2(40)) PARAM_ID,
                    CAST(''A'' AS VARCHAR2(40)) KEY,
                    1.0 VALUE FROM DUAL',
            'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID',       
           'ParallelDesc:describe'))
```

ParallelDesc:describe
```
import cx_Oracle
import pandas as pd
import os
import sys
import gc
import logging

def describe(df, arg1):
    df_value = df['VALUE']
    desc_df = df_value.describe()
    desc_columns = desc_df.index.tolist()
    desc_values = desc_df.tolist()
    
    eqpId = [] # EQP_ID
    unitId = [] # UNIT_ID
    lotId = [] # LOT_ID
    waferId = [] # WAFER_ID
    recipe = [] # RECIPE
    paramId = [] # PARAM_ID
    
    for i in range(len(desc_values)):
        eqpId = df['EQP_ID'][0]
        unitId = df['UNIT_ID'][0]
        lotId = df['LOT_ID'][0]
        waferId = df['WAFER_ID'][0]
        recipe = df['RECIPE'][0]
        paramId = df['PARAM_ID'][0]

    pdf = pd.DataFrame(data={'EQP_ID': eqpId, 'UNIT_ID': unitId, 'LOT_ID': lotId, 'WAFER_ID' : waferId, 'RECIPE': recipe, 
                            'PARAM_ID': paramId, 'KEY_NAME' : desc_columns, 'VALUES': desc_values})
    return (pdf)

```
Wrapping above BDAE's SQL

```
SELECT *
FROM table(apEval(
   cursor(SELECT 'EQP-200' EQP_ID FROM dual),
   'SELECT CAST(''A'' AS VARCHAR2(40)) EQP_ID, 
           CAST(''A'' AS VARCHAR2(40)) UNIT_ID,
           CAST(''A'' AS VARCHAR2(40)) LOT_ID,
           CAST(''A'' AS VARCHAR2(40)) WAFER_ID,
           CAST(''A'' AS VARCHAR2(40)) RECIPE,
           CAST(''A'' AS VARCHAR2(40)) PARAM_ID,
           CAST(''A'' AS VARCHAR2(40)) KEY,
           1.0 VALUE FROM DUAL',
   'ParallelDescByWrapper:describe'))
```
ParallelDescByWrapper:describe

```
import FDCDescribeParallel
import pandas as pd

def describe(df_arg):
    return FDCDescribeParallel.get_fdc_descriptive_statistics_eqp(df_arg)
```

Package FDCDescribeParallel is 
```
import pandas as pd
import numpy as np
import sqlalchemy

def get_fdc_descriptive_statistics():
    DATABASE = "oracle19c"
    SCHEMA = "rquser"
    PASSWORD = "nebula"

    connstr = "oracle://{}:{}@{}".format(SCHEMA, PASSWORD, DATABASE)
    engine = sqlalchemy.create_engine(connstr)
    conn = engine.connect()

    SQL = "SELECT /*+ parallel(5) */* \
          FROM table(APGROUPEVALPARALLEL(\
                CURSOR(SELECT * FROM FDC_TRACE),\
                CURSOR(SELECT EQP_ID, UNIT_ID FROM FDC_TRACE WHERE ROWNUM < 1000001),\
                'SELECT CAST(''A'' AS VARCHAR2(40)) EQP_ID, \
                        CAST(''A'' AS VARCHAR2(40)) UNIT_ID,\
                        CAST(''A'' AS VARCHAR2(40)) LOT_ID,\
                        CAST(''A'' AS VARCHAR2(40)) WAFER_ID,\
                        CAST(''A'' AS VARCHAR2(40)) RECIPE,\
                        CAST(''A'' AS VARCHAR2(40)) PARAM_ID,\
                        CAST(''A'' AS VARCHAR2(40)) KEY,\
                        1.0 VALUE FROM DUAL',\
                        'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID',\
               'ParallelDesc:describe'))"

    df = pd.read_sql_query(SQL, conn)
    conn.close()
    return df

def get_fdc_descriptive_statistics_eqp(df_arg):
    DATABASE = "oracle19c"
    SCHEMA = "rquser"
    PASSWORD = "nebula"

    connstr = "oracle://{}:{}@{}".format(SCHEMA, PASSWORD, DATABASE)
    engine = sqlalchemy.create_engine(connstr)
    conn = engine.connect()

    SQL = "SELECT /*+ parallel(5) */* \
          FROM table(APGROUPEVALPARALLEL(\
                CURSOR(SELECT * FROM FDC_TRACE \
                       WHERE EQP_ID='{}' \
                ),\
                CURSOR(SELECT EQP_ID, UNIT_ID FROM FDC_TRACE WHERE ROWNUM < 1000001),\
                'SELECT CAST(''A'' AS VARCHAR2(40)) EQP_ID, \
                        CAST(''A'' AS VARCHAR2(40)) UNIT_ID,\
                        CAST(''A'' AS VARCHAR2(40)) LOT_ID,\
                        CAST(''A'' AS VARCHAR2(40)) WAFER_ID,\
                        CAST(''A'' AS VARCHAR2(40)) RECIPE,\
                        CAST(''A'' AS VARCHAR2(40)) PARAM_ID,\
                        CAST(''A'' AS VARCHAR2(40)) KEY,\
                        1.0 VALUE FROM DUAL',\
                        'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID',\
               'ParallelDesc:describe'))".format(df_arg['EQP_ID'][0])

    df = pd.read_sql_query(SQL, conn)
    conn.close()
    return df
```


