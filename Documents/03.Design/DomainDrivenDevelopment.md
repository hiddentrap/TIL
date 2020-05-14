# DDD: Domain-Driven-Development

## 아키텍쳐 개요

[참고필요](https://private-space.tistory.com/tag/DDD)

[참고필요2](https://12bme.tistory.com/522)

### 4가지 영역

#### 표현 Layer (Controller), 최상위 계층

사용자 Request를 서비스 Layer에 전달하고 그 결과를 사용자에게 Response

#### 서비스 Layer (응용)

기능 구현 (Feature, Use-Case)

#### 도메인 Layer

도메인 모델을 로직으로 구현 한다. 해당 도메인 모델에 대한 비지니스 규칙을 구현 한다.

#### External Layer (Repository, I/O, External API, Infra etc), 최하위 계층

DBMS, Message Queue 등 인프라 chanel

### 의존성 역전 DI

​	DB를 관리하는 클래스 A가 있고, DB에 데이터를 저장해야 하는 도메인 Entity B가 있다고 할때, B는 A를 의존하고 있기 때문에, B를 단독으로 테스트하기가 어렵다. 또한, DB가 아닌 외부 API를 이용하여 한다고 할때 B가 A를 의존하고 있기 때문에 B에 변경을 가해야 하는 문제가 생긴다.

이러한 의존성과 관련한 문제를 해결하기 위한 전략이 의존성 역전 DI패턴이다.

이를 해결하기 위해 B -> A의 의존관계를 인터페이스를 활용하여 B(고수준)-> C(고수준) <-A(저수준) 로 의존관계를 바꾼다.

즉, B는 A를 직접 사용하는 대신 A의 인터페이스인 C를 사용하고 A는 C를 구현하게 되면된다.

## Domain Modeling 개요

### 도메인 모델링

- 비지니스와 가장 가까운 코드영역으로 가장 변화가 많으므로 쉽게 수정이 용이하게 작성해야 한다.
- 비지니스 로직에 맞는 규칙을 구현하는 코드는 도메인 모델

#### 도메인

해결(개선이나 자동화)해야 할 비지니스 프로세스를 지원하는 활동들의 집합: 구매, 조달, 제품설계, 물류, 배송 등

#### 모델: 추상화

비지니스 프로세스나 지원하는 활동들을 정제하고 추상화한 청사진

### 모든것이 Object일 필요는 없다

파이썬의 경우 멀티패러다임 언어이므로. 함수를 사용할 수도 있다. 어떤 때는 클래스를 사용하는 것이 더 비효율적이다.

### Object Orient 설계 원칙을 적용하기 최적이다.

- SOLID 원칙
- has-a vs is -a
- 상속 보다는 조합 등

### ValueObject

- 고유 식별자가 없다.
- 개념적으로 속성을 표현할 때 사용한다.

### Entity

- 엔티티의 속성값은 시간이 지남에 따라 변화할 수 있다. 
- 고유 식별자를 갖는다.

- 도메인의 교유한 개념을 표현한다.
- 도메인 모델의 데이터와 관련 기능을 포함한다.

### Aggregate 도메인 모델 묶음, 집합, 군집화

- 관련 도메인 Entity와 Value의 집합 또는 묶음 이다.
- Aggregate에 포함되는 도메인 오브젝트를 수정하는 유일한 방법은 Aggregate에 구현한 메서드를 호출해서 수정하는 방법 뿐이다.
- 쇼핑사이트를 예로들면, 쇼핑카트가 Aggregate가 될 수 있다. 쇼핑카트는 여러가지 단일 유닛 상품들의 집합, 송이, 무더기, 클러스터이다. 
- Aggregate 오브젝트는 public이지만, 포함되는 entity나 vo는 private이다.
- Aggregate : Repository = 1 : 1

### 예제 : 주문

#### 도메인 개념에서 '주문'

- 주문
- 배송지 정보
- 주문자
- 주문 목록
- 총 결제금액

'주문'은 하위 5개 도메인 및 벨류를 묶어 표현하기에 적당하다. 

애그리거트를 구성하기 위해서는 적절한 루트 엔티티를 선정한다.

'주문'은 하위 개념인 배송지 정보, 주문자 등을 입력받아 루트 엔티티로 사용하기 적절하다.

Aggregate는 모든 정보를 갖는 완전한 객체로 사용해야 한다: 주문 Aggregate를 생성하기 위해서 배송지 정보, 주문자, 주문 목록, 총 결제금액은 필수 값이다.

```java
public class Order {

    private OrderNo id;
    private List<OrderLine> orderLines;
    private OrderState state;
    private ShippingInfo shippingInfo;
    private Money totalAmounts;

    public void payment() { ... }
    public void shipped() { ... }
    public void startDelivery() { ... }
    public void completeDelivery() { ... }
    public void cancel() { ... }

    public void changeShippingInfo(ShippingInfo newShippingInfo) { ... }
}
```

- Order : Aggregate - 다른 private 도메인 Entity 혹은 VO를 포함하며 이를 수정하는 메서드 포함

- OrderNo : Aggregate의 식별자

- OrderLine : 주문 정보 - 상품종류, 가격, 개수 등을 포함하는 도메인 Entity

  ```java
   public class OrderLine {
       private Product product;
       private Money price;
       private int quantity;
       private Money amounts;
   }
  ```

- OrderState : 주문 상태 정보

  ```java
   public enum OrderState {
       PAYMENT_WAITING {
           public boolean isShippingChangeable() {
               return true;
           }
       },
  
       PREPARING {
           public boolean isShippingChangeable() {
               return true;
           }
       },
  
       SHIPPED,
       DELIVERING,
       DELIVERING_COMPLETED,
       CANCELED;
  
       public boolean isShippingChangeable() {
           return false;
       }
   }
  ```

- ShippingInfo : 배송지 정보

  ```java
   public class ShippingInfo {
       private Receiver receiver;
       private Address address;
   }
  ```

- Money: 총 주문 금액 VO

#### 주문 aggregate를 위한 repository

```java
  public interface OrderRepository {
      Order findByNumber(OrderNumber number);
      void save(Order order);
      void delete(Order order);
  }
```

### 주의사항

- 도메인 Entity나 VO는 get/set 메소드를 정의하지 않는다. 생성자로 설정한다.
  - get/set은 도메인의 핵심 개념이나 의도를 표현하지 못한다.
  - 도메인은 해당 개념이 어떤 행위를 하고, 어떻게 상태가 변하는 지에 집중한다.
  - get/set으로 객체의 상태값을 계속 바꿔서 사용하는 행위는 '객체지향'이 아닌 '절차지향'에 가깝다.
- 도메인 객체는 완전항 상태로 사용한다.
  - 주문을 하기 위해 OrderLine(주문정보), ShippingInfo(배송지 정보)는 반드시 포함되어야 한다.
  - Order 생성 후 정보를 추가한다면 정보의 일부가 누락되는 상황이 생길 수 있다.
- 도메인 용어를 명확히 정의한다.
  - 상품이 준비되어 배송 올 때까지의 단계를 StepN 으로 정의하면 가독성이 떨어지므로, OrderState.PAYMENT_WAITTING처럼 상태에 대해 명확하게 정의한 단어는 개발자가 소스 코드를 이해하는데 좋다.
- VO는 불변 타입 객체로 사용한다.
  - 값의 변화시킬 수 있으면 잘못된 참조로 인한 오류가 발생 가능하다.