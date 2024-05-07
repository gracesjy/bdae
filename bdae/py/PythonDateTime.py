import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import os
import sys
import urllib, base64


def DateTime():

   dsn_tns = cx_Oracle.makedsn("192.168.0.26", 1521, "FREE")
   conn = cx_Oracle.connect('rquser', 'nebula', dsn_tns)
   '''conn = cx_Oracle.connect('rquser', 'nebula', 'oracle19c', cx_Oracle.SYSOPER)'''
   cursor=conn.cursor()
   cursor.execute(
           "SELECT \
                   wc.wait_class  AS waitclass, \
                   to_char(begin_time, 'YYYY-MM-DD HH:MI:SS') AS sample_time, \
                   round((wh.time_waited) / wh.intsize_csec, 3) AS DB_time \
            FROM V$SYSTEM_WAIT_CLASS wc, \
                 v$waitclassmetric_history wh \
            WHERE wc.wait_class != 'Idle' \
              AND wc.wait_class_id = wh.wait_class_id \
            UNION \
            SELECT \
                  'CPU' AS waitclass, \
                   to_char(begin_time, 'YYYY-MM-DD HH:MI:SS') AS sample_time, \
                   round(VALUE/100, 3) AS DB_time \
            FROM v$sysmetric_history \
            WHERE GROUP_ID = 2 \
              AND metric_name = 'CPU Usage Per Sec' \
            ORDER by sample_time, waitclass")
            
   data = cursor.fetchall()
   ls = ['waitclass', 'sample_time', 'db_time']

   aframe = pd.DataFrame(data, columns=ls)
   return (aframe)

