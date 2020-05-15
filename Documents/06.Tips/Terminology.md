# Terminology

## Design

##### Abstraction = Interface = Port

##### Implementation of Abstraction or Interface = Adapter

파이썬에는 Interface가 없으므로, 추상화 베이스 클래스(ABC)를 상속받은 클래스를 Port로 간주한다.

##### Stub = Dummy

아직 완성되지 않은 하부 모듈 대신 사용하는 모듈

##### Test Double: 테스트 대역

테스트가 진행되는 동안 운영환경에서 사용될 특정 함수, 데이터 모듈, 혹은 라이브러리 역할을 대신하는 이른바 대역

##### stateful

영속성있는, 상태 추적이 가능한, 저장소에 저장되는

##### Functional Test = Acceptance Test = End to End Test = Black Box Test = UseCase Test

사용자 관점에서 애플리케이션 외부를 테스트

##### UnitTest

개발자 관접에서 내부를 테스트

##### Domain = apps in Django

##### Consumer, Consume

소비자, 소비하다 = 사용자, 사용하다. 단, 사용자는 사람을 지칭할 수 있기에 소비자를 사용한다. 소비자는 사람, 서비스, APIs 무엇이든지 될 수 있다.

Language 

OOP(Object Oriented Programming): Single Responsible Pattern, Open Closed Pattern, Liskove... , Interface Serregatin Pattern, Dependency Inversion Pattern and other Design Patternj

TDD(BDD) : Test Driven Development(Behavial Driven Development)

MVC Pattern, MVT Pattern, Rest API, GraphQL

AOP : Aspect Oriented Programming

DDD : Domain Driven Development - Domain Model, APIs, Interface, Service, External I/O, ValueObject, Aggregate, Entity

EDA : Event Driven Architecture - Domain Events and MessageBus

SOA : Service Oriented Architeture

MSA : Micro Service Architecutre 

##### Immutable Object = 불변객체

생성한뒤에 상태(속성) 값을 변경할 수 없는 객체

##### CORS (Cross-Origin Resource Sharing)

웹브라우저는 특정사이트에 접속중인 상태에서 다른 사이트를 접근하는 경우 Same Origin Policy위반 이라고 판단하기 때문에(XSS 방지목적) FronteEnd에서 BackEnd접속시 BackEnd단에서 CORS 설정이 필요하다.