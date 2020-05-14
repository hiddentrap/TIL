# Unit of Work Pattern

​	원자성 동작에 대한 추상화: 데이터 무결성에 관한 패턴

데이터 레이어로부터 서비스 레이어를 분리시킨다. UoW는 저장소의 싱글 엔트리포인트로서 역할한다. 

즉, 서비스 레이어로부터 데이터 레이어와 관련한 코드를 추상화하여 감춤으로써 서비스 레이어에 다음과 같은 기능을 제공한다.

- 동작중에 사용중인 오브젝트가 변하지 않도록 데이터베이스의 스냅샷을 보장
- 변화를 한번에 저장하거나 저장하지 않을 수 있다.
- 레포지토리를 얻거나 저장소를 제어할 수 있는 간단한 API를 사용할 수 있다.

장점

- 원자성 동작에 대한 추상화와 컨텍스트 매니저를 얻음으로써 시각적으로 블럭안의 코드들이 원자적으로 동작함을 알 수 있게 된다.
- 트랜잭션이 시작하고 종료되야 할 때를 명시적으로 제어할 수 있다. 어플리케이션이 안전하게 실패함을 보장받을 수 있으므로 오퍼레이션이 일부만 커밋 되는 상황은 없다.
- 클라이언트 코드와 저장소코드를 분리한다.
- events 와 메세지 버스에도 도움이 된다.

단점

- Django 나 Flask가 제공하는거 쓰면 편하게 살 수 있는데..;;

## Test for UoW

intergration/test_uow.py

```python
def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    session = session_factory()
    insert_batch(session, 'batch1', 'HIPSTER-WORKBENCH', 100, None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)  
    with uow:
        batch = uow.batches.get(reference='batch1')  
        line = model.OrderLine('o1', 'HIPSTER-WORKBENCH', 10)
        batch.allocate(line)
        uow.commit()  

    batchref = get_allocated_batch_ref(session, 'o1', 'HIPSTER-WORKBENCH')
    assert batchref == 'batch1'
  

def insert_batch(session, ref, sku, qty, eta):
    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        ' VALUES (:ref, :sku, :qty, :eta)',
        dict(ref=ref, sku=sku, qty=qty, eta=eta)
    )


def get_allocated_batch_ref(session, orderid, sku):
    [[orderlineid]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid=orderid, sku=sku)
    )
    [[batchref]] = session.execute(
        'SELECT b.reference FROM allocations JOIN batches AS b ON batch_id = b.id'
        ' WHERE orderline_id=:orderlineid',
        dict(orderlineid=orderlineid)
    )
    return batchref


def test_rolls_back_uncommitted_work_by_default(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_batch(uow.session, 'batch1', 'MEDIUM-PLINTH', 100, None)

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert rows == []


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None)
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert rows == []

```

## UoW Abstraction: Context Manager Way

service_layer/unit_of_work.py

```python
DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(  
    config.get_postgres_uri(),
))

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory  

    def __enter__(self):
        self.session = self.session_factory()  # type: Session  
        self.batches = repository.SqlAlchemyRepository(self.session)  
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  

    def commit(self):  
        self.session.commit()

    def rollback(self):  
        self.session.rollback()


```

`__exit__`: with와 함께 실행될때, teardown

`__enter__`: with와 함께 실행될때, setup

## Fake UoW for Test

unit/test_services.py

```python
class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.batches = FakeRepository([])  
        self.committed = False  

    def commit(self):
        self.committed = True  

    def rollback(self):
        pass



def test_add_batch():
    uow = FakeUnitOfWork()  
    services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)  
    assert uow.batches.get("b1") is not None
    assert uow.committed


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()  
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)  
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)  
    assert result == "batch1"
```

## Using UoW in Service Layer

service_layer/services.py

```python
def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        uow: unit_of_work.AbstractUnitOfWork  
):
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork  
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = model.allocate(line, batches)
        uow.commit()
    return batchref
```

## Using Example

```python
def reallocate(line: OrderLine, uow: AbstractUnitOfWork) -> str:
    with uow:
        batch = uow.batches.get(sku=line.sku)
        if batch is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batch.deallocate(line)  
        allocate(line)  
        uow.commit()

```

deallocate 실패시 롤백, allocate 실패시 롤백

```python
def change_batch_quantity(batchref: str, new_qty: int, uow: AbstractUnitOfWork):
    with uow:
        batch = uow.batches.get(reference=batchref)
        batch.change_purchased_quantity(new_qty)
        while batch.available_quantity < 0:
            line = batch.deallocate_one()  
        uow.commit()
```

deallocation 실패치 롤백