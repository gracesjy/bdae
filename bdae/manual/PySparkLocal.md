# PySpark Local Mode

```
import os
from pyspark.sql import SparkSession

# Define the Python executable path or alias
python_path = r'C:\Users\jinyoung.song\.conda\envs\tf39\python.exe'  
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['PYSPARK_DRIVER_PYTHON'] = python_path


spark = SparkSession.builder \
    .appName("Your App Name") \
    .master("local") \
    .config("spark.python.worker.exec", python_path) \
    .getOrCreate()
"""
spark = SparkSession.builder \
    .appName("Your App Name") \
    .master("local") \
    .getOrCreate()
"""
data = [('001','Smith','M',40,'DA',4000),
        ('002','Rose','M',35,'DA',3000),
        ('003','Williams','M',30,'DE',2500),
        ('004','Anne','F',30,'DE',3000),
        ('005','Mary','F',35,'BE',4000),
        ('006','James','M',30,'FE',3500)]

columns = ["cd","name","gender","age","div","salary"]
df = spark.createDataFrame(data = data, schema = columns)
df.show()
df.collect()
```
