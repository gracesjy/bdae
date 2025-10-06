# BDAE (Big Data Analysis Enabler), AI Enabler for Oracle Database

***Big Data Analysis Enabler(BDAE)*** enables parallel processing of Python and R without data movement based on Oracle In-Database.
Because it implements the ***Oracle Data Cartridge Interface***, it is not limited to a specific schema and supports ***Dynamic SQL***.
(contact : gracesjy@naver.com)<br>

***BDAE*** is executed as a SQL statement and the results are retrieved like the results of a general SQL statement, 
so a separate application server is unnecessary, and all logic (including the backend) can be implemented in Python and R. 

***BDAE*** can be used for the following purposes:
1. AI for Training and Inference (Real-Time)
2. Powerful ETL jobs, Fundamental data perspective work for AI tasks
3. Integration BI or any solutions capable of using Oracle Database
4. Smart Factory, Financial, Health, .., no restrictions.
5. ...

***It*** is built on Oracle In-Database technology and has platform features that enable ***Oracle Database(TM)***
to be used not only as a simple storage for general AI tasks, but also as a non-stop operating environment
without the overhead of data movement during learning and inference.

<img src="https://github.com/gracesjy/bdae/blob/main/images/Oracle_In_Database.png" width="50%" height="50%">

Below Image shows the operating location of ***BDAE*** in the form of Oracle In-Database.
Parallel distributed processing is a feature of Oracle In-Database, and analysts do not need to consider it in their modules, which increases the reusability of logic.
In addition, the fact that it can be integrated with various analysis engines can be seen as an advantage of BDAE. 

<img src="https://github.com/gracesjy/bdae/blob/main/images/BDAE_ARCH.png" width="50%" height="50%">


This can improve performance by reducing the number of DB calls while writing backend programs in Python and R.<br>
***Note)*** <br>
1.    ***BDAE*** was developed with inspiration from ***Oracle R Enterprise*** and was created solely using Oracle manuals.<br>
      However, it took a lot of time to develop through trial and error due to the lack of examples.<br>
      This is a work that I thought of and created on my own.<br>
2.    ***BDAE*** enables your Python/R modules to run with parallelism like ***Oracle R Enterprise***. <br>
3.    But, ***BDAE*** has no alogithm unlike **Oracle R Enterprise**, just Tool for AI (Machine Learning). <br>
      Algorithms are not included because they are constantly evolving and changing. This is also because analysts can do better. <br>
## ***BDAE*** Table Functions
BDAE has special SQL statements related to Oracle In-Database and provides table functions for four types of analysis for Python and R respectively.<br>

1. apEval(SQL_args, SQL_output, R_script_name/PythonModuleName:start_function)
2. apTableEval(SQL_input, SQL_args, SQL_output, R_script_name/PythonModuleName:start_function)
3. apRowEval(SQL_input, SQL_args, SQL_output, No_of_Rows, R_script_name/PythonModuleName:start_function)
4. apGroupEval(SQL_input, SQL_args, SQL_output, GroupColumns, R_script_name/PythonModuleName:start_function)

apEval() is for simple testing without input data, while the rest all have input data. Each can be used for its own purpose, and the R and Python analysis modules are reusable. <br>
The most commonly used ones are apTableEval() and apGroupEval(), and the difference between the two is that apGroupEval has Group By built-in, allowing for parallel distributed processing. <br>

1. SQL_input : is a SQL statement describing the data to be analyzed and must be independently executed and queried.
2. SQL_args  : can represent hyperparameters or reference data for the analysis module. For example, hyperparameters can be expressed as follows: <br>
```
      select 0.000001 learning_rate, 100 epochs from dual
```
3. SQL_output : is the part where you enter the SQL statement for output or the View or Table name, and the type and number of columns must match the data.frame or pandas DataFrame in the return part of the R or Python analysis module.

4. No_of_Rows : means that the SQL_input data is split into each defined number and the analysis module is called and executed.
5. R_script_name/PythonModuleName:start_function : is where you enter the names of the registered R and Python modules you want to analyze. They are all managed in separate tables, and unlike R, Python is slightly different in the parts where you write the module name and the function name to start execution.
6. GroupColumns : applies only to apGroupEval() and is equivalent to inserting Group By in a SQL statement into the apTableEval() function. In other words, apGroupEval() defines that parallel distributed processing is performed based on these columns, and each column name can be written as col1, col2, col3, .. Therefore, analysts do not need to consider parallel distributed processing.
   
## How To run (3 Steps to Run !)
1. Register your Python/R model in the designated Oracle Database's table or save file in PYTHONPATH directory.
2. Register the SQL to bind source data and your model.
3. Run the SQL and get the results.  you can get results any tools capable of connecting Oracle Database.
***Note*** Using BDAE Web, you can simply and easily register Python/R and SQLs with Editor. (just copy & paste from Jupyter Notebook or Something)

### Step-1) Make Your Python module (ML/DL/ ...)

You must make entry function of module, for example describe().
others are helper functions. 

