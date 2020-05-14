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

### 신규 추가 파일없이 변경 내용 커밋하기

```
$ git commit -a -m 'second commit'
```

​	commit -a: 모든 변경 내용을 관리 가능 파일(이전에 커밋한 이력이 있는 파일)에 자동으로 반영한다

### 신규 파일 추가하고 변경 내용 확인 및 커밋하기

```
$ git status
$ git add .
$ git diff
$ git commit -am 'third commit'
```

### 커밋 히스토리 확인

```
$ git log --oneline
```

### 브랜치 목록 조회

#### 로컬

```
$ git branch --list
```

#### 원격

```
$ git branch -r
```

#### 로컬 + 원격

```
$ git branch -a
```

### 잘못 생성된 브랜치 삭제

```
$ git branch --delete bn
```

