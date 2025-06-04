### BDAE R 모듈 DB 관련 사항

DATETIME 관련이다.  아래 TKIN_TIME, TKOUT_TIME 은 오라클 TimeStamp 데이터 타입이다.<br>

```
SELECT * 
      FROM 
        table(asTableEval( 
          cursor(SELECT ID, BIN1, BIN2, DURABLE_ID, LOT_ID, TKIN_TIME, TKOUT_TIME FROM LOT_SUM), 
          NULL,
          'V_LOTSUM',
          'R_lotsum'))

-- 아래는 위의 V_LOTSUM View 이다.
CREATE VIEW V_LOTSUM AS SELECT ID, BIN1, BIN2, DURABLE_ID, LOT_ID, TKIN_TIME, TKOUT_TIME FROM LOT_SUM WHERE ROWNUM < 1
```

R_lotsum R 모듈은 단순하다.<br>
오라클 Input Query Data 를 받아서 그대로 다시 던져주는 것이다. <br>
이건 단순히 Timestamp 를 테스트 하기 위한 것 뿐이다.

```
# NEW_TYPE
# variable data supplided by BDAE
library(psych)
library(reshape)
library(logr)

log_open("/tmp/rlog2.log")
log_print("------")
log_print(nrow(data))
log_print(names(data))
log_print(data)
df <- data
df
```

다음은 기술통계량을 테스트 하면서 
```
SELECT * 
      FROM table(asTableEval(
         	cursor(SELECT ID, BIN1, BIN2, DURABLE_ID, LOT_ID, TKIN_TIME, TKOUT_TIME FROM LOT_SUM),
         	cursor(SELECT * FROM TITANIC),
            'SELECT CAST(''A'' as VARCHAR2(40)) as vars, CAST(''A'' as VARCHAR2(40)) variable,
           1.0 value FROM dual',
           'TitanicDescribeByArgs'))
```

TitanicDescribeByArgs 는 다음과 같다.  TITANIC 테이블에 대한 기술통계량을 args 쪽으로 돌린 것이다.<br>
LOT_SUM 테이블은 Timestamp 를 Query 하는지 확인하기 위한 것일 뿐이다.<br>
아래의 R 모듈은 반드시 SCRIPT_TYPE 컬럼(RSCRIPT 테이블)이 Normal 이 아니어야 한다. <br>
그러면 data, args 가 반드시 고정된 변수다. <br>
위의 cursor(SELECT ID, BIN1, BIN2, DURABLE_ID, LOT_ID, TKIN_TIME, TKOUT_TIME FROM LOT_SUM) --> data 변수<br>
위의 cursor(SELECT * FROM TITANIC) --> args 변수 <br>

```
# NEW_TYPE
# variable data supplided by BDAE
library(psych)
library(reshape)
library(logr)

log_open("/tmp/rlog2.log")
log_print("------")
log_print(nrow(data))
log_print(names(data))
log_print(data)

df_des <- describe(args)
df_des <- cbind(vars_name=rownames(df_des),df_des)
df_des_select = subset(df_des, select=-vars)
df_des_select_unpivot = melt(df_des_select,id=c('vars_name'))
df_des_select_unpivot$variable <- as.character(df_des_select_unpivot$variable)
df_des_select_unpivot
```
