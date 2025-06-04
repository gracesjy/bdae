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
