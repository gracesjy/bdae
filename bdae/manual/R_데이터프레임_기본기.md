## R data.frame  기본 핸들링

다음을 간단히 데이터 프레임으로 만들자.  주의할 사항은 stringsAsFactor=FALSE<br>
반드시 넣어야 한다.

```
    resno <- c(101, 102, 103, 104, 105)
    rname <- c('ANDREA', 'NY', 'YANIS', 'CLEVETH', 'ASHIYA')
    rage <- c('51', '23', '52', '76', '98')
    df <- data.frame(resno, rname, rage, stringsAsFactors=FALSE)
```

간단히 기술통계량을 구하는 것은 다음의 2가지 라이브러리를 넣자.
```
library(psych)
library(reshape)
```

데이터프레임의 각 컬럼 타입은 다음과 같이 해서 알아보자.
```
sapply(df, class)
```

기술통계량은 다음과 같이 한다.  리턴도 테이터프레임이다.
```
df_des = describe(df)

> df_des
       vars n mean   sd median trimmed  mad min max range skew kurtosis   se
resno     1 5  103 1.58    103     103 1.48 101 105     4    0    -1.91 0.71
rname*    2 5    3 1.58      3       3 1.48   1   5     4    0    -1.91 0.71
rage*     3 5    3 1.58      3       3 1.48   1   5     4    0    -1.91 0.71


```
인덱스가 resno, rname, range 로 나온다. 그리고 vars 가 바로 이것들의 인덱스이다. <br>
인덱스를 컬럼으로 만들자. 아래 결과에서 vars_name 이 생겼다.
```
df_des <- cbind(vars_name=rownames(df_des),df_des)
> df_des
       vars_name vars n mean       sd median trimmed    mad min max range skew
resno      resno    1 5  103 1.581139    103     103 1.4826 101 105     4    0
rname*    rname*    2 5    3 1.581139      3       3 1.4826   1   5     4    0
rage*      rage*    3 5    3 1.581139      3       3 1.4826   1   5     4    0
       kurtosis        se
resno    -1.912 0.7071068
rname*   -1.912 0.7071068
rage*    -1.912 0.7071068
```

기존 vars 는 삭제하자. (여기에서는 삭제말고 이것만 빼고 선택했다.)
```
df_des_select = subset(df_des, select=-vars)
```

이제 unpivot 하자.
```
df_des_select = subset(df_des, select=-vars)
```

BDAE 에 리턴하기전에 기술통계량은 반드시 unpivot 해야 한다.<br>
그리고 타입도 체크한다.
```
df_des_select_unpivot = melt(df_des_select,id=c('vars_name'))
sapply(df_des_select_unpivot, class)
> sapply(df_des_select_unpivot, class)
  vars_name    variable       value 
"character"    "factor"   "numeric" 
> 

```
variable 이 factor 이고, 이것은 좋지 않다. 이것을 반드시 string 으로 한다.<br>
```
df_des_select_unpivot$variable <- as.character(df_des_select_unpivot$variable)

> df_des_select_unpivot$variable <- as.character(df_des_select_unpivot$variable)
> sapply(df_des_select_unpivot, class)
  vars_name    variable       value 
"character" "character"   "numeric" 
```

자. 이제 이것을 SQL 문으로 하면
```
SELECT * 
   FROM 
   table(asEval( 
   NULL, 
   'SELECT CAST(''A'' as VARCHAR2(40)) as vars, CAST(''A'' as VARCHAR2(40)) variable,
           1.0 value FROM dual', 
   'Describe'))
```

자, 이제 BDAE 에 입력을 해 보자. <br>
1. R  모듈

   ```
function() {

    library(psych)
    library(reshape)

    resno <- c(101, 102, 103, 104, 105)
    rname <- c('ANDREA', 'NY', 'YANIS', 'CLEVETH', 'ASHIYA')
    rage <- c('51', '23', '52', '76', '98')
    df <- data.frame(resno, rname, rage, stringsAsFactors=FALSE)
	
	 df_des <- describe(df)
    df_des <- cbind(vars_name=rownames(df_des),df_des)
    df_des_select = subset(df_des, select=-vars)
    df_des_select_unpivot = melt(df_des_select,id=c('vars_name'))
    df_des_select_unpivot$variable <- as.character(df_des_select_unpivot$variable)
    
	 return (df_des_select_unpivot)
}
   ```

2.  SQL
```
SELECT * 
   FROM 
   table(asEval( 
   NULL, 
   'SELECT CAST(''A'' as VARCHAR2(40)) as vars, CAST(''A'' as VARCHAR2(40)) variable,
           1.0 value FROM dual', 
   'Describe'))
```

