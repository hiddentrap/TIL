# Dependency Injection

Composition Root = bootstrap script = Dependency Injector

Entrypoints(Flask/Redis) -> call -> Bootstrapper: 핸들러를 with 적당한 DI (Test는 fakes, Prod는 Real) -> pass injected handlers to -> Message Bus : 이벤트와 명령을 주입된 핸들러로 디스패치

## Bootstrapper

### 핸들러 준비 : Manual DI with Closures and Partials

클로져나 부분함수를 사용해서 DI 구현

```python
# existing allocate function, with abstract uow dependency
def allocate(
        cmd: commands.Allocate, uow: unit_of_work.AbstractUnitOfWork
):
    line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
    with uow:
        ...

# bootstrap script prepares actual UoW

def bootstrap(..):
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    # prepare a version of the allocate fn with UoW dependency captured in a closure
    allocate_composed = lambda cmd: allocate(cmd, uow)

    # or, equivalently (this gets you a nicer stack trace)
    def allocate_composed(cmd):
        return allocate(cmd, uow)

    # alternatively with a partial
    import functools
    allocate_composed = functools.partial(allocate, uow=uow)  1

# later at runtime, we can call the partial function, and it will have
# the UoW already bound
allocate_composed(cmd)


def send_out_of_stock_notification(
        event: events.OutOfStock, send_mail: Callable,
):
    send_mail(
        'stock@made.com',
        ...


# prepare a version of the send_out_of_stock_notification with dependencies
sosn_composed  = lambda event: send_out_of_stock_notification(event, email.send_mail)

...
# later, at runtime:
sosn_composed(event)  # will have email.send_mail already injected in
```

클로져(람다 또는 이름있는 함수) 와 부분함수의 차이점은 클로져는 변수의 늦은 바인딩을 사용한다 이는 의존성이 변할수 있는 경우 혼란을 야기할 수 있다.

클래스를 사용한 구현 (그닥 비추 너무 장황함)

```python
# we replace the old `def allocate(cmd, uow)` with:

class AllocateHandler:

    def __init__(self, uow: unit_of_work.AbstractUnitOfWork): 
        self.uow = uow

    def __call__(self, cmd: commands.Allocate):
        line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
        with self.uow:
            # rest of handler method as before
            ...

# bootstrap script prepares actual UoW
uow = unit_of_work.SqlAlchemyUnitOfWork()

# then prepares a version of the allocate fn with dependencies already injected
allocate = AllocateHandler(uow)

...
# later at runtime, we can call the handler instance, and it will have
# the UoW already injected
allocate(cmd)
```

## A Bootstrap Script

- 기본 의존성을 선언해놓지만 오버라이딩 할 수 있다.
- app이 시작할때 init 이 동작한다.
- 핸들러에 모든 의존성을 주입한다.
- app과 message bus를 위한 핵심 오브젝트를 반환한다.

allocations/bootstrap.py

```python
def bootstrap(
    start_orm: bool = True,  
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),  
    send_mail: Callable = email.send,
    publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:

    if start_orm:
        orm.start_mappers()  

    dependencies = {'uow': uow, 'send_mail': send_mail, 'publish': publish}
    injected_event_handlers = {  
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {  
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(  
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters  
    deps = {
        name: dependency
        for name, dependency in dependencies.items()  
        if name in params
    }
    return lambda message: handler(message, **deps)  

```

