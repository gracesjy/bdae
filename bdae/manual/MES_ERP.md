## 강의 내용 발췌 .. 간단한 부분만

```
import pandas as pd
import numpy as np

# SCM
scm_data = {'Week': weeks_data, 'Demand': np.random.randint(50,100,weeks)}
scm_df = pd.DataFrame(scm_data)

# ERP Data
erp_data = {'Week': weeks_data, 'ProductionPlan': np.random.randint(40,80,weeks)}
erp_df = pd.DataFrame(erp_data)

# MES Data
mes_data = {'Week': weeks_data, 'ActualProduction': np.random.randint(30,70,weeks)}
mes_df = pd.DataFrame(mes_data)

# Combind dataframe
combined_df = pd.merge(scm_df, erp_df, on='Week')
combined_df = pd.merge(combined_df, mes_df, on='Week')

```
