## R 오라클 연결 방법

다른 것들과 동일하지만, 먼저 TNS 를 사용하는 법<br>
먼저 DBI, ROracle 설치할 것
```
Sys.setenv("ORACLE_HOME"="/u01/app/oracle/product/12.2.0.1/db_1")
library(ROracle)
library(DBI)
drv <- Oracle()
conn <- dbConnect(drv, "rquser", "nebula", "EXADB")
cur <- dbSendQuery(conn,
"SELECT *
 FROM (
   SELECT IDX, ITEM_NAME, ITEM_VALUE
   FROM SPC_DATA
   )
   PIVOT (MAX(ITEM_VALUE) AS ITEM_VALUE FOR (ITEM_NAME)
   IN (
    'ITEM01' AS ITEM01,
    'ITEM02' AS ITEM02,
    'ITEM03' AS ITEM03,
    'ITEM04' AS ITEM04,
    'ITEM05' AS ITEM05
   )
 ) ORDER BY IDX"
)
df <- dbFetch(cur)
```

두번째는 thin client 연결 방법
```
library(DBI)
library(ROracle)

driv <- dbDriver("Oracle")

connect.string <- paste(
  "(DESCRIPTION=",
  "(ADDRESS=(PROTOCOL = TCP)(HOST = 177.175.54.97)(PORT = 1521))",
  "(CONNECT_DATA=(SERVER = DEDICATED)",
  "(SERVICE_NAME = FREE)))", sep = "")

conn <- dbConnect(driv, username="rquser", password="nebula", dbname=connect.string)
df <- dbGetQuery(conn,"SELECT * FROM FDC_TRACE WHERE ROWNUM < 10")
```
