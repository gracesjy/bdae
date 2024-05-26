## Using Oracle Parallel Processing for Massive Data

```
SELECT /*+ parallel(5) */
       *      
FROM table(APGROUPEVALPARALLEL( 
      CURSOR(SELECT * FROM FDC_TRACE), -- Driving Table (or Query) related Parallel Processing
      CURSOR(SELECT EQP_ID, UNIT_ID FROM FDC_TRACE WHERE ROWNUM < 1000001),  -- Sub Parameter Table (or Query)
          
      'SELECT CAST(''A'' AS VARCHAR2(40)) PARAM_NAME, 1.0 COUNTS FROM DUAL', -- Output Table or (View)
            
      'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID', -- Parallel related Columns
            
      'groupby_test:sumup')) -- Python Module and its Function to run
```

You can define below functions as you want.
```
create or replace  FUNCTION apGroupEvalParallel(
                          inp_cur IN fdc_tracePkg.cur, par_cur SYS_REFCURSOR,
                          out_qry VARCHAR2,  grp_col VARCHAR2, exp_nam VARCHAR2)
RETURN ANYDATASET PIPELINED PARALLEL_ENABLE (PARTITION inp_cur BY HASH(EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID))
CLUSTER inp_cur BY (EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID)
USING RQUSER.APGRPEVALIMPL;
```
You can define the package as you want
```
create or replace  PACKAGE  "FDC_TRACEPKG" AS
TYPE cur IS REF CURSOR RETURN fdc_trace%ROWTYPE;
END fdc_tracePkg;
```
