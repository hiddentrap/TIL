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



## 정규표현

```python
#정규표현식
# re.match(pattern, str) : 시작부터 찾음 in str
# re.search(pattern, str) : 위치상관 없이 찾음 in str

# 아무 문자중 하나
re.match(f'[bcdfghjklmnpqrstvwxyz]', 'chair') -> c

# 아무 문자중 하나 이상
re.match(f'[bcdfghjklmnpqrstvwxyz]+', 'chair') -> ch
re.match(f'[bcdfghjklmnpqrstvwxyz]+', 'apple') -> None

# 그룹사용
re.match(f'([bcdfghjklmnpqrstvwxyz]+)', 'chair') -> ('ch',)

# 그룹안에 서브그룹 사용가능
match = re.match('(foo(bar)baz)', 'foobarbaz') -> ('foobarbaz', 'bar')
# 캡쳐제외영역
re.match('(foo(?:bar)?baz)', 'foobarbaz') -> ('foobarbaz')
re.match('(foo(?:bar)?baz)', 'foobaz') -> ('foobaz')

# 2개 그룹, (1개 이상 자음, 1개 이상 아무문자)
re.match(f'([bcdfghjklmnpqrstvwxyz]+)(.+)', 'chair') -> ('ch','air')
re.match(f'([bcdfghjklmnpqrstvwxyz]+)(.+)', 'apple') -> None
# 2개 그룹, (1개 이상 자음(옵션), 1개 이상 아무문자)
match = re.match(f'([bcdfghjklmnpqrstvwxyz]+)?(.+)', 'apple') -> (None, 'apple')
match.groups() -> (None, 'apple')
match.group(1) -> None
match.group(2) -> 'apple'

match = re.match(f'([bcdfghjklmnpqrstvwxyz]+)?(.+)', 'chair') -> ('ch', 'air')
match.groups() -> ('ch', 'air')
match.group(1) -> 'ch'
match.group(2) -> 'air'

match = re.match(f'([bcdfghjklmnpqrstvwxyz]+)?(.+)', 'CHAIR') -> (None, 'CHAIR')
match = re.match(f'([bcdfghjklmnpqrstvwxyz]+)?(.+)', 'CHAIR', re.IGNORECASE) -> ('CH', 'AIR')

match = re.match(f'([bcdfghjklmnpqrstvwxyz]+)?(.+)', 'rdnzl') -> ('rdnz', 'l')
# 위에가 ('rdnzl', None)이 아닌 이유: 두번째 그룹의 +(1개 이상) 때문 -> *(0개 이상)
match = re.match(f'([bcdfghjklmnpqrstvwxyz]+)?(.*)', 'rdnzl') -> ('rdnzl', None)

# 1개이상 자음(옵션) + 1개 모음 + 0개 이상 아무문자
re.match(f'([bcdfghjklmnpqrstvwxyz]+)?([aeiou])(.*)', 'cake') -> ('c','a','ke')
re.match(f'([bcdfghjklmnpqrstvwxyz]+)?([aeiou])(.*)', 'rdnzl') -> None
re.match(f'([bcdfghjklmnpqrstvwxyz]+)?([aeiou])(.*)', '123') -> None

숫자		\d		[0123456789], [0-9]
특수문자		\s		[ \t\n\r\x0b\0c], string.whitespace
문자		\w		[a-zA-Z0-9_-]
아무거나	.	
한개이상	+
0개이상	*
$끝에서
{3} 3개 ^[.XO]{9}$ = 9자리의 .이나 X나 O로 이루어진 문자열 그뒤($)나 그 앞(^)에 아무것도 없음

re.search('\d', 'abc123!') = re.search('[0123456789]', 'abc123!') = re.search('[0-9]', 'abc123!')

# 1개 이상  = +
re.search('\d+', 'abc123!') = 123
re.search('\w+', 'abc123!') = abc123

# 부정형 ^을 붙이거나 숏형을 대문자로 쓰면 부정형
re.search('[^0-9]+', 'abc123!') = abc
re.sarch('\D+', 'abc123!') = abc
re.search('\W', 'abc123!') = !

숫자		\D		[^0123456789], [0-9]
특수문자		\S		[^ \t\n\r\x0b\0c], string.whitespace
문자		\W		[^a-zA-Z0-9_-]

re.split(r'\W', 'abc123!') = ['abc123', ''] : !가 없다
re.split(r'(\W)', 'abc123!') = ['abc123', '!', ''] : 그룹으로 묶어주면 !도 리턴한다.
    
#정규표현식 미리 컴파일해놓기
splitter = re. compile("([a-zA-Z](?:[a-zA-Z']*[a-zA-Z])?)")
splitter. split("Don't worry, spiders,")
['', "Don't", ' ', 'worry', ', ', 'spiders', ',']

# Greedy 매칭이 기본
text = 'The quick <adjective> <noun> jumps <preposition> the lazy <noun>.'
re.search('<.+>', text) -> '<adjective> <noun> jumps <preposition> the lazy <noun>'
# Non-greedy 매칭을 하려면 but <<bar> 이런경우 문제됨 -> <<bar>
re.search('</+?>', text) -> '<adjective>'
# 더 정확하게 하려면 이려면 <<bar>도 -> <bar>
re.search('<[^<>]+>', text)
# 그룹으로 플레이스 홀더와 플레이스폴더 내용 분리
re.search('(<([^<>]+)>)', text) -> (<adjective>, adjective)

#re.findall() 패턴을 찾아서 리스트로 리턴
re.findall('(<([^<>]+)>)', text) -> [
    (<adjective>, adjective),
    (<noun>, noun), 
    ...
]

#내용 바꾸기
re.sub('<noun>', 'dog', 'The quick blue <non> jumps <preposition> the lazy <noun>.', count = 1) -> 'The Quick blue dog jumps <preposition< the lazy <noun>.'
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

