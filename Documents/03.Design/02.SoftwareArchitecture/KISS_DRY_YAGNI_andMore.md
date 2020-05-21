# 개발자가 알아야할 7가지

## 1. DRY - Don't Reapeat Yourself

​	중복된 코드를 작성하지 말자

중복된 코드가 생긴다면, 이를 함수로 감싸서 사용하면 중복된 코드를 피할 수 있다.

## 2. KISS - Keep It Simple Stupid

​	간단하고 단순하게 만드는 것은 어려운 일이다. 

닭잡는데 소잡는 칼을  가져다 쓰지 말자. 예를 들면, 간단한 웹사이트 하나 만드는데 마이크로서비스 아키텍쳐 같이 복잡한 설계를 가져다 쓰지 말자. 

> Let's KISS it and do something simpler

## 3. YAGNI - You Aren't Gonna Need It

​	KISS에 이어지는 이야기로서, 실제로 필요하지 않는 모듈, 프레임워크 그리고 의존성을 추가하지 말자.

사용자에게 간단한 프로토타입을 보여주기위해 일하고 있는 상황을 상상해보자.

어딘가에서 React에 대한 블로그 글을 읽고나서, 이것으로 개발하기로 결정한다. 그리고는 flux의 구현체들을 비교한뒤에 Redux를 사용하기로 한다. 또, JSX를 처리하기 위해 webpack이 필요해질 수 있다.

서버로 사용하기위해 nodejs를 설치하고 여기에 실시간 통지를 위한 Socket.IO를 추가한다.

마침내, 프로덕트 매니저에게 컨셉을 보여줄 멋진 웹 페이지를 완성했다. 근데 알고보니 프로덕트 매니저는 웹페이지의 스크린샷을 캡쳐해 슬라이드의 한 페이지로 사용했을 뿐이다.

스크린샷 한장을 만들기 위해 정말로 React + Redux + Socket.IO가 필요했을까?

## 4. TDD - Test Driven Development

​	4단계로 요약하면,

1. 구현할 함수를 결정한다.
2. 그 함수에 대한 테스트를 먼저 작성한다. 당연히 아직 아무 코드가 없기 때문에 해당 테스트는 실패한다.
3. 해당 테스트를 통과할 수 있는 함수에 대한 구현 코드를 작성한다.
4. 구현 코드에 대한 리팩토링을 수행하고 이를 반복한다.

 이런 식으로 코드를 작성하는 것이 대단히 효율적임을 보여주는 연구들이 이미 많이 있다. 테스트를 먼저 작성하게 되면 100% 가까운 테스트 코드 커버리지를 얻을 수 있게된다. 또한, 에러를 디버깅하는데 시간을 줄이고 코딩에 더 많은 시간을 할애하게 되는 효과를 얻을 수 있다.

## 5. SOLID Principles

> S - Single Responsibility Principle (단일책임)
>
> O - Open -Closed Principle (개방 폐쇄)
>
> L - Liskov Substitution Principle (리스코프 치환)
>
> I - Interface Segregation Principle (인터페이스 분리)
>
> D - Dependency Inversion Principle (의존성역전)

### SRP

​	각각의 함수는 정확하게 한가지만 해야한다는 명확한 목표를 갖는다.

loginUserAndGetGroups() 이런 함수가 나오면 안된다. 두 개로 쪼갤 수 있다. 함수를 만들 때마다 좀 더 작은 함수로 분리될 수 있는지 생각해보자.

로그인하는 사용자마다 선호하는 음악, 선호하는 드라마, 선호하는 영화를 보여줘야 한다고 가정해보자. 이 기능은 getMusic(), getShows(), getMovies()로 나눌 수 있다.

그런데 만약에 이 3개 함수들이 항상 함께 호출 된다고 하자. 그렇다고 getShowsAndMoviesAndMusic()을 만들 수도 없고 3개 함수들을 매번 각각 호출할 수도 없는 노릇이다.

대신에, 3개 함수를 각각 호출하는 코드를 감싸는 함수 getUserMedia()를 만들어 사용하자.

함수가 then 또는 and 없이 어떤일을 하는지 기술할 수 없다면 SRP를 위반했을 가능성이 크다.

ex: aloocate_and_send_mail_if_out_of_stock()

### OCP

​	확장에는 열려있고 수정에는 닫혀있어야 한다.

즉, 클래스, 메서드, 모듈 등의 Entity는 Interface와 같은 추상화 클래스를 통해 기능을 변경하거나 확장을 하는 것은 가능하나, 외부에서 참조하는 코드는 수정하지 않아야 한다.

만약 CalcMethod에서 getResult()를 정의하는 인터페이스를 참조하여 사용한다고 하였을때 getResult()를 구현하는 구현 클래스 Plus, Minus에 더해 Multiple, Devide 구현 클래스를 추가하여 기능은 확장할 수 있어야 하지만, 기능을 추가한다고 해서 이를 참조하는 CalcMethod를 수정하게 하면 안된다는 의미

### LSP

​	

### ISP



### DIP

​		상위 수준의 모듈(도메인)은 하위 레벨의 모듈(인프라)에 대해서 의존성을 갖으면 안된다. 대신, 추상화에 대해서 의존성을 갖게 해야 한다.

A는 B에 의존성이 있다 = A는 B에 의존한다 = A는 B를 알고 있다 = A는 B를 import 한다.

## 6. BDUF - Big Design Up Front

​	이는 폭포수 모델 시대의 잔재로서, 복잡한 설계에서 시작하지 말라는 것을 상기시키기 위함이다. 단 한줄의 코드를 작성하기 전에 3개월의 설계시간을 보내서는 안된다. 작은 것에서부터 시작하고 이를 반복하라.

BDUF는 결국 KISS와 YAGNI를 실천하지 않는 것이다.

## 7. SOC - Separation of concerns

​	한 번에 한가지만! 하나의 함수, 클래스, 객체에서 모든걸 다 하려고 하지 말라.

이는 결국 SOLID 원칙중 - "단일책임 원칙"과 일맥상통힌다.

> 하나를 더 작은 여러개로 나눌 수 있다면 고민하지 말고 나눠라