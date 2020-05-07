# Git

## 개념

[지옥에서 온 Git](https://opentutorials.org/course/2708/15606)

## 시나리오별 사용법

### 원격 저장소(Repository) 에서 기존 프로젝트 시작

1. 프로젝트 폴더로 사용할 디렉토리 생성 및 이동

2. 해당 디렉토리에서 Git Bash shell 실행

3. 프로젝트 Clone (저장소 복제)

   ```
   $ git clone https://github.com/hiddentrap/TIL.git .
   ```
   
   git clone <원격저장소> <로컬경로>: 원격 저장소를 로컬경로에 복제

### 로컬 저장소 에서 신규 프로젝트 시작

1. 프로젝트 폴더로 사용할 디렉토리 생성 및 이동

2. 해당 디렉토리에서 Git Bash shell 실행

3. 프로젝트 Init (저장소 생성 또는 초기화)

   ```
   $ git init
   $ git add README.md
   $ git commit -m "first commit"
   $ git remote add origin https://github.com/hiddentrap/TIL.git
   $ git push -u origin master
   ```
   
   add: 파일 컨텐츠(README.md)를 변경내역 관리대상 Index(Stage)에 추가
   
   commit -m "주석": 변경내역을 로컬저장소에 기록(Snapshot)
   
   remote add <원격저장소 이름> <원격저장소 주소>: 원격저장소 추가
   
   git push <-u> <원격저장소 이름> <브랜치 이름>: 원격저장소에 브랜치의 변경내역 업로드

### 원격 저장소 브랜치 내려받기

```
$ git pull origin master
```

​	pull <원격저장소 이름> <브랜치 이름>