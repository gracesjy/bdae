# Nan and Infinity Example

Python Module. Only use numpy for Nan and Infinity !!
```
import pandas as pd
import numpy as np

def returnNAN():
    df = pd.DataFrame([['motor type',1, np.inf],
                      [np.nan, 2, 3.2],
                      ['RF', np.nan, 4.5]],
                      columns = list('abc'))
    return df
```

SQL
```
SELECT ID, VALUE2, case when VALUE3=binary_double_infinity then 'Infinity' else TO_CHAR(VALUE3) END AS VALUE3 FROM (   
SELECT *
FROM table(apEval(
   NULL,
   'SELECT CAST(''A'' AS VARCHAR2(10)) ID, 1 Value2, 
           1.0 VALUE3 
    FROM dual',
   'NAN_TEST:returnNAN'))
   )

```
