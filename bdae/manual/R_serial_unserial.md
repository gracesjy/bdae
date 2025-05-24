### R Serialization, Unserialization

1. Serialization
   다음을 예제를 샘플로 삼자.
   
   ```
    library(RProtoBuf)
    buf <- RProtoBuf::serialize_pb(iris, NULL)
    
    raw.lst <- vector("list", 1)
    raw.lst[[1L]] <- buf
    df <- data.frame(name='serial01',stringsAsFactors=FALSE)
    df$blob <- raw.lst
    df
   ```
   SQL 문은 다음과 같다.
   ```
    SELECT *
       FROM
       table(asEval(
       NULL,
       'SELECT CAST(''A'' AS VARCHAR2(40)) "name", TO_BLOB(NULL) "blob" FROM dual',
       'R_serial_new'))
   ```
    
3. DeSerialization
   앞의 Serialization 을 다시 풀어서 사용, 예를 들면 예측(Inference) 하기 위한 것이다.
   ```
    # data, args
    
    library(RProtoBuf)
    x = args$blob
    class(x) <- class(x)[-match("AsIs", class(x))]
    d <- x[[1]]
    class(d) <- class(d)[-match("AsIs", class(d))]
    pdf <- RProtoBuf::unserialize_pb(d)
    pdf$Species <- as.character(pdf$Species)
    pdf
   ```
   이것의 SQL 문은 다음과 같다.<br>
   ```
    select *
    from table(
        asEval(
           cursor(
              SELECT "name", "data" as "blob" FROM serial WHERE "name" = 'serial01'
           ),
           'select 1.0 A, 1.0 B, 1.0 C, 1.0 D, cast(''A'' as VARCHAR2(4000)) species from dual',
           'R_unserial'))
   ```

   참고로, 위에서 사용한 args 부분에 해당되는 아래 SQL 문은 1. Serialization 의 리턴 값을 테이블에 입력한 것이다.
   ```
    SELECT "name", "data" as "blob" FROM serial WHERE "name" = 'serial01',
    
   ```
4. BDAE SQL 은 섞이면 안된다.
   아래 처럼 섞으면 작동하지 않는다. 그 이유는 분석은 데이터를 모아서 해야 하는데, CURSOR() 작동에 문제가 생긴다.<br>
   임시 테이블을 사용하거나, R 패키지를 만들어서 사용하라.
   ```
    select *
      from table(
          asEval(
             cursor(
    		   SELECT * 
    		   FROM
    		   table(asEval(
    		   NULL,
    		   'SELECT CAST(''A'' AS VARCHAR2(40)) "name", TO_BLOB(NULL) "blob" FROM dual',
    		   'R_serial_new')) 
             ),
             'select 1.0 A, 1.0 B, 1.0 C, 1.0 D, cast(''A'' as VARCHAR2(4000)) species from dual',
             'R_unserial'));
   ```
