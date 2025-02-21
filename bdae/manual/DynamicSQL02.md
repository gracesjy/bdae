### Dynamic SQL Example
** by ATLAS, Raymond **

```
create or replace NONEDITIONABLE TYPE dyn_atlas AS OBJECT
 (
   atype ANYTYPE --<-- transient record type

 , STATIC FUNCTION ODCITableDescribe(
                   rtype OUT ANYTYPE,
                   inp_cur IN SYS_REFCURSOR,
                   ref_cur IN SYS_REFCURSOR,
                   stmt  IN  VARCHAR2
                   ) RETURN NUMBER

 , STATIC FUNCTION ODCITablePrepare(
                   sctx    OUT dyn_atlas,
                   tf_info IN  sys.ODCITabFuncInfo,
                   inp_cur IN SYS_REFCURSOR,
                   ref_cur IN SYS_REFCURSOR,
                   stmt    IN  VARCHAR2
                   ) RETURN NUMBER

 , STATIC FUNCTION ODCITableStart(
                   sctx IN OUT dyn_atlas,
                   inp_cur IN SYS_REFCURSOR,
                   ref_cur IN SYS_REFCURSOR,
                   stmt IN     VARCHAR2
                   ) RETURN NUMBER

 , MEMBER FUNCTION ODCITableFetch(
                   SELF  IN OUT dyn_atlas,
                   nrows IN     NUMBER,
                   rws   OUT    ANYDATASET
                   ) RETURN NUMBER

 , MEMBER FUNCTION ODCITableClose(
                   SELF IN dyn_atlas
                   ) RETURN NUMBER
 );
```

