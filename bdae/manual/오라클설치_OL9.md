# OEL 9 + Oracle 23AI + Python with anaconda + R + BDAE 까지 테스트 위한 것들
 - OEL8 과 비슷하면서 다름.<br><br>
 
 
< 기본 OEL9 설치 ><br>
1. HDD 는 120 GB 이상, 메모리 4GB 이상, Network Device 는 2개(Host 전용 Adapter 추가)<br>
   Host 전용 Adapter 는 177.175.54.1 로 설정.<br><br>
   
2. SW 부분은 Workstation 만 설정해도 됨.<br>
3. 모두 설치 후 dnf update 한 상태<br>
4. 클립 보드 양방향, 공유 폴더 설정 <br>

.. 이것으로 ova 포맷으로 Export 받아 둔 상태이며 여기에서 아래 설치를 출발한다.<br>



 
1. vi /etc/selinux/config  에서  SELINUX=disabled:  로 세팅<br>

2. 방화벽 등의 서비스 disable, (준비된 .sh 활용해도 큰 무리 없음)<br>

[root@oracle ~]# systemctl status firewalld <br>
[root@oracle ~]# systemctl stop firewalld <br>
[root@oracle ~]# systemctl disable firewalld <br>
[root@oracle ~]# systemctl status firewalld<br>

3. host name and ip 설정<br>
cat /etc/hosts 내용에 아래를 추가<br><br>

177.175.54.97 oel9.localdomain oel9<br><br>

4. 아래를 통해서 oracle 계정 및 기타 설정하는 것을 자동으로 (준비된 것 활용도 됨)<br>
dnf -y install oracle-database-preinstall-23ai<br>

 > /etc/passwd, /etc/group 에 oracle 관련 생성되었는지 확인하고,<br>
 > /etc/group 에서 vboxsf:x:977:oracle,raymond 를 추가 하여 /media/sf_LinuxGuru 에 두 계정 접근 권한 준다.<br><br>

5. 미리 받아 둔 것을 사용하자.<br>
dnf localinstall ./oracle-database-free-23ai-1.0-1.el9.x86_64.rpm<br><br>


6. R 설치 (OEL 8 과는 다르다.)<br><br>

dnf install epel-release   <br>
dnf --enablerepo=ol9_codeready_builder install flexiblas-netlib64<br>
dnf --enablerepo=ol9_codeready_builder install flexiblas-devel<br>
dnf --enablerepo=ol9_codeready_builder install libtirpc-devel<br>
dnf install R<br>

root 에서 R 실행 후에, <br>
> install.packages("Rcpp")<br><br>
 
 완료 후에 /usr/lib64/R/library/Rcpp 로 들어가서<br>
 > mkdir lib<br>
 > cd lib<br>
 > ln -s ../libs/Rcpp.so libRcpp.so 만들어 줌<br>
 

7. 메모리를 줄인 후에 재기동 (너무 작으면 안되더라.. 5G 정도 필요함)<br>
<br>
/etc/init.d/oracle-free-23ai configure<br>
> 위를 실행하면 암호 물어 봄, a*l*2*3*9 등으로 임의 설정하면 시간 소모 후 ..<br>
> su - root 로 로그인 후, passwd oracle 로 오라클 암호 설정 함.<br>
> GUI (그놈) 설정에서 사용자 설정에서 oracle 에 자동 로그인 등을 설정해 두면 편리.<br>
  - 관리자 권한 주고, 자동 로그인 체크<br>

8 재기동 하기 전 Virtual Box 설정 (옵션 임)<br>
1) 메모리를 5G + 1G 정도로 늘림<br>
2) 네트워크 host 177.175.54.97 용 확인<br>
3) 클립보드 설정, 공유 폴더 설정 확인<br>


9 재기동 후 oracle 로 들어가서<br>

** su - oracle **<br>
$ vi .bash_profile 편집<br>
export ORACLE_BASE=/opt/oracle<br>
export ORACLE_HOME=/opt/oracle/product/23ai/dbhomeFree/<br>
export ORACLE_SID=FREE<br>
export PATH=$PATH:$ORACLE_HOME/bin<br>
export NLS_LANG=AMERICAN_AMERICA.KO16KSC5601<br>
alias ss='sqlplus / as sysdba'<br>
alias sysc='sqlplus sys/oracle@localhost:1521/FREE as sysdba'<br>
alias sysp='sqlplus sys/oracle@localhost:1521/FREEPDB1 as sysdba'<br>

