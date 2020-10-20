# Python

## PIP

> pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available

Windows10에서 Anaconda를 사용할 경우, 환경번수 PATH에 추가

```
C:\ProgramData\Anaconda3
C:\ProgramData\Anaconda3\Scripts
C:\ProgramData\Anaconda3\Library\bin
```

### SSL 관련 오류 발생시

```
pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org

pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 파이참 파이썬 콘솔 한글 깨짐

Ctrl+Alt+S

Build, Execution, Deployment > Console > Python Console

```
Starting script 제일 하단에
!chcp 65001 추가
```

또는

```
sys.stdout = io.TestIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TestIOWrapper(sys.stderr.detach(), encoding='utf-8')
을 소스 최상단에 추가
```



### 파이참 터미널에서 venv activation이 잘안되면

Settings > Tools > terminal > Shell path

```
"cmd.exe" /k ""D:\Study\TIL\Projects\GUI\trader\venv\Scripts\activate.bat""
```



## 동시성 프로그래밍

### 쓰레드

daemon 기본 속성: False : 메인 쓰레드가 종료되도 자신의 작업이 끝날 때까지 계속 실행



## Requirements 설치

```
install -r requirements.txt
```



## Modules

```
- ipython
- mypy
	자료형 체커, http://mypy-lang.org
- flake8
	코드 분석기, report problems or errors, http://flake8.pycqa.org/en/latest/
- pylint
	코드 분석기, report problems or errors, www.pylint.org/
- pytest
	파이썬 테스트 프레임워크
- black
	파이썬 코드 포매터, https://github.com/psf/black
- yapf
	파이썬 코드 포매터, Yet Another Python Formatter, https://github.com/google.yapf
	$ yapf -i hello.py
- pendulum
	날짜시간을 쉽게 다를 수 있게 함.
```

## PyTest

```
pytest -xv test.py
-x Failed 되면 즉시 멈춤
-v 자세하게 보기
-pdb 디버그 모드

output:
> 에러 바로 전 라인
E 에러
- 예상값
+ 실제값

1. test function 이름은 test_ 로 시작해야함

pytest중에 print로 찍을 수 있게 만들기
프로젝트 루트에 pytest.ini 만들고
[pytest]
addopts = -s

```

### 절차

```
test작성
코드작성
mypy -type 
pytest -xv code.py
yapf -i code.py or black code.py
flake8 code.py or pylint code.py
```

