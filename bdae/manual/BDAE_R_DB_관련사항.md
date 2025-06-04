### BDAE R 모듈 DB 관련 사항

DATETIME 관련이다.  아래 TKIN_TIME, TKOUT_TIME 은 오라클 TimeStamp 데이터 타입이다.<br>
***asTableEval***

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

다음은 asRowEval 에 대한 예제이다. <br>
아래 TO_CHAR(VALUE) 부분은 OverFlow 오류가 나기 때문인데, 그 이유는 <br>
아래 임의로 의미 없는 ? 100 Row 마다 TitanicDescribe 를 수행하게 하였는데, <br>
100 건의 데이터의 NA 가 많아서 Infinity 에 가까운 숫자가 나오는데, JAVA 에서 <br>
처리가 안되어 문자열로 변경한 것 뿐이다.

***asRowEval***
```
SELECT VARS, VARIABLE, TO_CHAR(VALUE) AS VALUE FROM (
SELECT * 
      FROM table(asRowEval(
         	cursor(SELECT * FROM TITANIC),
         	NULL,
            'SELECT CAST(''A'' as VARCHAR2(40)) as vars, CAST(''A'' as VARCHAR2(40)) variable,
            1.0 value FROM dual',
            100, -- 매 100 Row 마다
           'TitanicDescribe')))
```

