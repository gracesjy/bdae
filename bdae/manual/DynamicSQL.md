### Dynamic SQL

```
CREATE PACKAGE dla_pkg AS

   /*
   || Pipelined function interface.
   */
   FUNCTION query_view(
            p_stmt IN VARCHAR2
            ) RETURN ANYDATASET PIPELINED USING dla_ot;

   /*
   || Record types for use across multiple DLA_OT methods.
   */
   TYPE rt_dynamic_sql IS RECORD
   ( cursor      INTEGER
   , column_cnt  PLS_INTEGER
   , description DBMS_SQL.DESC_TAB2
   , execute     INTEGER
   );

   TYPE rt_anytype_metadata IS RECORD
   ( precision PLS_INTEGER
   , scale     PLS_INTEGER
   , length    PLS_INTEGER
   , csid      PLS_INTEGER
   , csfrm     PLS_INTEGER
   , schema    VARCHAR2(30)
   , type      ANYTYPE
   , name      VARCHAR2(30)
   , version   VARCHAR2(30)
   , attr_cnt  PLS_INTEGER
   , attr_type ANYTYPE
   , attr_name VARCHAR2(128)
   , typecode  PLS_INTEGER
   );

   /*
   || State variable for use across multiple DLA_OT methods.
   */
   r_sql rt_dynamic_sql;

END dla_pkg; 
```

```
CREATE OR REPLACE TYPE GPM.dla_ot AS OBJECT
 (
   atype ANYTYPE --<-- transient record type

 , STATIC FUNCTION ODCITableDescribe(
                   rtype OUT ANYTYPE,
                   stmt  IN  VARCHAR2
                   ) RETURN NUMBER

 , STATIC FUNCTION ODCITablePrepare(
                   sctx    OUT dla_ot,
                   tf_info IN  sys.ODCITabFuncInfo,
                   stmt    IN  VARCHAR2
                   ) RETURN NUMBER

 , STATIC FUNCTION ODCITableStart(
                   sctx IN OUT dla_ot,
                   stmt IN     VARCHAR2
                   ) RETURN NUMBER

 , MEMBER FUNCTION ODCITableFetch(
                   SELF  IN OUT dla_ot,
                   nrows IN     NUMBER,
                   rws   OUT    ANYDATASET
                   ) RETURN NUMBER

 , MEMBER FUNCTION ODCITableClose(
                   SELF IN dla_ot
                   ) RETURN NUMBER
 );
 
CREATE OR REPLACE TYPE BODY GPM.dla_ot
AS
STATIC FUNCTION ODCITableDescribe(
                    rtype OUT ANYTYPE,
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
                     sctx    OUT dla_ot,
                     tf_info IN  sys.ODCITabFuncInfo,
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
        sctx := dla_ot(r_meta.type);

        RETURN ODCIConst.Success;

     END;
	      STATIC FUNCTION ODCITableStart(
                     sctx IN OUT dla_ot,
                     stmt IN     VARCHAR2
                     ) RETURN NUMBER IS

        r_meta dla_pkg.rt_anytype_metadata;

    BEGIN

        /*
        || We now describe the cursor again and use this and the described
        || ANYTYPE structure to define and execute the SQL statement...
        */
        dla_pkg.r_sql.cursor := DBMS_SQL.OPEN_CURSOR;
        DBMS_SQL.PARSE( dla_pkg.r_sql.cursor, stmt, DBMS_SQL.NATIVE );
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
                     SELF   IN OUT dla_ot,
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
                     SELF IN dla_ot
    ) RETURN NUMBER IS
     BEGIN
        DBMS_SQL.CLOSE_CURSOR( dla_pkg.r_sql.cursor );
        dla_pkg.r_sql := NULL;
        RETURN ODCIConst.Success;
     END;

  END;
  
```
