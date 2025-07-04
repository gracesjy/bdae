## ${\textsf{\color{magenta}Descriptive Statistics}}$

> 다음의 데이터로 해 본 것이다.  sns.load_dataset('titanic') 은 pandas dataframe 임.<br>
> df_melt 부분을 잘 살펴 보면 각 항목 별로 기술통계량을 보여준다.
```
import pandas as pd
import numpy as np
import seaborn as sns

data = sns.load_dataset('titanic')
data.describe()
desc = data.describe()
desc.reset_index(inplace=True)
desc.columns = ['vars', 'survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']
df_melt = pd.melt(desc, id_vars=['vars'])
```

이 데이터를 DB 에 넣은 후에 기술 통계량을 구한다.<br>

1. 먼저 모듈을 BDAE 에 넣는다.<br>

> BDAE 는 기본적으로 컬럼명이 모두 대문자로 변환해 준다. <br>
> 따라서 컬럼명을 소문자로 바꾸는 것은 알고리즘 작성자에 따른다. <br>

```
import pandas as pd
import numpy as np
import seaborn as sns

def describe(df):
    colums_ = df.columns.tolist()
    df.columns = list(map(str.lower,colums_))
    df_desc = df.describe()
    df_desc.reset_index(inplace=True)
    df_desc.columns = ['vars', 'passengerid', 'survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']
    df_melt = pd.melt(df_desc, id_vars=['vars'])
    return df_melt
```

2. SQL 을 만든다. <br>
> 참고로 툴에서 오라클의 이미 정의된 오해 가능한 컬럼 이름(예: index, type 등)이 <br>
> 있는 경우 "" 를 사용하는 것을 보여주고 있다.
```
SELECT
	*
FROM
	TABLE(apTableEval(
         	CURSOR(
           SELECT "PassengerId", "Survived", "Pclass", "Name",
	                "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked", "TYPE"
           FROM Titanic),
         	 NULL,
           'SELECT  CAST(''AA'' AS VARCHAR2(40)) vars,
                    CAST(''AA'' AS VARCHAR2(40)) variable,
                    1.0 value
            FROM dual',
           'TitanicDesc:describe'))
```
