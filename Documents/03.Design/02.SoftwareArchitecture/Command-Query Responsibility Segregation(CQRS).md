# Command-Query Responsibility Segregation(CQRS)

명령(CUD)-조회(R) 책임 분리

## 도메인 모델은 명령

도메인에는 비지니스 규칙이 기술된다. 예를들면, '재고량보다 더 많은량을 할당할 수 없다', '각각의 주문은 하나의 배치에만 할당될 수 있다.' 이를 테스틀로 기술하면

unit/test_batchs.py

```python
def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('order-ref', "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18

...

def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False
```

이 규칙들을 적용하기 위해서는 각 오퍼레이션들의 정합성을 보장할 필요가 있고 이를 위해 작은 덩어리의 작업의 commit을 돕는 Unit of Work 패턴과 Aggregate를 사용한다.

또, 이런 작은 덩어리 작업들의 변화에 대한 커뮤니케이션을 위해 도메인 이벤트 패턴을 사용하고 이를 통해 '재고가 데미지를 입거나 손실되었을때 배치에서 할당가능한 수량을 조정하고 필요하다면 할당된 주문을 재할당 시킨다'라는 규칙을 적용할 수 있다.

이런한 복잡성이 존재하기때문에 시스템 상태를 변경할 때 규칙을 적용할 수 있고 데이터 쓰기를 위한 유연한 도구들을 작성했다.

## 데이터 일관성

고객 A가 제품 A를 조회하고 30초 뒤에 주문을 하는데 그 사이 고객 B가 제품 A를 구매 했다면 고객 A의 주문 처리를 어떻게 할 것인가? 주문을 취소할 것인가 또는 재고를 더 구매하고 배송기한을 늦출 것인가

분산 시스템은 불일치상태이기 때문에 항상 시스템의 현재 상태를 체크할 필요가 있다. 웹서버 하나와 두 고객이있는 경우, 잠재적으로 오래된 데이터를 갖게된다. 또는 현실세계와의 불일치를 항상 내제하고 있다.

따라서, 이러한 상황에 대처하기 위한 비지니스 프로세스가 필요하다.  

|        | 읽기             | 쓰기                    |
| ------ | ---------------- | ----------------------- |
| 행위   | 단순한 읽기      | 복잡한 비지니스 로직    |
| 캐싱   | 높은 캐싱 가능성 | 캐싱불가                |
| 일관성 | 보장불가         | 트랜잭션으로 보장해야함 |

| 구현체                             | 장점                                                         | 단점                                                         |
| ---------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Repository 사용                    | 단순하고 일관성 있다.                                        | 복잡한 쿼리 패턴에서 성능이슈                                |
| ORM 사용                           | DB설정과 모델을 재사용할 수 있다.                            | 다른 쿼리 언어가 필요                                        |
| 순수 sql                           | 표준 쿼리 구문으로 성능을 정밀 제어                          | DB스키마를 변경하려면 쿼리 및 ORM정의를 변경해야 하며 고도로 정규화된 스키마에는 여전히 성능 제한이 있을 수 있음 |
| 별도의 Read Store 사용 with Events | 읽기용 사본은 확장 가능하고 데이터가 변경될때 view가 구성되기 때문에 쿼리가 단순해질 수 있다. | 복잡한 기술                                                  |



## Post/Redirect/Get and CQS

