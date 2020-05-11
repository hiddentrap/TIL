# Python

## PIP

> pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available

Windows10에서 Anaconda를 사용할 경우, 환경번수 PATH에 추가

```
C:\ProgramData\Anaconda3
C:\ProgramData\Anaconda3\Scripts
C:\ProgramData\Anaconda3\Library\bin
```

## Development Flow

1. 사용자 관점에서 Functional Test를 작성한다.
2. 기능 테스트가 실패하면, 통과할 수 있는 방법을 고민한다.
3. 도출된 해결방법을 기술할 코드가 동작해야 하는 기능을 단위테스로 작성한다.
4. 단위 테스트가 실패하면, 통과할 수 있을만큼만의 최소한의 코드만 작성한다.
5. 기능 테스트가 완전해질 때까지 3과 4를 반복한다.
6. 기능 테스트를 재실행해서 통과하는지 또는 제대로 동작하는지 확인하고 2번부터 다시 반복한다.