# TDD - Test Driven Development

## Principle

내가 작성한 모든 코드는 테스트 되어야 한다.

## WorkFlow

**Functional Test 작성 - Unit Test 작성 - Code 작성 - Functional Test 성공시 Refactoring**

1. Functional Test 작성 - 사용자 입장에서 기술하는 기능(UseCase) 테스트

2. Functional Test가 실패하면, 성공시키기 위해 작성해야할 코드를 생각해보고 그 코드의 동작을 정의하기 위한 unit test들을 작성

3. unit test가 실패하면, 성공시키기 위해 가능한한 적은 양의 어플리케이션 코드를 작성한다. Functional Test가 성공할 때까지, 2번과 3번을 반복한다.

   ```
   python manage.py test
   ```

   FunctionalTest는 **사용자 행위를 기술**하듯 작성한다.

   Unit Test는 **Given-When-Then 패턴**으로 작성한다

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

