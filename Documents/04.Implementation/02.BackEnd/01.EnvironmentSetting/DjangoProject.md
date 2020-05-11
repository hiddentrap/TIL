# DJango Project

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

## Project Structure

- superlists: 프로젝트 폴더 Root
  - functional_tests.py: Function Test (Use-Case)
  - superlists: Global Application
    - `__init__`.py
    - settings.py : Project 전역 설정
    - urls.py : 
    - wsgi.py

## Server Management

- python3 manage.py runserver : 서버 실행

- (서버 실행 중에 별도 터미널에서) python3 functional_tests.py : Functional Test 실행

- 

