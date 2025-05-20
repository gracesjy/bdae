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
4.  
5. ㄴㄴㄴ
6. ㄴ
7. ㄴ
8. ㄴ
9. ㄴ
10. ㄴㄴ
