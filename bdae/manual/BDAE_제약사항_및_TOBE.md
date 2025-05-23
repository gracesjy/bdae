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
   > R (아래의 스크립트 개선 사항 - 4번 숙독 필요)
   > function 이름이 고정되고, 최대 2개의 argument 가 가능하다.
   > function(df, df_arg) { 까지를 그대로 따라야 한다.
   ```
    function(df, df_arg) {

      return (pdf)
    }
   ```

3. 리턴 되는 Python pandas DataFrame, R data.frame 은 모두 1개 이상의 컬럼을 지녀야 한다.<br>
   특히 Pandas 의 datetime 의 경우 홀로 있게 되면 PyDateTime 으로 인식되지 않는다. <br>
   따라서 1개 이상의 컬럼이 되는 것을 권장한다.<br><br>

   그렇지만, heuristic 하게 연습해서 Pandas Dataframe 이 오직 datetime 멤버만 있어도 아래와<br>
   같이 해 보니, 되더라. <br>
   아래와 같은 단순한 Python 코드를 보자.
   ```
   import pandas as pd
   
   def test():
       df = pd.DataFrame({
           'Birth':['2019-01-01 09:10:23',
                               '2020-10-23 17:02:33']})
       df['Birth'] = pd.to_datetime(df['Birth'], format='%Y-%m-%d %H:%M:%S', errors='raise')
       return df   
   ```
   여기서 이 시간은 localtime 이 아닌 UTC 시간이다.<br>
   이것의 BDAE SQL은 다음과 같다.
   ```
   SELECT *
   FROM table(apEval(
      NULL,
      'SELECT 
              TO_TIMESTAMP(NULL) Birth
      FROM dual',
      'DateTimeTest:test'))
   ```
   문제는 이 경우 PyDate_Check(), PyDateTime_Check() 등으로 들어오질 않는다.<br>
   오직 PyLong_Check() 로 들어오게 된다는 점이다.  time_t 는 long 이기에 <br>
   이 경우 int int_value = PyLong_AsLong(next); 를 사용하면 절대 안된다.<br>
   <br>
   일반적인 C 코드는 다음과 같다. <br>
   ```
   long timestamp_seconds = (long)long_value/1000000000;
   // Convert timestamp to a struct tm
   struct tm *time_info;
   /* 아래는 로컬 시간 */
   //time_info = localtime(&timestamp_seconds); // Use localtime for local timezone
   /* 아래는 UTC 시간 */
   time_info = gmtime(&timestamp_seconds);
   // Format the time into a string
   char time_string[80];
   strftime(time_string, sizeof(time_string), "%Y-%m-%d %H:%M:%S", time_info);
   ```

4. R 스크립트 입력의 개선사항
   Oracle R Enterprise 는 패키지 위주로 되어 있지만, BDAE 는 Embedded SQL 위주이다.<br>
   R 스크립트의 입력할 때 Oracle R Enterprise 에서 많이 힘들었기 때문에 <br>
   BDAE Web 으로 입력을 한다.  이건 정말 잘했다. <br><br>

   R 스크립트를 function() 과 기존은 죽 아래로 내려가는 두가지가 있었다. <br>
   아래로 죽 내려가는 서술형태가 좋긴 하다.  다만 이것의 제약 사항은 <br>
   R 엔진에게 데이터와 Argument 의 변수명을 확정 지어야 한다는 점이다. <br>
   ***데이터 : data***,  ***Argument : args*** 로 고정하기로 한다.<br>
   또한, RSCRIPT 테이블의 ***SCRIPT_TYPE*** 컬럼에 ***Normal*** 이 아닌 ***NEW_TYPE*** 으로 해야 한다.<br>
   이와 같은 형태의 R script 는 다음과 같이 안에 함수를 별도로 넣어도 된다.<br>
   ```
   library(kohonen)
   library(jpeg)
   library(logr)
   library(htmltools)
   library(RCurl)
   log_open("/tmp/rlog.log")
   log_print("Here is a test log statement")
   
   
   train  <- sample(1:150, 100) 
   train_set  <-  list(x = as.matrix(iris[train,-5]), Species = as.factor(iris[train,5])) 
   test_Set <- list(x = as.matrix(iris[-train,-5]), Species = as.factor(iris[-train,5])) 
   gr <- somgrid(xdim = 3, ydim = 5, topo = "hexagonal") #grid 갯수 및 모양 설정
   ss <- supersom(train_set, gr, rlen = 200, alpha = c(0.05, 0.01)) #som 학습하기
   
   
   my<-function(img_file) {
      log_print('in my function ..')
      log_print(paste('file_name : ', img_file))
      log_print(paste('file_size : ', file.info(img_file)[1, "size"]))
   	zz <- file(img_file, "rb")
   	jpg1_lraw.lst <- vector("list", 1)
   	jpg1_lraw.lst[[1L]] <- readBin(zz, "raw", file.info(img_file)[1, "size"])
   	close(zz)
   
   	df <- data.frame(name=img_file,stringsAsFactors=FALSE)
   	df$blob <- jpg1_lraw.lst
      
      unlink(img_file)
   	return (df)
   }
   
   name <- c("/tmp/kohonen01.jpg","/tmp/kohonen02.jpg","/tmp/kohonen03.jpg","/tmp/kohonen04.jpg")
   
   jpeg(name[1])
   plot(ss,type="changes")
   dev.off()
   jpeg(name[2])
   plot(ss, type="count", main="Node Counts")
   dev.off()
   jpeg(name[3])
   plot(ss, type="dist.neighbours", main = "SOM neighbour distances", shape = "straight")
   dev.off()
   jpeg(name[4])
   plot(ss, type="dist.neighbours", palette.name=grey.colors, shape = "straight")
   dev.off()
   
   log_print('first image :')
   
   
   df = my(name[1])
   for (i in 2:length(name)) {
      df_tmp = my(name[i])
      df = rbind(df, df_tmp)
   }
   #df_tmp2 = my(name[2])
   #df_tmp3 = my(name[3])
   #df_tmp4 = my(name[4])
   #df = rbind(df_tmp1, df_tmp2, df_tmp3, df_tmp4)
   df
   ```
   참고로 이것을 호출하는 BDAE SQL 은 다음과 같다.
   ```
   SELECT *
      FROM
      table(asEval(
      NULL,
      'SELECT CAST(''A'' AS VARCHAR2(40)) HEADER, TO_BLOB(NULL) IMG FROM dual',
      'R_ml_new'))
   ```



   

   
   

