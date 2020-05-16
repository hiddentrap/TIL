# Domain Events and Message Bus pattern

Message Bus = Message Broker (Message Oriented Middleware)= Message Que = publish and subscriber (RabbitMQ, Apache kafka, Redis, IBM WebSphere MQ ...)

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

### 서비스 펑션을 메시지 핸들러로 리팩터링하기

새로운 이벤트 2개 정의: AllocationRequired, BatchCreated

domain/events.py

```python
@dataclass
class BatchCreated(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None

...

@dataclass
class AllocationRequired(Event):
    orderid: str
    sku: str
    qty: int
```

services.py를 handlers.py로 변경: 그리고 이미 정의된 send_out_of_stock_notification 핸들러를 추가한다. 그리고 기존 서비스 펑션들을 핸들러로 수정하기 위해 input을 event와 UoW로  변경한다.

service_layer/handlers.py

```python
def add_batch(
        event: events.BatchCreated, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get(sku=event.sku)
        ...


def allocate(
        event: events.AllocationRequired, uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(event.orderid, event.sku, event.qty)
    ...


def send_out_of_stock_notification(
        event: events.OutOfStock, uow: unit_of_work.AbstractUnitOfWork,
):
    email.send(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )
```

서비스 레이어 API가 더 구조화 되고 일관성있게 되었으며 개개이 원시 데이터 타입이 아닌 잘 정의된 오브젝트를 사용하게 되었다. 또한 events 에서 input validation을 수행할 수 있다.

메세지 버스가 UoW로부터 이벤트를 수집할수 있게 수정

service_layer/messagebus.py

```python
def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):  
    results = []
    queue = [event]  
    while queue:
        event = queue.pop(0)  
        for handler in HANDLERS[type(event)]:  
            results.append(handler(event, uow=uow))  4
            queue.extend(uow.collect_new_events())             
    return results
```

UoW에서 이벤트롤 직접 버스로 전달하지 않도록 수정

service_layer/unit_of_work.py

```python
class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for product in self.products.seen:
            while product.events:
                yield product_events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
```

테스트를 events관점으로 수정: 기존의 서비스 함수를 호출하는 관점에서 이벤트를 생성해서 메시지 버스에 넣는 걸로 수정

tests/unit/test_services -> tests/unit/test_handlers.py

```python
# pylint: disable=no-self-use
from datetime import date
from unittest import mock
import pytest

from allocation.adapters import repository
from allocation.domain import events
from allocation.service_layer import handlers, messagebus, unit_of_work


class FakeRepository(repository.AbstractRepository):

    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, product):
        self._products.add(product)

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

    def _get_by_batchref(self, batchref):
        return next((
            p for p in self._products for b in p.batches
            if b.reference == batchref
        ), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass



class TestAddBatch:

    def test_for_new_product(self):
        uow = FakeUnitOfWork()
        #services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
        messagebus.handle(
            events.BatchCreated("b1", "CRUNCHY-ARMCHAIR", 100, None), uow
        )
        assert uow.products.get("CRUNCHY-ARMCHAIR") is not None
        assert uow.committed


    def test_for_existing_product(self):
        uow = FakeUnitOfWork()
        messagebus.handle(events.BatchCreated("b1", "GARISH-RUG", 100, None), uow)
        messagebus.handle(events.BatchCreated("b2", "GARISH-RUG", 99, None), uow)
        assert "b2" in [b.reference for b in uow.products.get("GARISH-RUG").batches]


class TestAllocate:

    def test_returns_allocation(self):
        uow = FakeUnitOfWork()
        #services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
        #result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
        messagebus.handle(
            events.BatchCreated("batch1", "COMPLICATED-LAMP", 100, None), uow
        )
        results = messagebus.handle(
            events.AllocationRequired("o1", "COMPLICATED-LAMP", 10), uow
        )
        assert results.pop(0) == "batch1"


    def test_errors_for_invalid_sku(self):
        uow = FakeUnitOfWork()
        messagebus.handle(events.BatchCreated("b1", "AREALSKU", 100, None), uow)

        with pytest.raises(handlers.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
            messagebus.handle(
                events.AllocationRequired("o1", "NONEXISTENTSKU", 10), uow
            )

    def test_commits(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            events.BatchCreated("b1", "OMINOUS-MIRROR", 100, None), uow
        )
        messagebus.handle(
            events.AllocationRequired("o1", "OMINOUS-MIRROR", 10), uow
        )
        assert uow.committed


    def test_sends_email_on_out_of_stock_error(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            events.BatchCreated("b1", "POPULAR-CURTAINS", 9, None), uow
        )

        with mock.patch("allocation.adapters.email.send") as mock_send_mail:
            messagebus.handle(
                events.AllocationRequired("o1", "POPULAR-CURTAINS", 10), uow
            )
            assert mock_send_mail.call_args == mock.call(
                "stock@made.com", f"Out of stock for POPULAR-CURTAINS"
            )

```

API를 Events 형태로 수정하기

entrypoints/flask_app.py

