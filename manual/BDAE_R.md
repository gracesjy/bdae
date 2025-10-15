## BDAE R Basic
분석가는 R 개발 시에 R Studio 나 Jupyter Notebook 을 사용하여 개발을 한다. 물론 다른 툴도 있을 것이다.<br>
개발 시에 Interactive 하게 개발을 하기 때문에 기본적으로 그대로 복사해서 BDAE Web 을 통해서 이름을 정해서 저장하면 된다. <br>

BDAE 의 R 을 위한 테이블 함수는 4가지가 존재한다.
1. asEval (SQL_args, SQL_output, R_module_name)
2. asRowEval (SQL_input, SQL_args, SQL_output, No_Of_Rows, R_module_name)
3. asTableEval (SQL_input, SQL_args, SQL_output, R_module_name)
4. asGroupEval (SQL_input, SQL_args, SQL_output, 'col1,col2,col3..', R_module_name)

***asEval()*** 을 제외하면 모두 분석하려는 ***SQL_input*** 이 존재한다. 데이터는 Oracle Database 에 존재하기 때문에 SQL Query 형태의 SQL_input 을 기술하며 이는 독립적으로도 조회가 가능한 형태의 SQL 문이어야 한다.<br>
***SQL_output*** 은 하이퍼 파라미터들이나, 재활용 가능한 함수들의 argument 들, 또는 Reference Data 그 자체일 수 있다.  단순 파라미터들은 SELECT .. FROM dual 을 사용하면 되며 Reference Data 의 경우 해당 Query 를 넣으면 된다.<br>
***SQL_output*** 은 SELECT .. FROM dual 이나, 테이블 명, View 명을 바로 적으면 되는데 이렇게 출력을 넣는 이유는 Oracle Database 의 SQL 실행 시의 방식 때문이다. <br>
***R_module_name*** 은 분석가의 R 스크립트의 저장할 때의 이름이며 이는 유일한 이름이어야 한다. <br>
***asRowEval()*** 은 ***정해진 Rows 수*** 마다 반복적으로 ***R_module_name*** 을 호출하여 그 결과를 모두 전달하겠다는 의미이다. No_Of_Rows 는 정수형 숫자가 된다.<br>
***asGroupEval()*** 에서 ***col1,col2,...*** 부분은 Group By 에 해당되는 것으로 ***SQL_input*** 에서 Group By 를 할 필요가 없다는 의미이다.  즉, 자동으로 Oracle Database 가 이에 반응하여 데이터를 Group By 한 후에 BDAE 에게 전달하고, BDAE 는 그 부분마다 ***R_module_name*** 을 호출한다.<br>
***asTableEval()*** 은 가장 많이 사용되고, 병렬 처리를 할 필요가 있을 때에는 ***asGroupEval()*** 을 사용하면 된다.  그때 ***R_module_name*** 은 재활용 될 수 있는 것이다.



