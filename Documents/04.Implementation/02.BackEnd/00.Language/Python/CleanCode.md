# Clean Code

클린 코드는 프로그래밍 언어 구분 없이 일반적으로 존재하는 개념인데, 파이썬에서는 좀 특이한 관습이 있다. '파이썬스럽게(Pythonic)' 라는 것인데, 이 때문에 같은 개념과 논리더라도 다른 프로그래밍 언어와는 클린 코드에 대한 구현이 조금 다르다.

그래서 이 책에서는 두 가지를 말한다. **파이썬스러운 코드와 이를 기반으로 한 클린 코드를 짜는 것.**
클린 코드에 대한 여러 서적들이 있지만 이 책을 먼저 잡은 이유도 이 때문이다. 클린 코드의 개념을 잘 알면서, 이를 파이썬스럽게 짤 수 있는 능력, 하다 못해 그럴 수 있는 '감'이라도 잡고 싶었다.

정리하는 글은 책의 목차를 그대로 따라가지 않는다. 위에 설명한 두 가지에 초점을 두어 내 나름대로 정리했다.
예제도 책이랑 일부 다르다. 직관적인 예제로 직접 재구성했다.
한편, 적지 않은 글들이 책에는 없는 내 생각의 글들이다. 따라서 틀릴 수 있다.
이 글을 읽는 사람은 어느 정도 파이썬을 써본 사람이라고 생각하고 글을 썼다.

그리고 파이썬스러운 코드가 무엇이고, 그 안에 내재된 파이썬의 문법 컨셉을 알아본다.
그다음으로 클린 코드에 대해 알아가며, 이를 어떻게 파이썬스럽게 구현해나가는지 알아본다.

------

# 파이썬스러운 코드

## 파이썬스럽다는 것

각 프로그래밍 언어마다 특정 작업을 수행하기 위해 해당 작업을 처리하는 고유한 기능 혹은 관용구를 가지고 있다. 이러한 기능과 관용구를 사용하는 이유는 일반적으로 더 나은 성능을 내기 때문이다. 코드도 더 줄일 수 있고, 이해하기도 더 쉽다.
이렇게 **파이썬의 고유한 기능과 관용구를 따르는 코드를 파이썬스럽다(Pythonic) 라고 한다.**
예를 들어 List comprehension 은 대표적인 파이써닉한 코드이다.

```
arr = [1, 2, 3, 4]

# 파이썬스럽지 않은 코드
result = []
for i in range(len(arr)):
    if arr[i] % 2 == 1:
        result.append(arr[i])

# 파이썬스러운 코드 (List comprehension 을 사용)
result = [num for num in arr if num % 2]
```

**파이썬스러운 코드로 훨씬 빠르고, 간결하고, 심플하며, 읽기 좋은 코드를 구현할 수 있다.**
이게 아직 간결하고 심플하게 느껴지지 않는다면, 아직 파이썬에 익숙해져있지 않다는 의미다.
파이썬을 계속해서 쓰다 보면 이런 식의 파이써닉한 코드에 적응하고 추구하게 된다.

파이썬스럽게 코딩하는 예제는 구글링 해보면 많이 있다.
대표적으로, 아래 링크에서 확인해볼 수 있다.

