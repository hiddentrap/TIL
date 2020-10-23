# Urllib, URL인코딩

HTTP를 GET으로 리퀘스트 할때, 파라메터에 한글이 포함되서 ascii로 표현할 수 없는 경우

```python
from urllib import parse

url = parse.urlparse('https://brownbears.tistory.com?name=불곰&params=123')

query = parse.parse_qs(url.query)
query2 = parse.parse_qsl(url.query)
result = parse.urlencode(query, doseq=True)

print(query)
print(query2)
print(result)

# {'name': ['불곰'], 'params': ['123']}
# [('name', '불곰'), ('params', 123)]
# name=%EB%B6%88%EA%B3%B0&params=123
```

```python
result = parse.urlencode(query) # doseq의 기본값은 False
print(result)
# name=%5B%27%EB%B6%88%EA%B3%B0%27%5D&params=%5B%27123%27%5D
```

##### 튜플 변수 인코딩

```python
query = [('name', '불곰'), ('params', 123)]
result = parse.urlencode(query, doseq=True)

print(result)
# name=%EB%B6%88%EA%B3%B0&params=123
```

##### 인코딩 지정을 원할 경우

```python
result = parse.urlencode(query, encoding='UTF-8', doseq=True)
print(result)
# name=%EB%B6%88%EA%B3%B0&params=123
```

##### 단순 문자열 인코딩 디코딩

```python
from urllib import parse
text = '불곰'
enc = parse.quote(text)
dec = parse.unquote(enc)
print(enc)
print(dec)
# %EB%B6%88%EA%B3%B0
# 불곰
```

##### 기타

```python
from urllib import parse
url = parse.urlparse('https://brownbears.tistory.com?name=불곰&params=123')
print(url)
# ParseResult(scheme='https', netloc='brownbears.tistory.com', path='', params='', query='name=불곰&params=123', fragment='')
```

https://brownbears.tistory.com/503?category=168282