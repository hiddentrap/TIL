# Flask Project

## Project Structure

- config.py
- domain : 도메인 모델, 클래스당 파일 1개 (helper parent class, Entity, ValueObject, Aggregate, exceptions.py, commands.py, events.py 등)
  - `__init__`.py
  - model.py
- service_layer : unit_of_work.py, service-layer exceptions
  - `__init__`.py
  - services.py
- adapters : 외부 I/O에 대한 추상화 (redis_client.py 등) 구현체 및 인터페이스
  - `__init__`.py
  - orm.py
  - repository.py
- entrypoints : 외부 접근 요청 처리
  - `__init__`.py
  - flask_app.py
- tests
  - `__init__`.py
  - conftest.py
  - unit
    - test_allocate.py
    - test_batches.py
    - test_services.py
  - integration
    - test_orm.py
    - test_repository.py
  - e2e : end to end test (Function Test, Use-case Test)
    - test_api.py