# Flask Coding

## ORM DI: ORM Depends on Model

### SQL Alchemy classical mapping

##### 모델이 ORM에 의존적인 코드 구현 Django

```python
class Order(models.Model):
    pass

class OrderLine(models.Model):
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()
    order = models.ForeignKey(Order)
```

##### Flask, orm.py

```python
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Order(Base):
    id = Column(Integer, primary_key=True)

class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Integer(String(250))
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)
```

##### ORM이 모델에 의존(Dpendency Inversion)하도록 코드 구현 orm.py

```python
from sqlalchemy.orm import mapper, relationship
import model

metadata = MetaData()

order_lines = Table(  
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

...

def start_mappers():
    lines_mapper = mapper(model.OrderLine, order_lines)  
```

##### ORM Test Code

```python
def test_orderline_mapper_can_load_lines(session):  1
    session.execute(
        'INSERT INTO order_lines (orderid, sku, qty) VALUES '
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )
    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]

```

##### Using ORM in View (Contorller)

```python
@flask.route.gubbins
def allocate_endpoint():
    session = start_session()

    # extract order line from request
    line = OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )

    # load all batches from the DB
    batches = session.query(Batch).all()

    # call our domain service
    allocate(line, batches)

    # save the allocation back to the database
    session.commit()

    return 201
```

### Repository Pattern: 저장소(DB)에 대한 추상화(pretending in memory)

| 장점                                                       | 단점                                      |
| ---------------------------------------------------------- | ----------------------------------------- |
| 저장소와 도메인 모델간에 간단한 인터페이스를 얻을 수 있다. | ORM과 매핑하기 위한 추가 코딩이 필요하다. |
| 단위 테스트를 위한 저장소 Mocking을 쉽게 할 수 있다.       |                                           |

단순한 CRUD 어플리케이션의 경우 도메인 모델 또는 Repository를 구현할 이유가 없다.

##### Repository Base Abstract class

abc.ABC: Abstract Base Class by Google: 추상클래스 생성을 위한 베이스 클래스: Interface

추상화 레이어는 최소한으로 한다. 추상화 레이어는 전반적으로 복잡도를 줄여주기는 하지만, 지역적으로 복잡도를 높이고, 유지보수해야할 코드를 증가시키기 때문이다.

repository.py

```python
class AbstractRepository(abc.ABC):

    @abc.abstractmethod  
    def add(self, batch: model.Batch):
        raise NotImplementedError  

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError

```

##### Repository AbstractRepository tests

test_repository.py

```python
def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)  
    session.commit()  

    rows = list(session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'  
    ))
    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
    
    
def insert_order_line(session):
    session.execute(  
        'INSERT INTO order_lines (orderid, sku, qty)'
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderline_id]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid="order1", sku="GENERIC-SOFA")
    )
    return orderline_id

def insert_batch(session, batch_id):  
    ...

def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)  

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference  3
    assert retrieved.sku == expected.sku  
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {  
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }

```

##### Repository implementation

repository.py

```python
class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()
```

##### Using Repository in View (Contorller)

```python
@flask.route.gubbins
def allocate_endpoint():
    batches = SqlAlchemyRepository.list()
    lines = [
        OrderLine(l['orderid'], l['sku'], l['qty'])
         for l in request.params...
    ]
    allocate(lines, batches)
    session.commit()
    return 201
```

##### Repository Pattern의 또 하나의 장점 : 테스트를 위한 Repository Mocking

```python
class FakeRepository(AbstractRepository):

    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
    
fake_repo = FakeRepository([batch1, batch2, batch3])
```

DB 세션 대신 집합을 저장소로 대체함으로써 간단하게 테스트를 위한 저장소를 Mocking할 수 있다.