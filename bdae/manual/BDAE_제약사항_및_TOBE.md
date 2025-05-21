### BDAE 제약 사항 및 To-Be 사항

1. Nan, Inf 처리 (완료)
   Python 및 R 의 Nan, Inf 처리에 따른다. <br>
   Oracle Number 의 경우 double 로 처리한다. <br>
   OCI API 사용 시에는 SQLT_DAT, SQLT_DATE, SQLT_CLOB, SQLT_VCS, SQLT_CHAR 등은 <br>
   모두 string 으로 읽은 뒤에 입력 타입에 따라서 Python, R 의 타입으로 변환된다. <br>
   소스는 col_R_args[c]->coltype, col_input_data[c]->coltype 등을 찾아서 참조

2. Python 모듈과 R 모듈은 BDAE 가 지정하는 방식을 따라야 한다.
   두가지 모두 함수의 argument 는 최대 2개이다. <br>
   첫번째는 데이터, 두번째는 참조 데이터 또는 모듈 내의 설정 등을 변경할 목적이다.
   > Python 
   ```
    def py_function(df, df_arg):

        # No restrictions
   
        return pdf
   ```
   > R
   > function 이름이 고정되고, 최대 2개의 argument 가 가능하다.
   > function(df, df_arg) { 까지를 그대로 따라야 한다.
   ```
    function(df, df_arg) {

      return (pdf)
    }
   ```

3. 리턴 되는 Python pandas DataFrame, R data.frame 은 모두 1개 이상의 컬럼을 지녀야 한다.<br>
   특히 Pandas 의 datetime 의 경우 홀로 있게 되면 PyDateTime 으로 인식되지 않는다. <br>
   따라서 1개 이상의 컬럼이 되는 것을 권장한다.
   

