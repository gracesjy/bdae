## BDAE R Basic
Analysts typically use R Studio or Jupyter Notebook for R development. Of Course, Other tools are available.<br>
Since development is interactive, you can simply copy and paste the data into BDAE Web, name it, and save it. <br>

There are four table functions for R in BDAE.
1. asEval (SQL_args, SQL_output, R_module_name)
2. asRowEval (SQL_input, SQL_args, SQL_output, No_Of_Rows, R_module_name)
3. asTableEval (SQL_input, SQL_args, SQL_output, R_module_name)
4. asGroupEval (SQL_input, SQL_args, SQL_output, 'col1,col2,col3..', R_module_name)

Except for ***asEval()***, there is a ***SQL_input*** to be analyzed. Since the data exists in an Oracle database, ***SQL_input*** is described in the form of a SQL Query, and this must be a SQL statement that can be queried independently.<br>

***SQL_args*** can be hyperparameters, arguments of reusable functions, or the Reference Data itself. For simple parameters, use SELECT .. FROM dual. For Reference Data, enter the corresponding Query.<br>
***SQL_output*** can be entered as SELECT .. FROM dual, or directly as the table name or view name, but the reason for including the output like this is due to the procedure of how SQL is executed within Oracle Database, so there is no other way. However, this format and the return format of the R data.frame must be the same. This part can be generated through a utility. <br>
***R_module_name*** is the name the analyst saves his R script as, and must be a unique name. <br>
***asRowEval()*** means to repeatedly call ***R_module_name*** every ***a certain number of rows*** and pass back all the results. No_Of_Rows must be an integer.<br>
***asGroupEval()*** The ***col1,col2,...*** parts correspond to Group By, which means that there is no need to Group By in ***SQL_input***. In other words, Oracle Database automatically reacts to this, Group Bys the data, and then passes it to BDAE, and BDAE calls ***R_module_name*** for each part.<br>
***asTableEval()*** is the most commonly used, and when parallel processing is needed, ***asGroupEval()*** can be used. In that case, ***R_module_name*** can be reused.

## BDAE R Example
### Infinity and NaN
1. Save below R code as R_infinity (As you want.)
```
X <- c(1,2,3,NA,5)
Y <- c(1.1,-1.0/0,1.0/0,4.0,5.34)

df <- data.frame(X,Y)
df
```
2. Make SQL to run above R script
```
SELECT A, case when B=-binary_double_infinity then '-Infinity' 
               when B=binary_double_infinity then '+Infinity'
               else TO_CHAR(B) END AS B FROM (
 SELECT *
   FROM
   table(asEval(
   NULL,
   'SELECT 1 as A, 1.0 as B FROM dual',
   'R_infinity'))
)
```
3. After run above SQL, results are as followings.<br>

|A	|B        |
|---|---------|
|1	|1.1      |
|2	|-Infinity|
|3	|+Infinity|
|4  |         |
|5	|5.34     |

