### Array

Python Code, CLOB but enable to parallel process.. 
```
def compress(df):
    value_list = df['VALUE'].tolist()
    values_str = ''
    len_values = len(value_list)
    for i in range(len_values):
        if i < (len_values -1):
            values_str = values_str + str(round(value_list[i], 5)) + ','
        else:
            values_str = values_str + str(round(value_list[i], 5))

    # for parallel
    DATABASE = "FREE"
    SCHEMA = "rquser"
    PASSWORD = "nebula"

    connstr = "oracle://{}:{}@{}".format(SCHEMA, PASSWORD, DATABASE)
    engine = sqlalchemy.create_engine(connstr)
    conn = engine.connect()
    
    # for CLOB and save data into table !
    dictDataForTbl = {'EQP_ID': [df['EQP_ID'][0]], 'UNIT_ID':  [df['UNIT_ID'][0]], 'LOT_ID':[df['LOT_ID'][0]], \
               'WAFER_ID': [df['WAFER_ID'][0]], 'RECIPE': [df['RECIPE'][0]], 'PARAM_ID': [df['PARAM_ID'][0]], 'ITEM_ARRAY': [values_str]}
    pdf = pd.DataFrame(dictDataForTbl)
    pdf.to_sql('FDC_ARRAY_SENSOR', conn, if_exists='append', index=False)
    conn.commit()
    location_of_data = values_str[:10] + '...'
    dictData = {'EQP_ID': [df['EQP_ID'][0]], 'UNIT_ID':  [df['UNIT_ID'][0]], 'LOT_ID':[df['LOT_ID'][0]], \
               'WAFER_ID': [df['WAFER_ID'][0]], 'RECIPE': [df['RECIPE'][0]], 'PARAM_ID': [df['PARAM_ID'][0]], 'ITEM_ARRAY': [location_of_data]}
    
    return pd.DataFrame(dictData)

```

SQL
```
SELECT /*+ parallel(5) */*
      FROM table(apGroupEvalParallel(
         	CURSOR(
            SELECT EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID,VALUE
              FROM fdc_trace 
              WHERE 1=1 
                AND EQP_ID='EQP-200'
                AND UNIT_ID='UNIT-02'
                AND LOT_ID='LOTB-101'
                AND RECIPE='RECIPE-200'
            ),
         	NULL,
            'SELECT  CAST(NULL AS VARCHAR2(40)) EQP,
             CAST(NULL AS VARCHAR2(40)) UNIT,
             CAST(NULL AS VARCHAR2(40)) LOT,
             CAST(NULL AS VARCHAR2(40)) WAFER,
             CAST(NULL AS VARCHAR2(40)) RECIPE,
             CAST(NULL AS VARCHAR2(40)) PARAM,
             CAST(NULL AS VARCHAR2(100)) LOCATION
             FROM DUAL',
            'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID',       
           'ArrayProcessingParallel:compress')) 
```


    
