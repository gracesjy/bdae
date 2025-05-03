# Docker 에서 BDAE Setup

1.  copy all files to docker container !<br>
    아래 oel8_runtime 폴더는 네이버 클라우드에 올려 두었다.<br>
    -- 아래 처럼 폴더로 해야 docker cp 를 한꺼번에 할 수 있다. * 가 먹지 않음 !<br>
    docker cp C:\LinuxGuru\oracle_linux_db_rpm\oel8_runtime oracle-23ai-free:/home/oracle<br><br>

2.  change ownership.<br>
    위의 docker cp 로 하면 root 소유권으로 올라간다.<br>
    > docker exec -it oracle-23ai-free /bin/bash<br>
    > $ su - root<br>
    > # chown -R oracle.oinstall /home/oracle/oel8_runtime<br>
    
    참 우수운 것이 아래 which 가 없으면 R 실행이 되질 않는다 !!!!!!!!!!<br><br>
    > cp which command to /usr/bin<br>

    > # cp /home/oracle/oel8_runtime/which /usr/bin
    > # chmod 777 /usr/bin/which

    > # exit

3. Installation python and R<br>
    아예 Anaconda 를 설치하는 것이 가장 혼란을 줄이는 것이고,<br>
    향후 R 과 Python 패키지 설치 시 유리하다.<br>
    > $ cd oel8_runtime<br>
    > $ sh ./Anaconda3-2024.10-1-Linux-x86_64.sh<br>
    > $ exit<br>

    > docker exec -it oracle-23ai-free /bin/bash<br>
    > (base) $ conda create -n tf39 python=3.9.*<br>
    > (base) $ conda activate tf39<br>
    
    > ## 세상 놀라운 것이 R 을 이렇게 설치하니 너무 좋다. !!<br>
    > ## R installation and BDAE dependencies<br>
    > (tf39)  $ conda install -c conda-forge r-essentials<br>

    > $ R<br>
    > > install.packages("Rcpp")<br>
    > > install.packages("/home/oracle/oel8_runtime/RInside_0.2.15.tar.gz")<br>

    # 반드시 해야 한다.<br>
    (tf39)  $ cd /home/oracle/anaconda3/envs/tf39/lib/R/library/Rcpp<br>
    (tf39)  $ mkdir lib<br>
    (tf39)  $ cd lib<br>
    (tf39)  $ ln -s ../libs/Rcpp.so libRcpp.so<br>
    

4.  move extproc.ora to $ORACLE_HOME/hs/admin<br>

   $ cd<br>
   $ cd oel8_runtime<br>
   $ mv extproc.ora  $ORACLE_HOME/hs/admin<br>

5. Installation BDAE<br>
   $ mkdir -p /home/oracle/workspace/ODCI_R_AnyDataSet/Debug<br>
   $ mkdir -p /home/oracle/workspace/ODCI_Python_AnyDataSet/Debug<br>
   $ cd <br>
   $ cd oel8_runtime<br>
   $ mv libODCI_R_AnyDataSet.so /home/oracle/workspace/ODCI_R_AnyDataSet/Debug<br>
   $ mv libODCI_Python_AnyDataSet.so /home/oracle/workspace/ODCI_Python_AnyDataSet/Debug<br>

6.  Database work<br>
   $ sqlplus / as sysdba<br>
       --
    ```
	CREATE TABLESPACE TS_MLDB 
	DATAFILE '/opt/oracle/oradata/FREE/TS_MLDATA01.dbf'
	SIZE 500M REUSE
	autoextend ON NEXT 1024K
	MAXSIZE UNLIMITED;

	ALTER SESSION SET "_ORACLE_SCRIPT"=TRUE;

	CREATE USER rquser IDENTIFIED BY nebula DEFAULT TABLESPACE TS_MLDB;
	GRANT CONNECT, RESOURCE TO rquser;
	GRANT DBA TO rquser;
     
  ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
  ```
 8.  import BDAE data into Oracle Database
```
     imp rquser/nebula file=./export.dmp fromuser=rquser touser=rquser
```
 9. check $ORACLE_HOME/hs/admin/extproc.ora
 ```
    SET LD_LIBRARY_PATH=/home/oracle/anaconda3/envs/tf39/lib/R/lib:/home/oracle/anaconda3/envs/tf39/lib/R/library/RInside/lib:/home/oracle/anaconda3/envs/tf39/lib/R/library/Rcpp/lib:/home/oracle/anaconda3/envs/tf39/lib:/opt/oracle/product/23ai/dbhomeFree/lib

SET R_HOME=/home/oracle/anaconda3/envs/tf39/lib/R
SET RHOME=/home/oracle/anaconda3/envs/tf39/lib/R
SET R_LIBS=/home/oracle/anaconda3/envs/tf39/lib/R/library
```
