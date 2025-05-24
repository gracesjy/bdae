### BDAE R 예외처리 방법

2017년 이후 Python 보다 R 의 예외처리는 세련되지 못하다고 생각했다.<br>
try catch 등 아무리 해도 라인까지 보여주지 못했다.<br>
특히 Syntax 오류를 일부러 주었을 때 죽는 문제가 있었다.
<br>

2025년 5월 24일에 다음을 적용하기로 했다.<br>
1.  R 의 parse('검증코드.r') 의 Syntax 점검을 실행전 먼저 수행한다.
    다음과 같이 나타난다. 이것은 2025년 5월 24일에 생각해서 적용, 테스트 했다.<br>
    R 엔진에서 parse('R_ml_new.r') 형태로 검증하기 때문에 Temp 파일을 생성 후 진행한다.<br>
    ```
    StatementCallback; uncategorized SQLException for SQL
       [SELECT * FROM table(asEval( NULL, 'SELECT CAST(''A'' AS VARCHAR2(40)) HEADER, TO_BLOB(NULL) IMG FROM dual', 'R_ml_new'))];
       SQL state [72000]; error code [20001]; ORA-20001: R_Eval_ODCITableFetch(),executeREval() failed.
       R syntax error exception : [[Error in parse("R_ml_new") : R_ml_new:10:5: unexpected symbol 9: 10: for i ^ ]]
       ORA-06512: "RQUSER.ASEVALIMPL", 112? https://docs.oracle.com/error-help/db/ora-20001/; nested exception is java.sql.SQLException:
       ORA-20001: R_Eval_ODCITableFetch(),executeREval() failed.R syntax error exception : [[Error in parse("R_ml_new")
       : R_ml_new:10:5: unexpected symbol 9: 10: for i ^ ]] ORA-06512: "RQUSER.ASEVALIMPL", 112? https://docs.oracle.com/error-help/db/ora-20001/
    ```
    위의 "R syntax error exception : [[Error in parse("R_ml_new") : R_ml_new:10:5: unexpected symbol 9: 10: for i ^ ]]" 는 정확히<br>
    다음과 같이 정확하게 Syntax 오류 라인 위치를 보여준다.<br>
    ```
        9:
        10: for i
                ^

        ]])
    ```
    
3.  실행했을 때에는 어쩔 수 없는 traceback() 을 활용한다.
    실행 시 특정 syntax 때문에 R Engine 이 죽는 현상이 그 동안 있어 왔었다.<br>
    library 가 없다든지, 특정 object (변수)가 잘못 된 것은 runtime 에서 찾을 수 있다.<br>
    그러나, 이것은 또 Syntax 오류가 아니기 때문에 서로 보완되어야 할 사항이다. <br>
    
