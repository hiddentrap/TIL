# Python

## PIP

> pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available

Windows10에서 Anaconda를 사용할 경우, 환경번수 PATH에 추가

```
C:\ProgramData\Anaconda3
C:\ProgramData\Anaconda3\Scripts
C:\ProgramData\Anaconda3\Library\bin
```

## Django

### workflow

1. 특정 URL로 HTTP request 유입
2. URL resolving으로 해당 request를 특정 view function으로 매칭한다.
3. view function에서 해당 request를 처리하고 HTTP response를 리턴한다.