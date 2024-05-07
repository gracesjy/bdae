WITH ORA_DATA AS
(
SELECT  
   wc.wait_class AS waitclass,
   TO_CHAR(TRUNC (begin_time, 'MI'), 'YYYYMMDDHH24MISS') 
      AS sample_time,
   ROUND ( (wh.time_waited) / wh.intsize_csec, 3) 
      AS DB_time
FROM V$SYSTEM_WAIT_CLASS wc, v$waitclassmetric_history wh
WHERE wc.wait_class != 'Idle'
   AND wc.wait_class_id = wh.wait_class_id
UNION
SELECT 
   'CPU' AS waitclass,
   TO_CHAR(TRUNC (begin_time, 'MI'), 'YYYYMMDDHH24MISS') 
      AS sample_time,
   ROUND (VALUE / 100, 3) 
      AS DB_time
FROM v$sysmetric_history
WHERE GROUP_ID = 2
   AND metric_name = 'CPU Usage Per Sec'
ORDER BY sample_time, waitclass
)
SELECT * 
FROM table(
   apTableEval(
     cursor(SELECT * FROM ORA_DATA),
     NULL,
     'SELECT ''AAAAAAAAAAAA'' DATA, TO_CLOB(NULL) XML FROM dual',
   'oracle_mon:make_mon')
)
