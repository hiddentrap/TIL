# Flask Project

## Project Structure

- code
- Dockerfile: Docker container 설정
- Makefile : 워크플로우 명령어 : make build, make test 등등
- README.md
- docker-compose.yml : Docker container 설정
- license.txt
- mypy.ini
- requirments.txt
  - src
    - setup.py : pip install -e setup.py 
    - allocation : Boundary
      - `__init__`.py
      - config.py
      - (MODEL)domain : 도메인 모델, 클래스당 파일 1개 (helper parent class, Entity, ValueObject, Aggregate, exceptions.py, commands.py, events.py 등)
        - `__init__`.py
        - model.py : 도메인 모델
      - (SERVICE)service_layer : unit_of_work.py, service-layer exceptions
        - `__init__`.py
        - services.py
        - unit_of_work.py : Unit of Work Pattern (Service Layer - Reposityro bonding)
      - (INTERFACE)adapters : 외부 I/O에 대한 추상화 (redis_client.py 등) 구현체 및 인터페이스
        - `__init__`.py
        - orm.py : object - db mapper 
        - repository.py : Repository Pattern - orm abstraction
      - (API)entrypoints : 외부 접근 요청 처리
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

allocation/config.py

```python
import os

def get_postgres_uri():  1
    host = os.environ.get('DB_HOST', 'localhost')  2
    port = 54321 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'allocation', 'allocation'
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    port = 5005 if host == 'localhost' else 80
    return f"http://{host}:{port}"
```

[environ-config](https://github.com/hynek/environ-config)

docker-compose.yml

```yml
version: "3"
services:

  app:  
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - postgres
    environment:  
      - DB_HOST=postgres  
      - DB_PASSWORD=abc123
      - API_HOST=app
      - PYTHONDONTWRITEBYTECODE=1  
    volumes:  
      - ./src:/src
      - ./tests:/tests
    ports:
      - "5005:80"  


  postgres:
    image: postgres:9.6  
    environment:
      - POSTGRES_USER=allocation
      - POSTGRES_PASSWORD=abc123
    ports:
      - "54321:5432"
```

setup.py

```python
from setuptools import setup

setup(
    name='allocation',
    version='0.1',
    packages=['allocation'],
)
```

Dockerfile

```python
FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
RUN apk add libpq

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN apk del --no-cache .build-deps

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
ENV FLASK_APP=allocation/entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80
```



| 계층                                                         | 컴포넌트                              | 설명                                                         |
| ------------------------------------------------------------ | ------------------------------------- | ------------------------------------------------------------ |
| Domain(비지니스 로직)                                        | Entity                                | 속성이 변하더라도 식별 가능한 도메인 오브젝트                |
|                                                              | Value Object                          | 불변 도메인 객체로서 동일한 객체로 대체 가능하다             |
|                                                              | Aggregate                             | 관련된 오브젝트 클러스터로서 데이터 변경을 위한 단위로 취급, 일관성 바운더리를 정의한다. |
|                                                              | Event                                 | 어떤 사건이 발생했음을 나타낸다                              |
|                                                              | Command                               | 시스템이 수행해야 하는 job                                   |
| Service Layer: 시스템이 수행해야 하는 job을 정의하고 다른 컴포넌트들을 조율한다. | Handler                               | 명령이나 이벤트를 받아서 일어나야 할 것을 수행한다.          |
|                                                              | Unit of Work                          | 데이터 무결성과 관련한 추상화. 각 UoW는 원자적 변경을 나타낸다. repositori를 사용 가능하게 하고 어그리게이트의 새로운 이벤트를 추적한다. |
|                                                              | Message Bus(internel)                 | 명령과 이벤트를 다루고 알맞은 핸들러로 라우팅한다.           |
| Adapter(Secondary) 시스템 밖으로 나가는 인터페이스의 구현체  | Repository                            | 영속성 저장소의 추상화로 각 어그리게이트는 각각의 레포지토리를 갖는다. |
|                                                              | Event Publisher                       | 외부 메세지 버스(브로커)에 이벤트를 publish한다.             |
| Entrypoints(Primary adapters): 외부 입력을 서비스 레이어로의 호출로 변환한다. | Web                                   | 웹 리퀘스트를 받아서 명령어로 변환하고 이를 내부 메시지 버스로 전달한다. |
|                                                              | Event consumer                        | 외부 메시지 버스로부터 이벤트를 읽어서 명령어로 변환하고 이를 내부 메시지 버스로 전달한다. |
| N/A                                                          | External message bus (message broker) | 이벤트로 내부통신을 사용하는 다른 서비스의 인프라스트럭쳐    |

