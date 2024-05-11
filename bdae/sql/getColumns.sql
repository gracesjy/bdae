-- First Column, Second Column for Output SQL
SELECT *
FROM table(apEval(
   cursor(
      SELECT 
            '/home/oracle/breast_cancer.csv' FILENAME 
      FROM dual),
   'SELECT CAST(''A'' AS VARCHAR2(40)) SUBJECT, CAST(''A'' AS VARCHAR2(40)) SQL_COLUMN FROM dual',
   'IMPORT_CSV:getColumns'));
