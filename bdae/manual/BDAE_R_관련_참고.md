## BDAE R 관련 참고 사항

R 은 디버깅하기 매우 어렵다. <br>
따라서 원칙을 반드시 지켜야 한다.  그렇지 않으면 오류를 찾기 어렵다. <br>
library 나 특정 오브젝트의 잘못된 타이핑은 찾아낼 수 있지만, 그 이상은 어렵다. <br>
다음은 알아 두자. <br>

### 데이터타입

1.  주는 데이터 타입
    VARCHAR2, NUMBER 로 가급적으로 형 변환 후 주는 것이 좋다. <br>
    NULL 부분은 처리가 되지만, 그래도 믿지는 말자. <br>
    2025.05.21 에 대부분의 NULL 처리는 완결 되었다. <br>

2.  R 코드 작성 시 주의 사항
    작성된 R 코드는 반드시 data.frame 포맷이어야 한다.<br>
    factor 로 된 부분은 반드시 string 으로 변경되어야 한다. <br>
    그래서 stringsAsFactor = FALSE 가 있는 것이고 이를 적용해서 data.frame 을 만들어야 한다.<br>
    DateTime 부분은 코딩을 했지만, 왠만하면 String 포맷으로 data.frame 에서 적용해서 리턴해라.<br>

    ```
    function() {
       emp.data <- data.frame(
       emp_id = c (1:5), 
       emp_name = c("Rick","Dan","Michelle","Ryan","Gary"),
       salary = c(623.3,515.2,611.0,729.0,843.25), 
       
       start_date = as.Date(c("2012-01-01", "2013-09-23", "2014-11-15", "2014-05-11",
          "2015-03-27")),
       stringsAsFactors = FALSE
       )
    
       return (emp.data)
    }

    ```
    위의 모듈을 테스트 하는 SQL 은 다음과 같다.
    ```
    SELECT * 
       FROM 
       table(asEval( 
       NULL, 
       'SELECT 1 as emp_id, CAST(''A'' AS VARCHAR2(40)) emp_name, 
               1.0 as salaray,  TO_DATE(NULL) start_date
        FROM dual', 
       'R_date'))
    ```

    이것에 대한 BDAE 코드 부분이다.<br>
    DateVector 는 Date 을 여러개 품고 있다. 주의하자. <br>
    ```
    Rcpp::DateVector dtv = df[k]; // @suppress("Invalid arguments")
    Rcpp::Date dt = dtv[j]; // @suppress("Invalid arguments")
    ```


