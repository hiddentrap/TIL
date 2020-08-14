# PostgreSQL

## Install with Docker

1. 아래와 같이 최신 postgres Docker 이미지를 다운로드 받습니다. 

   ```
   $ docker pull postgres
   ```

2. admin 비밀번호를 셋팅하는 방법은 다음과 같습니다.  [2번 건너뛰고 3번으로 진행]

   ```
   $ docker run -d -p 5432:5432 --name pgsql -e POSTGRES_PASSWORD=mysecretpassword postgres
   ```

3. Docker 볼륨을 생성하여 데이터를 계속해서 유지해야 한다면 다음 옵션을 사용합니다. 

   ```
   $ docker volume create pgdata
   $ docker run -d -p 5432:5432 --name pgsql -it --rm -v pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=[password] postgres
   ```

4. 컨테이너에 접속하여 postgres 설정을 진행합니다. 

   ```
   $ docker exec -it pgsql bash
   
   root@cb9222b1f718:/# psql -U postgres
   psql (10.3 (Debian 10.3-1.pgdg90+1))
   Type "help" for help.
   postgres=# CREATE DATABASE mytestdb;
   CREATE DATABASE
   postgres=#\q
   ```

5. 기본 이미지에서 추가 초기화 작업을 진행할 경우 다음과 같이 설정을 진행합니다. 

   - 다음 예제는 사용자와 데이터베이스를 추가하는 작업입니다. 

   ```
   root@12345# vi /docker-entrypoint-initdb.d/init-user-db.sh
   
   #!/bin/bash
   set -e
   
   psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
     CREATE USER docker;
     CREATE DATABASE docker;
     GRANT ALL PRIVILEGES ON DATABASE docker TO docker;
   EOSQL
   ```

6. 다음과 같이 설정을 진행했다면 외부에서 데이터베이스를 사용할 수 있습니다. 

## Administration

### 사용자 생성

```
create user redmine password 'redmine';

select  * from pg_user;

\du

CREATE USER name [ [ WITH ] option [ ... ] ]
Option들 중 중요한 것들만 간략하게 설명하면 다음과 같다.

SUPERUSER | NOSUPERUSER ; Superuser 여부. 기본값은 NOSUPERUSER이다.
CREATEDB | NOCREATEDB ; DB생성 권한 부여 여부. 기본값은 권한 없음 이다.
CREATEUSER | NOCREATEUSER ; User생성 권한 부여 여부. 기본값은 권한 없음 이다.
PASSWORD 'password' ; Password 설정
```

### DB 생성

```
create database redmine owner redmine;

select  * from pg_database

\l

Option들을 간단하게 살펴보면 다음과 같다.

OWENR : DB owner. Owner 외에 다른 계정은 역할 제한이 있다.
TEMPLATE : DB Template에 의해 생성될 때 Template 이름이다. 기본값은 template1이다.
ENCODING : Data Encoding 방법. 값을 지정할 때 LC_CTYPE, LC_COLLATE value와 연계되기 때문에 주의해야 한다.
LC_COLLATE : String Data를 기준으로 정렬할 때 정렬 기준. 예를 들면 ko_KR.UTF-8은 기본적으로 한글 기준으로 정렬하되, 한글 외의 문자는 UTF-8에 의해 정렬하라는 의미다. 본 시스템 설치 시 ko_KR.UTF-8이 기본값으로 설정되어 있다. (template1의 기본값)
LC_CTYPE : 대, 소문자, 숫자 등과 같은 문자 분류를 위한 설정.
TABLESPACE : Table Space를 임의로 설정할 때 사용.
ALLOW_CONNECTIONS : 외부에서 접속 가능 여부 설정
CONNECTION LIMIT : DB 접속 제한 설정.
IS_TEMPLATE : DB Template 인지 여부 설정
```

