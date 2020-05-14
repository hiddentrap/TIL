# Domain Events and Message Bus pattern

publishes event to -> Message Bus -> dispaches events to -> Handler functions()

## 배경

재고가 바닥난 경우, 구매팀한테 그 사실을 메일로 알려줘라!!

모델의 책임은 재고가 없다는 사실을 알아채는 것까지이다. 재고가 없다는 사실을 구매팀에게 알려주는 메일을 보내는 것은 모델의 책임이 아니다.

서비스 레이어에는 detail한 구현을 두면 안된다. 또한, 서비스 레이어를 하위 레벨에 의존하게 하면 안되므로 데이터베이스를 unit of work으로 추상화하여 레벨업 한다음 DI를 구현한것 처럼. 서비스 레이어를 레벨업된 추상화로 같은 레벨에서 의존하도록 만들어 DI를 실현한다.

모두 메시지 버스에 탑승하라~!

## 장단점

### 장점

- 요청에 대한 응답으로 여러 액션을 취해야 할때 책임을 분리할 수 있는 방법
- 이벤트 핸들러는 애플리케이션 코어 로직과 분리되어 있어 나중에 구현을 수정하기 용이하다.
- 도메인 이벤트는 실제 세상을 모델링하는데 좋은 방법이다 그리고 이해관계자와 모델링을 진행할때 비지니스 용어의 일부로 사용할 수 있다.

### 단점

- 추가적으로 생각해야 할 거리가 생기며 동작이 작동하는 방법을 파악하기 명확하지 않다
- 이벤트 핸들링 코드는 동기방식으로 실행되서 핸들리가 이벤트를 모두 처리하지 못하면 종료되지 못해서 퍼포먼스에 영향을 줄 수도 있다.
- 이벤트 핸들러와 무한루프 간에 순환의존관계에 대한 가능성에 주의를 기울여야 한다.

## 패턴 구현

### 이벤트는 단순한 데이터 클래스

- 이벤트는 Value Object의 일종이다 : 이벤트는 행위를 갖지 않는 순수 데이터 구조체이다. 도메인 언어로 이벤트 이름을 만들고 도메인 모델의 일부로 생각한다.

- model.py에 기술한다. events.py로 독립된 파일에 기술 할 수도 있다.

  예제

  ```python
  from dataclasses import dataclass
  
  class Event:  
      pass
  
  @dataclass
  class OutOfStock(Event):  
      sku: str
  ```

  - 부모 클래스로 그루핑 가능
  - @dataclass : 어노테이션 변수 생성자 자동 생성

### 모델에서 이벤트 발생

도메인 모델이 어떤 사실이 발생했다는것을 기록하는 것을 이벤트를 발생시킨다 라고 한다.

어그리게이트가 이벤트를 발생시키는지 테스트

tests/unit/test_product.py

```python
def test_records_out_of_stock_event_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    product = Product(sku="SMALL-FORK", batches=[batch])
    product.allocate(OrderLine('order1', 'SMALL-FORK', 10))

    allocation = product.allocate(OrderLine('order2', 'SMALL-FORK', 1))
    assert product.events[-1] == events.OutOfStock(sku="SMALL-FORK")  
    assert allocation is None
```

product.events[]는 어떤 일이 일어났는지 Event 오브젝트의 리스트 형태로 가지고 있다.

model.py

```python
class Product:

    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number
        self.events = []  # type: List[events.Event]  

    def allocate(self, line: OrderLine) -> str:
        try:
            #...
        except StopIteration:
            self.events.append(events.OutOfStock(line.sku))  
            # raise OutOfStock(f'Out of stock for sku {line.sku}')  
            return None
```

### Message Bus는 Events 와 Handlers를 매핑시킨다

​	메시지 버스는 단순한 publish-subscribe 시스템이다.

service_layer/messagebus.py

```python
def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_out_of_stock_notification(event: events.OutOfStock):
    email.send_mail(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )


HANDLERS = {
    events.OutOfStock: [send_out_of_stock_notification],

}  # type: Dict[Type[events.Event], List[Callable]]
```

### event를 message bus에 탑승시키는 3가지 방안- Publishing

#### 1. 서비스 레이어가 모델로부터 이벤트를 받아서 message bus에 넣는다.

services.py

```python
from . import messagebus
...

def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        try:  
            batchref = product.allocate(line)
            uow.commit()
            return batchref
        finally:  
            messagebus.handle(product.events)  
```

#### 2. 도메인 모델 말고 서비스 레이어에서 이벤트를 직접 발생시킨다. 중간추천

services.py

```python
def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.allocate(line)
        uow.commit() 

        if batchref is None:
            messagebus.handle(events.OutOfStock(line.sku))
        return batchref
```

할당에 실패해도 커밋하도록 하고, 문제가 발생하지 않으면 항상 커밋한다, 변경하지 않았을 때 커밋하는 것은 아무 문제도 없고 코드를 깔끔하게 유지할 수 있다.

#### 3. UoW가 event를 message bus로 publishing한다. 추천하는 방법

service_layer/unit_of_work.py

```python
class AbstractUnitOfWork(abc.ABC):
    ...

    def commit(self):
        self._commit()  
        self.publish_events()  

    def publish_events(self):  
        for product in self.products.seen:  
            while product.events:
                event = product.events.pop(0)
                messagebus.handle(event)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

...

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    ...

    def _commit(self):  
        self.session.commit()
```

adapter/repository.py

```python
class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[model.Product]  

    def add(self, product: model.Product):  
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:  
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Product):  
        raise NotImplementedError

    @abc.abstractmethod  
    def _get(self, sku) -> model.Product:
        raise NotImplementedError



class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):  
        self.session.add(product)

    def _get(self, sku):  
        return self.session.query(model.Product).filter_by(sku=sku).first()
```

services.py

```python
def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.allocate(line)
        uow.commit()
        return batchref
```

tests/unit/test_services.py

```python
class FakeRepository(repository.AbstractRepository):

    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, product):
        self._products.add(product)

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

...

class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    ...

    def _commit(self):
        self.committed = True
```

상속을 끊고 프로텍트 메서드를 제거한 개선판 repository.py

```python
from typing import Set, Protocol
from allocation.domain import model



class AbstractRepository(Protocol):

    def add(self, product: model.Product):
        ...

    def get(self, sku) -> model.Product:
        ...



class TrackingRepository:
    seen: Set[model.Product]

    def __init__(self, repo: AbstractRepository):
        self.seen = set()  # type: Set[model.Product]
        self._repo = repo

    def add(self, product: model.Product):
        self._repo.add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:
        product = self._repo.get(sku)
        if product:
            self.seen.add(product)
        return product



class SqlAlchemyRepository:

    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()
```

ABCs 를 typing.Protocol로 바꾸는 것이 좋다.

