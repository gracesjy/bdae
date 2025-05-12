### How to make <span style="color:blue">BDAE's SQL output</span> using pandas dataframe.
1) 분석 코드를 DB 에 등록 해서 사용한다.  이 분석 코드는 재활용된다.(Register Analysis Codes into DB)<br>
2) SQL 문으로 실행 결과를 실시간으로 확인한다. (Run SQL and see the results in Real-Time)<br>
3) 병렬 분산 처리를 수행한다.  이때 분석 코드는 관여하지 않고, Oracle Database 의 병렬 분산 처리를 이용한다.<br>
   (Use Oracle Parallelism.)
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
