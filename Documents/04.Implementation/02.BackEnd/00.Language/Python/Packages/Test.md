# Test

https://jiyeonseo.github.io/2020/03/10/pytest/

## 설치

```sh
pip install -U pytest
```

## 구조

```
setup.py
mypkg/
    __init__.py
    app.py
    view.py
    test/
        __init__.py
        test_app.py
        test_view.py
        ...
```

## 설정

project root/pytest.ini

```
[pytest]
addopts = -xv -s
```

- s: 테스트 내 print, logging 출력

https://docs.pytest.org/en/latest/reference.html#ini-options-ref

## 테스트 스킵

```python
@pytest.mark.skipif(os.environ.get("PROFILE", "local") != 'local', reason="run this test only at local")
```

```python
@pytest.mark.skip(reason="Just give me a reason")
```

## fixture

```python
@pytest.fixture()
def random_number():
    import random
    return random.randrange(1,10)

def test_random_range(random_number):
    assert random_number > 1 and random_number < 10 
```

- 테스트 시에 필요한 변수, 함수, 모듈, 클래스 등을 쉽게 가져다 쓸 수 있게 만들고, 함수의 arguments로 받아 바로 쓸 수 있게 해주는 기능.
- 사용가능한 fixture 확인

```
$ pytest --fixtures
```

### 설명

```sh
pip install pytest-it
```



```python
from pytest import mark as m

@m.describe("예시용 클래스")
class TestExample(object):

    @m.context("@pytest.mark.it을 이용할 때")
    @m.it("'- It: ' 데코레이터에 맞게 보여준다")
    def test_it_decorator(self):
        pass
```

```sh
- Describe: 예시용 클래스...

  - Context: @pytest.mark.it을 이용할 때...
    - ✓ It: '- It: ' 데코레이터에 맞게 보여준다
```