```
create or replace NONEDITIONABLE TYPE BODY dyn_atlas
AS
STATIC FUNCTION ODCITableDescribe(
                    rtype OUT ANYTYPE,
                    inp_cur IN OUT SYS_REFCURSOR,
                    ref_cur IN OUT SYS_REFCURSOR,
                    stmt  IN  VARCHAR2
                    ) RETURN NUMBER IS

       r_sql   dla_pkg.rt_dynamic_sql;
       v_rtype ANYTYPE;

   BEGIN

       /*
       || Parse the SQL and describe its format and structure.
       */
       r_sql.cursor := DBMS_SQL.OPEN_CURSOR;
       DBMS_SQL.PARSE( r_sql.cursor, stmt, DBMS_SQL.NATIVE );
       DBMS_SQL.DESCRIBE_COLUMNS2( r_sql.cursor, r_sql.column_cnt, r_sql.description );
       DBMS_SQL.CLOSE_CURSOR( r_sql.cursor );

       /*
       || Create the ANYTYPE record structure from this SQL structure.
       || Replace LONG columns with CLOB...
       */
       ANYTYPE.BeginCreate( DBMS_TYPES.TYPECODE_OBJECT, v_rtype );

       FOR i IN 1 .. r_sql.column_cnt LOOP

          v_rtype.AddAttr( r_sql.description(i).col_name,
                           CASE
                              --<>--
                              WHEN r_sql.description(i).col_type IN (1,96,11,208)
                              THEN DBMS_TYPES.TYPECODE_VARCHAR2
                              --<>--
                              WHEN r_sql.description(i).col_type = 2
                              THEN DBMS_TYPES.TYPECODE_NUMBER
                              ----
                              WHEN r_sql.description(i).col_type IN (8,112)
                              THEN DBMS_TYPES.TYPECODE_CLOB
                              --<>--
                              WHEN r_sql.description(i).col_type = 12
                              THEN DBMS_TYPES.TYPECODE_DATE
                              --<>--
                              WHEN r_sql.description(i).col_type = 23
                              THEN DBMS_TYPES.TYPECODE_RAW
                              --<>--
                              WHEN r_sql.description(i).col_type = 180
                              THEN DBMS_TYPES.TYPECODE_TIMESTAMP
                              --<>--
                              WHEN r_sql.description(i).col_type = 181
                              THEN DBMS_TYPES.TYPECODE_TIMESTAMP_TZ
                              --<>--
                              WHEN r_sql.description(i).col_type = 182
                              THEN DBMS_TYPES.TYPECODE_INTERVAL_YM
                              --<>--
                              WHEN r_sql.description(i).col_type = 183
                              THEN DBMS_TYPES.TYPECODE_INTERVAL_DS
                              --<>--
                              WHEN r_sql.description(i).col_type = 231
                              THEN DBMS_TYPES.TYPECODE_TIMESTAMP_LTZ
                              --<>--
                           END,
                           r_sql.description(i).col_precision,
                           r_sql.description(i).col_scale,
                           r_sql.description(i).col_max_len,
                           r_sql.description(i).col_charsetid,
                           r_sql.description(i).col_charsetform );
       END LOOP;

       v_rtype.EndCreate;

       /*
       || Now we can use this transient record structure to create a table type
       || of the same. This will create a set of types on the database for use
       || by the pipelined function...
       */
       ANYTYPE.BeginCreate( DBMS_TYPES.TYPECODE_TABLE, rtype );
       rtype.SetInfo( NULL, NULL, NULL, NULL, NULL, v_rtype,
                      DBMS_TYPES.TYPECODE_OBJECT, 0 );
       rtype.EndCreate();

       RETURN ODCIConst.Success;

    END;
	    STATIC FUNCTION ODCITablePrepare(
                     sctx    OUT dyn_atlas,
                     tf_info IN  sys.ODCITabFuncInfo,
                     inp_cur IN OUT SYS_REFCURSOR,
                     ref_cur IN OUT SYS_REFCURSOR,
                     stmt    IN  VARCHAR2
                     ) RETURN NUMBER IS

        r_meta dla_pkg.rt_anytype_metadata;

    BEGIN

        /*
        || We prepare the dataset that our pipelined function will return by
        || describing the ANYTYPE that contains the transient record structure...
        */
        r_meta.typecode := tf_info.rettype.GetAttrElemInfo(
                              1, r_meta.precision, r_meta.scale, r_meta.length,
                              r_meta.csid, r_meta.csfrm, r_meta.type, r_meta.name
                              );

        /*
        || Using this, we initialise the scan context for use in this and
        || subsequent executions of the same dynamic SQL cursor...
        */
        sctx := dyn_atlas(r_meta.type);

        RETURN ODCIConst.Success;

     END;



	 STATIC FUNCTION ODCITableStart(
                     sctx IN OUT dyn_atlas,
                     inp_cur IN OUT SYS_REFCURSOR,
                     ref_cur IN OUT SYS_REFCURSOR,
                     stmt IN     VARCHAR2
                     ) RETURN NUMBER IS

        r_meta dla_pkg.rt_anytype_metadata;
        -- r_fetch rt_fetch_attributes;
        cursor_x INTEGER;
        cursor_y INTEGER;
        delimeter VARCHAR2(10);
        l_idx PLS_INTEGER;
        idx PLS_INTEGER;
        total_idx PLS_INTEGER;
        total_sql VARCHAR2(32767);
        v_values VARCHAR2(4000);
    BEGIN

        /*
        || We now describe the cursor again and use this and the described
        || ANYTYPE structure to define and execute the SQL statement...
        */

        cursor_x := DBMS_SQL.TO_CURSOR_NUMBER(inp_cur);
        DBMS_SQL.define_column(cursor_x, 1, v_values, 32767);
        -- DBMS_SQL.DEFINE_COLUMN(cursor_x, 1, v_values);
        -- DBMS_SQL.DEFINE_COLUMN(cursor_x, 2, v_values, 32767);
        LOOP
          IF DBMS_SQL.FETCH_ROWS(cursor_x) = 0 THEN
             EXIT;
          END IF;
          DBMS_SQL.COLUMN_VALUE(cursor_x,1, v_values);
          --    v_values :=r_fetch.v2_column;

          -- END IF;
       END LOOP;
        -- DBMS_SQL.CLOSE_CURSOR (cursor_x);

        total_sql := 'SELECT * FROM (';
        total_sql := total_sql || ' SELECT Y.ROW_, Y.COL_, ';
        total_sql := total_sql || '     CASE ';
        total_sql := total_sql || ' WHEN COL_NAME =''A'' THEN X.A';
        total_sql := total_sql || ' WHEN COL_NAME =''B'' THEN X.B';
        total_sql := total_sql || ' END AS VAL';
        total_sql := total_sql || ' FROM MATRIX Y, T1 X';
        total_sql := total_sql || ' WHERE X.CONTEXT=Y.CONTEXT ';
        total_sql := total_sql || ' AND Y.TABLE_NAME=''T1'' ';
        total_sql := total_sql || ' UNION ';
        total_sql := total_sql || ' SELECT Y.ROW_, Y.COL_, ';
        total_sql := total_sql || ' CASE ';
        total_sql := total_sql || ' WHEN COL_NAME =''C'' THEN X.C ';
        total_sql := total_sql || ' WHEN COL_NAME =''D'' THEN X.D ';
        total_sql := total_sql || ' END AS VAL';
        total_sql := total_sql || ' FROM MATRIX Y, T2 X';
        total_sql := total_sql || ' WHERE X.CONTEXT=Y.CONTEXT ';
        total_sql := total_sql || ' AND Y.TABLE_NAME=''T2'' ';
        total_sql := total_sql || ' UNION ';
        total_sql := total_sql || ' SELECT Y.ROW_, Y.COL_, ';
        total_sql := total_sql || ' CASE ';
        total_sql := total_sql || ' WHEN COL_NAME =''B'' THEN X.B ';
        total_sql := total_sql || ' WHEN COL_NAME =''C'' THEN X.C ';
        total_sql := total_sql || ' END AS VAL ';
        total_sql := total_sql || ' FROM MATRIX Y, T3 X ';
        total_sql := total_sql || ' WHERE X.CONTEXT=Y.CONTEXT';
        total_sql := total_sql || ' AND Y.TABLE_NAME=''T3'' ';
        total_sql := total_sql || ' ) ORDER BY ROW_';
        dla_pkg.r_sql.cursor := DBMS_SQL.OPEN_CURSOR;

        DBMS_SQL.PARSE( dla_pkg.r_sql.cursor, total_sql, DBMS_SQL.NATIVE );
        DBMS_SQL.DESCRIBE_COLUMNS2( dla_pkg.r_sql.cursor,
                                    dla_pkg.r_sql.column_cnt,
                                    dla_pkg.r_sql.description );

        FOR i IN 1 .. dla_pkg.r_sql.column_cnt LOOP

           /*
           || Get the ANYTYPE attribute at this position...
           */
           r_meta.typecode := sctx.atype.GetAttrElemInfo(
                                 i, r_meta.precision, r_meta.scale, r_meta.length,
                                 r_meta.csid, r_meta.csfrm, r_meta.type, r_meta.name
                                 );

           CASE r_meta.typecode
              --<>--
              WHEN DBMS_TYPES.TYPECODE_VARCHAR2
              THEN
                 DBMS_SQL.DEFINE_COLUMN(
                    dla_pkg.r_sql.cursor, i, '', 32767
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_NUMBER
              THEN
                 DBMS_SQL.DEFINE_COLUMN(
                    dla_pkg.r_sql.cursor, i, CAST(NULL AS NUMBER)
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_DATE
              THEN
                 DBMS_SQL.DEFINE_COLUMN(
                    dla_pkg.r_sql.cursor, i, CAST(NULL AS DATE)
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_RAW
              THEN
                 DBMS_SQL.DEFINE_COLUMN_RAW(
                    dla_pkg.r_sql.cursor, i, CAST(NULL AS RAW), r_meta.length
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_TIMESTAMP
              THEN
                 DBMS_SQL.DEFINE_COLUMN(
                    dla_pkg.r_sql.cursor, i, CAST(NULL AS TIMESTAMP)
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_TIMESTAMP_TZ
              THEN
                 DBMS_SQL.DEFINE_COLUMN(
                    dla_pkg.r_sql.cursor, i, CAST(NULL AS TIMESTAMP WITH TIME ZONE)
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_TIMESTAMP_LTZ
              THEN
                 DBMS_SQL.DEFINE_COLUMN(
                    dla_pkg.r_sql.cursor, i, CAST(NULL AS TIMESTAMP WITH LOCAL TIME ZONE)
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_INTERVAL_YM
              THEN
                 DBMS_SQL.DEFINE_COLUMN(
                    dla_pkg.r_sql.cursor, i, CAST(NULL AS INTERVAL YEAR TO MONTH)
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_INTERVAL_DS
              THEN
                 DBMS_SQL.DEFINE_COLUMN(
                    dla_pkg.r_sql.cursor, i, CAST(NULL AS INTERVAL DAY TO SECOND)
                    );
              --<>--
              WHEN DBMS_TYPES.TYPECODE_CLOB
              THEN
                 --<>--
                 CASE dla_pkg.r_sql.description(i).col_type
                    WHEN 8
                    THEN
                       DBMS_SQL.DEFINE_COLUMN_LONG(
                          dla_pkg.r_sql.cursor, i
                          );
                    ELSE
                       DBMS_SQL.DEFINE_COLUMN(
                          dla_pkg.r_sql.cursor, i, CAST(NULL AS CLOB)
                          );
                 END CASE;
              --<>--
           END CASE;
        END LOOP;

        /*
        || The cursor is prepared according to the structure of the type we wish
        || to fetch it into. We can now execute it and we are done for this method...
        */
        dla_pkg.r_sql.execute := DBMS_SQL.EXECUTE( dla_pkg.r_sql.cursor );

        RETURN ODCIConst.Success;

     END;
	      MEMBER FUNCTION ODCITableFetch(
                     SELF   IN OUT dyn_atlas,
                     nrows  IN     NUMBER,
                     rws    OUT    ANYDATASET
                     ) RETURN NUMBER IS

        TYPE rt_fetch_attributes IS RECORD
        ( v2_column    VARCHAR2(32767)
        , num_column   NUMBER
        , date_column  DATE
        , clob_column  CLOB
        , raw_column   RAW(32767)
        , raw_error    NUMBER
        , raw_length   INTEGER
        , ids_column   INTERVAL DAY TO SECOND
        , iym_column   INTERVAL YEAR TO MONTH
        , ts_column    TIMESTAMP
        , tstz_column  TIMESTAMP WITH TIME ZONE
        , tsltz_column TIMESTAMP WITH LOCAL TIME ZONE
        , cvl_offset   INTEGER := 0
        , cvl_length   INTEGER
        );
        r_fetch rt_fetch_attributes;
        r_meta  dla_pkg.rt_anytype_metadata;


     BEGIN

        IF DBMS_SQL.FETCH_ROWS( dla_pkg.r_sql.cursor ) > 0 THEN

           /*
           || First we describe our current ANYTYPE instance (SELF.A) to determine
           || the number and types of the attributes...
           */
           r_meta.typecode := SELF.atype.GetInfo(
                                 r_meta.precision, r_meta.scale, r_meta.length,
                                 r_meta.csid, r_meta.csfrm, r_meta.schema,
                                 r_meta.name, r_meta.version, r_meta.attr_cnt
                                 );

           /*
           || We can now begin to piece together our returning dataset. We create an
           || instance of ANYDATASET and then fetch the attributes off the DBMS_SQL
           || cursor using the metadata from the ANYTYPE. LONGs are converted to CLOBs...
           */
           ANYDATASET.BeginCreate( DBMS_TYPES.TYPECODE_OBJECT, SELF.atype, rws );
           rws.AddInstance();
           rws.PieceWise();

           FOR i IN 1 .. dla_pkg.r_sql.column_cnt LOOP

              r_meta.typecode := SELF.atype.GetAttrElemInfo(
                                    i, r_meta.precision, r_meta.scale, r_meta.length,
                                    r_meta.csid, r_meta.csfrm, r_meta.attr_type,
                                    r_meta.attr_name
                                    );

              CASE r_meta.typecode
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_VARCHAR2
                 THEN
                    DBMS_SQL.COLUMN_VALUE(
                       dla_pkg.r_sql.cursor, i, r_fetch.v2_column
                       );
                    rws.SetVarchar2( r_fetch.v2_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_NUMBER
                 THEN
                    DBMS_SQL.COLUMN_VALUE(
                       dla_pkg.r_sql.cursor, i, r_fetch.num_column
                       );
                    rws.SetNumber( r_fetch.num_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_DATE
                 THEN
                    DBMS_SQL.COLUMN_VALUE(
                       dla_pkg.r_sql.cursor, i, r_fetch.date_column
                       );
                    rws.SetDate( r_fetch.date_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_RAW
                 THEN
                    DBMS_SQL.COLUMN_VALUE_RAW(
                       dla_pkg.r_sql.cursor, i, r_fetch.raw_column,
                       r_fetch.raw_error, r_fetch.raw_length
                       );
                    rws.SetRaw( r_fetch.raw_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_INTERVAL_DS
                 THEN
                    DBMS_SQL.COLUMN_VALUE(
                       dla_pkg.r_sql.cursor, i, r_fetch.ids_column
                       );
                    rws.SetIntervalDS( r_fetch.ids_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_INTERVAL_YM
                 THEN
                    DBMS_SQL.COLUMN_VALUE(
                       dla_pkg.r_sql.cursor, i, r_fetch.iym_column
                       );
                    rws.SetIntervalYM( r_fetch.iym_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_TIMESTAMP
                 THEN
                    DBMS_SQL.COLUMN_VALUE(
                       dla_pkg.r_sql.cursor, i, r_fetch.ts_column
                       );
                    rws.SetTimestamp( r_fetch.ts_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_TIMESTAMP_TZ
                 THEN
                    DBMS_SQL.COLUMN_VALUE(
                       dla_pkg.r_sql.cursor, i, r_fetch.tstz_column
                       );
                    rws.SetTimestampTZ( r_fetch.tstz_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_TIMESTAMP_LTZ
                 THEN
                    DBMS_SQL.COLUMN_VALUE(
                       dla_pkg.r_sql.cursor, i, r_fetch.tsltz_column
                       );
                    rws.SetTimestamplTZ( r_fetch.tsltz_column );
                 --<>--
                 WHEN DBMS_TYPES.TYPECODE_CLOB
                 THEN
                    --<>--
                    CASE dla_pkg.r_sql.description(i).col_type
                       WHEN 8
                       THEN
                          LOOP
                             DBMS_SQL.COLUMN_VALUE_LONG(
                                dla_pkg.r_sql.cursor, i, 32767, r_fetch.cvl_offset,
                                r_fetch.v2_column, r_fetch.cvl_length
                                );
                             r_fetch.clob_column := r_fetch.clob_column ||
                                                    r_fetch.v2_column;
                             r_fetch.cvl_offset := r_fetch.cvl_offset + 32767;
                             EXIT WHEN r_fetch.cvl_length < 32767;
                          END LOOP;
                       ELSE
                          DBMS_SQL.COLUMN_VALUE(
                             dla_pkg.r_sql.cursor, i, r_fetch.clob_column
                             );
                       END CASE;
                       rws.SetClob( r_fetch.clob_column );
                 --<>--
              END CASE;
           END LOOP;

           /*
           || Our ANYDATASET instance is complete. We end our create session...
           */
           rws.EndCreate();

        END IF;

        RETURN ODCIConst.Success;

     END;

	MEMBER FUNCTION ODCITableClose(
                     SELF IN dyn_atlas
    ) RETURN NUMBER IS
     BEGIN
        DBMS_SQL.CLOSE_CURSOR( dla_pkg.r_sql.cursor );
        dla_pkg.r_sql := NULL;
        RETURN ODCIConst.Success;
     END;

  END;
```

```
create or replace NONEDITIONABLE FUNCTION  sampleODCI(inp_cur IN SYS_REFCURSOR,
ref_cur IN SYS_REFCURSOR, p_stmt IN VARCHAR2)
RETURN ANYDATASET PIPELINED USING dyn_atlas;
```

```
SELECT * FROM table(
  sampleODCI(CURSOR(SELECT 'AAAA' AS name FROM dual), CURSOR(SELECT 'AAAA' AS name FROM dual), 'SELECT 1 AS ROW_, 1 AS COL_, CAST(''A'' AS VARCHAR2(40)) AS VAL FROM DUAL'));

```
