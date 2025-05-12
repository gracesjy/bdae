## ${\textsf{\color{green}Compress of Sensor Data}}$

```

import pandas as pd

def compress(df):
    df.columns = ['eqp_id','unit_id','lot_id','wafer_id', 'recipe', 'param_id', 'value']
    value_list = df['value'].tolist()
    values_str = ''
    len_values = len(value_list)
    for i in range(len_values):
        if i < (len_values -1):
            values_str = values_str + str(round(value_list[i], 5)) + ','
        else:
            values_str = values_str + str(round(value_list[i], 5))

    
    dictData = {'EQP_ID': [df['eqp_id'][0]], 'UNIT_ID':  [df['unit_id'][0]], 'LOT_ID':[df['lot_id'][0]], 'WAFER_ID': [df['wafer_id'][0]], 'RECIPE': [df['recipe'][0]], 'PARAM_ID': [df['param_id'][0]], 'ITEM_ARRAY': [values_str]}
    return pd.DataFrame(dictData)
```

How to run ..

```
SELECT *
      FROM table(apGroupEvalParallel(
         	CURSOR(
            SELECT EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID,VALUE
              FROM fdc_trace 
              WHERE 1=1 
                AND EQP_ID='EQP-200'
                AND UNIT_ID='UNIT-02'
                AND LOT_ID='LOTB-101'
                AND RECIPE='RECIPE-200'
                AND PARAM_ID IN ('param_b-36', 'param_b-35')
            ),
         	NULL,
            'FDC_ARRAY_SENSOR',
            'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID',       
           'ArrayProcessing:compress'))  
```