웹 클라이언트가 포스트로 서버에 보낸 후 페이지를 새로고침하면 또 포스트를 하기 때문에 서버는 웹파이지를 바로 반환하는 것이 아니라 리다이렉트를 통해서 반환 시킨다. [패턴설명](https://en.wikipedia.org/wiki/Post/Redirect/Get)

이는 CQS(command-query separation)의 간단한 예시이다: 기능은 수정이나 응답 상태 하나만 가져야 한다.

스위치를 껏다 켜는 작업없이 불이 켜져잇는지 물어볼 수 있다.

CQS를 따라서 allocate를 수정해보자. 지금 allocate는 주문을 받아서 재고를 할당하기 위해 서비스 레이어를 호출하고 마지막에 200 OK응답과 배치 ID를 리턴한다. 

이를 간단한 200OK 응답을 리턴하도록 수정하고 대신에 새로운 할당 상태를 조회하는 read-only endpoint 를 제공한다.

POST 후에 GET API Test : e2e/test_api.py

```python
@pytest.mark.usefixtures('postgres_db')
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_202_and_batch_is_allocated():
    orderid = random_orderid()
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    api_client.post_to_add_batch(laterbatch, sku, 100, '2011-01-02')
    api_client.post_to_add_batch(earlybatch, sku, 100, '2011-01-01')
    api_client.post_to_add_batch(otherbatch, othersku, 100, None)

    r = api_client.post_to_allocate(orderid, sku, qty=3)
    assert r.status_code == 202

    r = api_client.get_allocation(orderid)
    assert r.ok
    assert r.json() == [
        {'sku': sku, 'batchref': earlybatch},
    ]


@pytest.mark.usefixtures('postgres_db')
@pytest.mark.usefixtures('restart_api')
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, orderid = random_sku(), random_orderid()
    r = api_client.post_to_allocate(
        orderid, unknown_sku, qty=20, expect_success=False,
    )
    assert r.status_code == 400
    assert r.json()['message'] == f'Invalid sku {unknown_sku}'

    r = api_client.get_allocation(orderid)
    assert r.status_code == 404
```

entrypoints/flask_app.py

```python
from allocation import views
...

@app.route("/allocations/<orderid>", methods=['GET'])
def allocations_view_endpoint(orderid):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    result = views.allocations(orderid, uow)  
    if not result:
        return 'not found', 404
    return jsonify(result), 200
```

allocation/views.py

```python
from allocation.service_layer import unit_of_work

def allocations(orderid: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = list(uow.session.execute(
            'SELECT ol.sku, b.reference'
            ' FROM allocations AS a'
            ' JOIN batches AS b ON a.batch_id = b.id'
            ' JOIN order_lines AS ol ON a.orderline_id = ol.id'
            ' WHERE ol.orderid = :orderid',
            dict(orderid=orderid)
        ))
    return [{'sku': sku, 'batchref': batchref} for sku, batchref in results]
```

views (query) 테스트 : tests/integration/test_views.py

```python
def test_allocations_view(sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    messagebus.handle(commands.CreateBatch('sku1batch', 'sku1', 50, None), uow)  1
    messagebus.handle(commands.CreateBatch('sku2batch', 'sku2', 50, today), uow)
    messagebus.handle(commands.Allocate('order1', 'sku1', 20), uow)
    messagebus.handle(commands.Allocate('order1', 'sku2', 20), uow)
    # add a spurious batch and order to make sure we're getting the right ones
    messagebus.handle(commands.CreateBatch('sku1batch-later', 'sku1', 50, today), uow)
    messagebus.handle(commands.Allocate('otherorder', 'sku1', 30), uow)
    messagebus.handle(commands.Allocate('otherorder', 'sku2', 10), uow)

    assert views.allocations('order1', uow) == [
        {'sku': 'sku1', 'batchref': 'sku1batch'},
        {'sku': 'sku2', 'batchref': 'sku2batch'},
    ]

```

## SELECT N+1 과 다른 성능 고려사항

SELECT N+1 은 ORM의 일반적인 성능 문제이다
: 오브젝트 리스트를 조회할 때, ORM은 필요한 오브젝트의 모든 IDS를 조회하는 최초 쿼리를 실행하고, 각 오브젝트에 대해서 속성값을 가져오기 위한 쿼리를 각각 실행한다. 특히 외래키 관계가 있는 오브젝트의 경우에 특히 그렇다.

join이 많아지면 쿼리가 느려질 수 밖에 없다.

## view에서 sql을 직접 쓰지 않는 대안

allocation/views.py

```python
def allocations(orderid: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = list(uow.session.execute(
            'SELECT sku, batchref FROM allocations_view WHERE orderid = :orderid',
            dict(orderid=orderid)
        ))
        ...
```

adapters/orm.py

```python
allocations_view = Table(
    'allocations_view', metadata,
    Column('orderid', String(255)),
    Column('sku', String(255)),
    Column('batchref', String(255)),
)
```

이럴경우, 모델을 최신상태로 유지하는게 문제다. Database View나 트리거가 일반적인 해결책이지만 이는 하나의 데이터베이스로만 국한된다.

## 이벤트 핸들러를 사용해서 모델테이블은 업데이트 하는법

Allocated의 두번째 핸들러 등록: service_layer/messagebus.py

```python
EVENT_HANDLERS = {
    events.Allocated: [
        handlers.publish_allocated_event,
        handlers.add_allocation_to_read_model
    ],
    events.Deallocated: [
    	handlers.remove_allocation_from_read_model,
    	handlers.reallocate
	],
```

핸들러 추가 : service_layer/handlers.py

추가

```python
def add_allocation_to_read_model(
        event: events.Allocated, uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            'INSERT INTO allocations_view (orderid, sku, batchref)'
            ' VALUES (:orderid, :sku, :batchref)',
            dict(orderid=event.orderid, sku=event.sku, batchref=event.batchref)
        )
        uow.commit()
```

삭제

```python
def remove_allocation_from_read_model(
        event: events.Deallocated, uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            'DELETE FROM allocations_view '
            ' WHERE orderid = :orderid AND sku = :sku',
```

read model 핸들러 업데이트

service_layer/handlers.py

```python
def add_allocation_to_read_model(event: events.Allocated, _):
    redis_eventpublisher.update_readmodel(event.orderid, event.sku, event.batchref)

def remove_allocation_from_read_model(event: events.Deallocated, _):
    redis_eventpublisher.update_readmodel(event.orderid, event.sku, None)
```

views.py

```python
def allocations(orderid):
    batches = redis_eventpublisher.get_readmodel(orderid)
    return [
        {'batchref': b.decode(), 'sku': s.decode()}
        for s, b in batches.items()
    ]
```

