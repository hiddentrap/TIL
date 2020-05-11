# Service Layer Pattern

Service Layer = orchestration layer = use-case layer

[endpoint api layer function: flask_app.py] [service layer function: services.py] [allocate domain service function: model.py]

## Domain Service VS Service Layer (Application Service)

Service Layer (Application Service): Requests 핸들러로서 일련의 동작들을 조율 및 조직한다.

- 데이터베이스로부터 데이터를 가져온다.

- 도메인 모델을 업데이트한다.

- 변화를 저장한다.

  이 행위들은 매 기능마다 반복되는 경향이 있고, 마땅히 비지니스 로직과 분리되어야 한다.

Domain Service: 도메인 모델에 속해있는 로직

- 모든 로직이 영속성 있는 Entity나 Value Object에 속해 있는 것은 아니다.
- 쇼핑카트 앱을 개발한다고 할 때, 세금계산을 Domain service로 뽑아낼 수 있다. 하지만 세금계산은 카트 모델을 업데이트하는 것과는 관계가 없지만 중요한 모델이다. 그렇다고 세금계산을 영속성 있는 entity로 구성할 수 는 없다. 결국 영속성 없는 TaxCalculator 클래스로 만들거나 claculate_tax 함수로 구현할 수 있다.



​	Service Layer는 EndPints API를 JSON 파싱, HTTP생성 으로 한정할 수 있게하여 매우 작게 유지하기 쉽게 한다. 

## Pros vs Cons

### Pros

- 모든 유즈 케이스를 한 곳에 집중시킬 수 있다.
- 도메인 로직을 뒤로 숨겨 리펙터링 하기 쉽게 한다.
- HTTP 처리와 로직을 분리할 수 있게한다.
- Repository 패턴과 결합하면 도메인 레이어보다 상위 레벨에서 테스트하기 더 용이하게 해준다.

### Cons

- 순수한 web app(db가 필요 없는)이라면 controllers/view 함수에 모든 유즈 케이스를 집중시킬수 있다.
- 그럼에도 불구하고 추상화가 늘어난다.
- 너무 많은 로직을 서비스 레이어에 몰아 넣으면 Anemic Domain 안티 패턴이 될 수 있다. 
- 서비스 레이어 없이 controller의 로직을 domain model로 배치하는 "fat models, thins controllers"를 고려해볼 수 도 있다.

## Tests for Service Function

test_api.py

```python
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_201_and_allocated_batch(add_stock):
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock([
        (laterbatch, sku, 100, '2011-01-02'),
        (earlybatch, sku, 100, '2011-01-01'),
        (otherbatch, othersku, 100, None),
    ])
    data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}
    url = config.get_api_url()
    r = requests.post(f'{url}/allocate', json=data)
    assert r.status_code == 201
    assert r.json()['batchref'] == earlybatch


@pytest.mark.usefixtures('restart_api')
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {'orderid': orderid, 'sku': unknown_sku, 'qty': 20}
    url = config.get_api_url()
    r = requests.post(f'{url}/allocate', json=data)
    assert r.status_code == 400
    assert r.json()['message'] == f'Invalid sku {unknown_sku}'
```

## Steps for Service Function

1. 저장소에서 오브젝트 fetch

2. 유효성 검증: 요청값 검증

3. 도메인 서비스 호출: 오브젝트 상태 변경

4. 성공적일 경우 변경된  내용 저장소에 저장 및 업데이트: 오브젝트 상태 저장

   flask_app.py : 세션관리, Request 파라메터 파싱, Response 상태코드 as json

   ```python
   @app.route("/allocate", methods=['POST'])
   def allocate_endpoint():
       session = get_session()  
       repo = repository.SqlAlchemyRepository(session)  
       line = model.OrderLine(
           request.json['orderid'],  
           request.json['sku'],  
           request.json['qty'],  
       )
       try:
           batchref = services.allocate(line, repo, session)  
       except (model.OutOfStock, services.InvalidSku) as e:
           return jsonify({'message': str(e)}), 400  
   
       return jsonify({'batchref': batchref}), 201  
   ```

   **services.py**: orchestration or use-case

   ```python
   class InvalidSku(Exception):
       pass
   
   
   def is_valid_sku(sku, batches):
       return sku in {b.sku for b in batches}
   
   def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
       batches = repo.list()  
       if not is_valid_sku(line.sku, batches):  
           raise InvalidSku(f'Invalid sku {line.sku}')
       batchref = model.allocate(line, batches)  
       session.commit()  
       return batchref
   ```

   