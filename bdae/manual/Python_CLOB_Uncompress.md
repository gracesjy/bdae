### CLOB column to split !

```
import pandas as pd
import BDAELogger as BDAE

def make_clob_to_list(df):
    # Remote Logging 
    BDAELogger = BDAE.BDAELogger('LOTSUM:make_clob_to_list')
    
    print("------------ LOTSUM:make_clob_to_list start ---------------")
    print("-Input DF\n" + str(df.info()))
    mapping = df['MAPPING'].to_list()[0]
    df.drop(labels='MAPPING', axis=1, inplace=True)
    df_org = df.copy()
    b = mapping.split(',').copy()
    df_x = pd.DataFrame(b, columns=['MAPPING'])
    for i in range(len(b) - 1):
        df_org = pd.concat([df_org, df])
    df_org.reset_index(drop=False, inplace=True)
    df_x.reset_index(drop=False, inplace=True)
    df_final = pd.merge(df_org, df_x, left_index=True, right_index=True, how='left')
    df_final.drop(labels='index_y',axis=1, inplace=True)
    df_final.drop(labels='index_x',axis=1, inplace=True)
    
    print("-Output DF\n" + str(df_final.head()))
    print("------------ LOTSUM:make_clob_to_list end ---------------")
      
    return (df_final)
```

```
SELECT * FROM 
        table(apTableEval( 
          cursor(SELECT * FROM LOT_SUM WHERE DURABLE_ID = 'Z100'), 
          NULL,
          'LOT_SUM2',
          'LOTSUM:make_clob_to_list'))
```
