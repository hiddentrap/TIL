# re 정규표현식

```python
#정규표현식
# re.match(pattern, str) : 시작부터 찾음 in str
# re.search(pattern, str) : 위치상관 없이 찾음 in str

# 아무 문자중 하나
re.match(f'[bcdfghjklmnpqrstvwxyz]', 'chair') -> c

# 아무 문자중 하나 이상
re.match(f'[bcdfghjklmnpqrstvwxyz]+', 'chair') -> ch
re.match(f'[bcdfghjklmnpqrstvwxyz]+', 'apple') -> None

# 검색결과 활용
matchObj = re.search('match', "'matchObj' is a good name, but 'm' is convenient.")
print(matchObj) -> <_sre.SRE_Match object; span=(1, 6), match='match'>

print(matchObj.group()) -> match : 일치된 문자열
print(matchObj.start()) -> 1 : 일치된 문자열의 시작 위치
print(matchObj.end()) -> 6 : 일치된 문자열의 끝 위치
print(matchObj.span()) -> (1,6) : 일치된 문자열의 (시작,끝) 위치 튜플

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

메타문자 : $()*+.?[]\^{}| : 일반문자취급 하려면앞에 \붙이면 됨
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

https://brownbears.tistory.com/506