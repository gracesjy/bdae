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

## R data.frame into Oracle Database
```
library(ROracle)
driv <- dbDriver("Oracle")
connect.string <- paste(
  "(DESCRIPTION=",
  "(ADDRESS=(PROTOCOL = TCP)(HOST = 127.0.0.1)(PORT = 1521))",
  "(CONNECT_DATA=(SERVER = DEDICATED)",
  "(SERVICE_NAME = FREE)))", sep = "")
conn <- dbConnect(driv, username="rquser", password="nebula", dbname=connect.string)
df_read <- dbGetQuery(conn,"SELECT * FROM FDC_TRACE WHERE ROWNUM < 10")
df_read

## make data.frame from csv file or something.
df <-  read.csv('wisc_bc_data.csv')
names(df)
 [1] "id"                "diagnosis"         "radius_mean"      
 [4] "texture_mean"      "perimeter_mean"    "area_mean"        
 [7] "smoothness_mean"   "compactness_mean"  "concavity_mean"   
[10] "points_mean"       "symmetry_mean"     "dimension_mean"   
[13] "radius_se"         "texture_se"        "perimeter_se"     
[16] "area_se"           "smoothness_se"     "compactness_se"   
[19] "concavity_se"      "points_se"         "symmetry_se"      
[22] "dimension_se"      "radius_worst"      "texture_worst"    
[25] "perimeter_worst"   "area_worst"        "smoothness_worst" 
[28] "compactness_worst" "concavity_worst"   "points_worst"     
[31] "symmetry_worst"    "dimension_worst"  

dbWriteTable(conn, "wisc_bc_data", df) 
[1] TRUE

dbCommit(conn)
[1] TRUE
> quit()
```
