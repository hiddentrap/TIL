# Terminology

## Design

##### Abstraction = Interface = Port

##### Implementation of Abstraction or Interface = adapter

파이썬에는 Interface가 없으므로, 추상화 베이스 클래스(ABC)를 상속받은 클래스를 Port로 간주한다.

##### Stub = Dummy

아직 완성되지 않은 하부 모듈 대신 사용하는 모듈

##### Test Double: 테스트 대역

테스트가 진행되는 동안 운영환경에서 사용될 특정 함수, 데이터 모듈, 혹은 라이브러리 역할을 대신하는 이른바 대역

##### stateful

영속성있는, 상태 추적이 가능한, 저장소에 저장되는

##### Functional Test = Acceptance Test = End to End Test = Black Box Test = UseCase Test