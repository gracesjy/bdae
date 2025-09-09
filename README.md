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
         	NULL,  -- Secondary Input Data
            'SELECT CAST(''A'' AS VARCHAR2(40)) SUBJECT,  -- Output Format
                  TO_CLOB(NULL) H1, TO_CLOB(NULL) H2, TO_CLOB(NULL) H3 
             FROM DUAL',
           'CAL_HOUSING_EDM:describe'))  -- Python Module for calling
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
docker run -d --ipc=host --name oracle_bdae_gpu --gpus all -p 1521:1521 -p 5500:5500 -p 8888:8888 oracle_bdae:0.7
```

<img src="https://github.com/gracesjy/bdae/blob/main/images/BDAE_DOCKER.png" width="90%" height="90%">

Please send me the mail if you want to test. (gracesjy@naver.com)<br>

## Summary (Manual)
https://github.com/gracesjy/bdae/blob/main/BDAE_Manual.pdf


#### For various reasons, Big Data Analysis Enabler is not registered as a trademark.
   
     


               

