# TDD - Test Driven Development

## Principle

내가 작성한 모든 코드는 테스트 되어야 한다.

## Test 종류

### Functional Test : End to End Test : UseCase Test

​	HTTP API를 대상으로 한다. 기능의 동작을 시현하기 위한 목적으로 작성한다.

### Service Layer Test

​	각 테스트는 기능과 페이크 I/O의 코드 실행 경로를 커버하는 경향이 있으며, 비지니스 로직의 시작과 끝을 테스트 한다

- 서비스 레이어 테스트를 작성할 때는 도메인 오브젝트 대신 primitive를 사용하여 도메인 모델과 의존성을 끊어 순수한 테스트를 작성할 수 있도록 한다.

### Domain Model Test

​	단위 범위에 집중적인 테스트 커버리지를 갖으며 엄격한 피드백을 줄 수 있다. 후에 서비스 레이어 테스트에 의해 기능이 테스트 될수 있으면 삭제하도록 한다.

## WorkFlow

**Functional Test 작성 - Unit Test 작성 - Code 작성 - Functional Test 성공시 Refactoring**

1. Functional Test 작성 - 사용자 입장에서 기술하는 기능(UseCase) 테스트

2. Functional Test가 실패하면, 성공시키기 위해 작성해야할 코드를 생각해보고 그 코드의 동작을 정의하기 위한 unit test들을 작성

   ```
   python manage.py runserver
   python functional_tests.psy
   ```

3. unit test가 실패하면, 성공시키기 위해 가능한한 적은 양의 어플리케이션 코드를 작성한다. Functional Test가 성공할 때까지, 2번과 3번을 반복한다.

   ```
   python manage.py test
   ```

4. unit test나 functional test가 성공하면 리팩터링이 필요한지 생각해보고 필요하다면 리팩터링 한다.

FunctionalTest는 **사용자 행위를 기술**하듯 작성한다.

Unit Test는 **Given-When-Then 패턴**으로 작성한다



##### 레드/그린/리팩터와 삼각법

단위 테스트-코드 주기를 레드, 그린, 리팩터로 설명하는 경우

- 실패할 단위 테스트를 작성함으로써 작업을 시작한다(레드)
- 이 테스트를 통과할 최소 코드를 작성한다(그린), 편법이라도 상관없다.
- 코드를 리팩터링해서 이해할 수 있는 코드로 만든다.

## Given-When-Then Pattern For Test writing

### Examples

#### 로그인

> Given - 로그인 페이지가 열린다.
>
> When - 유저가 ID와 패스워드를 입력하고 로그인 버튼을 누른다.
>
> Then - 유저는 홈페이지에 로그인 상태로 진입한다.

#### 주식매매

> 시나리오: 사용자는 거래가 마감되기 전에 매도 요청을 한다.
>
> Given
>
> - 사용자는 마이크로소프트 주식 100주를 가지고 있다.
> - 사용자는 애플 주식 150주를 가지고 있다.
> - 현재 시각은 장 마감시간 전이다.
>
> When
>
> * 사용자는 마이크로소프트 주식 20주에 대해 매도 요청을 한다.
>
> Then
>
> * 사용자는 마이크로소프트 주식 80주를 가지고 있다.
> * 사용자는 애플 주식 150주를 가지고 있다.
> * 마이크로소프트 주식 20주의 매도주문이 실행되었다.

### Given: pre-condition

​	시나리오 진행에 필요한 값을 설정, 테스트의 상태를 설정, **Setup**, **Arrange**

### When: event or operation

​	시나리오 진행 필요 조건 명시, 테스트하고자 하는 행동,  **Exercise**, **Act**

### Then: post-conditions

​	시나리오를 완료했을 때 보장해야하는 결과를 명시, 예상되는 결과 기술, **Verify**, **Assert**

## 테스트 범위 설정

수 : 90점 이상, 우 : 80~89점, 미 : 70~79점, 양 : 60~69점, 가 : 59점 미만에 대하여

- **동등분할**은 대표값으로 95점, 85점, 75점, 65점, 55점을 입력
- **경계값 분석**은 90점, 89점, 80점, 79점, 70점, 69점, 60점, 59점을 입력

## 조합 테스트 범위 설정

### Pairewise testing

#### Tool - PICT

##### Download

[PICT Tool](http://www.pairwise.org/pict/win/pict.exe)

[GitHub](https://github.com/microsoft/pict)

##### 사용법

```
Type:          Single, Span, Stripe, Mirror, RAID-5
Size:          10, 100, 500, 1000, 5000, 10000, 40000
Format method: Quick, Slow
File system:   FAT, FAT32, NTFS
Cluster size:  512, 1024, 2048, 4096, 8192, 16384, 32768, 65536
Compression:   On, Off
```

Test Data의 경우의 수를 txt파일로 기술하고,

```
pict.exe testData.txt > testCase.xls
```

실행하면, 테스트해야할 조합의 경우의 수를 만들어 준다.

