# Bs4

웹 크롤러를 만들거나 html에서 필요한 정보를 검색할 때, BeautifulSoup 라이브러리를 사용하여 편리하게 코딩할 수 있습니다.

# 설치

```
$ pip3 install beautifulsoup4
```

beautifulsoup에는 기본적으로 파이썬 표준라이브러리인 html 파서를 지원하지만, lxml이라는 모듈이 더 빠르게 동작하므로 lxml 모듈도 설치해 줍니다.

```
$ pip3 install lxml
```



아래는 beautifulsoup에서 사용할 수 있는 파서의 장단점을 보여주는 테이블 입니다.

| Parser             | 선언방법                                                     | 장점                                                       | 단점                             |
| :----------------- | :----------------------------------------------------------- | :--------------------------------------------------------- | :------------------------------- |
| 파이썬 html.parser | BeautifulSoup(markup, 'html.parser')                         | 설치할 필요 없음적당한 속도                                |                                  |
| lxml HTML parser   | BeautifulSoup(markup, 'lxml')                                | 매우 빠름                                                  | lxml 추가 설치 필요              |
| lxml XML parser    | BeautifulSoup(markup, 'lxml-xml') BeautifulSoup(markup, 'xml') | 매우 빠름유일하게 지원되는 xml parser                      | lxml 추가 설치 필요              |
| html5lib           | BeautifulSoup(markup, 'html5lib')                            | 웹 브라우저와 같은 방식으로 페이지를 파싱유효한 HTML5 생성 | html5lib 추가 설치 필요매우 느림 |

# 사용법

기본 선언 및 테스트 HTML은 아래와 같습니다.

```python
from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html>

<head>
   <title>Page title</title>
</head>

<body>
   <div>
      <p>a</p>
      <p>b</p>
      <p>c</p>
   </div>
   <div class="ex_class">
      <p>d</p>
      <p>e</p>
      <p>f</p>
   </div>
   <div id="ex_id">
      <p>g</p>
      <p>h</p>
      <p>i</p>
   </div>
   <h1>This is a heading</h1>
   <p>This is a paragraph.</p>
   <p>This is another paragraph.</p>
   <a href="http://brownbears.tistory.com" class="a"/>
</body>

</html>
"""


bs = BeautifulSoup(html, 'lxml')
```

## find(name, attrs, recursive, string, **kwargs)

조건에 맞는 태그를 가져옵니다. 만약 조건에 맞는 태그가 1개 이상이면 가장 첫 번째 태그를 가져옵니다.

```
result = bs.find('p')
print(result)


# <p>a</p>
```

## find_all(name, attrs, recursive, string, limit, **kwargs)

조건에 맞는 모든 태그들을 가져옵니다.

```
result = bs.find_all('p')
print(result)

# [<p>a</p>, <p>b</p>, <p>c</p>, <p>d</p>, <p>e</p>, <p>f</p>, <p>g</p>, <p>h</p>, <p>i</p>, <p>This is a paragraph.</p>, <p>This is another paragraph.</p>]
```

## class 명으로 찾기

```
result = bs.find('div', class_='ex_class')
print(result)


# <div class="ex_class">
# <p>d</p>
# <p>e</p>
# <p>f</p>
# </div>
```

## id 명으로 찾기

```
result = bs.find('div', id='ex_id')
print(result)


# <div id="ex_id">
# <p>g</p>
# <p>h</p>
# <p>i</p>
# </div>
```

## 해당 태그명 출력

```
result = bs.find('div', id='ex_id')
print(result.name)

# div
```

## 해당 id명 출력

```
result = bs.find('div', id='ex_id')
print(result['id'])

# ex_id
```

## 해당 class명 출력

```
result = bs.find('div', class_='ex_class')
print(result['class'])


# ex_class
```

## 태그 사이에 있는 내용 출력

```
result = bs.find('div', class_='ex_class')
print(result.p.text)

# d

result = bs.find('div', class_='ex_class')


# 검색된 div 태그 내의 모든 p태그를 조회
for tag in result.find_all('p'):
    print(tag.text)

# d
# e
# f
```

## 태그 내의 속성값 출력

```
result = bs.find('a', class_='a')
print(result.get('href'))
# http://brownbears.tistory.com
```



위에서 설명한 방법만으로 충분히 HTML을 파서할 수 있습니다. 더 자세한 내용은 https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 에서 확인할 수 있습니다.