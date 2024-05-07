SELECT *
FROM table(apEval(
   NULL,
   'SELECT CAST(''A'' AS VARCHAR2(40)) CLASS_NAME,
       CAST(''A'' AS VARCHAR2(80)) Sample_time, 1.0 DB_TIME FROM dual',
   'db_test:DateTime'))
