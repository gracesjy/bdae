select * from table (apEval (NULL, 'SELECT CAST(''AA'' AS VARCHAR2(40)) NAME, TO_CLOB(NULL) IMAGE FROM dual' , 'DLExam:logisticReg'))