```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    try:
        # batchref = services.allocate(
        # request.json['orderid'],  1
        # request.json['sku'],
        # request.json['qty'],
        # unit_of_work.SqlAlchemyUnitOfWork(),
        event = events.AllocationRequired(
            request.json['orderid'], request.json['sku'], request.json['qty'],
        )
        results = messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())
        batchref = results.pop(0)
    except InvalidSku as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({'batchref': batchref}), 201
```

새 이벤트 추가하기: BatchQuantityChanged

domain/events.py

```python
@dataclass
class BatchQuantityChanged(Event):
    ref: str
    qty: int
```

새 테스트 추가하기 : TestChangeBatchQuantity

unit/test_handler.py

```python
class TestChangeBatchQuantity:

    def test_changes_available_quantity(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            events.BatchCreated("batch1", "ADORABLE-SETTEE", 100, None), uow
        )
        [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
        assert batch.available_quantity == 100

        messagebus.handle(events.BatchQuantityChanged("batch1", 50), uow)

        assert batch.available_quantity == 50


    def test_reallocates_if_necessary(self):
        uow = FakeUnitOfWork()
        event_history = [
            events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
            events.BatchCreated("batch2", "INDIFFERENT-TABLE", 50, date.today()),
            events.AllocationRequired("order1", "INDIFFERENT-TABLE", 20),
            events.AllocationRequired("order2", "INDIFFERENT-TABLE", 20),
        ]
        for e in event_history:
            messagebus.handle(e, uow)
        [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
        assert batch1.available_quantity == 10
        assert batch2.available_quantity == 50

        messagebus.handle(events.BatchQuantityChanged("batch1", 25), uow)

        # order1 or order2 will be deallocated, so we'll have 25 - 20
        assert batch1.available_quantity == 5
        # and 20 will be reallocated to the next batch
        assert batch2.available_quantity == 30
```

새 구현 추가(핸들러, 새로운 쿼리타입)

핸들러 추가: service_layer/handers.py

```python
def change_batch_quantity(
        event: events.BatchQuantityChanged, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get_by_batchref(batchref=event.ref)
        product.change_batch_quantity(ref=event.ref, qty=event.qty)
        uow.commit()
```

repository에 새 쿼리 타입 추가 adapters/repository.py

```python
class AbstractRepository(abc.ABC):
    ...

    def get(self, sku) -> model.Product:
        ...

    def get_by_batchref(self, batchref) -> model.Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_batchref(self, batchref) -> model.Product:
        raise NotImplementedError
    ...

class SqlAlchemyRepository(AbstractRepository):
    ...

    def _get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()

    def _get_by_batchref(self, batchref):
        return self.session.query(model.Product).join(model.Batch).filter(
            orm.batches.c.reference == batchref,
        ).first()
```

FakeRepository에도 추가한다. unit/test_handelrs.py

```python
class FakeRepository(repository.AbstractRepository):
    ...

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

    def _get_by_batchref(self, batchref):
        return next((
            p for p in self._products for b in p.batches
            if b.reference == batchref
        ), None)
```

핸들러를 메세지 버스에 등록한다. service_layer/messagebus.py

```python
HANDLERS = {
    events.BatchCreated: [handlers.add_batch],
    events.BatchQuantityChanged: [handlers.change_batch_quantity],
    events.AllocationRequired: [handlers.allocate],
    events.OutOfStock: [handlers.send_out_of_stock_notification],

}  # type: Dict[Type[events.Event], List[Callable]]
```

단위테스트 이벤트 핸덜러 분리를 위한 Fake Message Bus

unit/test_handlers.py

```python
class FakeUnitOfWorkWithFakeMessageBus(FakeUnitOfWork):

    def __init__(self):
        super().__init__()
        self.events_published = []  # type: List[events.Event]

    def publish_events(self):
        for product in self.products.seen:
            while product.events:
                self.events_published.append(product.events.pop(0))
```

이제, 모든 event chain 테스트가 아닌 BatchQuantityChanged가 AllocationRequired 이벤트를 발생시키는지 테스트 할 수 있다.

처음에 edge-to-edgt 테스트로 시작해서 필요할 경우에만 격리시킨 테스트를 수행해라

 unit/test_handlers.py

```python
def test_reallocates_if_necessary_isolated():
    uow = FakeUnitOfWorkWithFakeMessageBus()

    # test setup as before
    event_history = [
        events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
        events.BatchCreated("batch2", "INDIFFERENT-TABLE", 50, date.today()),
        events.AllocationRequired("order1", "INDIFFERENT-TABLE", 20),
        events.AllocationRequired("order2", "INDIFFERENT-TABLE", 20),
    ]
    for e in event_history:
        messagebus.handle(e, uow)
    [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
    assert batch1.available_quantity == 10
    assert batch2.available_quantity == 50

    messagebus.handle(events.BatchQuantityChanged("batch1", 25), uow)

    # assert on new events emitted rather than downstream side-effects
    [reallocation_event] = uow.events_published
    assert isinstance(reallocation_event, events.AllocationRequired)
    assert reallocation_event.orderid in {'order1', 'order2'}
    assert reallocation_event.sku == 'INDIFFERENT-TABLE'
```

