## Using Oracle Parallel Processing for Massive Data

SELECT /*+ parallel(5) */
       *
      FROM table(APGROUPEVALPARALLEL(
         	cursor(SELECT * FROM FDC_TRACE), -- Driving Table (or Query) related Parallel Processing
         	CURSOR(SELECT EQP_ID, UNIT_ID FROM FDC_TRACE WHERE ROWNUM < 1000001),  -- Sub Parameter Table (or Query)
            'SELECT CAST(''A'' AS VARCHAR2(40)) PARAM_NAME, 1.0 COUNTS FROM DUAL', -- Output Table or (View)
            'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID', -- Parallel related Columns
           'groupby_test:sumup')) -- Python Module and its Function to run
