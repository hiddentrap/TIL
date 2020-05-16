# Event-Driven Architecture With Microservices

External Message Bus  = Message Broker = ex. Redis, Event Stroe

##### 장점

- 서비스 결합에서 자유롭다. 개개의 서비스들을 추가하거나 수정하기 쉬워진다.

##### 단점

- 정보의 전체적인 흐름을 보기가 더 어려워진다.
- 결과론적 정합성은 새로운 문제를 야기한다. 
- 메세지 안전성과 최소 1회 최대1 회 배달의 선택 문제는 생각해봐야 한다.

시스템을 명사로 정의하는대신 동사로 정의해라.

주문 -> 주문하기, 배치 -> 할당하기

이렇게 정의하게 되면 어떤 시스템이 무엇에 대해 어떤 책임을 져야 하는지 분리하기 좀 더 쉬워진다.

마이크로서비스는 일관성, 완전성 바운더리가 되므로 결과적인 완전성을 수용할수 있고 이는 동기식 호출에 의존할 필요가 없다는 의미가 된다.

각각의 서비스는 외부로부터 명령을 받게 되고 그 처리 결과를 이벤트로 기록한다. 그러면 다른 서비스들은 그 이벤트를 듣고 다음 단계의 워크플로우를 시작한다.

시스템들간의 HTTP API 호출의 일시적 결합을 위해 비동기 메세징을 사용한다.

상위 시스템에서 들어온 BatchQuantityChanged 외부 메시지를 처리하고 Allocated 이벤트를 하위 시스템을 향해 publish 한다.

- 시스템들이 독립접으로 실패할 수 있어서,  파손된 행위를 핸들링하기 더 쉬워진다: 할당시스템에 문제가 있어도 여전히 주문을 받을 수 있다.
- 시스템간 결합된 힘을 줄일 수 있다. 주문하기 시스템에 변경을 가하거나 프로세스에 새로운 단계를 추가하더라도 이는 다른 시스템에 영향을 주지 않는다.

## Redis를 통합을 위한 Publish/Subscribe 채널로 사용하기

서비스 또는 핸들러를 위한 메세지 버스 처럼 시스템간에 이벤트롤 주고받을 방법이 필요하다.

이런 인프라스트럭쳐를 메세지 브로커라고 부른다. 메세지 브로커의 역할은 publisher들로부터 메세지를 가져다가 subscriber들에게 전달해주는 것이다.

메세지 브로커에는 Event Stroe, Kafka, RabbitMQ, Redis 등이 있다.

## End-to-End Test 작성

e2e/test_external_events.py

두개 배치를 준비하고 그 중 하나에 할당한다 그리고 할당된 배치의 수량을 주문보다 적게 바꿔서, 주문이 재할당되는지를 확인한다.

```python
def test_change_batch_quantity_leading_to_reallocation():
    # start with two batches and an order allocated to one of them  
    orderid, sku = random_orderid(), random_sku()
    earlier_batch, later_batch = random_batchref('old'), random_batchref('newer')
    api_client.post_to_add_batch(earlier_batch, sku, qty=10, eta='2011-01-02')  
    api_client.post_to_add_batch(later_batch, sku, qty=10, eta='2011-01-02')
    response = api_client.post_to_allocate(orderid, sku, 10)  
    assert response.json()['batchref'] == earlier_batch

    subscription = redis_client.subscribe_to('line_allocated')  

    # change quantity on allocated batch so it's less than our order  
    redis_client.publish_message('change_batch_quantity', {  
        'batchref': earlier_batch, 'qty': 
    })

    # wait until we see a message saying the order has been reallocated  
    messages = []
    for attempt in Retrying(stop=stop_after_delay(3), reraise=True):  
        with attempt:
            message = subscription.get_message(timeout=1)
            if message:
                messages.append(message)
                print(messages)
            data = json.loads(messages[-1]['data'])
            assert data['orderid'] == orderid
            assert data['batchref'] == later_batch
```

api_client는 시스템 내부 호출을 requests.post로 래핑하는 헬퍼다.

redis_client는 테스트 헬퍼로서, Redis 채널하고 메세지를 주고 받을수 있게 한다. 

simple Redis message listner: entrypoints/redis_eventconsumer.py

```python
r = redis.Redis(**config.get_redis_host_and_port())


def main():
    orm.start_mappers()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('change_batch_quantity')  

    for m in pubsub.listen():
        handle_change_batch_quantity(m)


def handle_change_batch_quantity(m):
    logging.debug('handling %s', m)
    data = json.loads(m['data'])  
    cmd = commands.ChangeBatchQuantity(ref=data['batchref'], qty=data['qty'])  
    messagebus.handle(cmd, uow=unit_of_work.SqlAlchemyUnitOfWork())
```

main()에서 change_batch_quantity를 구독한다.

핸들러에서 json으로 deserialize해서 Command로 변환한다음 서비스 레이어로 전달한다.

simple Redis message publisher: adapters/redis_eventpublisher.py

```python
r = redis.Redis(**config.get_redis_host_and_port())


def publish(channel, event: events.Event):  1
    logging.debug('publishing: channel=%s, event=%s', channel, event)
    r.publish(channel, json.dumps(asdict(event)))

```

예제에서는 채널을 하드코딩 했는데, 이벤트 클래스/명칭에 따라서 적당한 채널을 매핑해놓고 사용할 수도 있다.

외부발송 이벤트 : domain/events.py

```python
@dataclass
class Allocated(Event):
    orderid: str
    sku: str
    qty: int
    batchref: str
```

Product 모델 수정: domain/model.py

```python
class Product:
    ...
    def allocate(self, line: OrderLine) -> str:
        ...

            batch.allocate(line)
            self.version_number += 1
            self.events.append(events.Allocated(
                orderid=line.orderid, sku=line.sku, qty=line.qty,
                batchref=batch.reference,
            ))
            return batch.reference
```

MessageBus 수정: service_layer/messagebus.py: 핸들러 추가

```python
HANDLERS = {
    events.Allocated: [handlers.publish_allocated_event],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]
```

핸들러 펑션 추가: service_layer/handlers.py

```python
def publish_allocated_event(
        event: events.Allocated, uow: unit_of_work.AbstractUnitOfWork,
):
    redis_eventpublisher.publish('line_allocated', event)
```

