# Oracle Database Installation into Oracle Linux 8 (Oracle Enterprise Linux), OL8 or OEL8
<span style="color:blue"> OEL 8 + Oracle 23AI + Python with anaconda + R + BDAE 까지 테스트 위한 것들 </span>

1.  설치 화면에서
   1. 저장 장치
   2. 소프트웨어 - Workstation 선택
   3. root 암호 설정
   > sudo passwd root
   4. 네트워크 호스트 이름 설정

   '''
   dnf update 수행
   /etc/hosts 
   177.175.54.97 vbox.localdomain vbox
   '''
   
   여기까지 한 후에 Virtual Box 로 내보내기 함.
   
   
** 복구후에는 아래 처럼 root 암호 **
** VirtualBox 설정에서 클립보드 양방향, 공유 폴더 선언 해야 함. **

'''
dnf -y install oracle-database-preinstall-23ai
'''

2. oracle db 설치
   이미 다운로드 해 둔 것임.
   > 먼저 오라클 계정 등의 시스템 설정 변경 건.
   > 
'''
dnf -y install oracle-database-preinstall-23ai
'''
또는
'''
dnf -y localinstall oracle-database-preinstall-23ai-1.0-2.el8.x86_64.rpm
sysctl -p    
'''
** 오라클 계정이 설정/권한 되었는지 확인 **
'''
tail -1 /etc/passwd
tail -7 /etc/group
'''
** /etc/group 에 다음 추가 - 마운트 파일에 접근 권한 oracle 에게 주려고
'''
vboxsf:x:974:oracle
'''

** vi /etc/selinux/config **
'''
SELINUX=disabled
'''

** 아래 관련 shell 만들어서 한꺼번에 실행 **
'''
systemctl stop firewalld
systemctl disable firewalld
 
systemctl stop bluetooth
systemctl disable bluetooth
 
systemctl stop chronyd
systemctl disable chronyd
mv /etc/chrony.conf /etc/chrony.conf.bak
 
systemctl stop ntpdate
systemctl disable ntpdate
 
systemctl stop avahi-daemon.socket
systemctl disable avahi-daemon.socket
 
systemctl stop avahi-daemon
systemctl disable avahi-daemon
 
systemctl stop libvirtd
systemctl disable libvirtd
'''


** passwd oracle 실행 **
이제 설치한다.<br>
'''
dnf localinstall ./oracle-database-free-23ai-1.0-1.el9.x86_64.rpm
'''
** 가상 시스템의 메모리를 좀 줄이고 실행 시킨 후에 **
'''
/etc/init.d/oracle-free-23ai configure 시킨다.
'''

** 가상 시스템 메모리를 다시 올려 두고 실행한다. **

'''
# su - oracle
$ vi .bash_profile 

export ORACLE_BASE=/opt/oracle
export ORACLE_HOME=/opt/oracle/product/23ai/dbhomeFree/
export ORACLE_SID=FREE
export PATH=$PATH:$ORACLE_HOME/bin
export NLS_LANG=AMERICAN_AMERICA.KO16KSC5601
alias ss='sqlplus / as sysdba'
alias sysc='sqlplus sys/oracle@localhost:1521/FREE as sysdba'
alias sysp='sqlplus sys/oracle@localhost:1521/FREEPDB1 as sysdba'
'''


** 오라클 설치 후에 작업 **

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


SELECT * FROM DBA_PROFILES WHERE PROFILE='DEFAULT';
ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;


imp rquser/nebula file=./export.dmp fromuser=rquser touser=rquser
'''

**  R 설치가 OEL8 이 OEL9 보다 어렵다 ?. 주의 해야 한다. **
'''
dnf install epel-release
dnf --enablerepo=ol8_codeready_builder install openblas-devel
dnf install R
'''

** R 에서 Rcpp 설치, 파일에서 RInside 설치한다. **
/usr/lib64/R/library/Rcpp 의 libs/Rcpp.so 를 lib/libRcpp.so 로 심볼릭 링크 후에<br>
oracle home (/home/oracle) 에서 workspace 디렉토리 만들고,<br>
    cd /home/oracle/workspace<br>
    cp /media/sf_LinuxGuru/oracle_linux_db_rpm/ODCI*.gz .<br>
    tar cvfz ... 푼다.<br>
	
eclipse 로 개발 환경은 <br>
    > mkdir $HOME/repo<br>
	> cp eclipse-inst-jre-linux64.tar.gz $HOME/repo<br>
	> cd $HOME/repo 에서 위를 푼다음, eclipse-installer 에서 실행 시키면 됨.<br>
	> 실행 한 다음 위의 workspace 를 선택하면 개발 환경은 끝난 것임.<br>
	> yum install clang 을 설치하면 좋다.<br><br>
	
	
	
시도 해 보기, 재기동 후 성공 했었음.<br>




** 아래는 참조 하면 된다.  **

1. 오류 찾기
'''
yum install libxml2-devel
dnf install protobuf
'''

다시 한번 재기동 후에 성공하나 확인


2. Ananconda 설치한다
   '''
conda create -n tf39 python=3.9.*
'''

> 반드시 activate 한 후에 R 설치한다.<br>
'''
conda activate tf39
conda install -c conda-forge r-essentials
'''

-- TEST .. 이것은 굳이 하지 않아도 된다.  참고만 하자. <br>
'''
    9  dnf -y localinstall oracle-database-preinstall-23ai-1.0-2.el8.x86_64.rpm
   63  dnf -y localinstall oracle-database-free-23ai-1.0-1.el8.x86_64.rpm
   65  dnf -y localinstall ./oracle-database-free-23ai-1.0-1.el9.x86_64.rpm
   71  dnf install libnsl
   75  dnf install epel-release
   76  dnf install R
   77  dnf --enablerepo=ol9_codeready_builder install flexiblas-devel
   78  dnf --enablerepo=ol8_codeready_builder install flexiblas-devel
   79  dnf --enablerepo=ol9_codeready_builder install flexiblas-netlib64
   80  dnf --enablerepo=ol8_codeready_builder install flexiblas-netlib64
   81  dnf --enablerepo=ol8_codeready_builder install openblas-devel
   82  dnf install R
   96  dnf install protobuf-compiler
   97  dnf install protoc
   98  dnf install libicu
  122  dnf install libblas-dev
  150  dnf install protobuf-devel
  160  dnf install R-studio
  161  dnf install R-studioexit
  178  dnf install gsl-devel
  180  dnf install curl-devel
  187  dnf install libxml2-dev
  252  dnf install libglpk-dev
  253  dnf -y install glpk
  255  dnf -y install glpk-devel

   89  yum install protobuf
  188  yum install gsl-devel
  189  yum install libxml2-devel
'''
