# Requests

##### 기본사용

```python
import requests
URL = 'http://www.tistroy.com'
response = requests.get(URL) # get, post, put, delete, head, options
response.status_code
response.text
```

##### GET

```python
params = {'param1':'value1','param2':'value'}
res = requests.get(URL, params=params)
res.url
```

##### POST

```python
data = {'param1':'value1','param2':'value'}
res = requests.post(URL, data=data)
```

```python
import requests, json
data = {'outer':{'inner':'value'}}
res = requests.post(URL, data=json.dumps(data))
```

##### SSL without 인증

```python
url = "https://www.naver.com" 
response = requests.post(url, verify=False) 
print("status code :", response.status_code)
```

##### SSL with 인증

```python
url = "https://www.naver.com" 
response = requests.post(url, auth=("id","pass"))
print("status code :", response.status_code)
```



##### Header, Cookie

```python
headers = {'Content-Type': 'application/json; charset=utf-8'}
cookies = {'seesion_id': 'sorryidontcar'}
res = requests.get(URL, headers=headers, cookies=cookies)
```

##### Response

```
res.apparent_encoding
res.close
res.connection
res.content
res.cookies
res.elapsed
res.encoding
res.histroy
res.is_permanent_redirect
res.is_redirect
res.iter_content
res.iter_lines
res.json # 응답이 json일경우 딕셔너리로 변환
res.links
res.ok
res.raise_for_status # 응답이 200 OK가 아니면 에러발생시킴
res.raw
res.reason
res.request # 내가 보낸 request 객체에 접근
res.status_code # 응답코드
res.text
res.url
```