[Inject](https://pypi.org/project/Inject)

[Punq](https://pypi.org/project/punq)

[dependencies](https://github.com/dry-python/dependencies)

## 메세지 버스는 런타임에 핸들러를 할당받는다.

service_layer/messagebus.py

```python
class MessageBus:  

    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],  
        command_handlers: Dict[Type[commands.Command], Callable],  
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):  
        self.queue = [message]  
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                self.handle_command(message)
            else:
                raise Exception(f'{message} was not an Event or Command')
                
    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug('handling event %s with handler %s', event, handler)
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception('Exception handling event %s', event)
                continue


    def handle_command(self, command: commands.Command):
        logger.debug('handling command %s', command)
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise

```

## Entrypoints 에서 Bootstrap 사용

entrypoints/flask_app.py

```python
-from allocation import views
+from allocation import bootstrap, views

 app = Flask(__name__)
-orm.start_mappers()  
+bus = bootstrap.bootstrap()

-    uow = unit_of_work.SqlAlchemyUnitOfWork()  
-    messagebus.handle(cmd, uow)
+    bus.handle(cmd)
```

## 테스트에서 DI초기화

integration/test_views.py

```python
@pytest.fixture
def sqlite_bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,  
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),  
        send_mail=lambda *args: None,  
        publish=lambda *args: None,  
    )
    yield bus
    clear_mappers()

def test_allocations_view(sqlite_bus):
    sqlite_bus.handle(commands.CreateBatch('sku1batch', 'sku1', 50, None))
    sqlite_bus.handle(commands.CreateBatch('sku2batch', 'sku2', 50, date.today()))
    ...
    assert views.allocations('order1', sqlite_bus.uow) == [
        {'sku': 'sku1', 'batchref': 'sku1batch'},
        {'sku': 'sku2', 'batchref': 'sku2batch'},
    ]
```

unit/test_handlers.py

```python
def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False,  
        uow=FakeUnitOfWork(),  
        send_mail=lambda *args: None,  
        publish=lambda *args: None,  
    )
```

## Adapter(인터페이스) 만들기

현재 두 가지 종류의 의존성이 있다.

service_layer/messagebus.py

```python
    uow: unit_of_work.AbstractUnitOfWork,  
    send_mail: Callable,  
    publish: Callable, 
```

UoW는 추상 베이스 클래스를 가지고 있고 이는 외부 의존성을 선언하고 관리하는 좀 무거운 옵션이다. 의존성의 상대적으로 복잡할 경우 사용한다.

email sender와 pub/sub publisher는 함수로 정의되어 있다. 단순한 의존성으로 동작한다.

작업에 주입해야할 의존성들이 다음과 같이 있다고 해보자.

- S3 파일 시스템 클라이언트
- key/value strore 클라이언트
- requests 세션 오브젝트

대부분의 경우 읽기 및 쓰기, GET 및 POST 등 단일 기능으로 캡쳐할 수 없는 보다 복잡한 API를 갖고 있다.

### 추상화와 구현체 정의

좀 더 일반적인 알림 API를 생각해보자. email이 될 수도 있고 SMS가 될 수도 있고 Slack 포스트가 될 수도 있다.

추상화 : adapters/notifications.py

```python
class AbstractNotifications(abc.ABC):

    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError

...

class EmailNotifications(AbstractNotifications):

    def __init__(self, smtp_host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server = smtplib.SMTP(smtp_host, port=port)
        self.server.noop()

    def send(self, destination, message):
        msg = f'Subject: allocation service notification\n{message}'
        self.server.sendmail(
            from_addr='allocations@example.com',
            to_addrs=[destination],
            msg=msg
        )
```

bootstrap script에서 의존성 변경: bootstrap.py

```python
 def bootstrap(
     start_orm: bool = True,
     uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
-    send_mail: Callable = email.send,
+    notifications: AbstractNotifications = EmailNotifications(),
     publish: Callable = redis_eventpublisher.publish,
 ) -> messagebus.MessageBus:
```

테스트를 위한 Fake Version 만들기 : unit/test_handlers.py

```python
class FakeNotifications(notifications.AbstractNotifications):

    def __init__(self):
        self.sent = defaultdict(list)  # type: Dict[str, List[str]]

    def send(self, destination, message):
        self.sent[destination].append(message)
...
```

테스트에서 사용하기: unit/test_handers.py

```python
    def test_sends_email_on_out_of_stock_error(self):
        fake_notifs = FakeNotifications()
        bus = bootstrap.bootstrap(
            start_orm=False,
            uow=FakeUnitOfWork(),
            notifications=fake_notifs,
            publish=lambda *args: None,
        )
        bus.handle(commands.CreateBatch("b1", "POPULAR-CURTAINS", 9, None))
        bus.handle(commands.Allocate("o1", "POPULAR-CURTAINS", 10))
        assert fake_notifs.sent['stock@made.com'] == [
            f"Out of stock for POPULAR-CURTAINS",
        ]
```

## 실제 통합 테스트

docekr-compose.yml

```dockerfile
version: "3"

services:

  redis_pubsub:
    build:
      context: .
      dockerfile: Dockerfile
    image: allocation-image
    ...

  api:
    image: allocation-image
    ...

  postgres:
    image: postgres:9.6
    ...

  redis:
    image: redis:alpine
    ...

  mailhog:
    image: mailhog/mailhog
    ports:
      - "11025:1025"
      - "18025:8025"
```

통합테스트에서 실제 EmailNotifications class를 사용하고 이는 Docker 클러스터의 MailHog 서버와 통신한다.

integration/test_email.py

```python
@pytest.fixture
def bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
        notifications=notifications.EmailNotifications(),  1
        publish=lambda *args: None,
    )
    yield bus
    clear_mappers()


def get_email_from_mailhog(sku):  2
    host, port = map(config.get_email_host_and_port().get, ['host', 'http_port'])
    all_emails = requests.get(f'http://{host}:{port}/api/v2/messages').json()
    return next(m for m in all_emails['items'] if sku in str(m))


def test_out_of_stock_email(bus):
    sku = random_sku()
    bus.handle(commands.CreateBatch('batch1', sku, 9, None))  3
    bus.handle(commands.Allocate('order1', sku, 10))
    email = get_email_from_mailhog(sku)
    assert email['Raw']['From'] == 'allocations@example.com'  4
    assert email['Raw']['To'] == ['stock@made.com']
    assert f'Out of stock for {sku}' in email['Raw']['Data']
```

##  DI and Bootstrap

- ABC를 사용해서 API를 정의해라
- 구현체를 작성해라
- fake를 만들고 이를 unit/service-layer/handler 테스트에서 사용해라
- Docker환경에서 구동될 수 있는 가상 Fake 서버를 찾는다
- 실제로 가상 Fake 서버와 테스트를 한다.