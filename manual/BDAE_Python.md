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