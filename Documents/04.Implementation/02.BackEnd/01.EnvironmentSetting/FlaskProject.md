# Flask Project

## Project Structure

- code
  - src
    - setup.py
    - allocation : Boundary
      - `__init__`.py
      - config.py
      - domain : 도메인 모델, 클래스당 파일 1개 (helper parent class, Entity, ValueObject, Aggregate, exceptions.py, commands.py, events.py 등)
        - `__init__`.py
        - model.py : 도메인 모델
      - service_layer : unit_of_work.py, service-layer exceptions
        - `__init__`.py
        - services.py
        - unit_of_work.py : Unit of Work Pattern (Service Layer - Reposityro bonding)
      - adapters : 외부 I/O에 대한 추상화 (redis_client.py 등) 구현체 및 인터페이스
        - `__init__`.py
        - orm.py : object - db mapper 
        - repository.py : Repository Pattern - orm abstraction
      - entrypoints : 외부 접근 요청 처리
        - `__init__`.py
        - flask_app.py : controller (http handle and url - service layer mapper)
  - tests
    - `__init__`.py
    - conftest.py
    - pytest.ini
    - unit
      - test_allocate.py : Domain Service Logic Test
      - test_batches.py : Domain Model Test
      - test_services.py : Service Layer Test
    - integration
      - test_orm.py : Orm Test
      - test_repository.py : Repository Pattern TEst
      - test_uow.py : Unit of Work pattern Test
    - e2e : end to end test (Function Test, Use-case Test)
      - test_api.py