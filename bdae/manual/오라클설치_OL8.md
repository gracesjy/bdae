# Oracle Database Installation into Oracle Linux 8 (Oracle Enterprise Linux), OL8 or OEL8
<span style="color:blue"> OEL 8 + Oracle 23AI + Python with anaconda + R + BDAE 까지 테스트 위한 것들 </span>

1.  설치 화면에서
   1. 저장 장치
   2. 소프트웨어 - Workstation 선택
   3. root 암호 설정
   > sudo passwd root
   4. 네트워크 호스트 이름 설정<br><br>


   dnf update 수행<br>
   /etc/hosts <br>
   177.175.54.97 vbox.localdomain vbox<br><br>

   
여기까지 한 후에 Virtual Box 로 내보내기 함.<br>
   
   
** 복구후에는 아래 처럼 root 암호 **<br>
** VirtualBox 설정에서 클립보드 양방향, 공유 폴더 선언 해야 함. **<br><br>

dnf -y install oracle-database-preinstall-23ai<br><br>

2. oracle db 설치<br>
   이미 다운로드 해 둔 것임.<br>
   > 먼저 오라클 계정 등의 시스템 설정 변경 건.<br>
   > <br>
dnf -y install oracle-database-preinstall-23ai<br>
또는<br>
dnf -y localinstall oracle-database-preinstall-23ai-1.0-2.el8.x86_64.rpm<br>
sysctl -p    <br>
<br>
** 오라클 계정이 설정/권한 되었는지 확인 **<br>
<br>
tail -1 /etc/passwd<br>
tail -7 /etc/group<br>
<br>
** /etc/group 에 다음 추가 - 마운트 파일에 접근 권한 oracle 에게 주려고<br>
<br>
vboxsf:x:974:oracle<br>
<br>

** vi /etc/selinux/config **<br>
<br>
SELINUX=disabled<br>
<br>

** 아래 관련 shell 만들어서 한꺼번에 실행 **<br>
<br><br>

systemctl stop firewalld<br>
systemctl disable firewalld<br>
 <br>
systemctl stop bluetooth<br>
systemctl disable bluetooth<br>
 <br>
systemctl stop chronyd<br>
systemctl disable chronyd<br>
mv /etc/chrony.conf /etc/chrony.conf.bak<br>
 
systemctl stop ntpdate<br>
systemctl disable ntpdate<br>
 
systemctl stop avahi-daemon.socket<br>
systemctl disable avahi-daemon.socket<br>
 
systemctl stop avahi-daemon<br>
systemctl disable avahi-daemon<br>
 
systemctl stop libvirtd<br>
systemctl disable libvirtd<br>


** passwd oracle 실행 **<br>
이제 설치한다.<br>
dnf localinstall ./oracle-database-free-23ai-1.0-1.el9.x86_64.rpm<br>
<br>
** 가상 시스템의 메모리를 좀 줄이고 실행 시킨 후에 **<br>
<br>
/etc/init.d/oracle-free-23ai configure 시킨다.<br>
<br><br>

** 가상 시스템 메모리를 다시 올려 두고 실행한다. **<br>

** su - oracle **<br>

$ vi .bash_profile <br>

export ORACLE_BASE=/opt/oracle<br>
export ORACLE_HOME=/opt/oracle/product/23ai/dbhomeFree/<br>
export ORACLE_SID=FREE<br>
export PATH=$PATH:$ORACLE_HOME/bin<br>
export NLS_LANG=AMERICAN_AMERICA.KO16KSC5601<br>
alias ss='sqlplus / as sysdba'<br>
alias sysc='sqlplus sys/oracle@localhost:1521/FREE as sysdba'<br>
alias sysp='sqlplus sys/oracle@localhost:1521/FREEPDB1 as sysdba'<br>


** 오라클 설치 후에 작업 **<br>
```
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
```

**  R 설치가 OEL8 이 OEL9 보다 어렵다 ?. 주의 해야 한다. **<br>
<br>
dnf install epel-release<br>
dnf --enablerepo=ol8_codeready_builder install openblas-devel<br>
dnf install R<br>
<br>

** R 에서 Rcpp 설치, 파일에서 RInside 설치한다. **<br>
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
	
	
	
시도 해 보기, 재기동 후 성공 했었음.<br><br>




** 아래는 참조 하면 된다.  **<br><br>

1. 오류 찾기<br>
yum install libxml2-devel<br>
dnf install protobuf<br>
<br>

다시 한번 재기동 후에 성공하나 확인<br>


2. Ananconda 설치한다<br>
<br>
conda create -n tf39 python=3.9.*<br><br>

> 반드시 activate 한 후에 R 설치한다.<br<br>

conda activate tf39<br>
conda install -c conda-forge r-essentials<br>


-- TEST .. 이것은 굳이 하지 않아도 된다.  참고만 하자. <br>
    9  dnf -y localinstall oracle-database-preinstall-23ai-1.0-2.el8.x86_64.rpm<br>
   63  dnf -y localinstall oracle-database-free-23ai-1.0-1.el8.x86_64.rpm<br>
   65  dnf -y localinstall ./oracle-database-free-23ai-1.0-1.el9.x86_64.rpm<br>
   71  dnf install libnsl<br>
   75  dnf install epel-release<br>
   76  dnf install R<br>
   77  dnf --enablerepo=ol9_codeready_builder install flexiblas-devel<br>
   78  dnf --enablerepo=ol8_codeready_builder install flexiblas-devel<br>
   79  dnf --enablerepo=ol9_codeready_builder install flexiblas-netlib64<br>
   80  dnf --enablerepo=ol8_codeready_builder install flexiblas-netlib64<br>
   81  dnf --enablerepo=ol8_codeready_builder install openblas-devel<br>
   82  dnf install R<br>
   96  dnf install protobuf-compiler<br>
   97  dnf install protoc<br>
   98  dnf install libicu<br>
  122  dnf install libblas-dev<br>
  150  dnf install protobuf-devel<br>
  160  dnf install R-studio<br>
  161  dnf install R-studioexit<br>
  178  dnf install gsl-devel<br>
  180  dnf install curl-devel<br>
  187  dnf install libxml2-dev<br>
  252  dnf install libglpk-dev<br>
  253  dnf -y install glpk<br>
  255  dnf -y install glpk-devel<br><br>

   89  yum install protobuf<br>
  188  yum install gsl-devel<br>
  189  yum install libxml2-devel<br>
<br>
