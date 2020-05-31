# Python Trick

[정리필요](https://dailyheumsi.tistory.com/224?category=855210)

## Ch2. 소소한것들

### Assert

디버깅 도구

```python
def apply_discount(product, discount):
    price = int(product['price'] * (1 - discount))
    assert 0 <= price <= product['price']  # 조건이 거짓이면 AssertionError 를 일으킨다.
    return price
```

디버깅 외의 용도로 사용하지 말것

```python
# 아래 같이 AssertionError 를 예외 처리하면 안된다.
try:
    apply_discount(product, discount)
except AssertionError:
    pass

# 아래와 같이 단언문을 유효성 검증에 사용하면 안된다.
def delete_product(product_id, user):
    assert user.is_admin(), "Must be admin"  # AssertionError 와 동시에 메시지를 출력한다.
    assert store.has_product(product_id), "Unknown product"
    store.get_product(product_id).delete()
    
# 유효성 검증에는 아래와 같이 일반적인 if 문을 사용하자.
def delete_product(product_id, user):
    if not user.is_admin():
        raise AuthError("Must be admin to delete")
    if not store.has_product(product_id):
        raise ValueError("Unknown product id")
    store.get_product(product_id).delete()
```

잘못사용예

```python
# tuple 에 값이 들어있으면 항상 True 로 판명된다.
assert (1 == 2, "This should fail")

# 위 코드의 의도대로라면, 아래와 같이 수정되어야 한다.
assert 1 == 2, "This should fail"
```



### 콤마사용

```python
names = [
    'Alice',
    'Bob',
    'Dilbert',
]
```



### With

리소스에 사용한다: file, 트랜잭션, lock 등

```python
f = open('hello.txt', 'w')
try:
    f.write('hello, world')
finally:
    f.close()
    
with open('hello.txt' , 'w' ) as f:
	f.write('hello, world!' )
    
    
some_lock = threading.Lock()

some_lock.acquire()
try:
    pass  # 뭔가를 한다.
finally:
    some_lock.release()
    
with some_lock:
    pass  # 뭔가를 한다.
```

#### With 지원객체 생성

with 지원객체 = Context Manager = With Statement Context Managers를 구현하는 함수나 클래스

```python
class ManagedFile: # open() 이랑 유사
    def __init__(self, name):
        self.name = name
        
    def __enter__(self):
        self.file = open(self.name, 'w')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            
            
 with ManagedFile('hello.txt') as f:
    f.write('hello, world')
    f.write('bye now')
    
    
from contextlib import contextmanager

@contextmanager
def managed_file(name):
    try:
        f = open(name, 'w')
        yield f
    finally:
        f.close()
   
  with managed_file('hello.txt') as f:
    f.write('hello, world')
    f.write('bye now')
```



### 언더스코어

- _var: private 사용을 의미, 문법적 강제는 없음
- _function: import * 하면 import 안됨
- var_: 파이썬 Keyword와 중복을 피하기 위한 꼼수성
- __var: 인터프리터가 name mangling 시킴
- `__var__`: 파이썬에서 사용하는 특별한 형태 개발자는 사용금지
- `_`: 템프성, 마지막 인터프리터의 평과결과를 갖는다.

```python
for _ in range(32):
	print('hello')
```



### 문자열 포매팅

```python
>>> name = "abc"
>>> f"Hello, {name}"
'Hello, abc'

>>> a = 5
>>> b = 10
>>> f'Five plus ten is {a + b} and not {2 * (a + b)}.'
'Five plus ten is 15 and not 30.'

>>> f"Hey {name}, there' s a {errno: #x} error!"
"Hey Bob, there's a 0xbadc0ffee error!"
```



## Ch3. Functions

### 함수=일급객체

파이썬 함수는 변수에 할당가능하고 데이터 구조에 저장할 수 있으며 파라메터로 넘기거나 리턴할 수 있다.

람다나 데코레이터의 기본이 되는 개념이며 함수형 프로그래밍으로 발전되는 개념이다.

#### 기본함수

```python
def yell(text):
	return text.upper() + '!'

>>> yell(' hello' )
'HELLO!
```

#### 함수는 객체

파이썬의 모든 데이터는 객체나 객체의 관계로써 표현된다. 문자열, 리스트, 모듈, 함수는 모두 오브젝트이다. 함수라고 특별한건 아니다. 함수 역시 오브젝트이다.

함수는 오브젝트이기 때문에 함수 역시 변수에 할당할 수 있다.

```python
bark = yell
bark('woof')
'WOOF!'
```

함수 객체와 함수의 이름은 별도의 분리된 개념이다. 그래서 yell을 삭제해도, bark가 해당 함수 객체를 여전히 가리키고 있기 때문에 함수 객체 자체는 삭제되지 않으므로, bark로 호출할 수 있다.

```python
del yell
yell('hello?')
NameError: "name 'yell' is not defined"
bark('hey')
'HEY!'
bark.__name__
'yell'
```

파이썬은 함수의 생성시점에 디버깅 목적으로 문자열 식별자를 함수에 붙여 놓는다.  이는 `__name__`으로 접근할 수 있는다. 이는 단순히 디버깅 목적이므로 함수를 호출하는것과는 전혀 무관하다. 

#### 자료구조에 함수저장

함수는 일급객체이기 때문에 다른 객체들 처럼 자료구조에 저장할 수 있다.

```python
funcs = [bark, str.lower, str.capitalize]
for f in funcs:
	print(f, f('hey there'))
<function yell at 0x10ff96510> 'HEY THERE!'
<method 'lower' of ' str' objects> 'hey there'
<method 'capitalize' of ' str' objects> 'Hey there'

funcs[0]('heyho')
'HEYHO!'
```

#### 함수 파라메터

```python
def greet(func):
	greeting = func('Hi, I am a Python program')
	print(greeting)

greet(bark)
'HI, I AM, PYTHON PROGRAM!'

>>> list(map(bark, ['hello', 'hey', 'hi']))
['HELLO!', 'HEY!', 'HI!']
```

#### 중첩함수

```python
def speak(text):
	def whisper(t):
		return t.lower() + '...'
	return whisper(text)

>>> speak('Hello, World')
'hello, world...'
```

#### 함수리턴

```python
def get_speak_func(volume):
	def whisper(text):
		return text. lower() + '...'
	def yell(text):
		return text. upper() + '!'
	if volume > 0. 5:
		return yell
	else:
		return whisper
    
>>> speak_func = get_speak_func(0.7)
>>> speak_func('Hello')
'HELLO!'
```

#### 클로져(Closure)

Inner function은 부모 함수의 상태값을 기억했다가 사용할 수 있다.

```python
def get_speak_func(text, voluem):
    def whisper():
        return text.lower()+'...'
    def yell():
        return text.upper() + '!'
    if volume > 0.5:
        return yell
    else:
        return whisper
    
get_speak_func('Hello, World', 0.7)()
'HELLO, WORLD!'


def make_adder(n):
    def add(x):
        return x + n
    return add

plus_3 = make_adder(3)
plus_5 = make_adder(5)
plus_3(4)
7
plus_5(4)
9
```

여기에서 make_adder는 미리 설정된 adder 함수를 생성하는 factory가 될 수 있다. 

#### 객체를 함수처럼

펑션은 객체이지만, 객체는 함수가 아니다. 하지만 객체도 호출가능하도록 만들어서 많은 경우에 함수처럼 취급할 수 있다.

```python
class Adder:
    def __init__(self, n):
        self.n = n
        
    def __call__(self, x):
        return self.n + x
    
plus_3 = Adder(3)
plus_3(4)
7
callable(plus_3)
True
```



### 람다 = 싱글표현 함수

`lambda`는 익명 함수의 객체를 얻기 위해 사용하는 키워드

1개 표현만 허용된다: 여러라인 사용불가, 어노테이션사용불가, 명시적 리턴문 사용불가

```python
add = lambda x, y: x+y
add(5,3)

(lambda x, y: x + y)(5,3)

def make_addr(n):
    return lambda x: x+n

plus_3(4)
7
```

이렇게 사용하면 lambda도 클로저가 된다.



### 데코레이터

#### 기본개념

호출가능 객체(함수, 메서드, 클래스)를 직접 수정하지 않고 동작을 수정하여 확장할 수 있게한다.

로깅, 인증과 접근제어, 비율제한, 캐싱 등

데코레이터를 이해하기위해 먼저 상기시킬것, 

함수는 객체다: 함수는 변수에 할당될 수 있고 파라메터로 전달할 수 있으며 리턴될 수도 있다.

함수는 다른 함수의 내부에서 정의될 수 있다: 클로져 (부모 함수의 상태값을 기억할 수 있다)

데코레이터는 함수를 장식하거나 감싸는 개념으로 감싸진 함수의 호출 전 후에 코드를 실행시킬 수 있게 해준다: 호출객체를 입력으로 하고 다른 호출 객체를 반환하는 호출객체

```python
def null_decorator(func):
    return func

def greet():
    return 'Hello'
greet = null_decorator(greet)

@null_decorator
def greet():
    return 'Hello!'
greet()
'Hello!'
```

```python
def uppercase(func):
    def wrapper():
        original_result = func()
        modified_result = original_result.upper()
        return modified_result
    return wrapper

@uppercase
def greet():
    return 'Hello!'
greet()
'HELLO!'
```

#### 함수에 데코레이터 복수개 적용

함수에 가까운 데코레이터부터 실행

```python
def strong(func):
    def wrapper():
        return '<string>' + func() + '</strong>'
    return wrapper

def emphasis(func):
    def wrapper():
        return '<em>' + func() + '</em>'
    return wrapper

@strong
@emphasis
def greet():
    return 'Hello!'
greet()
'<string><em>Hello!</em></strong>'
```

#### 데코레이터에 파라메터전달

*args와 **kwargs 이용

```python
def proxy(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

```python
def trace(func):
    def wrapper(*args, **kwargs):
        print(f'TRACE: calling {func.__name__}() '
             f'with {args}, {kwargs}')
        
        original_result = func(*args, **kwargs)
        
        print(f'TRACE: {func.__name__}() '
             f'returned {original_result!r}')
        
        return original_result
    return wrapper

@trace
def say(name, line):
    return f'{name}: {line}'

say('Jane', 'Hello, World')
'TRACE: calling say() with ("Jane", "Hello, World"), {}'
'TRACE: say() returned "Jane: Hello, World"'
'Jane: Hello, World'
        
```

#### 디버깅 가능한 데코레이터 작성

데코레이팅하면 원래 함수의 이름, docstring, 파라메터 리스트가 클로저에 의해 숨겨진다.

```python
def greet():
    """Return a friendly greeting."""
    return ' Hello! '
decorated_greet = uppercase(greet)

>>> greet. __name__
'greet'
>>> greet. __doc__
'Return a friendly greeting. '
>>> decorated_greet. __name__
'wrapper'
>>> decorated_greet. __doc__
None
This mak
```

이는 functools.wraps 데코레이터를 사용해서 해결할 수 있다.

```python
import functools

def uppercase(func):
    @functools.wraps(func)
    def wrapper():
        return func().upper()
    return wrapper
```



### 가변인자

#### *args, **kwargs (optional parameter)

```python
def foo(required, *args, **kwargs):
    print(required)
    if args:
        print(args)
    if kwargs:
        print(kwargs)
        
>>> foo()
TypeError:
"foo() missing 1 required positional arg: 'required'"
>>> foo('hello')
hello
>>> foo('hello', 1, 2, 3)
hello
(1, 2, 3)
>>> foo('hello', 1, 2, 3, key1='value' , key2=999)
hello
(1, 2, 3)
{'key1' : 'value' , ' key2' : 999}
```

*args : 튜플, **kwargs : 딕셔너리

#### 가변인자 전달

```python
def foo(x, *args, **kwargs):
    kwargs['name' ] = 'Alice'
    new_args = args + ('extra', )
    bar(x, *new_args, **kwargs)
```

### 파라메터 언패킹

그닥...

### NONE RETURN

파이썬은 명시적으로 RETURN 하지 않으면 묵시적으로 None 리턴된다.

return 이 없으면 프로시져,

**그래도 명시적으로 return None 해주자**

## Ch4. Class & OOP

### 객체비교: is vs ==

값비교: == (equal)

객체비교: is (레퍼런스 비교, identical)

### 문자열변환

모든 클래스에는 `__repr__`을 정의할 필요가 있다. : `__str__`이 없으면 `__repr__`을 대신 호출

`__str__` : 객체를 스트링으로 변환하려 할때 호출되는 메서드 : 사람이 보기 편한 스트링

'2017-02-02'

`__repr__`: `__str__`과 비슷하지만 차이가 있음 : 같은 객체를 copy & paste로 생성할수 있는 코드가 좋지만 현실적으로 거시기 하니까 그냥 이것은 개발자가 보기 편한 용도로 (디버깅등)

'datetime.date(2017, 2, 2)'

```python
class Car:
    def __init__(self, color, mileage):
        self. color = color
        self. mileage = mileage

        def __repr__(self):
            return ' __repr__ for Car'
        def __str__(self):
            return ' __str__ for Car'
        
>>> my_car = Car(' red' , 37281)
>>> print(my_car)
__str__ for Car
>>> ' {}' . format(my_car)
'__str__ for Car'
>>> my_car
__repr__ for Car
```

```python
class Car:
    def __init__(self, color, mileage):
        self. color = color
        self. mileage = mileage
        
    def __repr__(self):
        return (f' {self. __class__. __name__}('
                f' {self. color! r}, {self. mileage! r})' )
    
    def __str__(self):
        return f' a {self. color} car'
```

`__repr__`에는 {a!r}처럼 !r을 붙여서 'out stpring' 으로 나오게 해서 `__str__` 의 출력과 구분되게 하자

### Exception 클래스 정의

```python
class BaseValidationError(ValueError):
    pass

class NameTooShortError(BaseValidationError):
    pass

class NameTooLongError(BaseValidationError):
    pass

class NameTooCuteError(BaseValidationError):
    pass

def validate(name):
    if len(name)<10:
        raise NameTooShortError(name)


try:
    validate(name)
except BaseValidationError as err:
    handle_validation_error(err)
```

### 객체 복사

파이썬에서 할당문은 객체의 복사본을 생성하지 않는다. 이는 단지 이름과 객체를 바인딩 시킬 뿐이다.

얕은복사: 1단계 복사로 copy가 재귀적으로 이루어지지 않아 그 자식 객체들은 복사되지 않는다.

```python
new_list = list(original_list)
new_dict = dict(original_dict)
new_set = set(original_set)
```

깊은복사: 완전한 복사로 자식 객체들꺼자 재귀적으로 복사

```python
>>> import copy
>>> xs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
>>> zs = copy. deepcopy(xs)
```

```python
class Rectangle:
    def __init__(self, topleft, bottomright):
        self.topleft = topleft
        self.bottomright = bottomright
        
    def __repr__(self):
        return (f'Rectangle({self.topleft!r}, '
                f'{self.bottomright!r})')
    
rect = Rectangle(Point(0, 1), Point(5, 6))
srect = copy.copy(rect)
>>> rect
Rectangle(Point(0, 1), Point(5, 6))
>>> srect
Rectangle(Point(0, 1), Point(5, 6))
>>> rect is srect
False
>>> rect.topleft.x = 999
>>> rect
Rectangle(Point(999, 1), Point(5, 6))
>>> srect
Rectangle(Point(999, 1), Point(5, 6))


>>> drect = copy.deepcopy(srect)
>>> drect.topleft.x = 222
>>> drect
Rectangle(Point(222, 1), Point(5, 6))
>>> rect
Rectangle(Point(999, 1), Point(5, 6))
>>> srect
Rectangle(Point(999, 1), Point(5, 6))
```

### 추상클래스

Abstract Base Classes(ABCs)는 자식클래스의 기반 클래스 메소드 구현을 보장한다.

```python
from abc import ABCMeta, abstractmethod
class Base(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass
    
    @abstractmethod
    def bar(self):
        pass
    
class Concrete(Base):
    def foo(self):
        pass
# We forget to declare bar() again.. .
```

### 이름있는튜플

일반튜플

```python
>>> tup = (' hello' , object(), 42)
>>> tup
(' hello' , <object object at 0x105e76b70>, 42)
>>> tup[2]
42
>>> tup[2] = 23
TypeError:
"'tuple' object does not support item assignment"
```

단점 인덱스 번호로만 접근가능

네임드 튜플 = 간단하게 불변 클래스 생성

```python
from collections import namedtuple

# Car 라는 이름의 불변 클래스를 생성하고 color 와 mileage 를 속성으로 가진다.
Car = namedtuple("Car", ["color", "mileage"])

>>> my_car = Car("red", 3812.4)
>>> my_car.color
"red"
>>> my_car.mileage
3812.4
>>> color, mileage = my_car  # 일반 튜플처럼 unpacking 도 가능하다.
```

상속

```python
Car = namedtuple("Car", ["color", "mileage"])

# namedtupled 의 _fields 속성으로 기존 속성목록을 가져온다.
ElectricCar = namedtuple("ElectricCar", Car._fields + ("charge", ))
>>> ElectricCar("red", 1234, 45.0)
ElectricCar(color="red", mileage=1234, charge=45.0)

>>> my_car. _asdict()
OrderedDict([(' color' , ' red' ), (' mileage' , 3812. 4)])
>>> json. dumps(my_car. _asdict())
'{"color": "red", "mileage": 3812. 4}'

>>> my_car. _replace(color=' blue' )
Car(color=' blue' , mileage=3812. 4)

>>> Car. _make([' red' , 999])
Car(color=' red' , mileage=999)
```

### 클래스변수 vs 인스턴스변수

클래스변수 = Static

```python
class Dog:
	num_legs = 4 # <- Class variable
    
	def __init__(self, name):
        self. name = name # <- Instance variable
        
class CountedObject:
    num_instances = 0
    
    def __init__(self):
        self. __class__.num_instances += 1
```

### 클래스,인스턴스, 스태틱메서드

```python
class MyClass:
    def method(self):
        return 'instance method called', self
    
    @classmethod
    def classmethod(cls):
        return 'class method called', cls
    
    @staticmethod
    def staticmethod():
        return 'static method called'
```

- 인스턴스 메서드 (인스턴스와 클래스에 둘다 접근 가능)
  - 인스턴스 자신의 속성은 : `self.속성`으로 접근 가능
  - 클래스 속성 접근은 `self.__class__`로 가능
  - 클래스 호출시 TypeError
- 클래스 메서드 (인스턴스에 접근 불가)
  - cls: 클래스 자신밖에 접근 불가, 
  - 클래스 호출 가능
- 스태틱 메서드 (인스턴스와 클래스 속성 모두에 접근 불가)
  - 클래스 호출 가능

클래스메서드 사용예 : Factory 패턴 구현체

```python
class Pizza:
    def __init__(self, ingredients):
        self. ingredients = ingredients
        
    def __repr__(self):
        return f' Pizza({self. ingredients! r})'
    
    @classmethod
    def margherita(cls):
        return cls([' mozzarella' , ' tomatoes' ])
    
    @classmethod
    def prosciutto(cls):
        return cls([' mozzarella' , ' tomatoes' , ' ham' ])
    
>>> Pizza([' cheese' , ' tomatoes' ])
Pizza([' cheese' , ' tomatoes' ])
>>> Pizza.margherita()
Pizza([' mozzarella' , ' tomatoes' ])
>>> Pizza.prosciutto()
Pizza([' mozzarella' , ' tomatoes' , ' ham' ])
```

스태틱 메서드 사용예

```python
import math

class Pizza:
    def __init__(self, radius, ingredients):
        self.radius = radius
        self.ingredients = ingredients
    
    def __repr__(self):
        return (f'Pizza({self.radius!r},'
                f'{self.ingredients!r})' )
    
    def area(self):
        return self.circle_area(self.radius)

    @staticmethod
    def circle_area(r):
        return r ** 2 * math.pi
    
>>> p = Pizza(4, [' mozzarella' , ' tomatoes' ])
>>> p
Pizza(4, {self. ingredients})
>>> p. area()
50. 26548245743669
>>> Pizza. circle_area(4)
50. 26548245743669
```

## Ch5. 데이터구조

### Dictionary, Maps, Hashtables

Dictionary = Maps = Hashmaps = Lookup tables = Associative arrays

딕셔너리  = 사전 = 맵 = 해쉬맵 = 룩업 테이블 = 연관배열

효과적인 검색, 삽입, 삭제 with Key

```python
phonebook = {
    'bob' : 7387,
    'alice' : 3719,
    'jack' : 7052,
}
squares = {x: x * x for x in range(6)}
>>> phonebook['alice' ]
3719
>>> squares
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

#### collections.OrderedDict

순서가 있는 Dictionary  by key, 3.6버전 이상은 일반 Dict가 OrderedDict로 동작

```python
>>> import collections
>>> d = collections.OrderedDict(one=1, two=2, three=3)
>>> d
OrderedDict([('one', 1), ('two', 2), ('three', 3)])
>>> d['four'] = 4
>>> d
OrderedDict([('one', 1), ('two', 2),
('three', 3), ('four', 4)])
>>> d. keys()
odict_keys(['one', 'two', 'three', 'four'])
```

#### collections.defaultdict

```python
>>> from collections import defaultdict
>>> dd = defaultdict(list)
# Accessing a missing key creates it and
# initializes it using the default factory,
# i.e. list() in this example:
>>> dd['dogs' ]. append('Rufus' )
>>> dd['dogs' ]. append('Kathrin' )
>>> dd['dogs' ]. append('Mr Sniffles' )
>>> dd['dogs' ]
['Rufus' ,'Kathrin' ,'Mr Sniffles' ]
```

#### collections.ChainMap

여러개의 딕셔너리를 하나의 딕셔너리처럼 검색할때

```python
>>> from collections import ChainMap
>>> dict1 = {' one' : 1, ' two' : 2}
>>> dict2 = {' three' : 3, ' four' : 4}
>>> chain = ChainMap(dict1, dict2)
>>> chain
ChainMap({' one' : 1, ' two' : 2}, {' three' : 3, ' four' : 4})
# ChainMap searches each collection in the chain
# from left to right until it finds the key (or fails):
>>> chain[' three' ]
3
>>> chain[' one' ]
1
>>> chain[' missing' ]
KeyError: ' missing'
```

#### collections.MappingProxyType

읽기전용 딕셔너리를 만들때 Wrapper

```python
>>> from types import MappingProxyType
>>> writable = {' one' : 1, ' two' : 2}
>>> read_only = MappingProxyType(writable)
# The proxy is read-only:
>>> read_only[' one' ]
1
>>> read_only[' one' ] = 23
TypeError:
"'mappingproxy' object does not support item assignment"
# Updates to the original are reflected in the proxy:
>>> writable[' one' ] = 42
>>> read_only
mappingproxy({' one' : 42, ' two' : 2})
```

### Array(배열)

#### 리스트

Mutable(수정가능한) Dynamic(동적) Array(배열)

요소의 타입에는 제한이 없다.

```python
>>> arr = [' one' , ' two' , ' three' ]
>>> arr[0]
'one'
# Lists have a nice repr:
>>> arr
[' one' , ' two' , ' three' ]
# Lists are mutable:
>>> arr[1] = ' hello'
>>> arr
[' one' , ' hello' , ' three' ]
>>> del arr[1]
>>> arr
[' one' , ' three' ]
# Lists can hold arbitrary data types:
>>> arr. append(23)
>>> arr
[' one' , ' three' , 23]
```

#### 튜플

Immutable(수정불가능한) Container (컨테이너)

요소의 타입에는 제한이 없다.

```python
>>> arr = ' one' , ' two' , ' three'
>>> arr[0]
'one'
# Tuples have a nice repr:
>>> arr
(' one' , ' two' , ' three' )
# Tuples are immutable:
>>> arr[1] = ' hello'
TypeError:
"'tuple' object does not support item assignment"
>>> del arr[1]
TypeError:
"'tuple' object doesn't support item deletion"
# Tuples can hold arbitrary data types:
# (Adding elements creates a copy of the tuple)
>>> arr + (23, )
(' one' , ' two' , ' three' , 23)
```

#### array.array

Basic Typed Arrays

리스트와 비슷하지만 요소의 타입이 한가지로만 제한된다

```python
>>> import array
>>> arr = array. array(' f' , (1. 0, 1. 5, 2. 0, 2. 5))
>>> arr[1]
1. 5
# Arrays have a nice repr:
>>> arr
array(' f' , [1. 0, 1. 5, 2. 0, 2. 5])
# Arrays are mutable:
>>> arr[1] = 23. 0
>>> arr
array(' f' , [1. 0, 23. 0, 2. 0, 2. 5])
>>> del arr[1]
>>> arr
array(' f' , [1. 0, 2. 0, 2. 5])
>>> arr. append(42. 0)
>>> arr
array(' f' , [1. 0, 2. 0, 2. 5, 42. 0])
# Arrays are "typed":
>>> arr[1] = ' hello'
TypeError: "must be real number, not str"
```

#### str

Immutable Arrays of Unicode Characters

```python
>>> arr = ' abcd'
>>> arr[1]
'b'
>>> arr
'abcd'
# Strings are immutable:
>>> arr[1] = ' e'
TypeError:
"'str' object does not support item assignment"
>>> del arr[1]
TypeError:
"'str' object doesn't support item deletion"
# Strings can be unpacked into a list to
# get a mutable representation:
>>> list(' abcd' )
[' a' , ' b' , ' c' , ' d' ]
>>> ' ' . join(list(' abcd' ))
'abcd'
# Strings are recursive data structures:
>>> type(' abc' )
"<class 'str'>"
>>> type(' abc' [0])
"<class 'str'>"
```

#### bytes

Immutable Arrays of Single Bytes

```python
>>> arr = bytes((0, 1, 2, 3))
>>> arr[1]
1
# Bytes literals have their own syntax:
>>> arr
b' x00x01x02x03'
>>> arr = b' x00x01x02x03'
# Only valid "bytes" are allowed:
>>> bytes((0, 300))
ValueError: "bytes must be in range(0, 256)"
# Bytes are immutable:
>>> arr[1] = 23
TypeError:
"'bytes' object does not support item assignment"
>>> del arr[1]
TypeError:
"'bytes' object doesn't support item deletion"
```

#### bytearray

Mutable Arrays of Single Byte

```python
>>> arr = bytearray((0, 1, 2, 3))
>>> arr[1]
1
# The bytearray repr:
>>> arr
bytearray(b' x00x01x02x03' )
# Bytearrays are mutable:
>>> arr[1] = 23
>>> arr
bytearray(b' x00x17x02x03' )
>>> arr[1]
23
# Bytearrays can grow and shrink in size:
>>> del arr[1]
>>> arr
bytearray(b' x00x02x03' )
>>> arr. append(42)
>>> arr
bytearray(b' x00x02x03*' )
# Bytearrays can only hold "bytes"
# (integers in the range 0 <= x <= 255)
>>> arr[1] = ' hello'
TypeError: "an integer is required"
>>> arr[1] = 300
ValueError: "byte must be in range(0, 256)"
# Bytearrays can be converted back into bytes objects:
# (This will copy the data)
>>> bytes(arr)
b' x00x02x03*'
```

#### 선택가이드

1. 복합요소를 저장할 것인가?
   1. 가변데이터인가?
      1. 리스트
   2. 불변데이터인가?
      1. 튜플
2. 성능이 중요하며, 단일요소를 저장할 것인가?
   1. 숫자인가?
      1. array.array or Numpy, Pandas 패키지 참고
   2. 유니코드 문자인가?
      1. 불변데이터인가?
         1. str
      2. 가변데이터인가?
         1. 리스트
   3. 싱글바이트 문자인가?
      1. 가변데이터인가?
         1. bytearray
      2. 불변데이터인가?
         1. bytes

일단 그냥 리스트 쓰고, 성능 튜닝 필요하게 되면 가이드대로 수정하자.

### Record, Structs, DTO 구현

#### dict

```python
car1 = {
' color' : ' red' ,
' mileage' : 3812. 4,
' automatic' : True,
}
car2 = {
' color' : ' blue' ,
' mileage' : 40231,
' automatic' : False,
}
# Dicts have a nice repr:
>>> car2
{' color' : ' blue' , ' automatic' : False, ' mileage' : 40231}
# Get mileage:
>>> car2[' mileage' ]
40231
# Dicts are mutable:
>>> car2[' mileage' ] = 12
>>> car2[' windshield' ] = ' broken'
>>> car2
{' windshield' : ' broken' , ' color' : ' blue' ,
' automatic' : False, ' mileage' : 12}
# No protection against wrong field names,
# or missing/extra fields:
car3 = {
' colr' : ' green' ,
174
5.3. Records, Structs, and Data Transfer Objects
' automatic' : False,
' windshield' : ' broken' ,
}
```

#### tuple

index스로만 접근 가능해서 가독성에 안좋다.

```python
# Fields: color, mileage, automatic
>>> car1 = (' red' , 3812. 4, True)
>>> car2 = (' blue' , 40231. 0, False)
# Tuple instances have a nice repr:
>>> car1
(' red' , 3812. 4, True)
>>> car2
(' blue' , 40231. 0, False)
# Get mileage:
>>> car2[1]
40231. 0
# Tuples are immutable:
>>> car2[1] = 12
TypeError:
"'tuple' object does not support item assignment"
# No protection against missing/extra fields
# or a wrong order:
>>> car3 = (3431. 5, ' green' , True, ' silver' )
```

#### 클래스로 정의

```python
class Car:
	def __init__(self, color, mileage, automatic):
	self. color = color
	self. mileage = mileage
	self. automatic = automatic
>>> car1 = Car(' red' , 3812. 4, True)
>>> car2 = Car(' blue' , 40231. 0, False)

# Get the mileage:
>>> car2. mileage
40231. 0
# Classes are mutable:
>>> car2. mileage = 12
>>> car2. windshield = ' broken'
# String representation is not very useful
# (must add a manually written __repr__ method):
>>> car1
<Car object at 0x1081e69e8>
```

#### collections.namedtuple

클래스처럼 재사용 가능한 청사진을 정의할 수 있다.

인덱스로만 접근 가능한 튜플의 단점을 보완한다.

```python
>>> from collections import namedtuple
>>> Car = namedtuple(' Car' , ' color mileage automatic' )
>>> car1 = Car(' red' , 3812. 4, True)
# Instances have a nice repr:
>>> car1
Car(color=' red' , mileage=3812. 4, automatic=True)
# Accessing fields:
>>> car1. mileage
3812. 4
# Fields are immtuable:
>>> car1. mileage = 12
AttributeError: "can' t set attribute"
>>> car1. windshield = ' broken'
AttributeError:
"'Car' object has no attribute 'windshield'"
```

#### typing.NamedTuple

namedtuple 개선판 : 정의하는 문법 개선, 타입힌트 지원

```python
>>> from typing import NamedTuple
class Car(NamedTuple):
	color: str
	mileage: float
	automatic: bool
>>> car1 = Car(' red' , 3812. 4, True)
# Instances have a nice repr:
>>> car1
Car(color=' red' , mileage=3812. 4, automatic=True)
# Accessing fields:
>>> car1. mileage
3812. 4
# Fields are immutable:
>>> car1. mileage = 12
AttributeError: "can' t set attribute"
>>> car1. windshield = ' broken'
AttributeError:
"'Car' object has no attribute 'windshield'"
# Type annotations are not enforced without
# a separate type checking tool like mypy:
>>> Car(' red' , ' NOT_A_FLOAT' , 99)
Car(color=' red' , mileage=' NOT_A_FLOAT' , automatic=99)
```

#### struct.Struct

Serialized C Structs

파이썬 데이터와 C구조체를 파이썬 바이트 객체로 변환: 네트워크에서 들어오거나 파일에 저장된 직렬화 바이너리 데이터 핸들링에 사용할 수 있다.

```python
>>> from struct import Struct
>>> MyStruct = Struct(' i?f' )
>>> data = MyStruct.pack(23, False, 42. 0)
# All you get is a blob of data:
>>> data
b' x17x00x00x00x00x00x00x00x00x00(B'
# Data blobs can be unpacked again:
>>> MyStruct.unpack(data)
(23, False, 42. 0)
```

#### types.SimpleNamespace

리스트와 유사하지만 abc['key']말고 abc.key로 사용할 수 있고 `__repr__`이 잘되어 있다.

```python
>>> from types import SimpleNamespace
>>> car1 = SimpleNamespace(color=' red' ,
. . . mileage=3812. 4,
. . . automatic=True)
# The default repr:
>>> car1
namespace(automatic=True, color=' red' , mileage=3812. 4)
# Instances support attribute access and are mutable:
>>> car1. mileage = 12
>>> car1. windshield = ' broken'
>>> del car1. automatic
>>> car1
namespace(color=' red' , mileage=12, windshield=' broken' )
```

#### 선택가이드

- 필드가 몇개 없다 (2~3개) : 그냥 튜플 쓰자.
- 불변데이터 필드가 필요하다: 튜플, collections.namedtuple, typing.NamedTuple 중에 아무거나 골라 써도 됨
- 필드 이름이 필요하다: collections.namedtuple, typing.NamedTuple
- 그냥 단순한게 좋다: dictionary 쓰자 JSON문법이랑 닮았다.
- 데이터 구조에 대한 제어가 필요하다: 클래스 정의해서 쓰고 @property와 세터 게터
- 오브젝트에 메서드를 추가할 필요가 있다: 클래스 정의해서 쓰거나 collections.namedtuple 나 typeing.NamedTuple를 확장해서 쓰자
- 저장이나 네트워크 전송을위해 공간효율이 필요히다: struct.Struct 사용하자

일반적으로는 그냥 typing.NamedTuple 쓰자

### Sets, Multisets

Set, 집합 = 정렬되지 않은 collection of objects, 중복요소를 허용하지 않는다.

삽입, 삭제, 합집합, 교집합, 멤버쉽테스트

```python
vowels = {'a' ,'e' ,'i' ,'o' ,'u' }
squares = {x * x for x in range(10)}
set1 = set() # ok
set2 = {} # bad
```

#### set

가변데이터

```python
>>> vowels = {' a' , ' e' , ' i' , ' o' , ' u' }
>>> ' e' in vowels
True
>>> letters = set(' alice' )
>>> letters. intersection(vowels)
{' a' , ' e' , ' i' }
>>> vowels. add(' x' )
>>> vowels
{' i' , ' a' , ' u' , ' o' , ' x' , ' e' }
>>> len(vowels)
6
```

#### frozenset

불변데이터

```python
>>> vowels = frozenset({' a' , ' e' , ' i' , ' o' , ' u' })
>>> vowels. add(' p' )
AttributeError:
"'frozenset' object has no attribute 'add'"
# Frozensets are hashable and can
# be used as dictionary keys:
>>> d = { frozenset({1, 2, 3}): ' hello' }
>>> d[frozenset({1, 2, 3})]
'hello'
```

#### collections.Counter

multiset(or bag): 

```python
>>> from collections import Counter
>>> inventory = Counter()
>>> loot = {' sword' : 1, ' bread' : 3}
>>> inventory. update(loot)
>>> inventory
Counter({' bread' : 3, ' sword' : 1})
>>> more_loot = {' sword' : 1, ' apple' : 1}
>>> inventory. update(more_loot)
>>> inventory
Counter({' bread' : 3, ' sword' : 2, ' apple' : 1})
>>> len(inventory)
3 # Unique elements
>>> sum(inventory. values())
6 # Total no. of elements
```

### Stack(LIFO)

Last In First Out

리스트나 배열과 다르게 랜덤 접근 불가

Insert = Push, Delete = Pop

#### list

append = push, pop = pop

```python
>>> s = []
>>> s. append(' eat' )
>>> s. append(' sleep' )
>>> s. append(' code' )
>>> s
[' eat' , ' sleep' , ' code' ]
>>> s. pop()
'code'
>>> s. pop()
'sleep'
>>> s. pop()
'eat'
>>> s. pop()
IndexError: "pop from empty list"
```

#### collections.deque

빠르고 견고한 스택

```python
>>> from collections import deque
>>> s = deque()
>>> s. append(' eat' )
>>> s. append(' sleep' )
>>> s. append(' code' )
>>> s
deque([' eat' , ' sleep' , ' code' ])
>>> s. pop()
'code'
>>> s. pop()
'sleep'
>>> s. pop()
'eat'
>>> s. pop()
IndexError: "pop from an empty deque"
```

#### queue.LifoQueue

병렬컴퓨팅의 잠금체계에 유용함

```python
>>> from queue import LifoQueue
>>> s = LifoQueue()
>>> s. put(' eat' )
>>> s. put(' sleep' )
>>> s. put(' code' )
33 cf. Python Docs: “queue.LifoQueue”
192
5.5. Stacks (LIFOs)
>>> s
<queue. LifoQueue object at 0x108298dd8>
>>> s. get()
'code'
>>> s. get()
'sleep'
>>> s. get()
'eat'
>>> s. get_nowait()
queue. Empty
>>> s. get()
# Blocks / waits forever.. .
```

앵간하면 스택이 필요시 collections.deque 사용할 것

### Queue(FIFO)

First in First Out 랜덤억세스 불가

#### list

겁나 느린 큐 - 쓰지말자

```python
>>> q = []
>>> q. append(' eat' )
>>> q. append(' sleep' )
>>> q. append(' code' )
>>> q
[' eat' , ' sleep' , ' code' ]
# Careful: This is slow!
>>> q. pop(0)
'eat'
```

#### collections.deque

빠르고 견고한 큐

```python
>>> from collections import deque
>>> q = deque()
>>> q. append(' eat' )
>>> q. append(' sleep' )
>>> q. append(' code' )
>>> q
deque([' eat' , ' sleep' , ' code' ])
>>> q. popleft()
'eat'
>>> q. popleft()
'sleep'
>>> q. popleft()
'code'
>>> q. popleft()
IndexError: "pop from an empty deque"
```

#### queue.Queue

병렬컴퓨팅에 락킹을 위한 큐 - 병렬처리할일이 잘 없다

```python
>>> from queue import Queue
>>> q = Queue()
>>> q. put(' eat' )
>>> q. put(' sleep' )
>>> q. put(' code' )
>>> q
<queue. Queue object at 0x1070f5b38>
>>> q. get()
'eat'
>>> q. get()
'sleep'
>>> q. get()
'code'
>>> q. get_nowait()
queue. Empty
>>> q. get()
# Blocks / waits forever.. .
```

#### multiprocessing.Queue

Shared Job Que

멀티 프로세서들에게 일을 분배해기 쉽게 한다.

```python
>>> from multiprocessing import Queue
>>> q = Queue()
>>> q. put(' eat' )
>>> q. put(' sleep' )
>>> q. put(' code' )
>>> q
<multiprocessing. queues. Queue object at 0x1081c12b0>
>>> q. get()
'eat'
>>> q. get()
'sleep'
>>> q. get()
'code'
>>> q. get()
# Blocks / waits forever.. .
```

### Priority Queues

우선순위큐

key의 우선순위에 따라 우선순위가 높은 값을 먼저 가져온다.

#### list

그닥 노권장 느림

```python
q = []
q. append((2, ' code' ))
q. append((1, ' eat' ))
q. append((3, ' sleep' ))
# NOTE: Remember to re-sort every time
# a new element is inserted, or use
# bisect.insort().
q.sort(reverse=True)
while q:
	next_item = q. pop()
	print(next_item)
# Result:
# (1, 'eat')
# (2, 'code')
# (3, 'sleep')
```

#### heapq

```python
import heapq
q = []
heapq.heappush(q, (2, ' code' ))
heapq.heappush(q, (1, ' eat' ))
heapq.heappush(q, (3, ' sleep' ))
while q:
	next_item = heapq.heappop(q)
	print(next_item)
# Result:
# (1, 'eat')
# (2, 'code')
# (3, 'sleep')
```

#### queue.PriorityQueue

```python
from queue import PriorityQueue
q = PriorityQueue()
q. put((2, ' code' ))
q. put((1, ' eat' ))
q. put((3, ' sleep' ))
while not q. empty():
	next_item = q. get()
	print(next_item)
# Result:
# (1, 'eat')
# (2, 'code')
# (3, 'sleep')
```

lock 오버헤드가 싫으면 heapq 를 쓰고 그게 아니면 일반적으로 그냥 queue.PriorityQueue를 쓰자

## Ch6. 반복&Iteration

### 파이썬다운 Loop

```python
my_items = ['a' ,'b' ,'c' ]

i = 0
while i < len(my_items):
	print(my_items[i])
	i += 1
    
for i in range(len(my_items)):
	print(my_items[i])
    
for item in my_items:
	print(item)
    
for (int i = a; i < n; i += s) {
// . ..
}

for i in range(a, n, s): # start, stop, step
# .. .
```

리스트

```python
>>> for i, item in enumerate(my_items):
. . . print(f' {i}: {item}' )
0: a
1: b
2: c
```

딕셔너리

```python
>>> emails = {
. . . ' Bob' : ' bob@example. com' ,
. . . ' Alice' : ' alice@example. com' ,
. . . }
>>> for name, email in emails. items():
. . . print(f' {name} -> {email}' )
'Bob -> bob@example.com'
'Alice -> alice@example. com'
```

### comprehensions

리스트 (순서가 있음)

```python
values = [expression for item in collection]

values = []
for item in collection:
	values.append(expression)

>>> squares = [x * x for x in range(10)]

>>> squares = []
>>> for x in range(10):
. . . squares.append(x * x)
```

리스트 조건문추가

```python
values = [expression for item in collection	if condition]

values = []
for item in collection:
	if condition:
		values. append(expression)

even_squares = []
for x in range(10):
	if x % 2 == 0:
		even_squares. append(x * x)

>>> even_squares = [x * x for x in range(10) if x % 2 == 0]
>>> even_squares
[0, 4, 16, 36, 64]
```

집합 (순서가 없음)

```python
squares = {x * x for x in range(-9,10)}
```

딕셔너리

```python
>>> { x: x * x for x in range(5) }
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### 리스트분할 및 콜론

```python
>>> lst = [1, 2, 3, 4, 5]
# lst[start:end:step]
>>> lst[1: 3: 1]
[2, 3]
>>> lst[: : 2]
[1, 3, 5]
>>> numbers[: : -1]
[5, 4, 3, 2, 1]
>>> lst = [1, 2, 3, 4, 5]
>>> del lst[:] # lst.clear()
>>> lst
[]

# referenc copy
>>> original_lst = lst
>>> lst[: ] = [7, 8, 9]
>>> lst
[7, 8, 9]
>>> original_lst
[7, 8, 9]
>>> original_lst is lst
True

# shallow copy
>>> copied_lst = lst[: ]
>>> copied_lst
[7, 8, 9]
>>> copied_lst is lst
False

```

### Iterator & Generators

아래는 그냥 교육적인 목적이고, 실지로는 이렇게 잘 안만들 쓴다.

왜냐, generator랑 yield로 더 쉽게 만들 수 있기 때문.

[https://hiddentrap.tistory.com/149](https://hiddentrap.tistory.com/149)

looping 가능한 객체: `__iter__`와 `__next__`구현 필요

실제로는, Iterator를 만들려면 클래스 기반으로 `__iter__`와 `__next__`, StopIteration 프로토콜을 구현하면 되는데, 이를 함수 기반으로 yield를 이용한 Iterator생성 방법인 Generator를 사용한다. Generator는 함수의 실행흐름이 종료되면 StopIteration 예외를 발생시킨다.

"**Generator  produce a sequence of results while a regular function produces a single return value**"

yiedl: 함수에서 실행을 일시정지 시켜놓고 값을 caller한테 돌려준다.

```python
class BoundedRepeater:
    def __init__(self, value, max_repeats):
        self.value = value
        self.max_repeats = max_repeats
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.max_repeats:
            raise StopIteration
        self.count += 1
        return self.value
    
def bounded_repeater(value, max_repeats):
    count = 0
    while True:
        if count >= max_repeats:
            return
        count += 1
        yield value
        
def bounded_repeater(value, max_repeats):
    for i in range(max_repeats):
        yield value

```

`__iter__`: 초기값 세팅하고 return 으로 자기 자신

`__next__`: 이터레이션시 리턴 값 구현 및 이터레이션 끝에서 rais StopIteration

yield: return 처럼 caller에 값을 넘겨주지만 return 은 실행시점에 callee의 상태값을 모두 날려 버린다. 하지만 yield 실행 시점에 callee의 상태값과 실행중인 포인트를 임시로 저장해놓는다.

**1. 이터레이터와 제네레이터**

PS, 이터레이션이 가능한 객체란, for item in items: 구문에 사용할 수 있는 items

**1.1 이터레이터 (클래스)**

이터레이션이 가능한 객체 생성용 클래스 : **__iter__** (초기값 세팅용으로 self 리턴), **__next__**(이터레이션시 리턴 값)을 구현하는 클래스로 이터레이션 끝에 도달하면 **raise StopIteration** 으로 예외 발생시켜주면 됨

**1.2 제네레이터 (함수)**

이터레이터 만들려면 귀찮으니까 좀 더 편하게 이터레이션이 가능한 객체를 만들어주는 함수 : yield 를 하나 이상 사용하면 제네레이터임. yield 는 return 하고 똑같이 값을 리턴해주는데 차이점은 return은 해당 시점에서 함수 실행을 끝내 버리지만 **yield는 해당 시점에 값을 리턴할뿐 객체와 상태값을 유지**하고 있음.

**1.3 제네레이터 함수 표현식** : 익명함수 처럼 쓰는법

my_list = [1, 3, 6, 10]
a = (x**2 for x in my_list) // a는 이터레이션 가능 객체가 됨

sum(x**2 for x in my_list) // 이런식으로 함수 안에서도 사용 가능

**1.4 제네레이터 장점**: 이터레이터 클래스 정의보다 간편(코드가 짧다)하고 효율적(리스트 마냥 전체 데이터를 메모리에 올려놓을 필요 없이 그때 그때 필요한 데이터 하나만 올려 놓는다)임

### Generator 표현식

my_list = [1, 3, 6, 10]
a = (x**2 for x in my_list) // a는 이터레이션 가능 객체가 됨

sum(x**2 for x in my_list) // 이런식으로 함수 안에서도 사용 가능

Generator 표현식과 List 컴플리헨션과 차이점

- 모든데이터를 다 만들어 놓지 않고 필요 시점에 하나씩만 만든다
- 리턴이 리스트가 아니고 제네레이터 객체이다.
- next()로 제네레이터를 호출해줘야 값이 생성된다. next(a)
- list()로 리스트 겍체로 변환할 수 있다.
- 제네레이터는 한반 사용되면 다시 시작하거나 재사용될 수 없으므로 다시 생성해서 사용해야 한다.

```python
genexpr = (expression for item in collection if condition)

def generator():
    for item in collection:
        if condition:
            yield expression
```

이런식으로도 사용가능

```python
for x in ('Bom dia' for i in range(3)):
    print(x)
    
sum((x * 2 for x in range(10)))
90
```

### Iterator 체인

Iterator Chain = 중첩 제네레이터 = pipeline in unix

## Ch7. Dictionary Trick

### Dictionary.get(key,default)

EAFP: 허락보다 용서가 쉽다 코딩 스타일 ㅋㅋㅋ : 파이썬 스타일

- 오류 코드를 사용하는 예외가 없으면 오류 처리를 논리의 기본 흐름에 직접 포함시켜야 한다.
- 예외로 인해 메인 플로우가 중단되므로 예외적인 경우가 아닌 로컬로 처리를 할 수 있다.
- EAFP와 결합된 예외는 오류 코드 예외를 쉽게 무시할 수 없기 때문에 우수하다.

검사를 수행하지 않고 일단 실행하고 예외처리를 진행

LBYL: 도약하기전에 확인해라 코딩 스카일ㅋㅋㅋ

실행하기전에 에러가 날만한 요소들을 조건절로 검사하고 수행

```python
# Bad code LBYL
def greeting(userid):
    if userid in name_for_userid:
        return 'Hi %s!' % name_for_userid[userid]
    else:
        return 'Hi there!'
    
# Good code EAFP
def greeting(userid):
    try:
        return 'Hi %s!' % name_for_userid[userid]
    except KeyError:
        return 'Hi there'
    
# BEST code Dictionary.get(key,default value)
def greeting(userid):
    return 'Hi %s!' % name_for_userid.get(userid, 'there')
```

### Dict 정렬

key로 정렬: sorted(dict.items())

value로 정렬: sorted(dict.items(), key=lambda x: x[1])

역정렬: sorted( , ,reverse = True)

### Switch/Case 따라하기

```python
if cond == 'cond_a':
	handle_a()
elif cond == 'cond_b':
    handle_b()
else:
    handle_default()
    

func_dict = {
    'cond_a' : handle_a,
    'cond_b' : handle_b,
}

func_dict.get(cond, handle_default)()


def func_dict(cond):
    return {
        'cond_a': handle_a,
        'cond_b': handle_b,
    }.get(cond, lambda: None)()
func_dict(cond)

def dispatch_dict(opr, x, y):
    return{
        'add': lambda: x+y,
        'sub': lambda: x-y,
        'mul': lambda: x*y,
        'div': lambda: x/y,
    }.get(opr, lambda:None)()
dispatch_dict('mu',2,8)

#프로덕션 레벨에선 위 코드를 실행할때마다 lambda 함수들이 임시로 생성되기 때문에 미리 상수로 생성해놓을 필요가 있다.

```

### Dict 합치기

```python
xs = {'a':1, 'b':2}
ys = {'b':3, 'c':4}

zs = {}
zs.update(xs)
zs.update(ys)

zs = {**xs, **ys} # 이게 더 빠르고 좋음
```

### Dict Printing

```python
>>> mapping = {'a' : 23, 'b' : 42, 'c' : 0xc0ffee}
>>> str(mapping)
{'b' : 42, 'c' : 12648430, 'a' : 23}


import json
json.dumps(mapping, indent=4, sort_keys=True)
{
"a": 23,
"b": 42,
"c": 12648430
}
# 단점은 primitive type만 된다 딴거 껴있으면 에러
# 복합구조도 안됨

# 그래서 결론은, 
import pprint
pprint.pprint(mapping)
```

