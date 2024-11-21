#### dynamic

```
https://www.oracle-developer.net/display.php?id=422
```

```
create or replace TYPE ramos_odci_clob AS OBJECT

(

  /*

  || ---------------------------------------------------------------------------------

  ||

  ||

  || ---------------------------------------------------------------------------------

  */

  atype ANYTYPE --<-- transient record type

, STATIC FUNCTION ODCITableDescribe(

                  rtype OUT ANYTYPE,

                  inp_cur IN OUT SYS_REFCURSOR

                  ) RETURN NUMBER

​

, STATIC FUNCTION ODCITablePrepare(

                  sctx    OUT ramos_odci_clob,

                  tf_info IN  sys.ODCITabFuncInfo,

                  inp_cur IN OUT SYS_REFCURSOR

                  ) RETURN NUMBER

​

, STATIC FUNCTION ODCITableStart(

                  sctx IN OUT ramos_odci_clob,

                  inp_cur IN OUT SYS_REFCURSOR

                  ) RETURN NUMBER

​

, MEMBER FUNCTION ODCITableFetch(

                  SELF  IN OUT ramos_odci_clob,

                  nrows IN     NUMBER,

                  rws   OUT    anydataset

                  ) RETURN NUMBER

​

, MEMBER FUNCTION ODCITableClose(

                  SELF IN ramos_odci_clob

                  ) RETURN NUMBER

);

​

​

create or replace TYPE BODY ramos_odci_clob

AS

    /*

    || ---------------------------------------------------------------------------------

    ||

    ||

    ||

    || ---------------------------------------------------------------------------------

    */

    ------------------------------------------------------------------------------------

    STATIC

FUNCTION ODCITableDescribe

                          (

                              rtype OUT ANYTYPE

                            , inp_cur IN OUT SYS_REFCURSOR

                          )

    RETURN NUMBER

IS

    v_rtype ANYTYPE;

    r_sql atlas_pkg.rt_dynamic_sql;

    stmtx VARCHAR2(1024);

BEGIN

    /*

    || Parse the SQL and describe its format and structure.

    */

    stmtx        := 'SELECT 1 ID, 1 BIN1, 1 BIN2, 1 BIN3, 1 BIN4, 1 BIN5, 1 BIN6, 1 BIN7, 1 BIN8, 1 BIN9, ';

    stmtx        := stmtx || 'CAST(''A'' AS VARCHAR2(200)) DURABLE_ID, 1 DURABLE_POS, ';

    stmtx        := stmtx || '1 IN_QTY, CAST(''A'' AS VARCHAR2(200)) LOT_ID, CAST(''A'' AS VARCHAR2(200)) MACHINE_ID, ';

    stmtx        := stmtx || '1 NG_QTY, CAST(''A'' AS VARCHAR2(200)) OPERATOR, 1 OUT_QTY, ';

    stmtx        := stmtx || 'CAST(''A'' AS VARCHAR2(200)) PROC_OPER_ID, CAST(''A'' AS VARCHAR2(200)) PROD_SPEC_ID, ';

    stmtx        := stmtx || 'CAST(''A'' AS VARCHAR2(200)) PROD_GRADE, 1 PROD_IDX, ';

    stmtx        := stmtx || 'CAST(''A'' AS VARCHAR2(200)) TKIN_TIME, CAST(''A'' AS VARCHAR2(200)) TKOUT_TIME ';

    stmtx        := stmtx || 'FROM DUAL';

    

​

    r_sql.cursor := DBMS_SQL.OPEN_CURSOR;

    DBMS_SQL.PARSE( r_sql.cursor, stmtx, DBMS_SQL.NATIVE );

    DBMS_SQL.DESCRIBE_COLUMNS2( r_sql.cursor, r_sql.column_cnt, r_sql.description );

    DBMS_SQL.CLOSE_CURSOR( r_sql.cursor );

    /*

    || Create the ANYTYPE record structure from this SQL structure.

    || Replace LONG columns with CLOB...

    */

    ANYTYPE.BeginCreate( DBMS_TYPES.TYPECODE_OBJECT, v_rtype );

    FOR i IN 1 .. r_sql.column_cnt

    LOOP

        v_rtype.AddAttr( r_sql.description(i).col_name, CASE

            --<>--

        WHEN r_sql.description(i).col_type IN (1,96,11,208) THEN

            DBMS_TYPES.TYPECODE_VARCHAR2

            --<>--

        WHEN r_sql.description(i).col_type = 2 THEN

            DBMS_TYPES.TYPECODE_NUMBER

            --<LONG defined as CLOB>--

        WHEN r_sql.description(i).col_type IN (8,112) THEN

            DBMS_TYPES.TYPECODE_CLOB

            --<>--

        WHEN r_sql.description(i).col_type = 12 THEN

            DBMS_TYPES.TYPECODE_DATE

            --<>--

        WHEN r_sql.description(i).col_type = 23 THEN

            DBMS_TYPES.TYPECODE_RAW

            --<>--

        WHEN r_sql.description(i).col_type = 180 THEN

            DBMS_TYPES.TYPECODE_TIMESTAMP

            --<>--

        WHEN r_sql.description(i).col_type = 181 THEN

            DBMS_TYPES.TYPECODE_TIMESTAMP_TZ

            --<>--

        WHEN r_sql.description(i).col_type = 182 THEN

            DBMS_TYPES.TYPECODE_INTERVAL_YM

            --<>--

        WHEN r_sql.description(i).col_type = 183 THEN

            DBMS_TYPES.TYPECODE_INTERVAL_DS

            --<>--

        WHEN r_sql.description(i).col_type = 231 THEN

            DBMS_TYPES.TYPECODE_TIMESTAMP_LTZ

            --<>--

        END, r_sql.description(i).col_precision, r_sql.description(i).col_scale, CASE r_sql.description(i).col_type

        WHEN 11 THEN

            32

        ELSE

            r_sql.description(i).col_max_len

        END, r_sql.description(i).col_charsetid, r_sql.description(i).col_charsetform );

    END LOOP;

    v_rtype.EndCreate;

    /*

    || Now we can use this transient record structure to create a table type

    || of the same. This will create a set of types on the database for use

    || by the pipelined function...

    */

    ANYTYPE.BeginCreate( DBMS_TYPES.TYPECODE_TABLE, rtype );

    rtype.SetInfo( NULL, NULL, NULL, NULL, NULL, v_rtype, DBMS_TYPES.TYPECODE_OBJECT, 0 );

    rtype.EndCreate();

    RETURN ODCIConst.Success;

END;

------------------------------------------------------------------------------------

STATIC

FUNCTION ODCITablePrepare

                         (

                             sctx OUT ramos_odci_clob

                           , tf_info IN sys.ODCITabFuncInfo

                           , inp_cur IN OUT SYS_REFCURSOR

                         )

    RETURN NUMBER

IS

    r_meta atlas_pkg.rt_anytype_metadata;

BEGIN

    /*

    || We prepare the dataset that our pipelined function will return by

    || describing the ANYTYPE that contains the transient record structure...

    */

    r_meta.typecode := tf_info.rettype.GetAttrElemInfo( 1, r_meta.precision, r_meta.scale, r_meta.length, r_meta.csid, r_meta.csfrm, r_meta.type, r_meta.name );

    /*

    || Using this, we initialise the scan context for use in this and

    || subsequent executions of the same dynamic SQL cursor...

    */

    sctx := ramos_odci_clob(r_meta.type);

    RETURN ODCIConst.Success;

END;

------------------------------------------------------------------------------------

STATIC

FUNCTION ODCITableStart

                       (

                           sctx    IN OUT ramos_odci_clob

                         , inp_cur IN OUT SYS_REFCURSOR

                       )

    RETURN NUMBER

IS

    r_meta atlas_pkg.rt_anytype_metadata;

    l_cursorid INTEGER;

BEGIN

    /*

    || We now describe the cursor again and use this and the described

    || ANYTYPE structure to define and execute the SQL statement...

    */

    atlas_pkg.r_sql.finished := 0;

    atlas_pkg.r_sql.cursor   := DBMS_SQL.TO_CURSOR_NUMBER(inp_cur);

    DBMS_OUTPUT.PUT_LINE ('ODCITableStart entered !');

    RETURN ODCIConst.Success;

END;

------------------------------------------------------------------------------------

MEMBER FUNCTION ODCITableFetch

                              (

                                  SELF  IN OUT ramos_odci_clob

                                , nrows IN NUMBER

                                , rws OUT ANYDATASET

                              )

    RETURN NUMBER

IS

TYPE rt_fetch_attributes

IS

    RECORD

    (

        v2_column     VARCHAR2(32767)

        , num_column  NUMBER

        , date_column DATE

        , clob_column CLOB

        , raw_column RAW(32767)

        , raw_error  NUMBER

        , raw_length INTEGER

        , ids_column INTERVAL DAY TO SECOND

        , iym_column INTERVAL YEAR TO MONTH

        , ts_column    TIMESTAMP

        , tstz_column  TIMESTAMP WITH TIME ZONE

        , tsltz_column TIMESTAMP WITH LOCAL TIME ZONE

        , cvl_offset   INTEGER := 0

        , cvl_length   INTEGER );

    r_fetch rt_fetch_attributes;

    r_meta atlas_pkg.rt_anytype_metadata;

    item_name_now  VARCHAR2(1000) := NULL;

    item_name_prev VARCHAR2(1000) := NULL;

    v_err_code     NUMBER;

    v_err_msg      VARCHAR2(255);

    l_row          NUMBER;

    l_total_row    NUMBER;

​

    delimeter      VARCHAR2(10);

    --

    id1            NUMBER;

    bin1           NUMBER;

    bin2           NUMBER;

    bin3           NUMBER;

    bin4           NUMBER;

    bin5           NUMBER;

    bin6           NUMBER;

    bin7           NUMBER;

    bin8           NUMBER;

    bin9           NUMBER;

    durable_id     VARCHAR2(40);

    durable_pos    NUMBER;

    in_qty         NUMBER;

    lot_id         VARCHAR2(40);

    machine_id     VARCHAR2(40);

    ng_qty         NUMBER;

    operator       VARCHAR2(40);

    out_qty        NUMBER;

    proc_oper_id   VARCHAR2(40);

    prod_spec_id   VARCHAR2(40);

    tkin_time      VARCHAR2(40);

    tkout_time     VARCHAR2(40);

    l_list         VARCHAR2(32767);

    mapping        CLOB;

    

    l_idx          PLS_INTEGER; 

    prod_idx       PLS_INTEGER;

​

    offset         NUMBER;

    amount         NUMBER;

    len            NUMBER;

    buf            VARCHAR2(32767);

​

BEGIN

    DBMS_OUTPUT.PUT_LINE ('ODCITableFetch entered !');

    l_row := 0;

    l_total_row := 0;

    delimeter := ',';

    

    -- ANYDATASET.BeginCreate( DBMS_TYPES.TYPECODE_OBJECT, SELF.atype, rws );

    IF atlas_pkg.r_sql.finished <= 0 THEN

        -- l_row := 0;

        

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 1, id1);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 2, bin1);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 3, bin2);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 4, bin3);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 5, bin4);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 6, bin5);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 7, bin6);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 8, bin7);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 9, bin8);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 10, bin9);

        

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 11, durable_id, 40);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 12, durable_pos);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 13, in_qty);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 14, lot_id, 40);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 15, machine_id, 40);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 16, ng_qty);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 17, operator, 40);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 18, out_qty);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 19, proc_oper_id, 40);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 20, prod_spec_id, 40);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 21, mapping);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 22, tkin_time, 40);

        DBMS_SQL.define_column (atlas_pkg.r_sql.cursor, 23, tkout_time, 40);

        

        item_name_now  := NULL;

        item_name_prev := NULL;

        --ANYDATASET.BeginCreate( DBMS_TYPES.TYPECODE_OBJECT, SELF.atype, rws );

        LOOP

            IF DBMS_SQL.FETCH_ROWS (atlas_pkg.r_sql.cursor) = 0 THEN

                DBMS_OUTPUT.PUT_LINE('NO_DATA_FOUND !  : '  || l_row);

                EXIT;

            END IF;

            

            ANYDATASET.BeginCreate( DBMS_TYPES.TYPECODE_OBJECT, SELF.atype, rws );

            

            l_total_row := l_total_row + 1;

            -- ID

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 1, r_fetch.num_column );

            id1 := r_fetch.num_column;

            

            -- BIN1 

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 2, r_fetch.num_column );

            bin1 := r_fetch.num_column;

            

            -- BIN2 

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 3, r_fetch.num_column );

            bin2 := r_fetch.num_column;

            

            -- BIN3 

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 4, r_fetch.num_column );

            bin3 := r_fetch.num_column;

            

            -- BIN4 

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 5, r_fetch.num_column );

            bin4 := r_fetch.num_column;

            

            -- BIN5 

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 6, r_fetch.num_column );

            bin5 := r_fetch.num_column;

            

            -- BIN6 

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 7, r_fetch.num_column );

            bin6 := r_fetch.num_column;

            

            -- BIN7

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 8, r_fetch.num_column );

            bin7 := r_fetch.num_column;

            

            -- BIN8 

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 9, r_fetch.num_column );

            bin8 := r_fetch.num_column;

            

            -- BIN9

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 10, r_fetch.num_column );

            bin9 := r_fetch.num_column;

            

            

            -- DURABLE_ID

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 11, r_fetch.v2_column );

            durable_id := r_fetch.v2_column;

            

            -- DURABLE_POS

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 12, r_fetch.num_column );

            durable_pos := r_fetch.num_column;

            

            -- IN_QTY

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 13, r_fetch.num_column );

            in_qty := r_fetch.num_column;

            

            -- LOT_ID

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 14, r_fetch.v2_column );

            lot_id := r_fetch.v2_column;

            

            -- MACHINE_ID

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 15, r_fetch.v2_column );

            machine_id := r_fetch.v2_column;

            

            -- NG_QTY

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 16, r_fetch.num_column );

            ng_qty := r_fetch.num_column;

            

            -- OPERATOR

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 17, r_fetch.v2_column );

            operator := r_fetch.v2_column;

            

            -- OUT_QTY

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 18, r_fetch.num_column );

            out_qty := r_fetch.num_column;

            

            -- PROC_OPER_ID

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 19, r_fetch.v2_column );

            proc_oper_id := r_fetch.v2_column;

            

            -- PROD_SPEC_ID

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 20, r_fetch.v2_column );

            prod_spec_id := r_fetch.v2_column;

            

            -- MAPPING

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 21, r_fetch.clob_column );

            offset := 1;

            len    := DBMS_LOB.getLength(r_fetch.clob_column);

            amount := 32767;

            WHILE offset < len LOOP

            

               DBMS_LOB.read(r_fetch.clob_column, amount, offset, l_list);

               offset := offset + amount;

               

            END LOOP; 

            

            -- l_list := r_fetch.v2_column;

            

            -- TKIN_TIME

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 22, r_fetch.v2_column );

            tkin_time := r_fetch.v2_column;

            

            -- TKOUT_TIME

            DBMS_SQL.COLUMN_VALUE( atlas_pkg.r_sql.cursor, 23, r_fetch.v2_column );

            tkout_time := r_fetch.v2_column;

            

            

            prod_idx := 1;

            l_idx := 0;

            LOOP 

               l_idx := instr(l_list, delimeter);

               IF l_idx > 0 THEN

                  rws.AddInstance();

                  rws.PieceWise();

                  

                  rws.SetNumber(id1);

                  rws.SetNumber(bin1);

                  rws.SetNumber(bin2);

                  rws.SetNumber(bin3);

                  rws.SetNumber(bin4);

                  rws.SetNumber(bin5);

                  rws.SetNumber(bin6);

                  rws.SetNumber(bin7);

                  rws.SetNumber(bin8);

                  rws.SetNumber(bin9);

                  

                  

                  rws.SetVarchar2(durable_id);

                  rws.SetNumber(durable_pos);

                  rws.SetNumber(in_qty);

                  rws.SetVarchar2(lot_id);

                  rws.SetVarchar2(machine_id);

                  rws.SetNumber(ng_qty);

                  rws.SetVarchar2(operator);

                  rws.SetNumber(out_qty);

                  rws.SetVarchar2(proc_oper_id);

                  rws.SetVarchar2(prod_spec_id);

                  rws.SetVarchar2(substr(l_list,1,l_idx-1));

                  rws.SetNumber(prod_idx);

                  rws.SetVarchar2(tkin_time);

                  rws.SetVarchar2(tkout_time);

                  DBMS_OUTPUT.PUT_LINE ('PROD_IDX  : ' || prod_idx);

                  prod_idx := prod_idx + 1;

                  l_list := substr(l_list,l_idx+length(delimeter));

               ELSE 

                  DBMS_OUTPUT.PUT_LINE ('LAST .. PROD_IDX  : ' || prod_idx);

                  rws.AddInstance();

                  rws.PieceWise();

                  

                  rws.SetNumber(id1);

                  rws.SetNumber(bin1);

                  rws.SetNumber(bin2);

                  rws.SetNumber(bin3);

                  rws.SetNumber(bin4);

                  rws.SetNumber(bin5);

                  rws.SetNumber(bin6);

                  rws.SetNumber(bin7);

                  rws.SetNumber(bin8);

                  rws.SetNumber(bin9);

                  

                  rws.SetVarchar2(durable_id);

                  rws.SetNumber(durable_pos);

                  rws.SetNumber(in_qty);

                  rws.SetVarchar2(lot_id);

                  rws.SetVarchar2(machine_id);

                  rws.SetNumber(ng_qty);

                  rws.SetVarchar2(operator);

                  rws.SetNumber(out_qty);

                  rws.SetVarchar2(proc_oper_id);

                  rws.SetVarchar2(prod_spec_id);

                  rws.SetVarchar2(l_list);

                  rws.SetNumber(prod_idx);

                  rws.SetVarchar2(tkin_time);

                  rws.SetVarchar2(tkout_time);

                  rws.EndCreate();

                  EXIT;

               END IF;

               

            END LOOP;

            DBMS_OUTPUT.PUT_LINE ('1st LOOP END !  : ' || l_list);

            EXIT;

        END LOOP;

        DBMS_OUTPUT.PUT_LINE ('2nd LOOP END !  : ' || l_list);

        

        -- DBMS_SQL.CLOSE_CURSOR(atlas_pkg.r_sql.cursor);

        atlas_pkg.r_sql.finished := 0;

    END IF;

    -- atlas_pkg.r_sql.finished := 10;

    DBMS_OUTPUT.PUT_LINE ('TOTAL  : ' || l_total_row);

    RETURN ODCIConst.Success;

END;

------------------------------------------------------------------------------------

MEMBER FUNCTION ODCITableClose

                              (

                                  SELF IN ramos_odci_clob

                              )

    RETURN NUMBER

IS

BEGIN

    atlas_pkg.r_sql          := NULL;

    atlas_pkg.r_sql.finished := 0;

    DBMS_OUTPUT.PUT_LINE ('ODCITableClose entered !  : ');

    RETURN ODCIConst.Success;

END;

END;

​

​

create or replace FUNCTION  productExplodeEvalCLob(inp_cur IN RAMOS_ODCI_CLOB_PKG.cur)

RETURN SYS.AnyDataSet PIPELINED PARALLEL_ENABLE (PARTITION inp_cur BY ANY)

USING RAMOS_ODCI_CLOB;

​

​

-- select * from table (

--  productExplodeEvalCLob(cursor(select * from LOT_SUM where lot_id = 'WKE21X1B31' AND machine_id='48PARA-03' AND DURABLE_ID='Z718')));
```
