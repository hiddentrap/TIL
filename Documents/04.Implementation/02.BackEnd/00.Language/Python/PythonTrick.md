# Python Trick

[정리필요](https://dailyheumsi.tistory.com/224?category=855210)

## Ch2.

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



## Ch3.

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

