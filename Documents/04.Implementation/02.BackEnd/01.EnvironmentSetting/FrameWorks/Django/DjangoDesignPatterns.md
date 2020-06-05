Don't Repeat Yourself (DRY), Loose coupling, Tight cohesion

# 어플리케이션 설계

### 요구사항 수집

1. 사용자와 직접 대화하라
2. 모든 니즈를 듣고 기록해라
3. 'models'과 같은 기술용어를 사용하지 말고 사용자 친화적이고 단순한 'user-profile'같은 용어를 사용하라
4. 올바른 기대를 심어줘라. 기술적으로 실현가능하거나 어렵지 않은경우 바로 말해줘라
5. 가능한한 스케지해서 비쥬얼적으로 표현해라 완벽할 필요는 없다.
6. 프로세스를 분해해라. 여러 단계의 기능은 화살표로 연결된 박스들로 분해해라
7. 사용자 스토리나 이해하기 쉬운 형태로 기능 리스트를 뽑아내라.
8. 기능의 우선순위를 높음, 중간, 낮음으로 분류해라
9. 새로운 기능에 대해서는 매우 보수적으로 접근해라.
10. 회의 후에는 잘못된 커뮤니케이션 방지를 위해 모두와 함께 기록한걸 공유해라

첫 회의는 아마 하루종일 이나 몇시간길이로 길겠지만 그 후 회의가 잦아지면서 30분이나 한시간정도면 될 것이다.

결과물은 **한 페이지 정도의 기록**과 몇개의 스케치다.

### 스토리 텔러

한 페이지 정도의 기록: 기술적이거나 구현에 관한 데이테일 보다는 사용자 경험에 초점을 맞춘다. 짧고 읽기에 흥미롭도록 : 재미지게

가능한한, 특정사용자로 빙의해서 직면한 문제와 어떻게 어플리케이션이 이를 해결하는지에 관해 기술해라.  친구에게 설명하듯이 기술한다.

`예시 SuperBook Script`

```
SuperBook 컨셉
다음 인터뷰는 미래에 우리의 SuperBook 웹사이트가 런칭 된다음에 수행되었다. 인터뷰전에 30분간의 사용자 테스트가 수행되었다.
:자기소개 해주세요
제 이름은 Aksel 이구요. 저는 뉴욕 시내에 살고 있는 회색 다람쥐 입니다. 따란사람들은 저를 Acorn이라고 불러요. 우리 아빠는 유명한 힙합 스타 T.Berry인데 아빠도 그렇게 불러요. 제 생각에 저는 가업을 잇기에는 노래를 잘 못하는거 같아요.
사실, 어린시절 약간 도벽이 있었구요. 아시다시피 땅콩 알러지도 있어요. 
:그래요 Acorn, 당신은 왜 사용자 테스트에 선정되었다고 생각하나요?
아마도, 제가 NY Start special에 덜 알려준 슈퍼히오로로 소개되어서인거 같아요. 사람들이 다람쥐가 맥북을 사용할수 있다는걸 신기하게 생각하는 거 같아요 (interviewer: 이 인터뷰는 채팅으로 했다). 더군다나 저는 다람쥐들에게 주목받고 있어요.
:당신이 본것을 기초로 해서, SuperBook에 대한 당신의 의견은 어때요?
대단한 아이디어 같아요. 사람들이 항상 슈퍼히어로를 볼수 있다는점이 말이에요. 그런데 아무도 대부분의 슈퍼히어로들이 외롭고 사회부적응인걸 신경쓰지 않아요. SuperBook은 그걸 바꿀 수 있을 거에요.
:다른 의견은?
우리같은 사람들을 위해 처음부터 만들어 진거 같아요. 제 말은 당신이 익명을 사용하고 싶을때 직업과 학력같은건 넌센스잖아요? 난 그런게 없다구요. 나도 이런걸 이해하는데 다른 사람은 어떻겠냐구
:당신이 알아챈 기능을 간단하게 말해줄래요?
그래요, 나는 이게 최근에 만들어진 소셜 네트워크라고 생각해요
- 아무런 사용자 이름으로 가입을 하고 (실제 이름을 더이상 입력할 필요가 없어요)
- 팬들은 다른 사람들을 친구로 추가하지 않아도 팔로우 할 수 있어요
- 포스팅을 하고 거기에 코멘트를 달수도 있고 이를 다른사람이게 다시 공유할 수 있어요
- 사적인 포스트를 다른 사용자에게 보낼 수 있어요
모든게 쉽고, 이를 사용하는데 특별한 노력이 필요하지 않아요
: 시간 내줘서 고마워요 Acorn

```

### HTML mockups

옛날에는 목업 하는데 포토샵하고 플래쉬를 써서 pixcel 단위로 퍼팩트하게 만들었는데 더이상 권장되지 않는 방법이다.

사실상 대부분의 디자이너들은 HTML에 레이아웃을 직접 생성한다.

CSS 프레임웍인 Bootstrap 이나 ZURB Foundation framework 같은거 써서 예쁘게 만들 수 있다.

