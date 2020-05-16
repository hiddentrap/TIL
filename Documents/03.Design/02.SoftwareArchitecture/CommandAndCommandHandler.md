# Commands and Command Handler

## Commands 와 Events 차이

- 이벤트와 마찬가지로 명령어도 시스템의 한 부분에서 다른 부분으로 명령을 보낸다는 점에서 메세지의 일종이다.
- 명령은 한 행위자에서 다른 특정한 행위자에게 결과를 기대하며 보내진다. API 핸들러에 Form 을 Post 하면 명령을 보내는 것이다.  또, 명령은 명령형 동사구로 "allocate stock", "delay shipment"처럼 이름 짓는다.
- 명령은 의도를 포함한다. 명령은 시스템으로 하여금 우리가 원하는 무언가를 하게끔 표현한다. 그 결과로서, 만약 명령이 실패하면 명령어를 보낸 sender는 에러 정보를 받을 필요가 있다.
- 이벤트는 관심있는 리스너들에게 브로드캐스팅 하는 것이다. BatchQuantityChanged를 퍼블리쉬 하면, 누가 이 이벤트를 가져갈지 모른다. 이벤트는 수동태로  "order allocated to stock", "shiment delayed"로 짓는다.
- 이벤트는 명령어가 성공 또는 실패 했음을 알리는데 사용하곤 한다.
- 이벤트는 과거에 어떤일이 생겼다는 사실을 내포하고 있다. 우리는 누가 이벤트를 핸들링하는지 모름으로 이벤트 센더는 수신자의 처리 결과를 신경쓰지 않는다.

|                | Event         | Command       |
| -------------- | ------------- | ------------- |
| Named          | 수동태구      | 명령형        |
| Error Handling | 독립사건      | 리턴          |
| Send to        | All listeners | 특정한 수신자 |
| Hander         | 0,N           | 0,1           |

events 로부터 command 분리 시키기

domain/commainds.py

```python
class Command:
    pass

@dataclass
class Allocate(Command):  
    orderid: str
    sku: str
    qty: int

@dataclass
class CreateBatch(Command):  
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None

@dataclass
class ChangeBatchQuantity(Command):  
    ref: str
    qty: int
```

events.AllocationRequired -> commands.Allocate

events.BatchCreated -> commands.CreateBatch

events.BatchQuantityChanged -> commands.ChangeBatchQuantity

## 예외처리에서 차이

시스템에서 이벤트와 명령어는 유사하게 취급되지면 완전하게 같은 것은 아니다. 

service_layer/messagebus.py

```python
Message = Union[commands.Command, events.Event]


def handle(message: Message, uow: unit_of_work.AbstractUnitOfWork):  1
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            handle_event(message, queue, uow)  2
        elif isinstance(message, commands.Command):
            cmd_result = handle_command(message, queue, uow)  2
            results.append(cmd_result)
        else:
            raise Exception(f'{message} was not an Event or Command')
    return results

def handle_event(
    event: events.Event,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug('handling event %s with handler %s', event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling event %s', event)
            continue


def handle_command(
    command: commands.Command,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork
):
    logger.debug('handling command %s', command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception('Exception handling command %s', command)
        raise


EVENT_HANDLERS = {
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.Allocate: handlers.allocate,
    commands.CreateBatch: handlers.add_batch,
    commands.ChangeBatchQuantity: handlers.change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]

```

Event 핸들러는 복수개가 가능하므로 List Command 핸들러는 1개만 가능

## Events, Commands, ErrorHandling

이벤트가 처리되지 않는다면 어떻게 될까? 시스템이 완전하고 일관된 상태인지 어떻게 확인할까? 메세지를 절반정도 처리하는 도중에 메모리 부족 오류로 프로세스가 종료되버리면 이 문제를 어떻게 하나..?

이 문제들은 이미 해결되어 있다. 일관성을 갖도록 애그리게이트가 바운더리를 갖도록 정의했고 UoW를 통해 에그레기이트에 대한 업데이트가 성공이됬던 실패가 됬단 원자성을 관리된다.

