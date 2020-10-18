# Redmine

<<<<<<< HEAD
## Install Redmine with docker

1. 아래와 같이 최신 redmine Docker 이미지를 다운로드 받습니다. 

   ```
   $ docker pull redmine
   ```

2. Docker 볼륨을 생성하여 데이터를 계속해서 유지하는 Container 실행 

   ```
   $ docker volume create redmine-plugins
   $ docker volume create redmine-themes
   $ docker volume create redmine-data
   
   $ docker run -d --name redmine -p 30002:3000 -e REDMINE_DB_USERNAME=redmine -e REDMINE_DB_PASSWORD=redmine -e REDMINE_DB_POSTGRES=192.168.0.50 -e REDMINE_DB_PORT=5433 -e REDMINE_DB_DATABASE=redmine -v redmine-plugins:/usr/src/redmine/plugins -v redmine-themes:/usr/src/redmine/public/themes -v redmine-data:/usr/src/redmine/files redmine
   
   $ docker exec -it redmine bash
   $ apt update
   $ apt install make gcc 
   ```

3. 참고. docker-compose.yml [mysql버전]

   ```
   version: '3'
   services:
   
     redmine:
       image: redmine
       restart: always
       ports:
         - 3000:3000
       environment:
         - REDMINE_DB_MYSQL=redmine
         - REDMINE_DB_PASSWORD=pass
         - REDMINE_PLUGINS_MIGRATE=true
       volumes:
         - ./redmine_data:/usr/src/redmine/files
         - ./redmine-plugins:/usr/src/redmine/plugins
         - ./redmine-themes:/usr/src/redmine/public/themes
   
     mysql_redmine:
       image: mysql:5.7
       restart: always
       environment:
         - MYSQL_ROOT_PASSWORD=pass
         - MYSQL_DATABASE=redmine
       volumes:
         - ./mysql-data_red:/var/lib/mysql 
   ```

   ```
   $ docker-compose up -d
   ```



## Install Plugins

**반드시 root 계정으로 설치하지 말것 redmine계정으로 su redmine**

### 일반적인 설치과정

```
# if the name of the redmine container is abt then use the following command to login:
docker exec -it abt bash

# change to plugins directory
cd plugins

# download source code
wget https://redmine.ociotec.com/attachments/download/440/scrum%20v0.16.2.tar.gz

# extract
tar xvf scrum\ v0.16.2.tar.gz
or
unzip xxx.zip

# install
bundle exec rake redmine:plugins:migrate

# restart container: 
docker restart abt
```



### redmine_dmsf

https://github.com/danmunn/redmine_dmsf

1. Container shell 접속	

   ```
   $ docker exec -it redmine bash
   $ cd plugins
   ```

1. 의존성 패키지 설치 (데비안 기준)

   ```
   apt-get install xapian-omega ruby-xapian libxapian-dev xpdf poppler-utils antiword unzip catdoc libwpd-tools libwps-tools gzip unrtf catdvi djview djview3 uuid uuid-dev xz-utils libemail-outlook-message-perl
   ```

2. Git clone

   ```
   su redmine
   git clone https://github.com/danmunn/redmine_dmsf
   git clone -b devel-2.0.1 https://github.com/danmunn/redmine_dmsf [특정버전 받는법]
   ```

3. 설치

   ```
   su redmine
   $ cd .. [redmine 디렉토리로 이동]
   $ bundle install
   $ RAILS_ENV=production bundle exec rake redmine:plugins:migrate NAME=redmine_dmsf
   $ chown -R www-data:www-data plugins/redmine_dmsf [권한부여]
   ```



### CKEditor

http://github.com/a-ono/redmine_ckeditor

```
$ docker exec -it redmine bash
$ apt-get install imagemagick
$ cd plugins
$ su redmine
$ git clone https://github.com/a-ono/redmine_ckeditor
$ cd ..
$ bundle install --without development test
$ rake redmine:plugins:migrate RAILS_ENV=production
```

```
$ wget https://github.com/a-ono/redmine_ckeditor/archive/master.zip
$ unzip master.zip
$ mv redmine_ckeditor-master/ redmine_ckeditor
$ rm master.zip
```

=======
- sudo --login
- docker ps / docker restart id
- cd /volume2/@docker/btrfs/subvolumes/dcd4552c3558d65900987b40c027a46d7f5abb5ec467ba0dc280a2d6f3ab70cf/home/redmine/redmine
- docker exec -i -t synology_redmine /bin/bash
- cd plugins
>>>>>>> b8d1b360e2dc176e5f33d6bc4f01b1d906dd2e62
