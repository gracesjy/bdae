SELECT *
FROM table(apEval(
   cursor(
      SELECT 
            '/home/oracle/DeepLearning/JupyterWorkspace/handson-ml2-master/datasets/housing/housing.csv' fileName 
      FROM dual),
   'SELECT 
       1.0 longitude,
       1.0 latitude,
       1.0 housing_median_age,
       1.0 total_rooms,
       1.0 total_bedrooms,
       1.0 population,
       1.0 households,
       1.0 median_income,
       1.0 median_house_value,
       CAST(''A'' as VARCHAR2(1000)) ocean_proximity
    FROM dual',
   'IMPORT_CAL_HOUSING:import_csv'))

-- above fileName converted to Uper Strings, FILENAME
-- we know only one df['FILENAME'] for importing ..
-- def import_csv(df):
--    df = pd.read_csv(df['FILENAME'][0])
--    return (df)