> **파이썬스러운 코드 작성을 위한 참고 링크들**
>
> - [이전 글 - 파이썬을 파이썬 답게. (코딩 문제편)](https://dailyheumsi.tistory.com/31)
> - [파이썬을 여행하는 히치하이커를 위한 안내서 - 코드 스타일](https://python-guide-kr.readthedocs.io/ko/latest/writing/style.html)
> - [책, 파이썬답게 코딩하기](http://www.yes24.com/Product/Goods/60493752)
> - [파이콘 2018 - Pythonic code가 과연 효율적일까? [안주은님\]](https://www.youtube.com/watch?v=Txz7K6Zc-_M&feature=youtu.be)

**이 글에서는 파이썬의 문법 컨셉을 다루며, 사용자가 파이썬스럽게 사용할 수 있도록 클래스를 설계하는 방법을 배운다.**
이 과정에서, 그저 사용하기만 하던 파이썬의 다양한 기능들이 어떻게 수행되는지 등을 알게 될 것이다.

##  

## 파이썬 문법 컨셉

### 1. 첨자형 객체

```
arr = [1, 2, 3, 4]

# 파이썬스럽지 않은 코드
last = arr[len(arr)-1]  # 4

# 파이썬스러운 코드
last = arr[-1]  # 4
odds = arr[::2]  # [1, 3]
evens = arr[1::2]  # [2, 4]
sliced = arr[2:4]  # [3, 4]
reverse = arr[::-1]  # [4, 3, 2, 1]
```

위와 같이 파이썬의 인덱스와 슬라이스 기능을 잘 사용하면 보다 파이써닉한 코드가 된다.
인덱스와 슬라이스 기능은 다음의 매직 메서드 덕분에 동작한다.

- `__getitem__`

**이 메서드를 구현한 객체를 첨자형 객체라고 한다.** 즉, `[]` 로 데이터에 접근할 수 있도록 설계한 객체다.
예를 들면 리스트(`List`) 나 사전(`Dict`) 이 첨자형 객체다.
만약 내가 설계하는 클래스에 위와 같은 인덱스와 슬라이스 기능을 넣고 싶다면 이 매직 메서드를 정의해주면 된다.
예를 들면 다음과 같다.

```
class Bag:
    def __init__(self, item_size, user):
        self._items = [None] * item_size
        self._item_cnt = 0

    def add_item(self, item):
        self._items[self._item_cnt] = item
        self._item_cnt += 1

    def __getitem__(self, index):
        return self._items[index]
>>> bag = Bag(10, "heumsi")
>>> bag.add_item("음료수")
>>> bag.add_item("김밥")
>>> bag[0] 
음료수
>>> bag[1]
김밥
>>> bag[2]
None
```

###  

### 2. 컨텍스트 관리자

```
# 파이썬스럽지 않은 코드
db_connector = DBConnector(id='id', password='password')
db_connector.connect()
... 
db_connector.close()

# 파이썬스러운 코드
with DBConnector(id='id', password='password') as db_connector:
    ...
```

파이썬에서 `with A as a: ...` 문법은 어떤 코드의 시작과 끝에 어떤 동작을 일정하게 취해주어야 할 때 사용된다.
예를 들어, 파일을 열고 닫거나 데이터베이스의 연결을 열고 닫는 등의 동작이 그렇다.
`with A as a: ...` 구문을 사용하려면 아래 두 메서드를 구현해야 한다.

- `__enter__(self)`

- ```
  __exit__(self, ex_type, ex_value, ex_traceback)
  ```

  - `ex_type, ex_value, ex_traceback` 는 예외가 발생한 경우에 받아오는 값이다.
  - 반환 값이 `None` 이 아니면 예외를 발생시킨다.

**이 두 메서드를 구현한 객체를 컨텍스트 관리자**라고 한다.
예를 들어 위의 `DBConnector` 는 내부적으로 다음과 같이 구현되어 있다.

```
class DBConnector:
    def __init__(self, id, password):
        print("1. DBConnector.__init__")

    def connect(self):
        print("3. DBConnector.connect")

    def close(self):
        print("6. DBConnector.close")

    def __enter__(self):
        print("2. DBConnector.__enter__")
        self.connect()

    def __exit__(self, ex_type, ex_value, ex_traceback):
        print("5. DBConnector.__exit__", end=" / ")
        print(f"ex_type : {ex_type}, ex_value: {ex_value}, exc_tb: {ex_traceback}")
        self.close()
>>> with DBConnector(id="id", password="password") as db_connector:
>>>     print("4. DB 연결 이후 할 일")
1. DBConnector.__init__
2. DBConnector.__enter__
3. DBConnector.connect
4. DB 연결 이후 할 일
5. DBConnector.__exit__ / ex_type : None, ex_value: None, exc_tb: None
6. DBConnector.close
```

한편, 클래스가 아닌 함수에 적용할 경우가 있다.
이럴 때는 **`contextlib.ContextDecorator` 를 상속받은 클래스를 데코레이터로 사용하여 적용할 수 있다.**
예를 들면, 함수의 시간을 측정하는 데코레이터를 다음과 같이 만들 수 있다.

```
import time
import contextlib

class Timer(contextlib.ContextDecorator):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.end = time.time()
        operation_time = self.end - self.start
        print(f"{self.name}의 수행시간 : {operation_time}")

@Timer("a()")
def a():
    return [i for i in range(1000000)]

@Timer("b()")
def b():
    result = []
    for i in range(1000000):
        result.append(i)
>>> a()
a()의 수행시간 : 0.07170891761779785
>>> b()
b()의 수행시간 : 0.12720584869384766
```

여담이지만, 리스트 컴프리헨션으로 짠 코드가 그렇지 않은 코드보다 수행 시간이 훨씬 빠르다는 걸 알 수 있다.
성능적으로도 파이썬스러운 코드를 써야 하는 이유다.

###  

### 3. 밑줄과 프로퍼티

##### 1) 밑줄(_)로 private 표현

```
# 파이썬스럽지 않은 코드
class A:
    def __init__(self, private_var):
        self.private_var = private_var

    def private_method(self):
        pass

# 파이썬스러운 코드
class A:
    def __init__(self, private_var):
        self._private_var = private_var

    def _private_method(self):
        pass
```

파이썬에는 자바에서 등장하는 `public` 이나 `private` 등의 접근 제어자가 문법적으로 없다.
다만 밑줄( `_`) 을 써서, `private` 을 표현한다.
표현한다고 한 것은, 말 그대로 파이썬 개발자들 간의 관습적인 표현이지, 문법적인 것은 아니다.
**따라서 `_` 로 시작하는 속성에 접근할 수 있다. 다만 접근하지 말라고 명시적으로 표현한 것이다.**

객체의 인터페이스로 공개하는 용도가 아니라면, 모든 멤버에 접두사로 `_` 를 달아주는 것이 좋다.

> **[`_` 의 또 다른 의미]**
>
> 파이썬에서 종종 다음과 같은 코드를 볼 때가 있을 것이다.
>
> ```
> def get_two_values():
>   return 1, 2
> 
> a, _ = get_two_values()
> ```
>
> 이때 `_` 는 사용되지 않는 변수의 이름으로 사용된다.
> 즉, 위 함수가 반환하는 값 중 두 번째 값은 현재 로직에 필요 없음을 나타내는 것이다.

> **[`__` 은 뭘까?]**
>
> 파이썬에서 변수나 클래스 메서드 이름 앞에 밑줄 두 개 ( `__`) 를 붙이는 코드를 볼 때가 있다.
> 이는 네임 맹글링 (Name Mangling) 으로 불리며, 조금 특별한 효과를 불러일으킨다.
> 다음 예를 보자.
>
> ```
> class Foo:
>  def __init__(self):
>      self.__bar = 42
> >>> foo = Foo()
> >>> print(foo.__bar)
> Traceback (most recent call last):
> File "<stdin>", line 1, in <module>
> AttributeError: 'Foo' object has no attribute '__bar'
> >>> print(foo._Foo__bar)
> 42
> ```
>
> 보다시피 `__bar` 는 `_Foo__bar` 가 되었다.
> 이처럼 네임 맹글링(`__` 을 붙이는 것)은 변수의 이름 앞에 클래스의 이름을 붙여준다.
> 이는 여러 번 확장되는 클래스의 메서드를 이름 충돌 없이 오버라이드 하기 위해 만들어졌다.
>
> 이러한 네임 맹글링을 통해 접근 제어자 private 의 효과를 본다고 생각하여, `_` 대신 `__` 을 사용하여 변수를 사용하는 코드들이 일부 있다. 하지만 이런 목적으로 네임 맹글링을 사용하는 것은 일부 부작용 효과를 불러일으키기 때문에 권장되지 않는다.
>
> **private 를 표현하고 싶다면 `_` 만 사용하자. 애초에 파이썬은 접근 제어자를 강제하는 철학을 가지고 있지 않다.**
>
> 참고: [Python Name Mangling and How to Use Underscores](https://medium.com/analytics-vidhya/python-name-mangling-and-how-to-use-underscores-e67b529f744f)

#####  

##### 2) g(s)etter 대신 프로퍼티 사용

```
# 파이썬스럽지 않은 코드
class User:
    EMAIL_FORMAT = re.compile(r"[^@]+@[^@]+[^@]+")

    def __init__(self, username):
        self.username = username
        self._email = None

    def get_email(self):
        return self._email

    def set_email(self, new_email):
        if not self._is_valid_email(new_email):
            print("유효한 이메일이 아닙니다.")
            return
        self._email = new_email

    def _is_valid_email(self, email):
        return re.match(self.EMAIL_FORMAT, email) is not None
>>> user = User("heumsi")
>>> user.set_email("heumsi")
유효한 이메일이 아닙니다.
>>> user.get_email()
None
>>> user.set_email("heumsi@naver.com")
>>> user.get_email()
heumsi@naver.com
```

**파이썬은 자바에서 흔히 보이는 `getter` 와 `setter` 의 철학을 가지지 않는다.**
애초에 private 과 같은 접근제어자가 없는 맥락과 마찬가지.
다만, `@property` 와 `@.setter` 라는 어노테이션을 통해 `getter` 와 `setter` 의 역할을 대신한다.

```
# 파이썬스러운 코드
import re

class User:
    EMAIL_FORMAT = re.compile(r"[^@]+@[^@]+[^@]+")

    def __init__(self, username):
        self.username = username
        self._email = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if not self._is_valid_email(new_email):
            print("유효한 이메일이 아닙니다.")
            return
        self._email = new_email

    def _is_valid_email(self, email):
        return re.match(self.EMAIL_FORMAT, email) is not None
>>> user = User("heumsi")
>>> user.email = "heumsi"
유효한 이메일이 아닙니다.
>>> user.email
None
>>> user.email = "heumsi@naver.com"
>>> user.email
heumsi@naver.com
```

`@property` 와 `.setter` 는 어떤 특별한 처리를 해야하는 경우에 활용한다.
단순히 값을 받아오거나 세팅하는 경우에는, 바로 멤버 변수로 바로 접근하여 처리하는 게 일반적이다.

###  

### 4. 반복과 관련된 객체

파이썬에서는 기본적으로 반복 가능한 객체들이 있다. 리스트나 튜플, 세트 등이 그런 것들이다. 이러한 객체들은 `for` 와 같은 루프 문을 통해 값을 반복적으로 가져올 수 있다.

파이썬에서 `for i in A` 반복문에서 `A` 가 될 수 있는 객체는 크게 2가지 있다.

- 이터러블 객체

  - `__iter__` 메서드를 구현한 객체다.

  - ```
    __iter__
    ```

     

    메서드는 이터레이터 객체를 반환한다.

    - 이터레이터 객체

      는

       

      ```
      __next__
      ```

       

      를 구현한 객체다.

      - `__next__` 는 반복 요소를 다음으로 이동시키고 기존의 값을 반환한다.

    - 이터레이터의

       

      ```
      __next__
      ```

       

      함수가,

       

      ```
      yield
      ```

       

      문을 사용하는 경우가 있는데, 이를

       

      제너레이터

      라고 한다.

      - `return` 을 사용하지 않고 `yield` 를 사용한다.
      - `yield` 는 어떤 값을 내보낸 뒤, 해당 함수가 다시 호출될 때까지 `yield` 그 자리에서 대기한다.

- 시퀀스 객체

  - `__len__`, `__getitem__` 메서드를 구현한 객체다.
  - 첫번째 인덱스 0부터 시작하여 포함된 요소를 한 번에 하나씩 차례로 가져올 수 있어야 한다.

 

파이썬 인터프리터가 반복문을 만나면 어떤 과정을 밟는지 살펴보자.
먼저 `for i in A` 와 같은 코드를 만나면 `A` 라는 객체가 이터러블 객체인지, 그리고 시퀀스 객체인지 순서대로 확인한다.

- 만약 이터러블 객체라면,

   

  ```
  __iter__
  ```

   

  를 호출하고, 이터레이터 객체를 반환받는다.

  - 그리고 이터레이터의 `__next__` 를 매 루프마다 호출한다.
  - `StopIteration` 을 반환하면 멈춘다.

- 만약 시퀀스 객체라면,

   

  ```
  __getitem__
  ```

   

  을 호출한다.

  - `IndexError` 가 발생할 때까지 인덱스를 증가시키며 반복적으로 호출한다.

- 둘 다 아니라면 `TypeError` 를 발생한다.

당장 이해가지 않아도 상관없다. 아래서 직접 이터러블과 시퀀스 객체를 만드는 예제를 보면 쉽게 이해할 수 있을 것이다.

##### 1) 이터러블 객체 만들기

```
from datetime import timedelta, date

class DateRangeIterable:
    """
    이 클래스는 __iter__ 와 __next__ 를 동시에 구현하고 있으므로,
    이터러블 객체이자, 이터레이터 객체다.
    """
    def __init__(self, start_date, end_date):
        print("__init__")
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        print("__iter__")
        return self

    def __next__(self):
        print("__next__")
        if self._present_day >= self.end_date:
            raise StopIteration
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today
>>> for day in DateRangeIterable(date(2019, 1, 1), date(2019, 1, 5)):
>>>    print(day)
__init__
__iter__
__next__
2019-01-01
__next__
2019-01-02
__next__
2019-01-03
__next__
2019-01-04
__next__
```

> **[이터러블, 이터레이터, 제너레이터]**
>
> 이 세 가지 개념이 매우 헷갈릴 수 있다. 따라서 잠깐 정리하고 가려고 한다.
> **이터러블은 `__iter__` 를 구현하여 반복 구문을 사용할 수 있게 정의한 객체다.** 즉 `for i in A: ...` 구문을 쓸 수 있도록 하는 객체다.
> (시퀀스 객체로도 가능하지만, 일반적으로 반복을 기대한다면 이터러블 객체가 맞다.)
> `__iter__` 는 이터레이터를 반환해야 한다.
>
> **이터레이터는 `__next__` 를 구현하여 한 번에 하나씩의 값을 생산하는 로직을 정의한 객체**다.
> 이터러블에서 쓰이지만, 이터러블 그 자체는 아니다. 예를 들어 다음 코드를 보자.
>
> ```
> class SequenceIterator:
>  def __init__(self, start=0, step=1):
>      self.current = start
>      self.step = step
> 
>  def __next__(self):
>      value = self.current
>      self.current += self.step
>      return value
> ```
>
> 위 객체는 이터레이터(`__next__` 가 존재)지만 이터러블은 아니다. (`__iter__` 가 없기 때문)
> 다만 위가 일반적인 경우는 아니고, 보통은 객체에 이터러블과 이터레이터 둘 다 구현한다.
>
> **제너레이터는 `yield` 문을 포함하고 있는 함수다.**
> 즉 위의 객체에서 `__next__` 가 `return value` 가 아니라 `yield value` 가 되면, `__next__` 함수는 제너레이터 된다.
> 제너레이터를 호출하면 제너레이터의 인스턴스를 만든다. 다음의 예를 통해 확인할 수 있다.
>
> ```
> def test_a():
>     for i in range(10):
>         yield i
> 
> >>> test_a()
> >>> <generator object test_a at 0x1096c8550>
> ```
>
> 이를 제너레이터 인스턴스라고 하는데, 이는 이터러블이자 이터레이터 객체다. (함수를 호출했는데 객체가 반환되었다. 굉장히 이상해 보일 수 있는데, 파이썬에서 제너레이터를 약간 특수하게 소개하는 이유이기도 한 것 같다.)
> 따라서, 이 인스턴스를 가지고 반복문을 돌릴 수 있다!
> 제너레이터는 미리 값을 생성하지 않기 때문에(Lazy), 보통 메모리를 절약하기 위해 사용된다.

#####  

##### 2) 시퀀스 객체 만들기

```
class DateRangeSequence:
    """
    이 클래스는 __getitem__ 과 __len__ 을 구현하고 있으므로
    시퀀스 객체이다.
    """
    def __init__(self, start_date, end_date):
        print("__init__")
        self.start_date = start_date
        self.end_date = end_date
        self._range = self._create_range()  # 시퀀스 객체는 이처럼 미리 메모리와 반복될 값들을 초기화한다.

    def _create_range(self):
        print("_create_range")
        days = []
        current_day = self.start_date
        while current_day < self.end_date:
            days.append(current_day)
            current_day += timedelta(days=1)
        return days

    def __getitem__(self, day_no):
        print(f"__getitem__({day_no})")
        return self._range[day_no]

    def __len__(self):
        print("__len__")
        return len(self._range)
>>> for day in DateRangeSequence(date(2019, 1, 1), date(2019, 1, 5)):
>>>     print(day)
__init__
_create_range
__getitem__(0)
2019-01-01
__getitem__(1)
2019-01-02
__getitem__(2)
2019-01-03
__getitem__(3)
2019-01-04
__getitem__(4)
```

> **[이터러블 객체와 시퀀스 객체의 트레이드 오프]**
>
> 이터러블은 매 루프마다 하나의 값만 반환하며 반복하는 반면,
> 시퀀스는 루프 초기에 반복해야 하는 모든 값을 미리 만들어둔 뒤 반복한다.
>
> 즉, 이터러블의 경우 메모리를 한번에 쓰지 않지만, 시퀀스는 메모리를 한 번에 쓰는 단점이 있다.
> 하지만, 이터러블은 특정 인덱스에 접근하는데 O(n) 만큼 걸리고, 시퀀스는 O(1) 만 걸리므로 속도면에서 빠르다.
>
> 이는 일반적인 컴퓨터 공학에서의 '공간(메모리)- 시간' 의 트레이드 오프적 관계다.

###  

### 5. 컨테이너 객체

**컨테이너 객체는 `in` 이라는 파이썬 문법에서 사용되는 객체로 다음 매직 메서드를 구현한 객체**다.

- `__contains__`

즉 아래 두 문장은 같은 문장이다.

```
element in container
container.__contains__(element)
```

어떤 객체를 컨테이너 객체로 잘 설계하면 훨씬 가독성이 좋다.
예를 들어, 다음과 같은 코드가 있다고 해보자.

```
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

...
if 0 <= coord.x <= 100 and 0 <= coord.y <= 100:
    ...
```

위 코드에서 `if` 구문은 보기에 조금 난잡하다.
다음과 같이 파이썬스럽게 설계하면 훨씬 보기 좋아진다.

```
class Grid:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __contains__(self, grid):
        if grid.x_min <= self.x <= grid.x_max and grid.y_min <= self.y <= grid.y_max

...
grid = Grid(0, 100, 0, 100)
if coord in grid:
      ...
```

###  

### 6. 객체의 동적인 속성

파이썬에서 `myObject.attribute` 와 같이 객체의 속성을 호출하는 경우, 다음의 과정을 거친다.

- `myObject.attribute` 호출

- ```
  __getattribute__
  ```

   

  호출

  - `attribute` 가 객체의 `__dict__` 에 없는 경우 `__getattr__` 를 호출한다.

```
class MyClass:
    def __init__(self, attribute):
        self.attribute = attribute

    def __getattribute__(self, item):
        print(f"__getattribute__({item})")
        return super().__getattribute__(item)

    def __getattr__(self, attribute):
        print(f"__getattr({attribute})")
        if attribute.startswith("fallback_"):
            name = attribute.replace("fallback_", "")
            return f"{name} 란 속성은 없습니다."
        raise AttributeError
>>> my_class = MyClass("hi~")
>>> my_class.attribute
__getattribute__(attribute)
hi~
>>>
>>> my_class.fallback_attribute
__getattribute__(fallback_attribute)
__getattr(fallback_attribute)
attribute 란 속성은 없습니다.
>>>
>>> my_class.not_exist_attribute
__getattribute__(not_exist_attribute)
__getattr(not_exist_attribute)
Traceback (most recent call last):
...
AttributeError
```

###  

### 7. 호출형 객체

**다음 매직 메서드를 구현하면, 클래스도 함수같이 호출형으로 사용할 수 있다.**

- `__call__`

다음 예제를 보면 쉽게 이해할 수 있다.

```
from collections import defaultdict

class CallCount:
    def __init__(self):
        self._counts = defaultdict(int)

    def __call__(self, argument):
        self._counts[argument] += 1
        return self._counts[argument]
>>> cc = CallCount()
>>> cc(1)
1
>>> cc(2)
1
>>> cc(1)
2
>>> cc(1)
3
```

###  

### 요약

| 문장                               | 매직 메서드                                           | 파이썬 컨셉              |
| ---------------------------------- | ----------------------------------------------------- | ------------------------ |
| `obj[key]` `obj[i:j]` `obj[i:j:k]` | `__getitem__(key)`                                    | 첨자형 객체              |
| `with obj: ...`                    | `__enter__` / `__exit__`                              | 컨텍스트 관리자          |
| `for i in obj: ...`                | - `__iter__` / `__next__` - `__len__` / `__getitem__` | - 이터러블 객체 - 시퀀스 |
| `obj.attribute`                    | `__getattribute__` / `__getattr__`                    | 동적 속성 조회           |
| `obj()`                            | `__call__`                                            | 호출형 객체              |

------

# 마무리

책 내용의 1/3 정도를 다룬 것 같다.
데코레이터, 디스크립터, 코루틴 등의 내용은 배제하였다.
위 기능들은 API 개발이나 프레임워크 개발 등, 개발자를 위한 개발 코드를 사용할 때 쓰일만한 것들이라 생각한다. 적어도 서비스 도메인 개발 코드를 다루는 내 입장에선 현재 필요하지 않기 때문에... 나중에 쓸 일이 있을 때 정리해보려 한다.

파이썬스러운(Pythonic) 코드는 계속해서 관심 가질 예정이다.
[책, 파이썬답게 코딩하기](http://www.yes24.com/Product/Goods/60493752) 의 목차를 보니 뭔가 읽어볼 만한 것 같다. 추후 읽고 정리할 날이 왔으면..?!

남은 포스팅은, 클린 코드에 대한 본격적인 내용이다.
클린 코드 이야기가 주지만, 파이썬도 띄워놓을 수가 없다. 파이썬 자체가 '가독성 좋은' 철학을 지향하기 때문에 클린 코드의 지향점을 문법적으로 구현한 것도 있기 때문이다. 또 PEP8 등, 코드 스타일에서 어느 정도 '아름다움' 을 정의해놓는 언어이기 때문에 개발하는 사람 입장에서는 이런 것을 알고 개발할 필요가 있다.
아무튼 다음 글에서 마저 정리해보겠다.



# 클린 코드란

클린 코드란 한 마디로 말해, **쉽게 이해 가능하며 지속적으로 개발하기 용이한 코드**를 말한다.
코드는 누구나 짤 수 있다. **하지만 보기 좋고 심플하면서도 핵심 로직을 잘 풀어낸 코드를 짜내는 건 아무나 할 수 없다.**
지속해서 성장하는 시스템에 유연하게 코드를 바꿀 수 있도록 설계해야 하고, 올바른 자료구조와 로직으로 하려는 일을 간단하게 드러내야 한다. 무엇보다 코드만 보고도 무엇을 하려는지 이해 가능해야 한다.
**클린 코드는 개발자에게 일종의 '선'과 같은 개념이다.** 현실적으로 불가능하더라도, 이러한 이상향이 있다는 것을 인지하고 내 코드를 평가할 수 있어야 한다. 적어도 내 코드가 별로인지 괜찮은지는 알아야 한다.

클린 코드는 특히 엔지니어간의 커뮤니케이션과 코드의 유지 관리성을 강조한다.

> 우리는 일반적으로 코드를 작성하는 것보다
> 읽는데 훨씬 많은 시간을 소비한다.

우리는 혼자 코딩하지 않으며 협업하며 일을 한다. 내 코드는 결국 누군가가 보게 되고, 그 누군가는 내 코드를 이해해야 한다. 따라서 애초에 **"이해하기 좋은 코드"** 를 짜는 것이 후에 누군가가 읽기에도 편하고, 유지 보수하기 좋다는 것이다.

------

# 코딩 가이드라인

참고로, "코딩 가이드라인"은 책에는 없는, 내가 지은 제목이다.
여기서는 코딩할 때 어떤 코딩 스타일을 따라야 하는지, 그러기 위해 어떤 기능들이 있는지 등을 간략히 살펴본다. 자세히 다루지는 않고 간단히 소개만 한다. 더 좋고 자세한 내용은 다른 블로그 분들의 포스팅을 링크해두었다.

아래 내용들이 클린 코드 그 자체는 아니다. 다만, 클린 코드가 말하는 "이해하기 좋은 코드" 가 되기 위한 권장 조건들이며, 클린 코드를 향하는 과정이라고 할 수 있겠다.
권장 조건이니 만큼, "필수적인 것"은 아니다. 실제 적용할 지는 팀마다 다르며, 자기가 속한 팀의 가이드라인이 있다면 그것을 준수하는 것이 먼저라고 생각한다. 하지만 아직 정해진 게 없다면, 아래 내용들을 숙지 후에 팀과 협의하여 가이드라인을 세워나가는 것도 좋다고 생각한다.

## 1. 코딩 스타일과 포매팅

### 코딩 스타일

좋은 코드의 레이아웃에서 가장 필요한 특성은 일관성이다. 코드가 일관되게 구조화되어 있으면 가독성이 높아지고 이해하기 쉬워진다. **코딩 스타일은 이처럼 일관된 코드 구조를 위한 관습(컨벤션) 이다.**
파이썬에는 PEP-8 이라는 표준 코딩 스타일 표준 문서가 있다. 따라서 대부분의 파이썬 개발자들은 이 코딩 스타일을 따른다. PEP-8 코딩 스타일에는 예를 들어 다음과 같은 것이 있다.

```
# 키워드 인자에 값을 할당할 때는 띄어쓰기를 사용하지 않는다.
def func(a=None, b=None):  
    pass

# 변수에 값을 할당할 때는 띄어쓰기를 사용한다.
a = 5  
b = 3

# 키워드 인자에 값을 할당할 때는 띄어쓰기를 사용하지 않는다.
func(a=5, b=3)
```

이렇게 하면 `a = 1` 로 검색하면 함수의 정의부를 찾게 되고, `a=1` 로 검색하면 이 파라미터가 호출부에서 사용되는 곳을 찾게 된다. 즉 검색할 때 효율적이다.

이런 류의 일종의 '룰' 을 정의해놓은 문서가 PEP-8 이다. 구체적인 게 궁금하면 아래 링크를 참고하자.

> **[PEP-8 공식 도큐먼트]**
>
> https://www.python.org/dev/peps/pep-0008/

실제로 코딩할 때는 pylint 라는 린터를 설치하여 코딩한다.
린터는 언어 문법과 코드 스타일이 올바르게 짜였는지 검사하는 프로그램인데, pylint 는 내가 작성한 파이썬 코드가 문법 오류는 없는지, PEP-8 에 부합하는지 등을 검사해준다. 보통 VS code 나 Pycharm 등 IDE 내부 플러그인에 포함되어있다. 보통은 이 방식으로 PEP-8 스타일을 준수하게 된다.

###  

### 코드 포매팅

**린터가 검사만 한다면, 포매터는 검사를 기반으로 올바른 코드 스타일로 수정까지 해준다.** 즉 내 코드를 바꾼다. 그런데 올바른 코드 스타일도 종류가 있다. PEP-8 문서를 보면 알겠지만, 좀 더 러프하게 방향성을 제시해줄 뿐, 어떤 정답 코드가 딱 하나가 있는 게 아니다. 그래서 포매터도 어떻게 수정할 것이냐에 따라 여러 종류가 있다.

Autopep8, yapf, black 등이 각각 나름의 스타일로 포매팅해주는 코드 포매터다.
이에 대한 자세한 내용은 아래 링크를 참고하자.

> **[파이썬 코드 체커와 포매터 종류]**
>
> [city7310 님 블로그 - 파이썬 코드 스타일 이야기 - (1) Style Checker, Formatter들 구경하기](https://velog.io/@city7310/파이썬-코드-포매터-이야기-5wjxdei9iv)

실제로 회사에서는 이런 코드 포매터를 도입하여 팀 내부의 코드 스타일을 엄하게 표준화한다. 그렇게 해야 팀 내 코드 스타일의 일관성을 확실하게 유지할 수 있고, 무엇보다 다른 스타일로 인한 git conflict 가 뜨지 않는다.

##  

## 2. Docstring

파이썬은 유독 "읽고 이해하기 좋음" 을 언어적으로 강조한다. 프로그래밍을 처음 하는 사람도 C 나 Java 보다 파이썬을 더 배우기 쉬운 이유도 이 때문이라고 생각한다. 다른 언어보다, 문법이 사람의 말과 닮아있다.

이러한 철학 때문인지 파이썬에서는 문서화를 중시한다. 그리고 Docstring 이라는 개념이 문법에 등장한다. Docstring 은 코드와 로직에 대한 설명을 적어두는 것이다.
주석과 다르다. 주석은 어쩔 수 없는 보충설명의 기능이고, 되도록이면 지양해야 한다.
**Docstring 은 보충설명이 아닌 문서다.** 코드와 컴포넌트에 대한 전반적인 설명이고, 내용은 코드 이해를 충분히 도울만큼이면 좋다.



![img](https://k.kakaocdn.net/dn/bS26pb/btqD2bQoQ9N/7qEYrWfQUvBtw4ZAqCzsD1/img.png)오픈소스 pandas 내 DataFrame 의 소스. docstring 이 아주 세세하게 잘 써져있다.



클래스나 함수 아래에 `"""` 를 감싼 뒤, 이 안에다가 적으면 된다.
이렇게 적은 내용은 실제로 String 객체 안에 담겨, `__doc__` 을 통해 코드에서 접근할 수 있다.
예를 들어 `DataFrame` 의 위 Docstring 은 `DataFrame.__doc__` 에 담겨있다.

Docstring 에도 유명한 스타일들이 있다.
sphinx, google, numpy 등의 스타일들이 대표적인 예다.
이 스타일들에 대한 간단한 설명은 다음 링크를 참고하자.

> **[파이썬 Docstring 스타일 예제]**
>
> [Mo Kweon 님 블로그 - 파이썬 (doc) 스타일 가이드에 대한 정리](https://medium.com/@kkweon/파이썬-doc-스타일-가이드에-대한-정리-b6d27cd0a27c)

이렇게 docstring 을 잘 짜 놓으면 이후 sphinx 를 이용하여 코드 문서화를 웹 페이지로 퍼블리싱할 수 있다. 우리가 오픈소스 공식문서를 볼 때 흔히 보는 그 페이지들이 바로 이 sphinx 를 이용하여 만든 페이지들이다.
sphinx 를 사용하는 예제는 다음 링크를 참고하자.

> **[파이썬 Sphinx 로 웹페이지 문서 만드는 예제]**
>
> [Kei Choi 님 블로그 - 파이썬 소스코드 문서화하기](http://www.hanul93.com/python-sphinx/)

##  

## 3. 타입 힌팅

### 어노테이션

파이썬은 동적으로 타입을 결정하기 때문에, 변수의 타입이 무엇인지 알기 어려운 경우가 많다. 특히 내가 짠 코드가 아닌 남의 코드를 볼 때 더욱 그렇다.
어노테이션은 이를 해결하기 위해 변수 옆에 타입을 명시해주는 기능이다.
예를 들면 다음과 같다.

```
def func(a: int,  b: str = None, c: MyClass = None) -> None:
    pass
```

위 함수는 `int`, `str`, `Myclass` 타입의 변수를 입력받고, 아무것도 반환하지 않는다.
**어노테이션은 명시만 해줄 뿐 실제로 그 타입인지 검사하지는 않는다. 그저 단순히 '힌트' 를 줄 뿐이다.**
(다만 Pycharm 과 같은 IDE 에서는 코딩할 때 올바른 타입을 할당했는지, 반환받았는지 등을 어노테이션 기반으로 알려주기도 한다. 되도록 어노테이션을 활용해야 하는 이유이기도 하다.)

파이썬 3.6 부터는 다음과 같이 변수에다가도 사용할 수도 있다.

```
>>> a: int = 1
>>> b: float = 2
>>> print(a, b)
1, 2
```

좀 더 복잡한 List 나 Dict 같은 컬렉션 타입이나 Class 타입은 어떻게 해야 할까?
이를 위해서는 `typing` 모듈을 사용해야 한다.
예를 들면 다음과 같다.

```
from typing import List

def func(a: List[int]) -> None:
    pass

a: List[int] = [1, 2, 3, 4]
func(a)
```

`typing` 모듈을 써서 일관성 있게 타입을 명시해주는 게 타입 힌팅의 정석이긴 하다.
다만 자료구조 복잡해질수록 타입 힌팅도 길어지게 되고, 과연 이게 읽기 좋은 코드인지는 생각해봐야 한다.

###  

### Mypy

mypy는 어노테이션을 기반으로 정말 그 타입이 사용되었는지 검사하는 도구다. 어노테이션만 사용하면 힌트만 줄 뿐, 검사하지는 않는다고 했는데, mypy 는 검사해서 잘못사용된 부분을 알려준다.
예를 들면 다음과 같다.

```
# test.py
a: int = "heumsi"
$ mypy test.py
test.py:1: error: Incompatible types in assignment (expression has type "str", variable has type "int")
Found 1 error in 1 file (checked 1 source file)
```

**mypy 는 위처럼 동적인 파이썬 코딩을 좀 더 Type safe 할 수 있게 도와준다.**
다만 가끔 잘못 탐지하는 경우도 있으므로 주의하자.
좀 더 자세한 내용은 아래 링크를 참고하자.

> **[타입 힌팅과 mypy 소개]**
>
> [Seorenn님 블로그 - Python 3 정적 타이핑 소개 및 소감(?)](https://seorenn.tistory.com/77)

##  

## 4. 자동 검사 설정

리눅스 개발환경에서 빌드를 자동화하는 가장 일반적인 방법은 makefile 을 사용하는 것이다.
빌드 외에도 포매팅 검사나 스타일 검사, 타입 검사, 테스트 등을 이 안에서 자동화할 수 있다.
예를 들면 다음과 같다.

```
# makefile

lint:
pylint src/ test/

typehint:
mypy src/ test/

test:
pytest src/ test/

checklist: lint typehint test

.PHONY: typehint test lint checklist
$ make checklist
```

위 커맨드는 코드 스타일, 타입, 테스트 검사를 차례대로 수행한다.
만약 이 중 하나라도 실패하면 전체 프로세스가 실패한 것으로 간주한다.

------

# 정리

클린 코드가 무엇인지 잠깐 설명하고, 클린 코드를 위한 최소한의 코딩 가이드라인을 적어보았다.
주요 키워드를 적어보면 다음과 같다.

- 코드 스타일
  - PEP-8 으로 일관된 코드 레이아웃 유지
  - 이를 위한 체커(린터)와 포매터
- Docstring
  - 코드 문서화는 코드를 쉽게 이해하게 한다.
  - sphinx 로 쉽게 API 웹 문서를 만들 수 있다.
- 타입 힌팅
  - 어노테이션으로 변수가 어떤 타입인지 명시
  - mypy 로 올바른 타입이 할당되었는지 검사
- 자동 검사 설정
  - 프로젝트 빌드 시에 팀의 코드 스타일을 따랐는지, 타입 오류는 없는지 등 검사
  - 이 외에도 테스트 수행 등 기능

저번 글이 너무 길었어서, 이번에는 좀 나누어서 가려고 한다.
다음 글은 좋은 코드의 일반적인 특징 등 좀 더 코드 단위로 살펴보는 글이 될 듯하다.



## 1. 계약에 의한 디자인

컴포넌트는 기능을 숨겨 캡슐화하고 함수를 사용할 고객에게는 API를 노출한다.
API를 디자인할 때는 예상되는 입력과 출력 그리고 부작용을 문서화해야 한다.
**코드가 정상 동작하기 위해 기대하는 입력과 호출자가 반환받기를 기대하는 것은 디자인의 하나가 되어야 한다.** 여기서 계약이라는 개념이 생긴다.

계약에 의한 디자인이란 양측이 동의하는 계약을 먼저한 다음, 계약을 어겼을 경우 명시적으로 왜 계속할 수 없는지 예외를 발생시키는 것이다. 계약은 주로 사전 조건과 사후 조건을 명시하지만 때로는 불변식과 부작용을 기술한다.

### 1.1. 사전조건과 사후조건

**사전조건은 함수나 메서드가 제대로 동작하기 위해 보장해야 하는 모든 것을 말한다.** 쉽게 말해 함수에 올바른 데이터를 전달하는 것이다. 예를 들어, 초기화된 객체, null이 아닌 값 등이 조건이 된다.
이러한 작업은 호출자(클라이언트)에게 부과된 임무다.
하지만 런타임 환경에서 올바른 입력 값을 전달하는지 알 수 없다. 따라서 기대하는 입력 값이 맞는지 확인해야 하는데, **클라이언트에서 함수 호출 전에 할지, 함수가 자체적으로 로직을 실행하기 전에 할 지 선택해야 한다.**
일반적으로 업계에서는 견고한 소프트웨어를 위해 후자를 택한다. 즉 입력에 대해 신뢰하지 않기 때문에, 함수 자체적으로 확인을 한다. 만약 본인이 이 모든 걸 제어할 수 있는 위치에 있다면, 한쪽에서만 하면 된다. 즉 사전 검증을 호출하는 쪽과 호출받는 쪽 모두에서 중복 구현하지 않고 한쪽에서만 구현하면 된다.

다음은 사전조건을 검증하는 예다.

```
def func(a: int, b: str):
    if not isinstance(a, int) or not isinstace(b, str):
        raise ValueError("입력 파라미터 타입이 올바르지 않습니다.")
```

**사후조건은 함수나 메서드가 반환된 후의 상태를 강제하는 계약이다.** 로직 처리 후, 호출자(클라이언트)가 원하는 결과를 전달하는 것이다. 호출자가 사전 조건만 잘 지키면 아무 문제없이 원하는 결과를 받아 사용할 수 있어야 한다.
이러한 작업은 컴포넌트(로직을 처리하는 함수나 메서드)에게 부과된 임무다.

### 1.2. 계약에 의한 디자인을 하는 이유

디자인 원칙의 주된 가치는 문제가 있는 부분을 효과적으로 식별하는 데에 있다. 계약에 의한 디자인을 사용하는 이유는, 런타임 오류가 발생했을 시 어디가 문제 있는지 빠르게 식별할 수 있기 때문이다. 즉 **오류가 사전 조건 검증에서 발생했는지, 사후 조건 검증에서 발생했는지 알 수 있다.** 전자라면 호출 쪽에 문제가 있는 것이고, 후자라면 함수 내부에 문제가 있는 것이다.

또한 함수나 메서드가 정상 동작하기 위해 기대하는 것이 무엇인지, 무엇을 기대할 수 있는지 명시적으로 정의한다. 이로써 코드를 읽는 사람은 프로그램의 구조와 의도를 명확히 알 수 있다.

------

## 2. 방어적 프로그래밍

방어적 프로그래밍은 계약에 의한 디자인과 달리, 계약이라는 것을 전제하지 않는다. 계약에서 예외를 발생시키고 실패하게 되는 모든 조건을 기술하는 대신, 객체나 함수 또는 메서드와 같은 코드의 모든 부분을 그저 **유효하지 않은 것으로부터 스스로 보호하도록 하는 것**이다.
방어적 프로그래밍의 주요 이슈는 2가지다.

- 예상할 수 있는 시나리오의 오류를 처리하는 방법 (에러 핸들링)
- 발생하지 않아야 하는 오류를 처리하는 방법 (어설션, Assertion)

### 2.1. 에러 핸들링

**오류가 발생하기 쉬운 상황에서 에러 핸들링 프로시저를 사용한다.** 일반적으로 데이터 입력 확인 시에 자주 사용된다.
에러 핸들링의 주요 목적은 다음을 결정하는 것이다.

- 예상되는 에러에 대해서 실행을 계속할 수 있을지
- 아니면 극복할 수 없는 오류여서 프로그램을 중단할지

에러 처리 방법의 일부는 다음과 같다.

#### 1) 값 대체

잘못된 값을 생성하거나 프로그램 전체가 종료될 위험이 있을 경우, 결과 값을 안전한 다른 값으로 대체하는 것이다. 일반적으로 '기본 값' 을 쓰는 것을 말한다.
예를 들어 `dict.get(key, default)` 의 두 번째 파라미터를 사용하면 기본 값을 나타낼 수 있다.

```
configuration = {"db_port": 5432}
...
# db_host 가 configuration 없을 시 기본적으로 "localhost" 를 값을 가져온다.
db_host = configuration.get("db_host", "localhost")
```

일반적으로 누락된 파라미터를 기본 값으로 바꾸어도 큰 문제는 없지만, 오류가 있는 데이터를 유사한 값으로 대체하는 것은 위험하며 일부 오류가 숨겨져 버릴 수 있다. 이 접근법을 사용할 때는 이러한 기준을 고려해야 한다.

#### 2) 예외 처리

어떤 경우에는 에러가 발생하기 쉽다는 가정으로 계속 실행하는 것보다 차라리 실행을 멈추는 게 낫다. 이런 경우 호출자에게 오류에 대해 명확하고 분명하게 알려줘야 한다. 이것이 예외 메커니즘이다. 이로써 호출자는 명확한 예외를 받아 호출자 나름의 예외 처리하여 원래의 비즈니스 로직이 끊기지 않도록 할 수 있다.

다음은 예외와 관련된 몇 가지 권장 사항이다.

##### a. 올바른 수준의 추상화 단계에서 예외 처리

예외 발생과 처리는 캡슐화된 로직과 일치해야 한다.
예외를 발생시키거나, 처리할 때 이 예외를 이 클래스가 발생시키는 게 맞는지, 또 이 클래스에서 처리하는 게 맞는지 등을 고려해야 한다.

##### b. Traceback 노출 금지

파이썬에서 traceback은 매우 유용하고 많은 디버깅 정보를 포함한다. 하지만 이 정보는 악의적인 사용자에게 매우 유용한 정보여서 중요 정보나 지적 재산의 유출이 발생할 위험이 있다.
오류가 너무 중요하다면 전파해도 된다. 다만 일반적으로는 사용자에게 문제를 알리려면 일반적인 메시지를 사용해야 한다.

##### c. 비어있는 except 블록 지양

말 그대로 다음과 같은 경우다.

```
try:
    process_data()
except:
    pass
```

이런 코드는 실패해야만 할 때조차도 결코 실패하지 않는다.
에러는 결코 조용히 전달되어서는 안 된다는 파이썬의 철학을 떠올리면 이는 파이썬스러운 코드가 아니다.

되도록이면 다음과 같이 처리하는 것이 옳다.

- `Exception` 을 상속받은 구체적인 예외를 정의하고, (예를 들어, `AttributeError` 등)
- 이러한 각 예외에 대해서 `except` 처리를 하는 것

##### d. 원본 예외 포함

오류 처리 과정에서 다른 오류를 발생시키고 메시지를 변경할 수도 있다.
이 경우 원래 예외를 포함하는 것이 좋다.

만약 파이썬에서 제공하는 기본 예외를 사용자 정의 예외로 래핑 하고 싶다면, 루트 예외에 대한 정보를 다음과 `raise ... from ...` 구문을 사용하여 같이 포함할 수 있다.

```
class InternalDataError(Exception):
    """ 사용자 정의 예외"""
    pass

def process(data_dictionary, record_id):
    try:
        return data_dictonary[record_id]
    except KeyError as e:
        raise InternalDataError("Record not present") from e
```

> **[더 참고하면 좋을 내용]**
>
> 사실 예외 처리는 간단하게 넘어갈 내용은 아니다.
> 하마님 블로그에 예외 처리와 관련된 나름 생각해볼 만한 내용들이 있어서 링크를 걸어둔다.
>
> [하마님 블로그 - 예외 처리에 대한 6가지 화두](https://hamait.tistory.com/712)

### 2.2. 어설션 사용하기

어설션은 절대로 일어나지 않아야 하는 상황에 사용되므로, assert 문에 사용된 표현식은 항상 참이여야 한다. **즉 어설션 조건은 프로그램의 실행 전제 조건을 설명한다.**

```
def process(data_dictionary, record_id):
    assert isinstance(data_dictionary, dict)  # data_dictionary 는 dict 라는 가정을 설명
    return data_dictionary[record_id]
```

에러 핸들링과 다르게, 어설션 조건 판별이 `False` 가 될 경우, `AssertionError` 을 발생시키고 프로그램을 중지시킨다. 이 `AssertionError` 를 `try ... except` 로 처리하는 것은 옳지 않다. 이 에러가 발생한다는 것은 애초에 프로그램 어딘가에 결함이 있다는 의미 있다는 것이다. 그리고 이러한 신호를 사전에 캐치하기 위해 어설션을 사용하는 것이기도 하다.

------

## 3. 관심사 분리

**책임이 다르면 컴포넌트, 계층 또는 모듈로 분리되어야 한다.**
프로그램의 각 부분은 기능의 일부분(관심사)에 대해서만 책임을 지며 나머지 부분에 대해서는 알 필요가 없다.

소프트웨어에서 관심을 분리하는 목표는 **"파급 효과"를 최소화하여 "유지보수성"을 향상시키는 것**이다.
여기서 파급효과는 어느 지점에서의 변화가 전체로 전파되는 것을 의미한다. 즉 쉽게 말해, 소프트웨어는 쉽게 변경될 수 있어야 한다.

### 응집력

- 컴포넌트는 잘 정의된 한 가지의 목적을 가져야 하며
- 가능하면 작아야 한다는 것을 의미한다.
- 응집력이 높을수록 재사용성은 높아진다.

### 결합력

- 두 개 이상의 객체가 서로 얼마나 의존적인지를 나타낸다.
- 결합력이 높으면 다음과 같은 문제를 일으킨다.
  - 낮은 재사용성
  - 파급 효과
  - 낮은 수준의 추상화

------

## 4. 개발지침 약어

### DRY / OAOO

- Do not Repeat Yourself
- Once And Only Once
- 코드를 변경하려고 할 때 수정이 필요한 곳은 단 한 군데만 있어야 한다.
- 즉, 중복을 최대한 피해야 한다.

### YAGNI

- You Ain't Gonna Need It
- 오직 현재의 요구사항을 잘 해결하기 위한 소프트웨어를 작성해야 한다.
- 내가 짜고 있는 코드가 일어나지도 않을 미래의 일을 예상하고, 코드를 더 복잡하게 만들고 있는 건 아닌지,
- 즉, 지금 필요하지도 않은 오버 엔지니어링을 하고 있는 건 아닌지 염두해야 한다.

### KIS

- Keep It Simple
- YAGNI 원칙과 비슷하다. 디자인이 단순할수록 유지 관리가 쉽다는 것이다.
- 모든 확장 가능성, 좀 더 일반화적인 추상화가 지금 기능 개발 시점에서는 섣부를 수 있다.
- 코드 측면의 단순함이란 문제에 맞는 가장 작은 데이터 구조(표준 라이브러리 등)를 사용하는 것을 의미한다.

### EAFP / LBYL

- Easier to Ask Forgiveness than Permisson
  - 허락보다 용서를 구하는 게 쉽다.
  - 일단 코드를 실행하고 실제 동작하지 않을 경우를 대응한다는 뜻이다.

```
try:
    with open(filename) as f:
        pass
except:
    pass
```

- Look Before You Leap
  - 도약하기 전에 살펴라.
  - 코드를 실행하기 전에, 먼저 무엇을 사용하려고 하는지 확인하라는 뜻이다.

```
if os.path.exists(filename):
    with open(filename) as f:
        pass
```

- **파이썬은 EAFP 방식으로 만들어졌다.**

------

## 5. 컴포지션과 상속

### 5.1. 상속이 좋은 선택인 경우

부모 클래스의 메서드를 공짜로 전수받을 수 있는 장점이 있지만, 한편으론 새로운 정의에 너무 많은 기능을 추가하게 되는 단점도 있다.

다음과 같은 경우, 상속은 좋은 선택의 예가 된다.

- 클래스의 기능을 그대로 물려받으면서 충분히 사용할 상황이 있고, 추가 기능을 더하거나 기존 기능을 수정하는 경우
- 인터페이스용 클래스를 정의하고, 이를 하위 클래스에서 이를 상속받아 기능을 강제하려는 경우
- 다형성을 통해 로직을 유연하게 설계하려는 경우 (`Exception` 을 상속받아 예외를 처리하는 경우가 대표적인 예다.)

**상속이 좋은 일반적인 경우를 한 단어로 표현한다면, "전문화"가 될 것이다.**
즉, 상속을 통하여 기본 객체에서 출발하여 세부적인 추상화를 할 수 있다.

### 5.2. 상속 안티 패턴

##### Bad Case

다음 예를 보자.

```
class TransactionPolicy(collections.UserDict):
    """잘못된 상속의 예"""

    def change_in_policy(self, customer_id, **new_policy_data):
        self[customer_id].update(**new_policy_data)
```

이 코드는 `UserDict` 를 상속받아, 도메인에 맞는 구체적인 `Dict` 형태의 클래스를 정의했다.
위 코드는 2가지의 문제가 있다.

1. TransactionPolicy 이름만 보고 어떻게 사전 타입인지 알 수 있을까?
2. `UserDict` 에 있는 `pop()`, `items()` 와 같은 메서드가 이 클래스에 실제로 필요할까?

즉, 상속을 잘못 사용한 것이다. 단지 첨자 기능을 얻기 위해 사전을 확장하는 것은 충분한 근거가 되지 않는다.
이것이 구현 객체를 도메인 객체와 혼합할 때 흔히 발생하는 문제다.

##### Good Case

**상속이 아닌 해결책은 바로 컴포지션을 이용하는 것이다.**
그리고 첨자 기능은 `__getitem__` 을 구현함으로써 충분히 이용할 수 있다.

```
class TransactionPolicy(collections.UserDict):
    """컴포지션을 통한 해결 예"""

    def __init__(self, policy_data, **extra_data):
        self._data = {**policy_data, **extra_data}  # Dict 의 기능을 _data 에 위임한다.

    def change_in_policy(self, customer_id, **new_policy_data):
        self._data[customer_id].update(**new_policy_data)

    # __getitem__ 과 __len__ 을 구현함으로써 Dict 의 첨자 기능을 이용할 수 있도록 한다.
    def __getitem__(self, customer_id):
        return self._data[customer_id]

    def __len__(self):
        return len(self._data)
```

### 5.3. 파이썬의 다중 상속

##### 메서드 결정 순서 MRO

파이썬에서 다중 상속이 발생할 때, 부모의 어떤 메서드가 먼저 사용될까?
한 마디로 말하면, 상속 순서가 앞쪽에 있는 부모 클래스의 메서드를 사용한다.
정확히는 MRO 알고리즘을 사용하여 메서드 우선순위를 정한다.

다음 예를 살펴보면 쉽게 이해할 수 있다.

```
class A:
    name = "class A"
    def __init__(self):
        print("class A init")

class B:
    name = "class B"
    def __init__(self):
        print("class B init")

class C(A, B):
    def __init__(self):
        super().__init__()
>>> C.name
class A
>>> C()
class A init
```

메서드의 결정 순서는 다음과 같이 확인해볼 수 있다.

```
>>> [cls.__name__ for cls in C.mro()]
['C', 'A', 'B', 'object']  # C -> A -> B -> object 순으로 메서드를 찾아 실행한다.
```

##### 믹스인 (Mixin) 클래스

믹스인 클래스는 코드를 재사용하기 위해 일반적인 행동을 캡슐화해놓은 기본 클래스다.
보통 **유틸리티성 메서드를 구현하고, 이러한 메서드가 필요한 다른 클래스는 이 클래스를 상속받으면 된다.**
예를 들면 다음과 같다.

```
class Serializer:
    def to_json(self):
        return json.dumps(self.__dict__)

    def to_pickle(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, path)
```

위 클래스는 직렬화 관련 메서드를 제공하는 유틸리티성 클래스다.

이러한 직렬화 메서드를 사용하고 싶은 클래스는 이 클래스를 상속받으면 된다.

```
class A(Serializer):
    def __init__(self, a, b):
        self.a = a
        self.b = b
>>> A(1, 2).to_json()
{"a": 1, "b": 2}
```

------

## 6. 함수와 메서드의 인자

### 6.1. 파이썬의 함수 인자 동작 방식

파이썬에서는 함수에 인자가 넘어온 경우 기본적으로 "참조" 형태로 가져온다.
다만 이 함수 내에서 인자의 값이 바뀔 경우, 이 인자가 가변형(mutable) 이냐 불변형(immutable) 이냐에 따라 그 결과가 달라진다. 아래 예를 보면 바로 확인해보자.

##### 인자가 가변형(mutable) 인 경우

```
def func(a):
    print(f"함수 내에서 값 할당 전 id : {id(a)}")
    a += "4"
    print(f"함수 내에서 값 할당 후 id : {id(a)}")

mutable = [1, 2, 3]
print(f"함수 호출 전 id : {id(mutable)}")
func(mutable)
print(f"함수 호출 후 id : {id(mutable)}")
print(mutable)
# 결과
함수 호출 전 id : 4424245064
함수 내에서 값 할당 전 id : 4424245064
함수 내에서 값 할당 후 id : 4424245064
함수 호출 후 id : 4424245064
[1, 2, 3, '4']
```

가변형일 경우, 함수 내에서 값을 수정하면 그대로 참조 객체에 수정된다.
`id` 도 모두 동일한 것을 알 수 있다.

##### 인자가 불변형(immutable) 일 경우

```
def func(a):
    print(f"함수 내에서 값 할당 전 id : {id(a)}")
    a += "4"
    print(f"함수 내에서 값 할당 후 id : {id(a)}")

immutable = "1 2 3"
print(f"함수 호출 전 id : {id(immutable)}")
func(immutable)
print(f"함수 호출 후 id : {id(immutable)}")
print(immutable)
# 결과
함수 호출 전 id : 4475811800
함수 내에서 값 할당 전 id : 4475811800
함수 내에서 값 할당 후 id : 4476143240
함수 호출 후 id : 4475811800
1 2 3
```

불변형일 경우, 함수 내에 할당 전 `id` 가 동일하지만 인자 값을 수정하는 순간 `id` 가 바뀌는 것을 알 수 있다. 즉, 값을 수정하는 순간 새로운 객체를 할당하는 것이다. 따라서, 기존 인자에 수정한 것이 반영되지 않는다.

> **[Tip] 일반적으로 함수 인자를 변경하지 않아야 한다. 최대한 함수에서 발생할 수 있는 부작용을 피하자.**

### 6.2. 함수 인자의 개수

함수 인자는 적을수록 좋다. **함수 인자가 많을수록 호출자와 밀접하게 결합된다는 신호이다.**
예를 들어 다음 함수를 보자.

```
def func(a, b, c, d, e, f, g, h, i, j, k):
    pass
```

호출자가 이 함수를 사용하려면 변수 `a` 부터 `k` 까지 모두 필요하다.
이런 문제를 어떻게 해결해야 할까?

크게 2가지 방법이 있다.

##### 전달하는 모든 인자를 포함하는 새로운 객체를 만드는 것

이 방법을 사용하면 다음처럼 코드가 바뀐다.

```
def func(class_param):
    pass
```

위 `a` ~ `k` 를 포함하는 객체 `class_param` 를 전달함으로써, 함수 인자 개수가 줄어들었다.
다만 이렇게 객체 자체가 넘어가는 경우, 함수 내부에 사용되지 않는 정보까지 같이 넘어갈 수 있다.
따라서, 애초에 객체를 올바르게 추상화하여 이런 오버헤드를 막을 필요가 있다.

##### 가변 인자나 키워드 인자를 사용하여 동적 서명

이 방법을 사용하면 다음처럼 코드가 바뀐다.

```
def func(*args, **kwargs):
    pass
```

이 방법은 파이썬스럽기는 하지만, 남용하지 않도록 주의해야 한다. 왜냐하면 매우 동적이어서 유지 보수하기가 어렵기 때문이다. 예를 들어 `kwargs` 에 어떤 변수가 담겨오는지 코드 자체에 명시되지 않기 때문에, 이 함수를 설계하는 사람은 이 정보를 코드 외적으로 알아야 할 필요가 있다.

> **[Tip]**
> 사실 애초에 함수에 너무 많은 인자가 오는 거 자체가 여러 작은 함수로 분리하라는 신호일 수 있다.
> **함수는 오직 한 가지 일만 해야 한다는 점을 기억하자.**

------

## 7. 결론

좋은 코드의 일반적인 특징 및 권장사항을 추가적으로 요약하면 다음과 같다.

- 소프트웨어를 독립성 있게 짜자.
  - 모듈, 클래스 또는 함수를 변경하면 수정한 컴포넌트가 외부 세계에 영향을 미치지 않아야 한다.
  - 이것은 바람직하지만 항상 가능한 것은 아니다. 하지만 최소화하기 위한 시도는 해야 한다.
  - 컴포넌트의 응집도를 높이고, 결합도를 낮추는 이유가 여기에 있다.
  - 또한, 입력되는 파라미터를 내부에서 수정하지 않아야 하는 이유도 이와 같은 목적이다.
  - 컴포넌트가 독립적이라면, 테스트도 독립적으로 구현할 수 있다. 이는 소프트웨어의 신뢰성과도 연결된다.
- 코드 구조를 잘 나누어 구조화 하자.
  - 여러 정의(클래스, 함수, 상수 등)가 들어있는 큰 파일을 만들지 말 자.
  - 유사한 컴포넌트끼리 정리하여 구조화 하자.
  - 유사한 정보를 중앙화 하자.
  - 이를 통해 필요한 모듈만 임포트 해올 수 있고, 메모리에 로드할 객체를 줄일 수 있다.