목업을 만드는 목적은 웹사이트의 현실적인 프리뷰를 만드는 것이다. 디테일이 완벽할 필요는 없다 그냥 정적인 HTML 파일과 동작하는 링크 그리고 간단한 자바스크립트 인터랙션이면 된다.

20%의 노력을 기울여 80%의 사용자 경험을 목업할 수 있으면 좋은 목업이다.

### 어플리케이션 설계

만들것에 대한 좋은 아이디어가 있을때, 바로 코딩하지 말고 생각해라. 

어떤 방법들이 있지? 트레이드 오프가 어떻게 될까? 컨텍스트에서 어떤 요소거 더 중요한가? 어떤 접근방법이 최고인가?

써드파티로 구현할 수 있나? 어떤 디자인패턴이 설계를 위해 좋을까?

### 프로젝트를 App으로 나누기

Django application = Project

Project = App + App + ... + App (약 15 ~ 20개)

App = Python Package : 재사용 가능한 기능 집합

### 재사용할까? 만들까?

SuperBook에서 사용할 인증용 3rd-pary package에 대한 고려

- python-social-auth: 소셜 로그인이 필요치 않으므로 탈락
- django-facebook: 특정 웹사이트가 제공하는 인증에 의존이 되므로 탈락
- djang-allauth: 의존성 있는 패키지 python-openid가 유지보수가 활발하지 않으므로 탈락
- Redis나 Node.js 같은 Python이 아닌 것에 대한 의존성이 존재하는 경우 탈락
- 재사용 불가능한 패키지

이런 패키지들이 나쁜것이 아니라 단지 우리의 니즈에 맞지 않기 때문에 django 내장 auth app으로 결정

반면에 아래와 같은 이유로 3rd 파티를 선호할 수 있다.

Too hard to get right: Do your model's instances need to form a tree?
Use dj ango-mptt for a database-effcient implementation
• Best or recommended app for the job: This changes over time but packages
such as dj ango-redis are the most recommended for their use case
• Missing batteries: Many feel that packages such as dj ango-model-utils
and dj ango-extensions should have been part of the framework
• Minimal dependencies: This is always good in my book

### 샌드박스

별도의 sandbox 가상환경을 만들어서 3rd  파티를 적용해 테스트해보고 이해도가 생기면 GIT으로 기존 프로젝트의 브랜치를 따서 적용한다. 

### 패키지분리

프로세스를 그려보면 SUperBook 프로젝트는 러프하게 다음과 같은 app으로 나뉜다.(완성은 아님)

- Authentication (내장 django.auth): 사용자 가입, 로그인, 로그아웃 핸들링
- Accounts(자체제작): 사용자 정보 관련 추가기능
- Posts(자체제작): 포스팅 및 코멘트 기능
- Pows(자체제작): 요소들이 얼마나 많은 좋아요를 받았는지 추적
- Bootstrap form(crispy-forms): 폼 레이아웃 및 스타일링

상기리스트는 개발도중 변할 수 있음

### 프로젝트 시작전에

