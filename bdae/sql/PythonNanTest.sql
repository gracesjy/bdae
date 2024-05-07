SELECT ID, VALUE2, case when VALUE3=binary_double_infinity then 'Infinity' else TO_CHAR(VALUE3) END AS VALUE3 FROM (   
SELECT *
FROM table(apEval(
   NULL,
   'SELECT CAST(''A'' AS VARCHAR2(10)) ID, 1 Value2, 
           1.0 VALUE3 
    FROM dual',
   'NAN_TEST:returnNAN'))
   )
