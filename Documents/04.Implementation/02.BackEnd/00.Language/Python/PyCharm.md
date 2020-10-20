# Pycharm

- 검색: Shift, Shfit
- Action: Ctrl + Shift + A
- 프로젝트창: Alt + 1
- 에디터창: F4
- **터미널: Alt + F12**
- 파이썬콘솔: Alt + 0
- **관련문서확인: Ctrl + Q**
- **정의확인: Ctrl + Shfit + I**
- 코드감싸기: Ctrl + Alt + T
- 윈도우 이동: Alt + 0, 1, 2, 3, 4 ...
- 파라메터확인 : Ctrl + P
- 문장 중간에서 줄바꿈: Shift + Enter
- 뒤로 라인추가 Ctrl+Enter, 앞으로 라인추가 Alt+Enter
- 라인복제: Ctrl + D
- 라인삭제: Ctrl + Y
- 줄 합치기 : Ctrl + Shift + J
- 문장 이동: Shift + Alt + 위아래 방향키
- 블럭 이동: Shift + Ctrl + 위아래 방향키
- html 속성 이동 : Shft + Ctrl + Alt + 좌우방향키
- **같은 단어 선택: Alt+J, Shift+Alt+J**
- import 정리: Ctrl + Alt + O
- Indent 정리 : Ctrl + Alt + L
- 소스 폴딩 : Ctrl + +, Ctrl + -, 한번에: Ctrl + Shift + +,-
- 단어단위로 삭제 : Ctrl + Del, Ctrl+ <-
- **멀티포커스 에디팅 : Ctrl + Ctrl 누르고 있는 상태에서 화살표**
- **오류라인 이동 F2**
- **정의로 이동 Ctrl+B**
- 라인번호로 이동 : Ctrl + G
- 부모 클래스로 이동: Ctrl + U
- 메서드 단위 이동: Alt + 위아래
- 이전창으로 : F12
- **참조찾기: Ctrl+F7, Alt+F7, Ctrl+Alt+F7**
- 프로젝트 전체에서 찾기 : Ctrl + Shift + F

## 리팩토링

- **리팩토링 메뉴 Ctrl+Alt+Shfit+T**
- 이름바꾸기 Shift+F6
- **메서드추출 Ctrl+Alt+M**
- 변수추출 Ctrl+Alt+V
- **파라메터 추출 Ctrl+Alt+P**

## 디버깅

- 디버깅: Shift+F9
- **단계실행 F7**
- 내코드안으로만 실행 Alt + Shift + F7
- **안들어가고 단계실행 F8**
- 호출한 지점으로 실행이동 F7로 들어왔을때 Shift + F8
- **다음 브포까지 실행 F9**
- **식조사 Alt + F8**
- 브포 안걸고 그냥커서로 이동 Alt+F9
- **브포찍기 Ctrl + F8**
- **브포라인에서 Ctrl+Shift+F8 조건 브포**
- 실행종료 Ctrl + F2
- 재실행 Ctlr+F5

## 코드자동완성

- 기본완성 Ctrl + Space, Ctrl + Alt + Space
- 감싸기 Ctrl _+ Alt + T
- 자동완성 Alt + Enter (Seeting/ intentions 참고)
- 히플완성 Alt+/. Alt + Shift + /
- f'abc'.p  -> print(f'a')  : postfix
- Live Template [인터넷 검색해보기]

## 기타 유용한 기능

- 북마크 F11
- 단축키 북마크 Ctrl + F11
- 북마크 이동 Shfit + F11
- Auto Scroll from Source
- 뷰모드: 코드리뷰시 Ctrl + ~
- 플러그인
  - BashSupport
  - .ignore

## Git

- **Alt + `**
- revert 뒤로 돌림
- version control
- Add -> Commit -> Push(GitHub)
- 최초에 프로젝트를 GIt에 넣을때
  - VCS > Enable Version control integration 또는 VCS > Import into Version Control
  - .idea 폴더 내용은 제외시킴 (ignore plugin : new > .ignore file > .gitignorefile > jetbrain, ADD, Commit, Push)
- 최초에 프로젝트를 git에서 clone 해올때: 프로그램 실행시 checkout from version control
- Git 초기화: Version Control settings 에서 삭제, 프로젝트 폴더에서 숨김폴더중 .git 폴더 날림
- Create Gist : 코드 공유
- clone : 다른 저장소의 내용을 내  로컬 레포지토리로 복사
- fork: 다른 저장소의 내용을 내 원격 저장서로 가져옴
- fetch: 원격 저장소의 변경 내용 이력만 업데이트 소스코드가 merge가 되진 않음
- pull: fetch + merge
- merge: 합쳐질 브랜치 체크아웃 (master)  -> Ctrl+Shift + ` -> merge할 브랜치에서 merge into current
- rebase: merge와 유사하지만 rebase권장
- 브랜치 삭제 (실무에서는 브랜치를 잘 삭제하지 않음 ): Ctrl+Shift + `에서 할 수 있음
- branch: Ctrl + Shift + `
  - Add 브랜치 (기능 추가)
  - 개선 브랜치
  - 수정 브랜치
  - 각 브랜치에서 작업후 나중에 master(운영 브랜치)로 merge
  - new Branch
  - check out : 현재 작업할 branch 지정
- Add (스테이징에 반영): Ctrl + Alt+ A
- Commit (스테이징 변화내용을 로컬 히스토리에 저장): Ctrl + K
- Push(로컬 히스토) : Ctrl + Shift + K
- 

## 기타

- 아나콘다
  - 아나콘다 설치 
    - 64bit graphic installer
    - anaconda prompt
  - 가상환경 설정 및 패키지 설치
    - anaconda prompt 
      - 가상환경 목록: conda info -e
      - 가상환경 생성: conda create -n 가상환경명 python=3.6
      - 가상환경 전환: activate 가상환경명 / conda deactivate
      - 가상환경 패키지 목록: conda list
      - 패키지 설치: cinda install 패키지명
      - 가상환경 삭제 : conda remove -n 가상환경명 --all
  - settings
  - project
  - project interpreter
    - add > conda environment > exists > 가상환경 경로(conda>env>가상환경명>python.exe)
    - 에러나면, 파이참 재부팅이나 가상환경 위에서 실행
    - anacondda prompt > activate 가상환경명 > pycharm64.exe 실행
  - 패키지 확인 및 추가설치
  - 소스코드 실행
- R
  - R 인터프리터 및 Rstudio 설치
  - plugins
  - R Support 설치
  - settings
  - Language
  - R 인터프리터 설정
  - 테스트코스 실행
  - https://cran.r-project.org/mirrors.html
  - https://www.rstudoi.com/products/rstudio/download/
- Flask 경량형 프레임워크 (REST API, Android Push, 테스트성, 간단한 웹페이지성)
  - new project
    - 
  - flask
  - 문법, 인터프리터설정
  - 가상환경 또는 project interpreter flask 설치
    - install flask
  - 서버 실행후 브라우저 테스트
- Django: 범용 프레임워크 (로그인, 관리자, 세션, ORM) ERP성 큰 프로젝트
  - 가상환경 설정 및 django 설치
    - install django
  - new project
  - 문법 및 인터프리터 설정
  - 서버 실행후 브라우저 테스트
- 그외

