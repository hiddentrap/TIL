# Python TDD

## Web Functional Test (End to End Test)

### Selenium

> selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH

```python
pip install webdriver-manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```

## URL View Mapping Test

```python
    def test_root_url_resolves_to_home_page_view(self):
        # Given Nothing

        # When
        found = resolve('/')

        # Then
        self.assertEqual(found.func, home_page)
```



## HTML Test

### Isolated way

```python
    def test_home_page_returns_correct_html(self):
        # Given
        request = HttpRequest()

        # When
        response = home_page(request)
        html = response.content.decode('utf8')

        # Then
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>서버관리</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
```

```python
 def test_home_page_can_save_a_POST_request(self):
        # Given
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'SERVER01'

        # When
        response = home_page(request)

        # Then
        self.assertIn('SERVER01', response.content.decode())
        expected_html = render_to_string('servers.html', {'new_item_text': 'SERVER01'})
        self.assertEqual(expected_html, response.content.decode())
```

### Django way

```python
    def test_uses_home_template(self):
        # Given Nothing

        # When
        response = self.client.get('/')

        # Then
        self.assertTemplateUsed(response, 'servers.html')
```

## Type Test: Type Annotation

[참고하여 정리필요](https://seorenn.tistory.com/77)

```
mypy test.py
```

## Mocking Framework 사용금지

​	Mocking Framework(mock.patch, monkeypatching, unittest.mock)을 사용하는 대신 Fake(추상화) Class를 만들어 사용하는 것이 낫다.

Fake(추상화) Class : 테스트에서만 사용할 수 있는 외부 컴포넌트 대체 동작 구현체 

Fake(추상화) Class를 사용한 테스트

스텁 = dummy : 아직 완성되지 않은 하부 모듈 대신 사용하는 모듈

```python
class FakeFileSystem(list): 

    def copy(self, src, dest): 
        self.append(('COPY', src, dest))

    def move(self, src, dest):
        self.append(('MOVE', src, dest))

    def delete(self, dest):
        self.append(('DELETE', src, dest))


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source = {"sha1": "my-file" }
    dest = {}
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    synchronise_dirs(reader.pop, filesystem, "/source", "/dest")

    assert filesystem == [("COPY", "/source/my-file", "/dest/my-file")]


def test_when_a_file_has_been_renamed_in_the_source():
    source = {"sha1": "renamed-file" }
    dest = {"sha1": "original-file" }
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    synchronise_dirs(reader.pop, filesystem, "/source", "/dest")

    assert filesystem == [("MOVE", "/dest/original-file", "/dest/renamed-file")]

```

## Integration Test (Adapter: External API - I/O Test)

orm test

```python
def test_orderline_mapper_can_load_lines(session):
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



def test_retrieving_batches(session):
    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        ' VALUES ("batch1", "sku1", 100, null)'
    )
    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        ' VALUES ("batch2", "sku2", 200, "2011-04-11")'
    )
    expected = [
        model.Batch("batch1", "sku1", 100, eta=None),
        model.Batch("batch2", "sku2", 200, eta=date(2011, 4, 11)),
    ]

    assert session.query(model.Batch).all() == expected


def test_saving_batches(session):
    batch = model.Batch('batch1', 'sku1', 100, eta=None)
    session.add(batch)
    session.commit()
    rows = list(session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    ))
    assert rows == [('batch1', 'sku1', 100, None)]

def test_saving_allocations(session):
    batch = model.Batch('batch1', 'sku1', 100, eta=None)
    line = model.OrderLine('order1', 'sku1', 10)
    batch.allocate(line)
    session.add(batch)
    session.commit()
    rows = list(session.execute('SELECT orderline_id, batch_id FROM "allocations"'))
    assert rows == [(batch.id, line.id)]


def test_retrieving_allocations(session):
    session.execute(
        'INSERT INTO order_lines (orderid, sku, qty) VALUES ("order1", "sku1", 12)'
    )
    [[olid]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid='order1', sku='sku1')
    )
    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        ' VALUES ("batch1", "sku1", 100, null)'
    )
    [[bid]] = session.execute(
        'SELECT id FROM batches WHERE reference=:ref AND sku=:sku',
        dict(ref='batch1', sku='sku1')
    )
    session.execute(
        'INSERT INTO allocations (orderline_id, batch_id) VALUES (:olid, :bid)',
        dict(olid=olid, bid=bid)
    )

    batch = session.query(model.Batch).one()

    assert batch._allocations == {
        model.OrderLine("order1", "sku1", 12)
    }
```

repository test

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
    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)',
        dict(batch_id=batch_id)
    )
    [[batch_id]] = session.execute(
        'SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"',
        dict(batch_id=batch_id)
    )
    return batch_id

def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        'INSERT INTO allocations (orderline_id, batch_id)'
        ' VALUES (:orderline_id, :batch_id)',
        dict(orderline_id=orderline_id, batch_id=batch_id)
    )


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
```

## Unit Test (model: entity or vo -> service)

초창기엔 Domain Model Test로 작성하다가 개발에 속도가 붙으면 Service Layer API Test로 전환 그러다가 문제에 부딪히면 다시 Domain Model Test에서 시작

### Service Layer API Test: 신규 기능 추가시

​	Service Layer API Test는 Domain Model에 대한 의존성을 제거해야 하고, primitive 타입만 사용하도록 한다.

- 코드 수정시 느슨한 Feedback
- 코드 수정시 낮은 장벽
- 높은 수준에서의 시스템 커버리지

### Domain Model Test: 새 프로젝트나 특정 문제 해결시

- 코드 수정시 빡쎈 Feedback
- 코드 수정시 높은 장벽
- 집중된 수준에서 커버리지