- 가상환경준비: venv, conda 등
- 버전 컨트롤 : Git, Mercurial 등
- 프로젝트 템플릿 선정
  - [two scoops](https://github.com/twoscoops/django-twoscoops-project)
  - [edge](https://github.com/arocks/edge) 등등
- 배포환경 : Fabric, Ansible 등

## 모델

### 모델이 뷰나 컨트롤러보다 큼

모델은 Djanog에서 데이터베이스를 객체지향으로 다루는 방법을 제공한다(쿼리 자동생성)

모델 클래스 = 데이터베이스 테이블

클래스 속성 = 테이블 컬럼

모델은 model admins, model forms, generic view의 기초가 된다.

모델은 의존성을 최소화는게 중요하다 뷰같은거 임포트 하지 말어라

### 모델사냥

- 사용자는 1개의 프로필을 갖는다

  - 사용자 1 : 프로필 1

- 사용자는 여러개의 코멘트와 여러개의 포스팅을 할 수 있다 

  - 사용자 1 : 코멘트 *
  - 사용자 1 : 포스트 *
  - 포스트 1 : 코멘트 *

- 좋아요는 한 사용자와 한 포스트의 조합으로 연결된다.

  - 사용자 1 : 좋아요 *
  - 포스트 1 : 좋아요 *

  이를 바탕으로 엔티티 다이어그램을 그리는 것은 권장된다. 이 단계에서 속성은 필요 없고 나중에 추가하면 된다. 프로젝트 전체를 나타내는 다이어그램을 그리고 이는 app을 분리하는것에 도움이된다.

다이어그램

- 박스는 엔티티를 내타내고 이는 모델이 된다.

- 명사는 보통 결국 엔티티가 된다.

- 화살표는 양방향이고 셋 중 한 관계를 나타낸다

  - 1 : 1
  - 1 : * (외래키로 구현)
  - *: *

  *쪽 entity에 외래키를 정의한다.

```python
class Profile(models.Model):
    user = models.OneToOneField(User)
    
class Post(models.Model):
    posted_by = models.ForeignKey(User)
    
class Comment(models.Model):
    commented_by = models.ForeignKey(User)
    for_post = models.ForeignKey(Post)
    
class Like(models.Model):
    liked_by = models.ForeignKey(User)
    post = models.ForignKey(Post)
```

### 모델을 여러파일로 쪼개기

`app/models/postable.py, post.py, comment.py`

`app/models/__init__.py`

```python
from postable import Postable
from post import Post
from comment import Comment
```

### 구조화 패턴

모델 설계 및 구조화를 위한 설계 패턴

#### Normalized models

문제점:  모델이 데이터 일관성 위반을 야기할 수 있는 중복 데이터를 갖는다.

해결책: 정규화를 통해 모델을 더 작은 모델로 쪼개고 논리 관계로 둘을 연결한다.

##### 문제점

Post 테이블 설계시 다음과 같이 한다면, (다른 컬럼 생략)

| Superhero Name    | Message                      | Posted on        |
| ----------------- | ---------------------------- | ---------------- |
| Captain Temper    | Has this posted yet?         | 2012/07/07 07:15 |
| Professor English | It should be 'Is' not 'Has'. | 2012/07/07 07:17 |
| Captain Temper    | Has this posted yet?         | 2012/07/07 07:18 |
| Capt. Temper      | Has this posted yet?         | 2012/07/07 07:19 |

맨 마지막 줄이 슈퍼히어로의 이름 일관성을 위반했다.

Captain Temper Vs Capt. Temper 

##### 해결책

테이블 정규화 3단계: 5단계까지 있지만 보통 3단계 까지만 하고 성능 때문에 역정규화도 한다.

정규화는 효율적으로 데이터를 저장할 수 있도록 돕는다. 모델이 완전히 정규화 되면, 군더더기 데이터가 없어지고, 각 모델은 논리 관계로 엮인 데이터만 포함하게 된다.

##### 정규화예제

| Name      | Orign       | Power                  | First Used At(Lat, Lon, Country, Time)                       |
| --------- | ----------- | ---------------------- | ------------------------------------------------------------ |
| Blitz     | Alien       | Freeze<br />Flight     | +40.75, -73.99; USA; 2014/07/03 23:12<br/>+34.05, -118.24; USA; 2013/03/12 11:3 |
| Hexa      | Scientist   | Telekinesis<br/>Flight | +35.68, +139.73; Japan; 2010/02/17 20:15<br/>+31.23, +121.45; China; 2010/02/19 20:30 |
| Traveller | Billionaire | Time-travel            | +43.62, +1.45, France; 2010/11/10 08:20                      |

###### 제 1정규화

- 컬럼에 값은 1개만
  - Power 컬럼에 값이 여러개 있으므로 이를 위반하고 있다.
- PK는 컬럼의 조합 또는 1개 컬럼으로만

| Name*     | Orign       | Power*      | Latitude  | Longitude  | Country | Time                 |
| --------- | ----------- | ----------- | --------- | ---------- | ------- | -------------------- |
| Blitz     | Alien       | Freeze      | +40.75170 | -73.99420  | USA     | 2014/07/03<br/>23:12 |
| Blitz     | Alien       | Flight      | +40.75170 | -73.99420  | USA     | 2013/03/12<br/>11:30 |
| Hexa      | Scientist   | Telekinesis | +35.68330 | +139.73330 | Japan   | 2010/02/17<br/>20:15 |
| Hexa      | Scientist   | Flight      | +35.68330 | +139.73330 | Japan   | 2010/02/19<br/>20:30 |
| Traveller | Billionaire | Time-travel | +43.61670 | +1.45000   | France  | 2010/11/10<br/>08:20 |

###### 제 2정규화

- 제 1정규화 조건을 모두 만족해야 한다.
- PK가 아닌 모든 컬럼은 PK전체에 의존적이어야 한다.
  - Orign은 Name에는 의존적이지만 Power에는 독립적이기 때문에 룰 위반이다.
  - 따라서, Orign은 별도의 테이블로 분리한다.
- *A는 B에 의존성이 있다. 의존적이다 : B에 의해 A가 정해진다.

Orign

| Name*     | Orign       |
| --------- | ----------- |
| Blitz     | Alien       |
| Hexa      | Scientist   |
| Traveller | Billionaire |

Sighting

| Name*     | Power*      | Latitude  | Longitude  | Country | Time                 |
| --------- | ----------- | --------- | ---------- | ------- | -------------------- |
| Blitz     | Freeze      | +40.75170 | -73.99420  | USA     | 2014/07/03<br/>23:12 |
| Blitz     | Flight      | +40.75170 | -73.99420  | USA     | 2013/03/12<br/>11:30 |
| Hexa      | Telekinesis | +35.68330 | +139.73330 | Japan   | 2010/02/17<br/>20:15 |
| Hexa      | Flight      | +35.68330 | +139.73330 | Japan   | 2010/02/19<br/>20:30 |
| Traveller | Time-travel | +43.61670 | +1.45000   | France  | 2010/11/10<br/>08:20 |

###### 제 3정규화

- 제 2정규화 조건을 모두 만족해야 한다.
- PK가 아닌 모든 컬럼은 PK전체에 의존적이지만 그외 컬럼에는 독립적이어야 한다.
  - Country컬럼은 Latitude와 Longtitude에 의해 결정되기 때문에 그외 컬럼에 독립적이지 못해서 룰 위반
  - 테이블 분리한다.

Location

| Location ID | Latitude* | Longitude* | Country |
| ----------- | --------- | ---------- | ------- |
| 1           | +40.75170 | -73.99420  | USA     |
| 2           | +35.68330 | +139.73330 | Japan   |
| 3           | +43.61670 | +1.45000   | France  |

Sighting

| User ID* | Power*      | Location ID | Time                 |
| -------- | ----------- | ----------- | -------------------- |
| 2        | Freeze      | 1           | 2014/07/03<br/>23:12 |
| 2        | Flight      | 1           | 2013/03/12<br/>11:30 |
| 4        | Telekinesis | 2           | 2010/02/17<br/>20:15 |
| 4        | Flight      | 2           | 2010/02/19<br/>20:30 |
| 7        | Time-travel | 3           | 2010/11/10<br/>08:20 |

Django 에서는 조합키를 지원하지 않으므로 Meta클래스에서 unique_together 속성을 적용한다.

```python
class Origin(models.Model):
    superhero = model.ForeignKey(settings.AUTH_USER_MODEL)
    origin = models.CharField(max_length=100)
    
class Location(models.Model):
    latitude = models.FloatField()
    longtitude = models.FloatField()
    
    class Meta:
        unique_together = ("latitude", "longitude")
        
class Sighting(models.Model):
    superhero = models.ForeignKey(settings.AUTH_USER_MODEL)
    power = models.CharField(max_length=100)
    location = models.ForeignKey(Location)
    sighted_on = models.DateTimeField()
    
    class Meta:
        unique_together = ("superhero", "power")
```

###### 역정규화

정규화는 성능에 불리한 영향을 끼칠 수 있다. 모델 갯수가 증가하면서 필요한 조인 쿼리도 증가하게된다. 예를 들면 USA에서 Freeze 능력을 갖고 있는 슈퍼히어로 수를 찾으려면 테이블 4개를 조인해야 한다. 정규화 전에는 모든 정보를 한 테이블에서 찾을 수 있었다.

설계시에는 정규화를 유지하다가 성능이 안나오면 역정규화할 데이터를 끌어내고 이를 역정규화 테이블에 매번 업데이트 해준다.

역정규화는 대규모 사이트에서 매우 일반적이다

##### 항상 정규화해야 하나?

너무 많은 정규화는 좋지 못하다. 

사용자 모델에 집주소를 위한 필드가 여러개 있을 수 있다. 엄격히 말하면 이 필드들을 주소 모델로 정규화 할 수 있으나 대부분 이는 불필요하다.

#### Model mixins

문제점: 구분되는 모델들이 같은 필드나 메서드를 갖고 있는 것은 DRY 원칙에 위배된다.

해결책: 공통된 필드와 메서드를 다양하고 재사용가능한 model mixins으로 추출한다.

##### 문제점

모델을 설계하는 동안, 아마 모델 클래스간에 공통된 속성이나 행위를 발견할 수 있을것이다. 예를들면, `Post`와 `Comment`모델은 `created`날짜와 `modified`날짜를 항상 기록해야 한다. 수기로 해당 필드들과 또 관련된 메서드를 컨씨 컨브이 하는 것은 DRY접근에 위배되게 된다.

Django 모델은 클래스이기 때문에 상속과 조합같은 객체지향 접근법이 가능한 해결책일 수 있다. 그러나, 조합은 필드에 간접적으로 접근하는 추가적인 레벨이 필요하게된다.

`Post와 Comments`를 위한 상속 베이스 클래스로 Django에서 3가지 종류를 사용할 수 있다. `concrete, abstract, proxy`

Concreate: 일반적인 상속, base클래스는 별도의 분리된 테이블과 매핑되기 때문에 베이스 필드에 접근할때마다 묵시적인 join이 필요하게되므로 끔찍한 성능이슈가 발생하게 된다.

Proxy: 부모 클래스에 새로운 행위만 추가 가능하고 새로운 필드는 추가할 수 없으므로 이러한 상황에서는 그닥 쓸모 없다.

Abstract:  이걸로 가즈아~!

##### 해결책

추상 베이스 클래스는 모델간에 데이터와 행위들을 공유하는 좋은 방법이다. 추상 클래스를 정의해도 데이터베이스에 실제로 해당하는 물리 테이블이 생성되지 않는다. 대신 추상 클래스를 상속받는 클래스에 필드들이 생성된다. 

추상 베이스 클래스 필드에 접근하는 것은 `join`이 필요하지 않는다 그 결과, 테이블들 내부에서만 필드들이 관리될 수 있다. 이러한 개이득 때문에, 대부분의 Django 프로젝트들은 추상 베이스 클래스를 공통 필드 또는 메서드를 구현하는데 사용한다. 

추상 베이스 클래스의 제약

- 외래키나 many to many 필드를 갖을 수 없다.
- 객체화 또는 저장될 수 없다.
- 매니저가 없기 때문에 쿼리에서 직접적으로 사용될 수 없다.

```python
class Postable(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    message = models.TextField(max_length=500)
    
    class Meta:
        abstract = True
        
class Post(Postable):
    ...
    
class Comment(Postable):
    ...
    
    
```

모델을 추상 베이스 클래스로 변환하기 위해서는 `Meta` inner 클래스에 `abstract = True`를 언급해줘야 한다. 이제 `Postable` 추상 베이스 클래스가 만들어졌다 하지만 재사용적이지는 못하다.

사실, `created`와 `modified`필드만 있었으면 타임스탬프가 필요한 거의 모든 모델에서 사용할 수 있다. 이러한 케이스에서 model mixin 을 정의한다.

##### Model mixins

Model mixins는 추상 클래스로서 모델에 부모 클래스로서 추가 될 수 있다. 파이썬은 java와 같은 언어와는 다르게 다중 상속을 지원하므로, 모델을 위한 부모 클래스를 갯수와 상관없이 열거할 수 있다. 

Mixins은 직교성이 있어야 하고 쉽게 조합가능해야 한다. Mixins은 이런 행위면에서 상속보다는 composition에 좀 더 가깝다. 끼워넣는 느낌

작은 mixins일 수록 낫다. mixin이 단일 책임원책을 위배하고 점덤 더 커질때마다 좀 더 작은 클래스로의 리팩토링을 고려해야 한다. mixin을 하나만 잘하도록 해야 한다.

이전 예제에서 model mixin을 개선해보자

```python
class TimeStampedModel(models.Model)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now = True)
    
    class Meta:
        abstract = True
        
class Postable(TimeStampedModel):
    ...
    
    class Meta:
        abstract = True
        
class Post(Postable):
    ...
    
class Comment(Postable):
    ...

```

이렇게 두개의 베이스 클래스로 나눌 수 있고 각각 기능은 명확하게 분리된다. 또 mixin은 재사용 가능해졌다.

#### User profiles

문제점: 모든 웹사이트는 다른 집합의 사용자 프로필 정보를 저장한다. 그러나 Django의 내장 User 모델은 인증 정보용 모델이다.

해결책: 사용자 프로필 클래스를 생성해서 user 모델과 one to one 관계로 연결한다.

##### 문제점

Django는 그나마 최신의 user model을 제공한다. 이를 super user생성이나 admin 인터페이스에 로그인 할 때 사용할 수 있따. full name, username, e-mail 같은 몇 개의 기본 필드를 가지고 있다.

근데 실제 프로젝트에서는 사용자에 대해 주소, 좋아하는 영화 또는 초능력 등의 무척 다양한 정보를 저장해야 한다. Django 1.5부터는 기본 user모델을 확장하거나 대체할 수 있게 되었다. 그러나 공식 문서는 커스텀 유저 정보 조차도 인증 데이터만 저장할 것을 강력하게 권고하고 있다.

특정 프로젝트는 다양한 타입의 사용자가 필요하다 예를 들면 SuperBook은 슈퍼히어로와 일반인이 있을 수 있다. 사용자 종류에 따라 공통된 필드도 있고 구별되는 필드도 있다.

##### 해결책

공식적으로 권장되는 해결책은 user profile model을 생성하는 것이다. 이 모델은 user-model과 one-to-one 관계를 맺어야 한다. 모든 추가적은 사용자 정보는 user profile model에 저장된다.

```python
class Profile(modelsModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
```

PostgreSQL같은 백엔드 데이터베이스에서의 병렬성 이슈를 예방하기위해 `primary_key`를 명시적으로 `True`로 설정해주는것이 권장된다. 나머지 모델의 나머지 부분은 생일, 좋은하는 색 같은 사용자 정보를 포함하면 된다.

profile model을 정의할때 모든 필드는 null값이나 defualt값을 허요하게 해서 사용자가 가입할때 모든 칸을 채울필요가 없게 해야 하고 profile 객체를 만들때 signal 핸들러도 초기 파라메터를 넘기지 않도록 보증한다.

##### Signals

user model 객체가 생성도때마다 상응하는 user profile 객체도 생성되어야 한다. 이는 signals를 사용해서 구현할 수 있다.

예를들면, user model에서 다음 signal 핸드러를 이용해서 `post_save` signal을 listen할 수 있다.

`signals.py`

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from . import models

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender, instance, created, **kwargs):
    if not created:
        return
    # Create the profile object, only if it is newly created
    profile = models.Profile(user=instance)
    profile.save()
```

참고로, profile model은 user 객체 외에 추가적인 초기 파라메터를 받지 않는다.

이전에, singal 코드의 초기화를 위한 특정 위치가 없었다. 보통 models.py에 임포트 되거나 구현되었다. 그러나, Django1.7부터 어플리케이션 초기화 코드 위치가 잘 정의되었다.

먼저, App의 `__init__.py`에

```python
default_app_config = "profiles.apps.ProfileConfig"
```

app.py에 있는 ProfileConfig 메서드를 서브클래싱하고 signal을 ready 메서드에 셋업한다. 

```python
from django.apps import AppConfig

class ProfileConfig(AppConfig):
    name = "profiles"
    verbose_name = 'User Profiles'
    
    def ready(self):
        from . import signals
```

이제 user.profile은 Profile 객체를 리턴한다.

##### Admin

현재 사용자 정보가 admin 페이지에 두개로 별도 분리되어 있어서 성가시므로, 편의를 위해 커스텀 UserAdmin을 정의하도록 한다.

`admin.py`

```python
from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model = Profile
    
class UserAdmin(admin.UserAdmin):
    inlines = [UserProfileInline]
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
```

##### Multiple profile Types

어플리케이션에서 여러 종류의 사용자 프로필이 필요하다고 가정하자. 사용자가 가져야할 프로필 종류를 기록해야할 필드가 필요하다. 프로필 데이터 자체는 별도의 모델이나 통합된 모델에 저장되어야 한다.

Aggregate 프로필 접근법을 사용하면, 프로필 정보의 유실이나 족잡도를 최소화 하면서 프로필 종류를 변경할 수 있는 유연성을 가져갈 수 있다.

예를 들면, SuperBook은 `SuperHero`타입의 프로필과 `Ordinary`타입의 프로필이 필요하게 된다. 이는 다음과 같은 싱글 통합 프로필을 사용해서 구현할 수 있다.

```python
class BaseProfile(models.Model):
    USER_TYPES = (
    (0, 'Ordinary'),
    (1, 'SuperHero'),
    )
    user = models.OneToOneFiled(settings.AUTH_USER_MODEL, primary_key=True)
    user_type = models.IntegerField(max_length=1, null=True, choices=USER_TYPES)
    bio = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return "{}: {:.20}". format(self.user, self.bio or "")
    
    class Meta:
        abstract = True

class SuperHeroProfile(models.Model):
    origin = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        abstract = True
        
class OrdinaryProfile(models.Model):
    address = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        abstract = True
        
class Profile(SuperHeroProfile, OrdinaryProfile, BaseProfile):
    pass
        
```

관심사 분리를 위해 프로필 정보를 여러개의 추상 베이스 클래스로 그룹화했다. `BaseProfile`클래스는 사용자 종류를 개의치 않는 공통된 프로필 정보를 포함한다. `user_type`으로 사용자의 프로필을 기록한다. 

`SuperHeroProfile`클래스와 `OrdinaryProfile`클래스는 슈퍼히어로와 일반사람에 특정된 프로필 정보를 포함한다. 그리고 `profile`클래스는 이 모든 베이스 클래스로부터 유도되어 프로필 정보의 합집합을 생성한다.

- 모든 프로필 정보 필드들은 nullable하거나 디폴트값이 있어야 한다.
- 이 접근법은 데이터베스 공간을 좀더 소모하지만 어마무시한 유연함을 제공한다
- active user type에 따라 입력할 폼을 달리 보여줘야 한다.

#### Service Objects

문제점: 모델이 덩치가 거대해져서 관리불가하게 될 수 있다. 테스트와 유지보수는 모델이 한가지 이상의 일을 할 수록 더 빡쎄진다.

해결책: 연관된 메소드들을 특화된 Service Object로 빼낸다.

##### 문제점

Django 초보에게 Fat models, Thins views는 겪언처럼 전해진다. View에는 프레젠팅 로직 이외에는 아무것도 있으면 안된다. 

그러나, 시간이 갈수록 갈 곳을 잃은 코드 조각은 models로 들어가는 경향이 있다. 곧. 모델은 코드들의 쓰레기장이 된다. 

다음과 같은 상황들이 닥치면 모델은 Service Object를 사용해야 하는 징조다.

- 외부 서비스와 인터랙션한다. 예를들면, 웹서비스를 이용해서 사용자가 SuperHero 프로필 을 얻을 자격이 있는지 확인
- DB와 상관없는 Helper tasks가 필요하다. Short URL을 만든다거나 랜덤 cpatcha를 만든다거나
- 데이터베이스 상태가 없는 짧게 사는 객체와 관련이 있는경우, Ajax 호출을 위한 JSON 응답 만들기 등
- Celery 태스트 같은 여러 인스턴스들과 연관되어 오래 실행되는 타스크

Django의 Model은 Active Record 패턴을 따른다. 이 패턴은 모델이 비지니스 로직과 디비접근을 둘 다 캡슐화 하도록 한다. 그러나 비지니스 로직은 최소로 유지해야 한다.

테스팅 도중에 사용하지 않더라도 디비를 모킹해야 한다는걸 발견하고 모델 클래스를 쪼개는것을 고려했다. Service Object가 권장된다.

##### 해결책

Service Object는 Plain old Python Objects( POPOs)이다. 보통 `services.py`나 `utils.py`로 별도의 파일로 분리된다.

예를들어 웹서비스 검사가 모델 메서드로 들어오는 때가 있다.

```python
class Profile(models.Model):
    ...
    def is_superhero(self):
        url = "http://api.herocheck.com/?q={0}".format(self.user.usnername)
        return webclient.get(url)
```

이를 서비스 오브젝트를 사용하도록 리팩터해보자

```python
from .services import SuperHeroWebAPI

    def is_superhero(self):
        return SuperHeroWebAPI.is_hero(self.user.username)
```

`services.py`

```python
API_RL = "http://api.herocheck.com/?q={0}"

class SuperHeroWebAPI:
    ...
    @staticmethod
    def is_hero(username):
        url = API_URL.format(username)
        return webclient.get(url)
```

대부분의 경우, 서비스 오브젝트의 메서드는 stateless 하다. 즉. 다른 클래스 속성과는 무관하게 함수의 파라메터로만 기능을 수행한다. 결국 static 메서드의 명확한 징조다.

비지니스 로직 또는 도메인 로직을 모델 밖으로 끄집어네서 서비스 오브젝트로 리팩토링 하는 것을 고려해라.

비지니스적인 이유로 사용자 이름으로 슈퍼히어로가 되는 것을 막는 블랙리스트가 있다고 가정하자. 우리 서비스 오브젝는 이를 지원할 수 있게 쉽게 수정될 수 있따

```python
class SuperHeroWebAPI:
    ...
    @staticmethod
    def is_hero(username):
        blackist = set(["syndrome", "kcka$$", "superfake"])
        url = API_URL.format(username)
        return username not in blacklist and webclient.get(url)
```

서비스 객체는 의존성이 없기에 db목킹없이 쉽게 테스트 할 수 있고 재사용할 수 있다.

Django에서는 시간이 걸리는 서비스는 Celery같은 태스크 큐를 사용해서 비동기로 실행한다. 오브젝트 액션은 Celery tasks로서 실행된다. 그런 tasks는 주기적으로나 딜레이 이후에 실행할 수 있다.

### 획득 패턴

#### Property field

문제점: 모델은 속성을 갖고 있고 이는 메서드로 구현된다. 그러나 이 속성들은 데이터베이스에 영구저장되어야 한다.

해결책: 해당 메서드에 property 데코레이터를 사용한다.

##### 문제점

모델 필드는 first name, last name, 생일 등 객체 속성을 저장한다. 그것들은 디비에 저장된다. 그러나 그 속성들로부터 유도되는 full name 이나 age 같은 속성들에 대한 접근도 필요하다.

그것들은 디비 필드에서 쉽게 계산될수 있다 결국, 독립적으로 저장될 필요가 없다. 몇몇 경우, 나이나 멤버쉽 포인트 활동상태 등에 근거한 자격요건 검사에 사용할 수 있는 조건이 될 수 있다.

get_age 와 같이 함수로 정의하여 구현할 수 있다

```python
class BaseProfile(models.Model):
    birthdate = models.DataField()
    # ...
    def get_age(self):
        today = datetime.date.today()
        return (today.year = self.birthdate.year) - int(
        		(today.month, today.day) <
        		(self.birthdate.month, self.birthdate.day))
```

 profile.get_age() 호출은 사용자의 나이를 계산해서 리턴한다.

그러나, profile.age로 접근하는게 훨씬 가독성 있다

##### 해결책

```python
@property
def get(self):
```

이러면, profile.age 로 접근가능

QuerySet 객체에는 사용불가. 즉. Profile.objects.exclude(age__lt=18)은 불가능

디미터의 법칙: 클래스위 내부 디테일을 감추기위해 property를 정의한다.

디미터의 법칙은 다수의 래퍼 프로퍼티를 생성하는 부작용이 있으므로 모델의 API를 개선하거나 결합도를 줄이는 선에서 적당히 사용한다.

##### Cached Properties

property를 호출할때마다 함수는 재계산을 하므로 비용이 높은 계산이라면 결과를 캐싱하는게 좋다. 그래야 다음번에 프로퍼티에 접근할때 캐싱한 결과를 반환한다.

```python
from django.utils.functional import cached_property
    #...
    @cached_property
    def full_name(self):
        # 외부 서비스 호출은 고비용이다
        return "{0} {1}".format(self.firstname, self.lastname)
```

캐싱된 값은 파이썬 인스턴스가 존재하는한 그 일부로 저장되었다가 리턴된다.

호출할때 cached=Falase를 전달하면 캐싱된 값 전달대신 계산한다.

#### Custom model managers

문제점: 모델에 대한 특정한 쿼리가 정의되고 코드를 통해 반복적으로 접근되면 DRY 법칙 위배다

해결책: 공통된 쿼리에 custom manager를 정의하고 의미있는 이름을 부여하라

##### 문제점

모든 Django 모델은 기본 매니저인 objects를 갖고있다. objects.all()을 실행하면 디비에 있는 모들의 모든 엔트리를 리턴한다. 우리는 항상 모든 엔트리의 부분집합에만 관심이 있다.

우리가 필요한 엔트리 집합을 찾아내기 위해 다양한 필터를 적용한다. 그것들을 선택하는 기준은 종종 우리의 코어 비지니스 로직이된다. 예를 들면 퍼블릭에게 접근될 수 있는 posts를 찾아내는 코드는 다음과 같을수 있따.

```
public = Posts.objects.filter(privacy="public")
```

이 기준은 나중에 변할 수 있다. 포스트가 편집중인 상태인지도 체크해볼 수 있다.

```
public = Posts.objects.filter(privacy=POST_PRIVACY.Public, draft=False)
```

그러나 해당 변경은 public 포스트가 필요한 모든곳에서 이루어져야 할 필요가 있다. 그래서 이런 공통적으로 사용되는 쿼리는 한곳에서만 정의되어야 한다.

##### 해결책

QuerySets은 엄청 강력한 추상화이다. 필요할때 lazy하게 평가된다. 결국 메서드 체이닝에 의해 길게 길게 만들어진 QuerySets는 퍼포먼스에 영향이 그닥 없다

사실, 필터들이 많이 적용될 수록 결과 데이터 셋은 줄어든다. 이는 항상 결과의 메모리 소비를 줄이게된다. 

모델 매니저는 QuerySet 객체를 얻기위한 편리한 인터페이스이다. 다른말로, 모델 매니저는 Django ORM를 사용해서 디비에 접근하는 것을 돕는다. 사실. 매지너는 QuerySet 객체를 감싸는 매우 작은 래퍼로 구현된다.

```
Post.objects.filter(posted_by__username="a")

Post.objects.get_queryset().filter(posted_by__username="a")
```

Django에 의해 성성된 기본 매니저 objects는 QuerySets을 리턴하는 all, filter, exclude 등의 여러 메서드를 갖고 있다. 그러나 이들은 디비에 대한 낮은 레벨의 API 형태이다.

Custom 매니저는 도메인에 특화된 높은 레벨의 API를 생성하는데 사용된다. 이는 더 가독성이 있고 구현 디테일어 더 낮은 영향도가 있다. 결국, 도메인에 가깝게 모델링된 높은 수준의 추상화에 대해서 다룰 수 있게 한다.

이전에 살펴봤던 public 포스트를 custom manager로 변환해보면

```python
# managers.py
from django.db.models.query import QuerySet

class PostQuerySet(QuerySet):
    def public_posts(self):
        return self.filter(privacy="public")
    
PostManager = PostQuerySet.as_manager
```

때때로 기본 objects 매니저를 custom 매니저로 교체하기도 한다

```python
from .managers import PostManager
class Post(Postable):
    ...
    objects = PostManager()
```

이렇게 함으로써, public_posts에 접근이 매우 단순해진다.

```python
public = Post.objects.public_posts()
```

리턴값이 QuerySet이기 때문에 결과에 필터를 더 할 수도 있다.

```
public_apology = Post.objects.public_posts().filter(message_startswith="Sorry")
```

##### 집합연산 on QuerySets

QuerySets 연산

```python
q1 = User.objects.filter(username__in=["a","b","c"])
q2 = User.objects.filter(username__in=["c", "d"])

from django.db.models import Q

#합집합
User.objects.filter(Q(username__in=["a","b","c"]) | Q(username__i=["c","d"]))

#교집합
User.objects.filter(Q(username__in=["a","b","c"]) & Q(username__i=["c","d"]))

#차집합
User.objects.filter(Q(username__in=["a","b","c"]) | ~Q(username__i=["c","d"]))
```

##### QuerySets 연결

지금까지, 동일한 베이스 클래스의 같은 종류의 QuerySets을 합쳤다. 그러나, 서로 다른 모델의 QurySets을 합치고 조작할 필요가 있을 수 있다.

예를들면, 사용자 활동 타임라인은 그들의 모든 포스트와 코멘트를 시간역순으로 포함하고 있다. 이전에 QuerySet 결합 메서드는 동작하지 않을 것이다. 쉬운 해결책은 이것들을 리스트로 변환해서 합치고 정렬하는 것이다.

```python
recent = list(posts)+list(comments)
sorted(recent, key=lambda e: e.modified, reverse=True)
```

불행이도 이 동작은 lazy QuerySets 객체로 평가된다. 두 리스트의 메모리 사용 결합의 비용이 클 수 있고 거대한 QuerySets을 리스트로 변환하는 것은 느리다.

더 나은 해결책은 메모리 소비를 줄이기 위해 이터레이터를 사용하는 것이다. 

```python
from itertools import chain
recent = chain(posts, comments)
sorted(recent, key=lambda e: e.modified, reverse=True)
```

QuerySet을 평가할때 이비 접근 비용은 꽤 높다. 그래서 QureSets평가는 미룰수 있을때까지 미루는게 좋다.



## 4. View 및 URLs

### View Patterns

#### access controlled views

##### 문제점

페이지는 조건에따라 접근가능해야 한다 해당 사용자가 로그인상태인지 스태프인지 등등

##### 해결책

뷰의 접근제어를 하는 mixnis이나 데코레이터를 사용해라

[django-brace](https://github.com/brack3t/django-braces)

```python
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin

class UserProfileView(LoginRequireMixin, DetailView):
    # 로그인 사용자에게만 노출
    pass

class LoginFormView(AnonymouseRquireMixin, FormView):
    # 로그인 사용자에게는 비노출
    authenticated_redirect_url = "/feed"
```

mixin 만들기

```python
class CheckOwnerMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.owner == self.request.user:
            raise PermissionDenied
        return obj
```



## 6.

## 9.

## 10.

## 11.