<br><br>
단 1개의 컬럼의 출력이 예전에는 안되었지만, 수정했다.
```
SELECT * 
   FROM 
   table(asEval( 
   NULL, 
   'SELECT TO_TIMESTAMP(NULL) start_date
    FROM dual', 
   'R_date_single'))
```
R_date_single 은 다음이다.
```
 function() {
   one_time <- as.POSIXct("2015-10-19 10:15")
   emp.data <- data.frame(
      start_date = c(one_time, one_time, one_time, one_time, one_time),
      stringsAsFactors = FALSE
   )

   return (emp.data)
}
```
***asGroupEvalParallel***
```
SELECT *
FROM table(asGroupEvalParallel(
  CURSOR(
            SELECT EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID,VALUE
              FROM fdc_trace 
              WHERE 1=1 
                AND EQP_ID='EQP-200'
                AND UNIT_ID='UNIT-02'
                AND LOT_ID='LOTB-101'
                AND RECIPE='RECIPE-200'
                AND PARAM_ID IN ('param_b-36', 'param_b-35')
            ),
  CURSOR(
     SELECT * FROM V_TITANIC
  ),
     'V_SIMPLE_RET',
            'EQP_ID,UNIT_ID,LOT_ID,WAFER_ID,RECIPE,PARAM_ID',       
           'ArrayProcessing'))

-- V_SIMPLE_RET
CREATE OR REPLACE VIEW "RQUSER"."V_SIMPLE_RET" ("A", "B", "C") AS 
  SELECT 
   1 A,
   CAST('A' as VARCHAR2(20)) B,
   CAST('A' as VARCHAR2(20)) C
  FROM dual;

```
ArrayProcessing 는 다음과 같다.
```
function(data, args) {

    library(logr)
    library(xts)
    library(quantmod)
    library(RCurl)
    library(log4r)
    library(xts)
    library(quantmod)
    library(RCurl)
    library(RProtoBuf)
   
    log_open("/tmp/rlog2.log")
    log_print("Here is a test log statement")
    #log_print(class(args1))
    log_print("data count : ")
    log_print(nrow(data))
    log_print(names(data))
    log_print("args count : ")
    log_print(nrow(args))
    log_print(names(args))
    log_print(args)
    log_print('========')


    resno <- c(101, 102, 103, 104, 105)
    rname <- c('ANDREA', 'NY', 'YANIS', 'CLEVETH', 'ASHIYA')
    rage <- c('51', '23', '52', '76', '98')
    df <- data.frame(resno, rname, rage, stringsAsFactors=FALSE)
    return (df)
```
***asEval***
```
SELECT * 
   FROM 
   table(asEval( 
   NULL, 
   'SELECT CAST(''A'' AS VARCHAR2(40)) PATH, 
           TO_CLOB(NULL) img 
    FROM dual', 
   'Graph_R_02'))
```
Graph_R_02 는 다음과 같다.
```
library(plotly)
library(htmltools)
p <- plot_ly(midwest, x = ~percollege, color = ~state, type = "box")
ppc <- htmltools::div(p, align='center')
htmltools::save_html(ppc, '/tmp/test04.html')
rawHTML01 <- paste(readLines('/tmp/test04.html'), collapse='\n')
unlink('/tmp/test04.html')

p2 <- plot_ly(
  x = c(-9, -6, -5, -3, -1), 
  y = c(0, 1, 4, 5, 7), 
  z = matrix(c(10, 10.625, 12.5, 15.625, 20, 5.625, 6.25, 8.125, 11.25, 15.625, 2.5, 3.125, 5, 8.125, 12.5, 0.625, 1.25, 3.125,
        6.25, 10.625, 0, 0.625, 2.5, 5.625, 10), nrow = 5, ncol = 5), 
  type = "contour" 
)

ppc2 <- htmltools::div(p2, align='center')
htmltools::save_html(ppc2, '/tmp/test05.html')
rawHTML02 <- paste(readLines('/tmp/test05.html'), collapse='\n')
unlink('/tmp/test05.html')

month <- c('January', 'February', 'March', 'April', 'May', 'June', 'July',
           'August', 'September', 'October', 'November', 'December')
high_2014 <- c(28.8, 28.5, 37.0, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9)
low_2014 <- c(12.7, 14.3, 18.6, 35.5, 49.9, 58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1)
data <- data.frame(month, high_2014, low_2014)
data$average_2014 <- rowMeans(data[,c("high_2014", "low_2014")])

#The default order will be alphabetized unless specified as below:
data$month <- factor(data$month, levels = data[["month"]])

p3 <- plot_ly(data, x = ~month, y = ~high_2014, type = 'scatter', mode = 'lines',
        line = list(color = 'transparent'),
        showlegend = FALSE, name = 'High 2014') %>%
  add_trace(y = ~low_2014, type = 'scatter', mode = 'lines',
            fill = 'tonexty', fillcolor='rgba(0,100,80,0.2)', line = list(color = 'transparent'),
            showlegend = FALSE, name = 'Low 2014') %>%
  add_trace(x = ~month, y = ~average_2014, type = 'scatter', mode = 'lines',
            line = list(color='rgb(0,100,80)'),
            name = 'Average') %>%
  layout(title = "Average, High and Low Temperatures in New York",
         paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(229,229,229)',
         xaxis = list(title = "Months",
                      gridcolor = 'rgb(255,255,255)',
                      showgrid = TRUE,
                      showline = FALSE,
                      showticklabels = TRUE,
                      tickcolor = 'rgb(127,127,127)',
                      ticks = 'outside',
                      zeroline = FALSE),
         yaxis = list(title = "Temperature (degrees F)",
                      gridcolor = 'rgb(255,255,255)',
                      showgrid = TRUE,
                      showline = FALSE,
                      showticklabels = TRUE,
                      tickcolor = 'rgb(127,127,127)',
                      ticks = 'outside',
                      zeroline = FALSE))

ppc3 <- htmltools::div(p3, align='center')
htmltools::save_html(ppc3, '/tmp/test06.html')
rawHTML03 <- paste(readLines('/tmp/test06.html'), collapse='\n')
unlink('/tmp/test06.html')


trace_0 <- rnorm(100, mean = 5)
trace_1 <- rnorm(100, mean = 0)
trace_2 <- rnorm(100, mean = -5)
x <- c(1:100)

data <- data.frame(x, trace_0, trace_1, trace_2)

p4 <- plot_ly(data, x = ~x, y = ~trace_0, name = 'trace 0', type = 'scatter', mode = 'lines') %>%
  add_trace(y = ~trace_1, name = 'trace 1', mode = 'lines+markers') %>%
  add_trace(y = ~trace_2, name = 'trace 2', mode = 'markers')

ppc4 <- htmltools::div(p4, align='center')
htmltools::save_html(ppc4, '/tmp/test07.html')
rawHTML04 <- paste(readLines('/tmp/test07.html'), collapse='\n')
unlink('/tmp/test07.html')
airquality_sept <- airquality[which(airquality$Month == 9),]
airquality_sept$Date <- as.Date(paste(airquality_sept$Month, airquality_sept$Day, 1973, sep = "."), format = "%m.%d.%Y")

p5 <- plot_ly(airquality_sept) %>%
  add_trace(x = ~Date, y = ~Wind, type = 'bar', name = 'Wind',
            marker = list(color = '#C9EFF9'),
            hoverinfo = "text",
            text = ~paste(Wind, ' mph')) %>%
  add_trace(x = ~Date, y = ~Temp, type = 'scatter', mode = 'lines', name = 'Temperature', yaxis = 'y2',
            line = list(color = '#45171D'),
            hoverinfo = "text",
            text = ~paste(Temp, '??F')) %>%
  layout(title = 'New York Wind and Temperature Measurements for September 1973',
         xaxis = list(title = ""),
         yaxis = list(side = 'left', title = 'Wind in mph', showgrid = FALSE, zeroline = FALSE),
         yaxis2 = list(side = 'right', overlaying = "y", title = 'Temperature in degrees F', showgrid = FALSE, zeroline = FALSE))

ppc5 <- htmltools::div(p5, align='center')
htmltools::save_html(ppc5, '/tmp/test08.html')
rawHTML05 <- paste(readLines('/tmp/test08.html'), collapse='\n')
unlink('/tmp/test08.html')

hdr <- c('plot01','plot02','plot03','plot04','plot05')
rawHTMLs <- c(rawHTML01, rawHTML02, rawHTML03, rawHTML04, rawHTML05)
df <- data.frame(hdr, rawHTMLs, stringsAsFactors=FALSE)
df
```
