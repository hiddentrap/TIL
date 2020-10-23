# Arrow 날짜/시간

##### 현재시간

```python
arrow.now().format('YYYY-MM-DD')
'2020-10-23'
```

##### 날짜 계산

```python
# 10년 뒤
arrow.now().shift(years=+10).format('YYYY-MM-DD')
'2030-10-23'

# 내일
arrow.now().shift(days=+1).format('YYYY-MM-DD')
'2020-10-24'

# 3시간전
arrow.now().shift(hours=-3).format('YYYY-MM-DD hh:mm:ss')
'2020-10-23 06:08:39'
```

##### 요일

```python
# 0~6 까지의 값을 리턴, 0=월요일, ...5=토요일, 6=일요일
arrow.now().weekday()

# 1~7 까지의 값을 리턴, 1=월요일, ...6=토요일, 7=일요일
arrow.now().isoweekday()
```

##### 이번달의 마지막날

```python
arrow.now().ceil('month').date().strftime('%Y-%m-%d')
'2020-10-31'
```

##### 이번달의 첫날

```python
arrow.now().floor('month').date().strftime('%Y-%m-%d')
'2020-10-01'
```

##### 지난달의 마지막날

```python
arrow.now().floor('month').shift(days=-1).format('YYYY-MM-DD')
'2020-09-30'

arrow.now().shift(months=-1).ceil('month').format('YYYY-MM-DD')
'2020-09-30'

shift(years, months, weeks, days, hours, minutes, seconds ...)
```

##### 시간수정

```
arrow.now().replace(hour=4, miniute=10)
```

##### 휴일 체크 with holidays pacakge

```python
import holidays

# 삼일절 대체공휴일 아닌데 대체공휴일 이슈있음 제기함
red_days = holidays.Korea()
# 특정일 공휴일 체크
arrow.get('2020-01-01').date() in red_days
'2020-01-01' in red_days
# 오늘 공휴일 체크
arrow.now().date() in red_days
# 공휴일 리스트
for date, name in sorted(holidays.Korea(years=2020).items()):
    print(date, name)
# 공휴일 지정
red_days.append({"2020-10-30": "임시공휴일"})
red_days.append(['2015-07-01', '07/04/2015'])
red_days.append(date(2015, 12, 25))

with open('cal.dat', 'wb') as file:
    pickle.dump(red_days, file)
    
with open('cal.dat','rb') as file:
    red_days = pickle.load(file)

```

https://blog.naver.com/PostView.nhn?blogId=hancury&logNo=221057426711

https://jinseyou.tistory.com/5



##### 기타사용법

```python
# 세계표준시
arrow.utcnow()
<Arrow [2020-10-23T00:23:07.561669+00:00]>

# 로컬시각 한국: utcnow + 9시간
arrow.now()
<Arrow [2020-10-23T09:23:11.779048+09:00]>

# Arrow 데이터 타입으로 변환
arrow.get('2020-10-23', 'YYYY-MM-DD')
arrow.get(datetime.now())
arrow.get(2020,10,23)

#속성값
arrow.now().year
2020

# datetime 데이터 타입으로 변환
arrow.now().date()
arrow.now().time()


```

