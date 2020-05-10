# Property

@property 적용전 sample

```python
class Citizen:
    def __init__(self, age_value):
        self._age = age_value

    def get_age(self):
        print("나이를 리턴합니다.")
        return self._age

    def set_age(self, age_value):
        print("나이를 새로 설정합니다.")
        self._age = age_value
```

@property 적용후

```python
class Citizen:
    def __init__(self, age_value):
        self.age = age_value

    @property
    def age(self):
        print("나이를 리턴합니다.")
        return self._age

    @age.setter
    def age(self, age_value):
        print("나이를 새로 설정합니다.")
        self._age = age_value
```

- @property 메서드는 private 변수(_변수)에 대한 getter로 사용된다. (citizen.get_age() 대신, citizen.age 사용가능 )
- @age.setter(메서드명.setter)는 해당 메서드를 citizen.age(30)이 아닌 citizen.age=30 처럼 사용가능케함
- 사용목적: 기존에 Citizen 을 사용하는 코드의 수정없이 wraping method를 정의하여 로직 수정을 용의하게하기 위함