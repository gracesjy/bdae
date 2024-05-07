WITH FDC_TRACE_DATA AS 
      (
          SELECT *
          FROM 
          ( SELECT EQP_ID, UNIT_ID, LOT_ID, WAFER_ID, RECIPE, 
                   PARAM_ID, TIMEKEY, VALUE
            FROM FDC_TRACE
            WHERE 1=1
                AND EQP_ID ='EQP-300'
                AND UNIT_ID ='UNIT-01'
                AND LOT_ID ='LOTC-101'
                AND WAFER_ID = 'LOTC-101-01'
                AND RECIPE = 'RECIPE-300'
          )
          PIVOT (MAX(VALUE) AS VALUE FOR (PARAM_ID)
          IN (
              'param_b-1' AS PARA_1,
              'param_b-2' AS PARA_2,
              'param_b-3' AS PARA_3,
              'param_b-4' AS PARA_4,
              'param_b-5' AS PARA_5,
              'param_b-6' AS PARA_6,
              'param_b-7' AS PARA_7,
              'param_b-8' AS PARA_8,
              'param_b-9' AS PARA_9,
              'param_b-10' AS PARA_10
          )
        ) 
      )
      SELECT * 
      FROM table(apTableEval(
         	cursor(SELECT * FROM FDC_TRACE_DATA),
         	CURSOR(SELECT EQP_ID, UNIT_ID FROM FDC_TRACE WHERE ROWNUM < 20),
          'SELECT CAST(''A'' AS VARCHAR2(40)) PARAM_NAME, 
                  1.0 EIGVALS 
           FROM DUAL',
           'PCA:run_pca_2nd')) 
