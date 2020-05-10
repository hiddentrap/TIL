# Data Classes

일반적인 클래스,

``` python
class RegularCard
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(rank={self.rank!r}, suit={self.suit!r})')

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.rank, self.suit) == (other.rank, other.suit)
```

Python 3.7에 포함된 기능, @dataclass 적용

```python
from dataclasses import dataclass

@dataclass
class DataClassCard:
    rank: str
    suit: str
```

- @dataclass는 생성자(`__init__()`): class(a,b,c), 비교기능(`__eq__()`): obj == obj, 출력기능(`__repr__()`): print(obj) 이 구현되어 있어 DRY, 코드 중복을 줄인다. 각 소스에서 rank가 몇번 등장하는지 확인
- 기본값 설정 가능
- Type hint는 필수, Any로 설정 가능
- immutalbe(불변) 클래스로 생성 가능: @dataclass(frozen=True)
- 고정된 속성값(멤버 변수)를 갖는 클래스 생성시 `__slots__ = ['rank', 'suit']` 를 정의하면 메모리 및 처리 효율을 높일 수 있다.



## Refer

[RealPython](https://realpython.com/python-data-classes/#basic-data-classes)

