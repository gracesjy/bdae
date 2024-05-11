import pandas as pd

#
# Sometimes, CSV columns have space, this can not be columns of Table.
# space replaced by _ 
def getColumns(df):
   df = pd.read_csv(df['FILENAME'][0])
   x = df.columns
   new_columns = []
   for column in x:
      y = column.replace(' ', '_')
      new_columns.append(y)

   df.columns = new_columns
   k =  df.dtypes.to_dict()
   
   sql_columns = []
   for key in k.keys():
      typestr = str(k.get(key))
      if typestr == 'float64' or typestr == 'float32' or typestr == 'float16' or typestr=='float':
         sql_columns.append('1.0 ' + key + ',')
      elif typestr == 'int64' or typestr == 'int32' or typestr == 'int16' or typestr == 'int':
         sql_columns.append('1 ' + key + ',')
      else:
         sql_columns.append('CAST(''AA'' AS VARCHAR2(40)) ' + key + ',')

   pdf = pd.DataFrame({'column_name': new_columns, 'sql_column' : sql_columns })
   return (pdf)


def doImport(df):
   pdf = pd.read_csv(df['FILENAME'][0])
   x = pdf.columns
   new_columns = []
   for column in x:
      y = column.replace(' ', '_')
      new_columns.append(y)

   pdf.columns = new_columns
   pdf.reset_index(drop=True)
   return pdf
