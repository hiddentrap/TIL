# Logging

## 레벨

- DEBUG: 간단히 문제를 진단하고 싶을 때 필요한 자세한 정보기록
- INFO: 계획대로 작동하고 있음을 알리는 확인 메시지
- WARNING: 소프트웨어가 작동은 하고 있지만, 예상치 못한 일이 발생했거나 할 것으로 예측된다는 것을 알림
- ERROR: 중대한 문제로 인해 소프트웨어가 몇몇 기능들을 수행하지 못함을 알림
- CRITICAL: 작동이 불가능한 수준의 심각한 에러

## 구성요소

- Logger: 로거 인터페이스

- Handler: logger에 의한 log의 목적지

- 핸들러종류

  - ```python
    용량제한
    log_max_size = 10 * 1024 * 1024
    log_file_count = 20
    fileHandler = logging.handlers.RotatingFileHandler(filename='./log.txt', maxBytes=log_max_size,
                                                       backupCount=log_file_count)
    ```

    | SocketHandler   | 외부 로그 서버로 소켓을 통해 전송   |
    | --------------- | ----------------------------------- |
    | DatagramHandler | UDP 통신을 통해 외부 서버로 전송    |
    | SysLogHandler   | Unix 류의 syslog 데몬에게 로그 전송 |
    | SMTPHandler     | 메일로 로그 전송                    |
    | HTTPHandler     | HTTP를 통해 로그 전송               |

- Filter: 

- Formater: log 문자열 모양

  - | 이름        | 포맷            | 설명                                                        |
    | :---------- | :-------------- | :---------------------------------------------------------- |
    | asctime     | %(asctime)s     | 날짜 시간, 밀리세컨드까지 출력. ex) 2017.11.17 12:31:45,342 |
    | created     | %(created)f     | 생성 시간 출력                                              |
    | filename    | %(filename)s    | 파일명                                                      |
    | funcnName   | %(funcName)s    | 함수명                                                      |
    | levelname   | %(levelname)s   | 로그 레벨(DEBUG, INFO, WARNING, ERROR, CRITICAL)            |
    | levelno     | %(levelno)s     | 로그 레벨을 수치화해서 출력(10, 20, 30, …)                  |
    | lineno      | %(lineno)d      | 소스의 라인 넘버                                            |
    | module      | %(module)s      | 모듈 이름                                                   |
    | msecs       | %(msecs)d       | 로그 생성 시간에서 밀리세컨드 시간 부분만 출력              |
    | message     | %(message)s     | 로그 메시지                                                 |
    | name        | %(name)s        | 로그 이름                                                   |
    | pathname    | %(pathname)s    | 소스 경로                                                   |
    | process     | %(process)d     | 프로세스(Process) ID                                        |
    | processName | %(processName)s | 프로세스 이름                                               |
    | thread      | %(thread)d      | Thread ID                                                   |
    | threadName  | %(threadName)s  | Thread Name                                                 |

```python
# handler 객체 생성
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename="information.log")

# formatter 객체 생성
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# handler에 level 설정
stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# handler에 format 설정
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
```



## 콘솔에 로그 출력

### 예시

```python
import sys
import logging
logging.basicConfig(level=logging.DEBUG,
					format='[%(asctime)s][%(levelname)s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
                    stream=sys.stdout
					)
logging.info('안내')
```

### 로거 생성 함수

```python
def make_logger(name=None):
    #1 logger instance를 만든다.
    logger = logging.getLogger(name)

    #2 logger의 level을 가장 낮은 수준인 DEBUG로 설정해둔다.
    logger.setLevel(logging.DEBUG)

    #3 formatter 지정
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    #4 handler instance 생성
    console = logging.StreamHandler()
    file_handler = logging.FileHandler(filename="test.log")
    
    #5 handler 별로 다른 level 설정
    console.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    #6 handler 출력 format 지정
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    #7 logger에 handler 추가
    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger
#-----------------------------------------------------

logger = make_logger()

logger.debug("test")
logger.info("test")
logger.warning("test")
```

## 설정파일에서 로거 생성

logging.conf

```python
##############################################################
## 키 정의
##############################################################
[loggers]
keys=root,log02,log03

[handlers]
keys=handle01,handle02

[formatters]
keys=form01

##############################################################
## 로거 정의
# root는 기본로거, log02는 콘솔만 출력, log03은 콘솔과 시간기준으로 순환하는 파일에 로깅
##############################################################
## 루트 로거 구성은 [logger_root]섹션에서 지정한다.
[logger_root]
handlers=handle01
level=INFO

[logger_log02]
qualname=log02
handlers=handle01
level=NOTSET
propagate=0

[logger_log03]
qualname=log03
handlers=handle01,handle02
level=NOTSET
propagate=0

##############################################################
## 핸들러 정의
# TimedRotatingFileHandler에는 "M"(분단위) 1분간격 2개 백업하도록 설정
# 시간단위로 순환하며 기록하고 싶다면 "H", 일단위로 순환하며 기록하고 싶다면 "D"
# 참고로 로깅하는 시점부터 만 1시간, 만 1일 
# 만약 일단위로 순환하되 자정마다 새로 순환하며 기록하고 싶다면 "midnight"를 지정
##############################################################
[handler_handle01]
class=StreamHandler
formatter=form01
level=NOTSET
args=(sys.stdout,)

[handler_handle02]
class=handlers.TimedRotatingFileHandler
formatter=form01
level=NOTSET
args=('%(str_log_file_name)s', 'M', 1, 2, 'utf8', False, False)
# args: filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None

##############################################################
## 포멧터 정의
##############################################################
[formatter_form01]
format=%(asctime)s.%(msecs)03dZ|%(levelname)s|%(funcName)s()|%(message)s
datefmt=%Y-%m-%dT%H:%M:%S
```

로거사용

```python
import logging
import logging.config
import time

str_log_file_name = "my.log"
logging.config.fileConfig("logging.conf", disable_existing_loggers=False, defaults={"str_log_file_name" : str_log_file_name}) 
# disable_existing_loggers=False: 기 존재 로거도 계속 사용하도록 한다
logger = logging.getLogger("log03")

def function1():
    logger.info('haha...')
    time.sleep(20)

for i in range(99):
    function1()
```

