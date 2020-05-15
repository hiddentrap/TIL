# Git

## 개념

[지옥에서 온 Git](https://opentutorials.org/course/2708/15606)

### 용어

**Stage**: commit 대상

**unstaged file**: staging 안 된 파일들로 수정되었어도 staging되지 않기 때문에 commit 대상이 아니다. git status 쳐보면 빨간 글씨로 나온다.

## Commit Message 작성법

- 제목과 본문은 한 줄 띄워 적는다
- 제목은 50자로 제한한다.
- 제목은 대문자로 작성한다.
- 제목은 마침표를 사용하여 끝내지 않는다.
- 제목은 명령조를 사용한다.
  - Add : 기능 혹은 코드 추가
  - Fix : 기존 코드 버그 수정 및 기능 수정
  - Rename : 파일 이름 및 명시된 이름 변경
  - Remove : 코드 삭제
  - Delete : 파일 삭제
  - Refactore : 코드 전면 수정
  - Move : 파일 이동
- 본문은 72자를 넘어가면 줄바꿈을 해준다.
- 본문에는 how가 아닌 what/why를 적는다.

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

### CheckOut 실패하는 경우 (Branch 이동 실패)

```
$ git reset 또는 git stash
```

​	주로 수정된 unstaged file이 존재할 때 checkout을 시도하면 나타나는 경우다.

이런경우 unstaged file을 add 시켜 stage에 올리고 commit한 뒤 checkout하면 되는데, 변경을 commit하지 않은체 checkout을 하고싶은 경우 두가지 방법이 있다.

기존 수정 내용을 다 날리고 브랜치를 바꾸고 싶은 경우 reset이용

reset: svn에서 revert와 같은 개념으로 변경 내용을 모두 되돌린다.

잘못된 브랜치에서 작업을 한 경우, 브랜치를 변경하고 수정 내용을 변경한 브랜치에서 불러오고 싶은 경우, stash 이용

stash: 변경된 내용과 마지막 커밋 정보를 임시 stack에 저장하고 working tree를 clean 시키므로 checkout이 가능하게 된다. 

브랜치를 변경한 후에는

```
# git stash pop
```

으로 원래 작업하던 내용을 불러올 수 있다.

list : stash stack 내용 보기

show : stash 상세보기

pop : stash 꺼내기

drop : stash 날리기

clear : stash 스택 비우기

