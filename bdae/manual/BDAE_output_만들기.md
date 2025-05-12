### How to make ${\textsf{\color{green}BDAE's SQL output}}$ using pandas dataframe.
> 예를 들면 아래의 BDAE SQL 문에서 출력을 지정하는 것이 복잡할 수 있다.

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
            'SELECT  CAST(''AA'' AS VARCHAR2(40)) EQP,
             CAST(''AA'' AS VARCHAR2(40)) UNIT,
             CAST(''AA'' AS VARCHAR2(40)) LOT,
             CAST(''AA'' AS VARCHAR2(40)) WAFER,
             CAST(''AA'' AS VARCHAR2(40)) RECIPE,
             CAST(''AA'' AS VARCHAR2(40)) PARAM,
             CAST(''AA'' AS VARCHAR2(100)) LOCATION
             FROM DUAL',
            'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID',       
           'ArrayProcessingParallel:compress'))  
```
> 위에서 아래 부분이 항상 만들기 고통스럽다. <br>
> 물론 아래를 View 로 만들면 좋다.  그러나, 그 전에는 일단 만들어야 한다.<br>

```
SELECT  CAST(''AA'' AS VARCHAR2(40)) EQP,
             CAST(''AA'' AS VARCHAR2(40)) UNIT,
             CAST(''AA'' AS VARCHAR2(40)) LOT,
             CAST(''AA'' AS VARCHAR2(40)) WAFER,
             CAST(''AA'' AS VARCHAR2(40)) RECIPE,
             CAST(''AA'' AS VARCHAR2(40)) PARAM,
             CAST(''AA'' AS VARCHAR2(100)) LOCATION
             FROM DUAL
```
> 아래 부분을 넣고 돌리면 알아서 만들어 준다.

```
def dtype_to_dbtype(typestr):
    return {
        'int64': lambda: '1',
        'object': lambda: "CAST(''AA'' AS VARCHAR2(40))",
        'float32': lambda: '1.0',
        'float64': lambda: '1.0',
        'datetime64[ns]': lambda: 'TO_TIMESTAMP(NULL)',
        'byte': lambda: 'TO_BLOB(NULL)'
    }.get(typestr, lambda: typestr + "not defined type.")()

def space_fill_underbar(column_name):
    return '_'.join(column_name.split(' '))

def get_bdae_output_format(df):
    types = df.dtypes
    column_name_list = []
    column_type_list = []
    for i in range(len(types.index.tolist())):
        column_name_list.append(types.index.tolist()[i])
        column_type_list.append(str(types[types.index.tolist()[i]]))
        print("%-40s %s" %(types.index.tolist()[i], str(types[types.index.tolist()[i]])))

    sql = 'SELECT '
    last_index = len(column_name_list) - 1
    for i in range(last_index + 1):
        if i == last_index:
            sql = sql + ' ' + dtype_to_dbtype(column_type_list[i]) + ' ' + space_fill_underbar(column_name_list[i])  + '\nFROM dual'
        else:
            sql = sql + ' ' + dtype_to_dbtype(column_type_list[i]) + ' ' + space_fill_underbar(column_name_list[i]) + ',\n'

    return (sql)
```

## how to use ?
```
sql = get_bdae_output_format(df)
print(sql)
```