<br><br>

  sqlplus / as sysdba 로 오라클 기동,<br>
  lsnrctl start 로 리스너 기동<br><br>
  
  sqlplus / as sysdba 에서 다음 실행하면<br>

  '''
  
	SELECT    
	A.TABLESPACE_NAME,
	A.FILE_NAME ,
	(A.BYTES - B.FREE)    "Used_space",
	B.FREE                "Free_space",
	A.BYTES               "Total_Space",
	TO_CHAR( (B.FREE / A.BYTES * 100) , '999.99')||'%' "FreeSpace"
	FROM
	(
	    SELECT FILE_ID,
	    TABLESPACE_NAME,
	    FILE_NAME,
	    SUBSTR(FILE_NAME,1,200) FILE_NM,
	    SUM(BYTES) BYTES
	    FROM DBA_DATA_FILES
	    GROUP BY FILE_ID,TABLESPACE_NAME,FILE_NAME,SUBSTR(FILE_NAME,1,200)
	)A,
	(
	    SELECT TABLESPACE_NAME,
	    FILE_ID,
	    SUM(NVL(BYTES,0)) FREE
	    FROM DBA_FREE_SPACE
	    GROUP BY TABLESPACE_NAME,FILE_ID
	)B
	WHERE A.TABLESPACE_NAME=B.TABLESPACE_NAME
	AND A.FILE_ID = B.FILE_ID;
	
	CREATE TABLESPACE TS_MLDB 
	DATAFILE '/opt/oracle/oradata/FREE/TS_MLDATA01.dbf'
	SIZE 500M REUSE
	autoextend ON NEXT 1024K
	MAXSIZE UNLIMITED;

	ALTER SESSION SET "_ORACLE_SCRIPT"=TRUE;

	CREATE USER rquser IDENTIFIED BY nebula DEFAULT TABLESPACE TS_MLDB;
	GRANT CONNECT, RESOURCE TO rquser;
	GRANT DBA TO rquser;

    # 데이터 import 시도 함
	imp rquser/nebula file=./export.dmp fromuser=rquser touser=rquser
'''	

9. Anaconda 설치<br><br>

   저장한 곳에서 시작..<br>
   conda create -n tf39 python=3.9.*<br><br>
   
   conda activate tf39<br><br>
   
   > R 설치 한다.<br>
   conda install -c conda-forge r-essentials<br><br>
   
   
   위의 R 에서 해 주었던 것을 반복 한다.<br><br>
   
   
10. RInside import (root 에서)<br>
  > install.packages("/media/sf_LinuxGuru/oracle_linux_db_rpm/RInside_0.2.15.tar.gz")<br>
   <br>
11. $ORACLE_HOME/hs/admin/extproc.ora 교체 해야 함.<br>
[oracle@oel9]$ cd /media/sf_LinuxGuru/oracle_linux_db_rpm<br>
[oracle@oel9 oracle_linux_db_rpm]$ cp extproc.ora $ORACLE_HOME/hs/admin<br><br>

12. oracle home (/home/oracle) 에서 workspace 디렉토리 만들고,<br>
    cd /home/oracle/workspace<br>
    cp /media/sf_LinuxGuru/oracle_linux_db_rpm/ODCI*.gz .<br>
	tar cvfz ... 푼다.<br><br>


13. eclipse 로 개발 환경은 <br>
    > mkdir $HOME/repo<br>
	> cp eclipse-inst-jre-linux64.tar.gz $HOME/repo<br>
	> cd $HOME/repo 에서 위를 푼다음, eclipse-installer 에서 실행 시키면 됨.<br>
	> 실행 한 다음 위의 workspace 를 선택하면 개발 환경은 끝난 것임.<br>
	> yum install clang 을 설치하면 좋다.<br><br>
	
	
13. 여기까지는 특별히 문제는 없었고, 아래는 기타 사항으로 트러블 슈팅 용임.<br>


   11  yum update
  122  yum install /media/sf_LinuxGuru/flexiblas-devel-3.0.4-7.el9.x86_64.rpm
  123  yum install flexiblas-devel
  124  yum config-manager --set-enabled powertools
  130  yum install /media/sf_LinuxGuru/flexiblas-devel-3.0.4-8.el9.x86_64.rpm
  132  yum install /media/sf_LinuxGuru/libtirpc-devel-1.3.3-9.el9.x86_64.rpm
  134  yum install /media/sf_LinuxGuru/flexiblas-devel-3.0.4-8.el9.x86_64.rpm

   24  dnf install -y oracle-database-preinstall-19c
   26  dnf install -y oracle-database-free*
   30  dnf install -y oracle-database-free-23ai-1.0-1.el9.x86_64.rpm
   65  dnf install .//home/raymond/다운로드/dbeaver-ce-25.0.3-stable.x86_64.rpm
   66  dnf install /home/raymond/다운로드/dbeaver-ce-25.0.3-stable.x86_64.rpm
   67  dnf install ibus-hangul
  112  dnf install -y R-4.3.3-1.el8.x86_64.rpm
  113  dnf install R-*
  114  dnf install R
  116  dnf install libicu
  117  dnf install epel-release
  118  dnf install R
  119  dnf install flexiblas-devel
  125  dnf install 'dnf-command(config-manager)' 
  126  dnf install R
  127  dnf install R --nobest
  128  dnf install R --skip-broken
  133  dnf install R
  135  dnf --enablerepo=ol9_codeready_builder install flexiblas-netlib64
  136  dnf install R
  137  dnf --enablerepo=ol9_codeready_builder install flexiblas-devel
  138  dnf install R
  153  dnf install libprotobuf
  154  dnf install protobuf
  155  dnf install protoc
  177  dnf install lib-curl
  178  dnf install curl-devel

