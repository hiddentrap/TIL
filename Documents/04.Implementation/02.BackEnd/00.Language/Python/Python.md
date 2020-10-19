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



## 동시성 프로그래밍

### 쓰레드

daemon 기본 속성: False : 메인 쓰레드가 종료되도 자신의 작업이 끝날 때까지 계속 실행



