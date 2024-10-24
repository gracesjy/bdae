## Pivot

```
import pandas as pd
step = ['7.1.1_1', '7.1.1_2', '7.1.1_3', '7.1.2_1', '7.1.2_2', '7.1.2_3']
desc = ['sop11', 'para11', 'para12', 'sop22', 'para22', 'para23']
sub1 = ['', 'value11', 'value12', '', 'value22', 'value23']
sub2 = ['','','','','value33', 'value44']
datax = { 'step' : step, 'desc': desc, 'sub1': sub1, 'sub2':sub2}
df = pd.DataFrame(datax)


df
df_melt = pd.melt(df, id_vars=['step'], value_vars=['desc', 'sub1', 'sub2'])
df_melt

df_pivot = df_melt.pivot(index='step',columns='variable', values='value')

```
