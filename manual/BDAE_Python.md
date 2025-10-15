## BDAE Python
### Features
BDAE recommends Python. This is because BDAE is built on C/C++, and the Python TraceBack API performs better than R when handling exceptions. <br><br> Python is also GPU-friendly. <br><br>
### Basic
There are four table functions for R in BDAE.
1. apEval (SQL_args, SQL_output, Python_module_name:start_function_name)
2. apRowEval (SQL_input, SQL_args, SQL_output, No_Of_Rows, Python_module_name:start_function_name)
3. apTableEval (SQL_input, SQL_args, SQL_output, Python_module_name:start_function_name)
4. apGroupEval (SQL_input, SQL_args, SQL_output, 'col1,col2,col3..', Python_module_name:start_function_name)

Except for ***apEval()***, there is a ***SQL_input*** to be analyzed. Since the data exists in an Oracle database, ***SQL_input*** is described in the form of a SQL Query, and this must be a SQL statement that can be queried independently.<br>

***SQL_args*** can be hyperparameters, arguments of reusable functions, or the Reference Data itself. For simple parameters, use SELECT .. FROM dual. For Reference Data, enter the corresponding Query.<br>
***SQL_output*** can be entered as SELECT .. FROM dual, or directly as the table name or view name, but the reason for including the output like this is due to the procedure of how SQL is executed within Oracle Database, so there is no other way. However, this format and the return format of the R data.frame must be the same. This part can be generated through a utility. <br>
***Python_module_name:start_function_name*** is the name the analyst saves his Python module as, and must be a unique module name and function name. <br>
***apRowEval()*** means to repeatedly call ***Python_module_name:start_function_name*** every ***a certain number of rows*** and pass back all the results. No_Of_Rows must be an integer.<br>
***apGroupEval()*** The ***col1,col2,...*** parts correspond to Group By, which means that there is no need to Group By in ***SQL_input***. In other words, Oracle Database automatically reacts to this, Group Bys the data, and then passes it to BDAE, and BDAE calls ***Python_module_name:start_function_name*** for each part.<br>
***apTableEval()*** is the most commonly used, and when parallel processing is needed, ***apGroupEval()*** can be used. In that case, ***Python_module_name:start_function_name*** can be reused.

### Difference Between BDAE Python and BDAE R
The difference between BDAE R and Python is that R requires only function names, while Python requires a module name and a starting function, and BDAE table functions begin with ap . The rest of the concept is the same. This module name is not a class.<br>

## BDAE Python Example
### Infinity and NaN

1. Python Code

```
import pandas as pd
import numpy as np

def argument_test(df_args):

    df = pd.DataFrame([['motor type',1, np.inf],
                      [np.nan, 2, 3.2],
                      ['RF', np.nan, 4.5]],
                      columns = ['name', 'var1', 'var2'])
    return df
```

2. SQL

```
SELECT ID, VALUE2, case when VALUE3=-binary_double_infinity then '-Infinity' 
               when VALUE3=binary_double_infinity then '+Infinity'
               else TO_CHAR(VALUE3) END AS VALUE3_RE FROM (SELECT * 
   FROM
   table(apEval(
cursor(SELECT 1.0 as param1, 'AAAAAA' as param2 from dual),
'SELECT CAST(NULL AS VARCHAR2(10)) ID, 1 Value2,1.0 VALUE3 FROM dual',
'Python_Exception:argument_test')))

```

3. Results

|ID|	VALUE2|	VALUE3_RE|
|--|----------|----------|
|motor type|	1|	+Infinity|
|2	|3.2|  |
|RF |	|	4.5|

### ML
1. Like AutoML, ..

```
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import plotly.graph_objects as go

def train(df, df_args):

    # 2. 피처 및 타겟 선택
    print(df.columns)
    features = df_args['FEATURES'][0].split(',')
    
    print(type(features))
    target = df_args['TARGET'][0]

    print(df.columns)
    X = df[features]
    y = df[target]
    
    # 3. 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. 모델 및 하이퍼파라미터 설정
    models = {
        'RandomForest': (RandomForestRegressor(), {
            'model__n_estimators': [100, 200],
            'model__max_depth': [None, 10]
        }),
        'XGBoost': (XGBRegressor(), {
            'model__n_estimators': [100, 200],
            'model__max_depth': [3, 6],
            'model__learning_rate': [0.1, 0.3]
        }),
        'LightGBM': (LGBMRegressor(), {
            'model__n_estimators': [100, 200],
            'model__max_depth': [3, 6],
            'model__learning_rate': [0.1, 0.3]
        })
    }
    
    results_df = pd.DataFrame()
    best_models = {}
    
    # 5. 모델별 하이퍼파라미터 튜닝 및 평가
    for name, (regressor, params) in models.items():
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('model', regressor)
        ])
        grid = GridSearchCV(pipe, params, cv=3, scoring='neg_root_mean_squared_error', n_jobs=1)
        grid.fit(X_train, y_train)
        best_model = grid.best_estimator_
        best_models[name] = best_model
    
        y_pred = best_model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # squared=False 제거
        r2 = r2_score(y_test, y_pred)
    
        results_df[name + '_RMSE'] = [rmse]
        results_df[name + '_R2'] = [r2]
    
    # 6. 앙상블 모델 생성 및 평가
    ensemble = VotingRegressor(estimators=[(name, model) for name, model in best_models.items()])
    ensemble.fit(X_train, y_train)
    y_pred_ensemble = ensemble.predict(X_test)
    rmse_ensemble = np.sqrt(mean_squared_error(y_test, y_pred_ensemble))
    r2_ensemble = r2_score(y_test, y_pred_ensemble)
    
    results_df['Ensemble_RMSE'] = [rmse_ensemble]
    results_df['Ensemble_R2'] = [r2_ensemble]
    
    return results_df
```

2. SQL

```
SELECT * 
      FROM table(apTableEval(
         	cursor(SELECT LONGITUDE,LATITUDE,POPULATION,HOUSEHOLDS,MEDIAN_HOUSE_VALUE from CAL_HOUSING),
         	cursor(SELECT 'LONGITUDE,LATITUDE,POPULATION,HOUSEHOLDS' FEATURES, 'MEDIAN_HOUSE_VALUE' TARGET FROM DUAL),
            'SELECT 1.0 RandomForest_RMSE, 1.0 RandomForest_R2, 1.0 XGBoost_RMSE, 1.0 XGBoost_R2, 1.0 LightGBM_RMSE, 1.0 LightGBM_R2, 1.0 Ensemble_RMSE, 1.0 Ensemble_R2 
             FROM DUAL',
           'Ensemble:train'))
```

3. Results

|RANDOMFOREST_RMSE|	RANDOMFOREST_R2|	XGBOOST_RMSE|	XGBOOST_R2	|LIGHTGBM_RMSE|	LIGHTGBM_R2	| ENSEMBLE_RMSE	|ENSEMBLE_R2|
|-|-|-|-|-|-|-|-|
|52240.6618085929	|0.794907175817684|	57931.1000813363|	0.747793267043923|	57671.0779768579	|0.750052231569059	|53545.2610316801	|0.784535758252917|
