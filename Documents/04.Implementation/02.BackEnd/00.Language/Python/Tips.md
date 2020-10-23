# Comprehension

```python
1. Looping
for c in string.ascii_lowecase: [1]
    if c not in 'aeiou':		[2]
        consonants += c			[3]

        2. List comprehension
[3][1][2]
[c for c in string.ascii_lowercase if c not in 'aeiou']

3. Filter (Functional Approach)
list(filter(lambda c: c not in 'aeiou', string.ascii_lowercase))
        
```

```python
1. Looping
verses = []						[1]
for n in range(1, day + 1):		[2]
    verses.append(verse(n))		[3]
    
2. List comprehension
[1] [3] [2]
verses = [verse(n) for n in range(1, day + 1)]

3. Map
[1] [3] [2]
verses = map(verse, range(1, day + 1))
```

```python
[choose(char) for char in args.text]

map(choose, args.text)

1. Looping
for n in range(3, 0, -1):
    print(verse(n))
    
2. List comprehension
[verse(n) for n in range(3,0,-1)]

3. map
map(verse, range(3, 0, -1)) = map(verse, [3,2,1])

4. etc.
[verse(3), verse(2_, verse(1)]
```

```python
if random.choice([False, True]):
    ransom.append(char.upper())
else:
    ransom.append(char.lower())
    
ransom.append(char.upper() if random.choice([False, True]) else char.lower())

# append: 리스트에 원소 한개 추가
# extend: 리스트에 여러개의 원소를 리스트로 추가

# random.choice: 리스트 요소중에 한개만 랜덤으로 취함
# random.sample(리스트, 갯수): 리스트 요소중 갯수를 취해서 리스트로 반환
# random.shuffle(리스트): 리스트 아이템 순서를 섞어버림 반환은 없음

# map(lambda n: n + 1, [1, 2, 3])
```



## HOF, Higher Order Function

```python
HOF = 파라메터로 다른 함수를 요구하는 함수

map = map(func, list) : func의 결과값으로 이뤄진 list 리턴
new list of values modified by function but not list type = map (function that returns modified value, list of values for the function)

filter = filter(func, list) : func의 리턴이 true인 list value 값으로 이뤄진 list 리턴
new list containing only elements that were true for function but not list type= filter (function that returns true of false, list of values for the function)

consonants = ''.join(filter(lambda c: c not in 'aeiou', string.ascii_lowercase))
list(filter(lambda c: c not in 'aeiou', string.ascii_lowercase))

cars = ['blue Honda', 'red Chevy', 'blue Ford']
list(filter(lambda car: car.startswith('blue '), cars'))

functiools.reduce
reduce(lambda x, y: x_y, [1,2,3,4,5]) -> (((1+2)+3)+4)+5
```



## 기타

```python
black xxx.py  : 코딩포맷 정렬
pylint xxx.py : warning 검사
mypy xxx.py   : 타입검사

or 연산자
p1 = match.group(1) or '' # 이런식의 표현 가능 None이나 False일 경우 '' 아니면 앞의 값 취함

긴 스트링을 만들때, 
pattern = (
    f'([{"cdf"}]+)?'     # capture on or more, optional
    f'([{"aeo"}])'       # capture at least one vowel
    f'(.*)'              # capture zero or more of anything
)
이런식으로 주석달면서 긴 스트링 패턴을 만들 수 있음 개꿀.

f'xxx' = 포맷스트링, r'xxx' = 로우스트링

인코딩 문제
상단에
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

https://github.com/minjaesong/cp-949-to-utf-8
    
프로그램 비정상 종료시
sys.exit("err msg"): 메시지는 sys.stderr로 나가고 리턴값은 1로 나간다
    
functiools.reduce
reduce(lambda x, y: x_y, [1,2,3,4,5]) -> (((1+2)+3)+4)+5

정렬
words = 'banana Apple Cherry anchovies cabbage Beets'
대문자 아스키값이 소문자 아스키값보다 작기 때문에 먼저 정렬
sorted(words) -> ['Apple', 'Beets', 'Cherry', 'anchovies', 'banana', 'cabbage']
대소문자 관계없이 정렬
sorted(words, key=str.casefold) -> ['anchovies', 'Apple', 'banana', 'Beets', 'cabbage', 'Cherry']

딕셔너리 만들때 zip : N 개의 리스트를 인자로 받아 각각의 카운터파트 요소를 합쳐 튜플 리스트를 리턴 
    list_a = ['a','b','c']
    list_b = ['1','2','3']
    zip(list_a,list_b) = [('a','1'),('b','2'),('c','3')]
headers = fh.readline().rstrip().split(',')
rec = dict(zip(headers, line.rstrip().split(',')))

dict(zip(list_a,list_b))->{'a':'1','b':'2','c':'3',}

테스트 목업 file mock up
text = io.StringIO('exercise,reps\nBurpees,20-50\nSitups,40-100')
assert read_csv(text) == [('Burpees', 20, 50), ('Situps', 40, 100)]

enumerate(list, start_index)= list of tuple (인덱스, 값)

cells_tmpl = '{} {} {}'
cells_tmpl.format(*cells[:3]) -> cells_tmpl.format(cells[0], cells[1], cells[2])

any([a,b,c]) = a or b or c
all([a,b,c]) = a and b and c

immutable dict = named tuple -> 3.8부터 TypedDict가 생김 (Mutable)
State = namedtuple('State', ['cell', 'player'])
state = State(1,'x')
state.cell -> 1
state.player -> x

from typing import List, NamedTuple, Optional
네임드 튜플을 상속받은 클래스
class State(NamedTuple):
board: List[str] = list('.' * 9)
player: str = 'X'
quit: bool = False
draw: bool = False
error: Optional[str] = None
winner: Optional[str] = None
    
TypedDict를 상속받은 클래스: 초기값 설정 불가로 state=State(board='.'*9, player='X')식으로 인스턴트화 시킬때 초기화해야 함
class State(TypedDict):
board: List[str] = list('.' * 9)
player: str
quit: bool
draw: bool
error: Optional[str] 
winner: Optional[str]


state = State(board=list('X...'), player='O')
state = state._replace(board=list('O...'))

타입힌트
def format_board(board: List[str]) -> str:
def main() -> None:
def get_move(state: State) -> State:
    
    
화면지움
print("\033[H\033[J")

아규먼트 파싱 argparse -> Tiny Python Projects : 385p참조
    
지정된 경로를 찾을 수 없습니다.
HKEY_CURRENT_USER\Software\Microsoft\Command Processor\AutoRun값을 탐색 하고 지우십시오.

```