```python
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import tempfile
import base64
from pandas.plotting import scatter_matrix

def make_output(df, key, data):
   df[key] = data
   return df

def image_to_html():
   tmp_file_name = tempfile.NamedTemporaryFile().name + '.png'
   plt.savefig(tmp_file_name)
   image = open(tmp_file_name, 'rb')
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   uri = '<img src="data:img/png;base64,' + image_64_encode.decode() + '">'
   html_str = "<html><body>" + uri + "</body></html>"
   if os.path.exists(tmp_file_name):
      os.remove(tmp_file_name)
   return html_str

def describe(housing):
   # 0) Prepare Output
   tupleStart = {'subject': [ 'General ML' ] }
   pdf = pd.DataFrame(tupleStart)

   # 1) Historam
   housing.hist(bins=50, figsize=(20,15))
   a = image_to_html()
   pdf = make_output(pdf, 'Histogram', a)

   # 2) Scatter Plot
   housing.plot(kind="scatter", x="LONGITUDE", y="LATITUDE", alpha=0.4,
             s=housing["POPULATION"]/100, label="POPULATION", figsize=(10,7),
             c="MEDIAN_HOUSE_VALUE", cmap=plt.get_cmap("jet"), colorbar=True,
             sharex=False)
   plt.legend()
   a = image_to_html()
   pdf = make_output(pdf, 'ScatterPlot', a)

   # 3) Scatter Matrix
   attributes = ["MEDIAN_HOUSE_VALUE", "MEDIAN_INCOME", "TOTAL_ROOMS",
              "HOUSING_MEDIAN_AGE"]
   scatter_matrix(housing[attributes], figsize=(12, 8))
   a = image_to_html()
   pdf = make_output(pdf, 'ScatterMatrix', a)
   
   return pdf

```

### Step-2) Make Your SQL to run

The input (Oracle Database's Table or View or Queries) is delivered 
pandas DataFrame format to your python entry point function,
and You must make the results into pandas DataFrame format !,
because of Oracle Database Query Results(RDBMS).

```sql
SELECT * 
      FROM table(apTableEval(
         	cursor(SELECT * FROM CAL_HOUSING),  -- Input Data (Driving Table)
         	NULL,  -- Secondary Input Data or Hyperparameters for your Python Module
            'SELECT CAST(''A'' AS VARCHAR2(40)) SUBJECT,  -- Output Format
                  TO_CLOB(NULL) H1, TO_CLOB(NULL) H2, TO_CLOB(NULL) H3 
             FROM DUAL',
           'CAL_HOUSING_EDM:describe'))  -- Python Module for calling
```
R Module function ***asTableEval()***, not ***apTableEval()***
```sql
SELECT * 
      FROM table(asTableEval(
         	cursor(SELECT * FROM CAL_HOUSING),  -- Input Data (Driving Table)
         	NULL,  -- Secondary Input Data or Hyperparameters for your R Module
            'SELECT CAST(''A'' AS VARCHAR2(40)) SUBJECT,  -- Output Format
                  TO_CLOB(NULL) H1, TO_CLOB(NULL) H2, TO_CLOB(NULL) H3 
             FROM DUAL',
           'CAL_HOUSING_EDM_describe'))  -- R Module for calling
```



### Step-3) Run above SQL and get Results
Like General SQL Queries' results, BDAE's results are the same.
(Any Applications you can develope using SQLs)

<img src="https://github.com/gracesjy/bdae/blob/main/images/ResultsEDM.png" width="90%" height="90%">



## Installation (dependencies)

Oracle Database is provided as Docker, and installation of Python and R with Anaconda has also become very convenient.<br>
Therefore, BDAE installation is very quick and can be installed within minutes.<br><br>
This Docker can be provided in tar file format and can be imported using methods such as docker load -i bdae_oracle.tar.<br><br>

If you have an NVIDIA Graphic Card and it is properly set up, you can use the GPU by loading the Docker image above and then giving the following options when running it.

```
docker run -d --init --ipc=host --name oracle_bdae_gpu --gpus all -p 1521:1521 -p 5500:5500 -p 8888:8888 oracle_bdae:0.7
```

<img src="https://github.com/gracesjy/bdae/blob/main/images/BDAE_DOCKER.png" width="90%" height="90%">

Please send me the mail if you want to test. (gracesjy@naver.com)<br>

## Summary (Manual)
https://github.com/gracesjy/bdae/blob/main/BDAE_Manual.pdf

## GCP Big Query
Comparing it to GCP BigQuery, the similarities with BigQuery include that both input and output data are in table format and that parallel processing is possible, while the differences are that BDAE allows analysts to directly input algorithms and MLOps like AutoML, and that large-scale data performance tuning can be left to Oracle Database.
```
CREATE OR REPLACE MODEL
  `bigquery-public-data.london_bicycles.bikeshare_model`
OPTIONS
  (model_type='LINEAR_REG') AS
SELECT
  start_station_name,
  end_station_name,
  duration,
  start_hour
FROM
  `bigquery-public-data.london_bicycles.cycle_hire`
WHERE
  start_station_name IS NOT NULL
  AND end_station_name IS NOT NULL
  AND duration IS NOT NULL
  AND start_hour IS NOT NULL
  AND RAND() < 0.01 -- 데이터 양이 너무 많아 샘플링함
```
If you change the BigQuery above to BDAE, it will look like this. Instead of creating tables haphazardly every time, you can consistently store F1, accuracy, and other metrics in the model table. Of course, analysts can create or provide these details.
```
INSERT INTO MODEL_TABLE
SELECT * 
      FROM table(apTableEval(
         	cursor(SELECT * FROM bigquery-public-data.london_bicycles.cycle_hire),  -- Input Data (Driving Table)
         	NULL,  -- Secondary Input Data or Hyperparameters 
            'SELECT CAST(NULL AS VARCHAR2(40)) name,  -- Output Format
                    CAST(NULL AS CLOUB) model,
                    1.0 accuracy, ...
             FROM DUAL',
           'YourAlgorithm:LinearReg'))  -- Python Module or R Module
```

#### For various reasons, Big Data Analysis Enabler is not registered as a trademark.
   
     


               