예를들어, 주문에 재고를 할당할 때 일관성 바운더리는 제품 에그리게이트가 된다. 이는 초과할당을 할 수 없다는 것을 의미한다.

정의에 따라서, 두 개의 에그리게이션이 즉시 일관성을 유지하지 않아도 되므로 한 이벤트를 처리하는데 실패하고 하나의 에그리게이트만 업데이트 되어도 시스템은 결국 완전하고 일관적이게 된다. 단 시스템의 제약사항을 위반하면 안된다.

다른 예를 들어보자. 

쇼핑몰을 만든다고 생각해보자. 마케팅 부서는 재방문하는 고객에게 리워드를 주고 싶어한다. 고객이 3번의 구매를 하게 되면 그 고객은 VIP로 분류되고 VIP고객은 특별 취급을 받게되고 Special offer를 제공받는다. 이는 다음과 같이 기술될 수 있다.

> Given: 구매 이력이 2번 있는 고객이 있다.
>
> When: 그 고객이 3번째 구매할 때,
>
> Then: 해당 고객은 VIP로 분류된다.
>
> When: 고객이 VIP로 분류되면
>
> Then: 해당 고객에게 축하메일을 보낸다.

구매이력 에그리게이트를 만들 필요가 있다. 그리고 해당 에그리게이트는 조건을 만족했을 때 도메인 이벤트를 발생시킨다.

```python
# Domains
class History:  # Aggregate

    def __init__(self, customer_id: int):
        self.orders = set() # Set[HistoryEntry]
        self.customer_id = customer_id

    def record_order(self, order_id: str, order_amount: int): 
        entry = HistoryEntry(order_id, order_amount)

        if entry in self.orders:
            return

        self.orders.add(entry)

        if len(self.orders) == 3:
            self.events.append(
                CustomerBecameVIP(self.customer_id)
            )

          
# Handlers
def create_order_from_basket(uow, cmd: CreateOrder): 
    with uow:
        order = Order.from_basket(cmd.customer_id, cmd.basket_items)
        uow.orders.add(order)
        uow.commit() # raises OrderCreated


def update_customer_history(uow, event: OrderCreated): 
    with uow:
        history = uow.order_history.get(event.customer_id)
        history.record_order(event.order_id, event.order_amount)
        uow.commit() # raises CustomerBecameVIP


def congratulate_vip_customer(uow, event: CustomerBecameVip): 
    with uow:
        customer = uow.customers.get(event.customer_id)
        email.send(
            customer.email_address,
            f'Congratulations {customer.first_name}!'
        )
```

## 동기 에러 복구

```python
def handle_event(
    event: events.Event,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug('handling event %s with handler %s', event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling event %s', event)
            continue
```

예를들어, CustomerBecameVIP 이벤트 메세지를 처리하다가 에러가 나면 로그에, 

```
Handling event CustomerBecameVIP(customer_id=12345)
with handler <function congratulate_vip_customer at 0x10ebc9a60>
```

이렇게 남아 있을 것이다.

에러발생시 로깅된 데이터를 통해 단위 테스트에서 재현해보가나 시스템에서 돌려볼 수 있다.

재시도를 위한 핸들러 service_layer/messagebus.py

```python
from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential 

...

def handle_event(
    event: events.Event,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork
):

    for handler in EVENT_HANDLERS[type(event)]:
        try:
            for attempt in Retrying(  
                stop=stop_after_attempt(3),
                wait=wait_exponential()
            ):

                with attempt:
                    logger.debug('handling event %s with handler %s', event, handler)
                    handler(event, uow=uow)
                    queue.extend(uow.collect_new_events())
        except RetryError as retry_failure:
            logger.error(
                'Failed to handle event %s times, giving up!,
                retry_failure.last_attempt.attempt_number
            )
            continue

```

첫 번째 시도가 성공하지 못하면,  exponential을 증가시켜서  재시도한다.