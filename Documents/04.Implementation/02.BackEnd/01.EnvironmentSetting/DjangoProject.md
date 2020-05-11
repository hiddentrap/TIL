# DJango Project

## Workflow

1. 특정 URL로 HTTP request 유입
2. URL resolving으로 해당 request를 특정 view function으로 매칭한다.
3. view function에서 해당 request를 처리하고 HTTP response를 리턴한다.

## Project Start

- django-admin.py startproject superlists
- git init . : git 초기화
- echo 'db.sqlite3' >>  .gitignore : 버전관리 제외처리
- git add. : 스테이징
- git status : 스테이징 상태 확인
- git rm -r --cached superlists/`__pycache__` : 캐쉬파일 삭제
- echo '`__pycache__`' >> .gitignore : 버전관리 제외처리
- echo '*.pyc' >> .gitignore : 버전관리 제외처리
- git status : 스테이징 상태 확인
- git add .gitignore : 버전관리 제외처리 파일 스테이징 추가
- git commit -m 'first commit' : 스테이징 파일 커밋

### 앱 추가

- python3 manage.py startapp lists

## Project Structure

​	하나의 프로젝트는 여러 앱을 가질 수 있으며, 다른 사람이 만든 외부 앱도 사용할 수 있다. 

- superlists: 프로젝트 폴더 Root
  - db.sqlite3
  - functional_tests.py: Function Test (Use-Case)
  - lists
    - admin.py
    - `__init__`.py
    - migrations
      - `__init__`.py
    - templates : html 템플릿
    - models.py
    - tests.py : 단위 테스트
    - views.py
  - manage.py
  - superlists: Global Application
    - `__init__`.py
    - settings.py : Project 전역 설정
    - urls.py : URL 과 View Function 매핑 for Global, include로 Sub app의 urls.py 지정가능
    - wsgi.py

## Server Management

- python3 manage.py runserver : 서버 실행
- (서버 실행 중에 별도 터미널에서) python3 functional_tests.py : Functional Test 실행
- python3 manage.py test : 단위 테스트 실행

## Source Version Control

- git status : untracked된 파일들을 확인한다.
  - untracked된 파일이 있을경우,
    - git add lists : untracked된 파일을 스테이징한다.
    - git diff --staged : 커밋하려는 추가 코드를 확인한다.
    - git commit -m "commit reason"
    
  - untracked된 파일이 없을경우,

    - git diff : 커밋하려는 파일들의 변경 내역을 확인한다.

    - got commit -am "commit reason"

