# @dataclass

타입 어노테이션을 사용하면 생성자를 자동으로 만들어 준다.

@dataclass(init=True, repr=False, eq=False, order=False, unsafe_hash=False, frozen=True)

@dataclass : 생성자 자동생성, @dataclass(frozen=True) 불변클래스

## 사용전

```python
class Product:
  def __init__(self, name: str, unit_price: float, quantity_on_hand: int=0):
    self.name = name
    self.unit_price = unit_price
    self.quantity_on_hand = quantity_on_hand

  def total_cost(self) -> float:
    return self.unit_price * self.quantity_on_hand
```

## 사용후

```python
from dataclasses import dataclass

@dataclass
class Product:
  name: str
  unit_price: float
  quantity_on_hand: int = 0

  def total_cost(self) -> float:
    return self.unit_price * self.quantity_on_hand

i = Product("book", 1000.0, 10)
i.total_cost() # 10000.0
```

