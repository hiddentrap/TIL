# Django Project



## Part1. Basic



### 개발환경 설정 on Windows



#### Conda

[miniconda3 x86 64bit Download](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)

**Conda update**

Anaconda prompt as administrator: 

```shell
conda update conda
```



#### IDE

VSCode, Pycharm and so on



#### GIT

[GitHub Client Download Page](https://desktop.github.com/)



#### PostgreSQL

[PostgreSQL Download Page](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)



#### 프로젝트 만들기



#### Conda 가상환경 생성

Anaconda prompt as administrator: 

```shell
conda create -n hellodjango python=3.8
conda activate hellodjango
```



#### Django 설치

Anaconda prompt as administrator: 

```shell
pip install django
```



#### Django 프로젝트 생성

Anaconda prompt as administrator: 

```shell
django-admin startproject hellodjango
```



#### 프로젝트 구조

기본구조

```
+hellodjango
	+hellodjango
        +__init__.py
        +asgi.py
        +settings.py 
        : 전역 설정파일, 모든 설정은 대문자로, 상수로 취급
        : SECRET_KEY - Django 프로젝트 생성시마다 랜덤, Django의 보안시스템에 사용
        : DEBUG - 디버깅모드 여부, 운영에선 False로 설정
        : https: //docs. djangoproject. com/en/stable/topics/settings/
        : https: //docs. djangoproject. com/en/stable/ref/settings/
        +urls.py
        +wsgi.py
+manage.py : django 명령어 실행기
```



### 프로젝트 실행



#### 데이터베이스 생성

```
python manage.py migrate
```



#### 서버실행

```
python manage.py runserver
```



#### 접속

[실행여부 확인 페이지 접속](http://127.0.0.1:8000 )



#### 서버중지

ctrl + c



#### SuperUser 계정 생성

```
python manage.py createsuperuser
```



### App 만들기

```
python manage.py startapp homepage
```



#### 프로젝트 구조

```
+hellodjango
+db.sqlite3
	+hellodjango
    	+__init__.py
    	+asgi.py
    	+settings.py 
    	: 전역 설정파일, 모든 설정은 대문자로, 상수로 취급
    	: SECRET_KEY - Django 프로젝트 생성시마다 랜덤, Django의 보안시스템에 사용
    	: DEBUG - 디버깅모드 여부, 운영에선 False로 설정
    	: https: //docs. djangoproject. com/en/stable/topics/settings/
    	: https: //docs. djangoproject. com/en/stable/ref/settings/
    	+urls.py
    	+wsgi.py
    +homepage
    	+__init__.py
    	+admin.py
    	+apps.py
    	+migrations
    		+__init__.py
    	+models.py
    	+tests.py
    	+views.py
+manage.py : django 명령어 실행기
```



#### 프로젝트 vs Apps

- 웹사이트를 실행하기 위해 필요한 모든 코드를 포함하는 폴더
- Django App은 Django 프로젝트 내부에 있는 폴더
- App은 Django 프로젝트에서 한가지 일을 하는 격리된 컴포넌트
- Django 프로젝트는 Django app들의 조합



#### 템플릿 설정

hellodjango/settings.py

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        -'DIRS': [],
        +'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

DIRS: templates 폴더 설정



#### View 추가

- Views는 Django프로젝트가 사용자와 커뮤니케이션 하는 방법이다. Veiws는 사용자에게 웹페이지, JSON, xlsx, PDF 등등을 리턴할 수 있다.

homepage/views.py

```python
from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'index.html'
```



#### URL Routing 추가

hellodjango/urls.py

```python
from homepage.views import HomepageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name='home'),
]
```



#### 템플릿 생성

- 뷰에서 웹페이지를 생성하기 위해서 HTML을 렌더링하기 위해 사용된다.
- TemplateView는 Django 템플릿을 렌더링해서 브라우저에 전송한다.

```
mkdir templates
```

templates/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Greetings</h1>
    <p>Hello, world!</p>
</body>
</html>
```

```
python manage.py runserver
```

[실행여부 확인 페이지 접속](http://127.0.0.1:8000 )



##### 템플릿에서 변수사용

templates/index.html

```html
    <p>{{ my_statement }}</p>
```



##### 템플릿에 변수 전달

homepage/views.py

```python
from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_statement'] = 'Nice to see you!'
        return context
```



##### 템플릿에서 View 메서드 호출

homepage/views.py

```python
from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_statement'] = 'Nice to see you!'
        return context
    
    def say_bye(self):
        return 'Goodbye'
```

templates/index.html

```html
    <p>{{ view.say_buy }}</p>
```



## Part2. Advance



### 개발환경 설정 on Windows

Anaconda prompt as administrator: 

```
conda create -n everycheese python=3.8
conda activate everycheese
```

#### Cookiecutter 라이브러리 설치 및 프로젝트 생성

쿠키커터는 2013년에 개발된 크로스 플랫폼 프로젝트 템플릿 제네레이터로 보일러플레이트:변경 없이 자주 쓰이는 코드를 자동 생성해준다.

```
conda install -c conda-forge cookiecutter
cookiecutter gh:roygreenfeld/django-crash-starter
```

##### 생성된 보일러플레이트

**Readme**

프로젝트 개요: 기능설명

**Settings**

```
config/settings/
	+base.py
	: 전역적으로 동일하게 사용되는 설정
	: TIME_ZONE = 'UTC'
	: ADMINS = 
	+local.py: 로컬에서 개발 설정
	+production.py: 운영 서버 설정
```

#### 데이터베이스 생성

```
환경변수 PATH에 Postgres bin 경로 추가
로그인사용자 ID로 Postgres에 사용자 생성해 놓을 것
createdb everycheese
```

#### 로컬 개발용 의존성 패키지 설치

```
requirements
	+base.txt: 전역 의존 패키지
	+local.txt: 로컬 개발시 의존 패키지
	+production.txt: 운영환경 의존 패키지
	+test.txt: 테스트용도 의존 패키지

pip install -r requirments/local.txt
```

#### 프로젝트 마이그레이션

```
python manage.py migrate
```

#### 프로젝트 실행

```
python manage.py runserver
```

[실행여부 확인 페이지 접속](http://127.0.0.1:8000 )

#### Git Repository 등록

```
git init
git remote add origin https://github.com/hiddentrap/everycheese.git
git add .
git commit -m "'django-crash-starter'로 생성한 보일러플레이트"
git push -u origin master
git log
```



### 보일러 플레이트

#### User Model

##### User

사용자

users/models.py

```python
class User(AbstractUser):

    # First Name and Last Name Do Not Cover Name Patterns
    # Around the Globe.
    name = models.CharField(
        _("Name of User"), blank=True, max_length=255
    )

    def get_absolute_url(self):
        return reverse(
            "users:detail", kwargs={"username": self.username}
        )
```

테스트

users/tests/test_models.py

```python
import pytest

from everycheese.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"
```

- pytest: test framework
- pytestmark = test용 database
- 테스트 케이스는 `test_`로 시작

#### User View

##### UserDetailview

**사용자 정보조회**: User 객체의 정보를 디스플레이

users/views.py

```python
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These Next Two Lines Tell the View to Index
    #   Lookups by Username
    slug_field = "username"
    slug_url_kwarg = "username"
```

- LoginRequiredMixin : 로그인 사용자만 접속 가능

##### UserUpdateView

**사용자 정보수정**

users/views.py

```python
class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "name",
    ]

    # We already imported user in the View code above,
    #   remember?
    model = User

    # Send the User Back to Their Own Page after a
    #   successful Update
    def get_success_url(self):
        return reverse(
            "users:detail",
            kwargs={'username': self.request.user.username},
        )

    def get_object(self):
        # Only Get the User Record for the
        #   User Making the Request
        return User.objects.get(
            username=self.request.user.username
        )
```

- fields : form 부분에 포함되는 필드 리스트

#### User Template

##### UserDetail

templates/users/user_detail.html

```html
  <div class="col-sm-12">
    <a class="btn btn-primary" href="{% url 'users:update' %}" role="button">My Info</a>
    <a class="btn btn-primary" href="{% url 'account_email' %}" role="button">E-Mail</a>
    <!-- Your Stuff: Custom user template urls -->
  </div>
```

- `url`은 템플릿 내장 태그로 URL 이름을 URL주소로 변환한다.
- My Info 버튼은 `users`네임스페이스에 있는 `update`를 URL로 변환하고 이는 결국 `users/urls.py`에 있는 `UserUpdeateView`로 매핑된다.
- E-Mail 버튼은 `account_email`이름의 URL로 변환되고 이 이름은 allauth 패키지의 urls.py에서 찾을 수 있다. django-crash-starter는 djagno-allauth가 탑재되어 있기 때문에 allauth에 정의되어 있는 URL이름을 사용할 수 있다.

### 보일드 플레이트 코드수정 예시

예시: User에 Bio필드 추가

##### Test 작성 및 실패확인

##### Model 수정

users/models.py

```python
class User(AbstractUser):

    # First Name and Last Name Do Not Cover Name Patterns
    # Around the Globe.
    name = models.CharField(
        _("Name of User"), blank=True, max_length=255
    )
    bio = models.TextField("Bio", blank=True)

    def get_absolute_url(self):
        return reverse(
            "users:detail", kwargs={"username": self.username}
        )
```

마이그레이션 (데이터베이스에 반영)

```
python manage.py makemigrations users
python manage.py migrate users
```



##### View 수정

users/views.py

```python
class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "name",
        "bio"
    ]

    # We already imported user in the View code above,
    #   remember?
    model = User

    # Send the User Back to Their Own Page after a
    #   successful Update
    def get_success_url(self):
        return reverse(
            "users:detail",
            kwargs={'username': self.request.user.username},
        )

    def get_object(self):
        # Only Get the User Record for the
        #   User Making the Request
        return User.objects.get(
            username=self.request.user.username
        )
```



##### Template 수정

templates/users/user_detail.html

```html
  <div class="row">
    <div class="col-sm-12">

      <h2>{{ object.username }}</h2>
      {% if object.name %}
        <p>{{ object.name }}</p>
      {% endif %}
      {% if object.bio %}
        <p>{{ object.bio|linebreaksbr }}</p>
      {% endif %}
    </div>
  </div>
```

##### Test 성공확인

```
coverage run -m pytest
```

테스트시 warning 제거를 원할경우: pytest.ini에 '-p no:warnings'

```
coverage report
```

`coverage.py`툴로 테스트 되지 않은 코드 커버리지를 확인한다.

```
coverage html
```

`htmlcov/index.html` 생성



##### Commit

```
git status
git add -A
git commit -m "Add bio field to User model, views, templates"
git push origin master
```

### App 추가

#### App 생성 및 위치이동

```
python manage.py startapp cheeses
mv cheeses everycheese/
```

#### 설정

everycheese/cheeses/apps.py

```python
name = 'everycheese.cheeses'
```

base.py

```
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
```

- `DJANGO_APPS`: Django 코드베이스의 코어 부분을 담당하는 Apps (건드릴일 없음)

- `THIRD_PARTY_APPS`: 파이썬 패키지 인덱스에있는 재사용가능한 Django Apps

- `LOCAL_APPS`: users app 같은 개발앱

  그러므로 `LOCAL_APPS`에 추가

  ```python
  LOCAL_APPS = [
      "everycheese.users.apps.UsersConfig",
      'everycheese.cheeses.apps.CheesesConfig',
      # Your stuff: custom apps go here
  ]
  ```

#### Model 추가

cheeses/models.py

```python
from autoslug import AutoSlugField
from django.db import models
from model_utils.models import TimeStampedModel


class Cheese(TimeStampedModel):
    class Firmness(models.TextChoices):
        UNSPECIFIED = "unspecified", "Unspecified"
        SOFT = "soft", "Soft"
        SEMI_SOFT = "semi-soft", "Semi-Soft"
        SEMI_HARD = "semi-hard", "Semi=Hard"
        HARD = "hard", "Hard"

    name = models.CharField("Name of Cheese", max_length=255)
    slug = AutoSlugField(
        "Cheese Address",
        unique=True,
        always_update=False,
        populate_from="name",
    )
    description = models.TextField("Description", blank=True)
    firmness = models.CharField(
        "Firmness", max_length=20,
        choices=Firmness.choices,
        default=Firmness.UNSPECIFIED,
    )

    def __str__(self):
        return self.name

```

`TimeStampedModel`: 오브젝트가 생성되었거나 수정되었을때 자동으로 추적하는 `created`와 `modified`필드를 자동으로 추가한다.

`AutoSlugField`: friendly-URL(SEO) 

```
<title>What is a slug?</title> 제목을 www.example.com/article/what-is-a-slug 주소로 저장
```

`Firmness`: enum class

#### DB 마이그레이션

Cheese 모델에 대한 데이터베이스 테이블 생성

```
python manage.py makemigrations cheeses
python manage.py migrate cheeses
```

##### 샘플데이터 생성

| DJango Shell                                          | Shell Plus                                                   |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| manage.py에 기술된 Django설정을 로드하는 Python Shell | 추가로 Django model class들을 로딩하는 shell로 Django Shell + `from everycheese.cheeses.models import Cheese`와 같다 |

```
python manage.py shell_plus
cheese = Cheese.objects.create(
name = 'Colby',
description = 'Similar to Cheddar but without undergoing the cheddaring process',
firmness = Cheese.Firmness.SEMI_HARD,
)
```

##### commit

```
git status
git add everycheese/cheeses/
git add config/settings/base.py
git commit -m "Add cheeses app"
git push origin master
```

#### Test 작성

##### 테스트 커버리지 확인

```
coverage run -m pytest
coverage report
coverage html
```

커버되지 않은 코드확인

```python
    def __str__(self):
        return self.name
```

##### Cheese Model을 위한 테스트 모듈 작성

- 기본생성된 `cheeses/tests.py` 삭제
- `tests/` 폴더 및 `tests/__init__.py`, `tests/test_models.py` 생성

##### 테스트 작성

tests/test_models.py

```python
import pytest
from ..models import Cheese

# Connects our tests with our database
pytestmark = pytest.mark.django_db


def test___str__():
    # Given
    cheese = Cheese.objects.create(
        name="Stracchino",
        description="Semi=sweet cheese that goes well with starches.",
        firmness=Cheese.Firmness.SOFT,
    )

    # When - Then
    assert cheese.__str__() == "Stracchino"
    assert str(cheese) == "Stracchino"
```

##### 테스트 실행

```
coverage run -m pytest
coverage report
coverage html
```

##### Commit

```
git add -A
git commit -m "Add cheese model tests"
git push origin master
git log --oneline
```

##### Django SuperUser 등록

```
python manage.py createsuperuser
```

##### Cheese 모델을 Admin에 등록

cheeses/admin.py

```python
from django.contrib import admin
from .models import Cheese

admin.site.register(Cheese)

```

##### Admin 에서 Cheese 추가

```
Camembert
A French cheese with a white, powdery rind and a soft, delicately salty interior
Soft

Gouda
A Dutch yellow cheese that develops a slight crunchiness and a complex salty toffee-like flavor as it ages
Hard

Cheddar
A relatively hard, pale yellow to off-white, and sometimes sharp-tasting cheese.
Hard
```

##### Commit

```
git commit -am "Register Cheese model with the admin"
git push origin master
```



#### List 작성

##### View 작성

###### Class Based View

- The Simplest Class-Based View
- Advantages of Class-Based Views
- Tips for Writing Class-Based Views

**가장 단순한 클래스 뷰**

```python
from django.http import HttpResponse
from django.views.generic import View

# Class-Based View
class MyView(view):

	def get(self, request, *args, **kwargs):
		return HttpResponse('Response to GET request')
    
    def post(self, request, *args, **kwargs):
        return HttpResponse('Response to POST request')
    
    def delete(self, request, *args, **kwargs):
        return HttpResponse('Response to DELETE reuqest')
    
# Function-Based View #1
def my_view(request, *args, **kwargs):
    if request.method == 'POST':
        return HttpResponse('Response to POST request')
    elif request.method == 'DELETE':
        return HttpResponse('Response DELETE request')
    return HttpResponse('Response GET request!!')

# Function-Based View #2
def my_view(request, *args, **kwargs) :
	METHOD_DISPATCH = {
        'POST' : HttpResponse('Response POST request! ' ), 
        'DELETE' : HttpResponse('Response DELETE request! ' ),
    }
	DEFAULT = HttpResponse('Response GET request!' )
	return METHOD_DISPATCH. get(request. method, DEFAULT)
```

**Classed-Based Views의 장점**

Mixin 은 클래스에 추가적인 속성이나 메소드를 제공하는 것을 말함

- 조합

  - 다중상속을 통한 클래스 조합이 가능하다: 다중상속시 ClassA(하위, 상위, 더상위) 순서
  - 다양한 오픈소스 패키지들을 확장해서 사용가능하다.

- Intelligent Defaults

  ```python
  from django. views. generic import UpdateView
  from . models import Item
  
  class ItemUpdateView(UpdateView):
      
  	model = Item
  	fields = ['name' ,'description' ,'price']
  ```

  - Item과 Fields를 기초데이터로 form을 자동 생성한다.
  - items/item_form.html
  - 템플릿에서 item 또는 object로 Item 레코드에 접근할 수 있다.

- 표준화된 HTTP 메서드 핸들링

  ```python
  from django. http import HttpResponse
  from django. views. generic import View
  
  	class SpecialView(View):
          
          def delete(self, request, *args, **kwargs):
              return HttpResponse('HTTP deletes!' )
          
          def post(self, request, *args, **kwargs):
              return HttpResponse('HTTP posts!' )
  ```

  - GET, PUT, OPTIONS등 핸들링되지 않은 요청에 대해서는 405를 반환한다.

**Tips for Class-Based Views**

- 기본값을 고수해라
- 다중상속을 이상하게 사용하지마라
- 인증 및 다른 행위: django-braces
- [quick reference](https://ccbv.co.uk)
- GET/POST 파라메터는 self.kwargs안에 있다.
- self.request로 request에 접근할 수 있다.



###### Cheese List View 작성

`cheeses/views.py`

```python
from django.views.generic import ListView, DetailView
from .models import Cheese


class CheeseListView(ListView):
    model = Cheese

```

##### Url - View 매핑

`everycheese/cheeses/urls.py`생성

```python
from django.urls import path
from . import views

app_name = "cheeses"
urlpatterns = [
    path(
        route='',
        view=views.CheeseListView.as_view(),
        name='list'
    ),
]
```

`config/urls.py`

```python
    path(
        "cheeses/",
        include("everycheese.cheeses.urls", namespace="cheeses")
    ),
```

##### 템플릿 작성

`templates/cheeses/cheese_list.html`생성

```html
{% extends "base.html" %}
{% block title %}Cheese List{% endblock title %}
{% block content %}
  <h2>Cheese List</h2>

<ul>
  {% for cheese in cheese_list %}
    <li><a href="#TODO">{{ cheese.name }}</a></li>
  {% endfor %}
</ul>
{% endblock content %}
```

##### 메뉴연결

`templates/base.html`

```html
        <li class="nav-item">
          <a class="nav-link" href="{% url 'cheeses:list' %}">Cheeses</a>
        </li>
```

**commit**

```
git add -A
git commit -m "Add cheese list page, add navbar link"
git push origin master
git log --oneline
```

#### Detail 작성

##### View 작성

`cheeses/views.py`

```python
class CheesetailView(DetailView):
    model = Cheese
```



##### Url - View 매핑

`everycheese/cheeses/urls.py`생성

```python
path(
	route='<slug:slug>/',
    view=views.CheeseDetailView.as_view(),
    name='detail'
),
```

##### 템플릿 작성

`templates/cheeses/cheese_list.html`

```html
{% extends "base.html" %}
{% block title %}Cheese List{% endblock title %}
{% block content %}
  <h2>Cheese List</h2>

<ul>
  {% for cheese in cheese_list %}
    <li><a href="{% url 'cheeses:detail' cheese.slug %}">{{ cheese.name }}</a></li>
  {% endfor %}
</ul>
{% endblock content %}
```

`templates/cheeses/cheese_list.html`생성

```html
{% extends "base.html" %}

{% block title %}Cheeses: {{ cheese.name }}{% endblock %}

{% block content %}

<h2>{{ cheese.name }}</h2>

{% if cheese.firmness %}
  <p>Firmness: {{ cheese.get_firmness_display }}</p>
{% endif %}

{% if cheese.description %}
  <p>{{ cheese.description }}</p>
{% endif %}

{% endblock content %}
```

**commit**

```
git add -A
git commit -m "Add cheese detail page"
git push origin master
git log --oneline
```

#### 테스트용 데이터 생성기 작성

- [factoryboy documentation](https://factoryboy.readthedocs.io/)
- [github for factoryboy](https://github.com/FactoryBoy/factory_boy)

`cheeses/tests/factories.py`

```python
from django.template.defaultfilters import slugify

import factory
import factory.fuzzy

from ..models import Cheese


class CheeseFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.lazy_attribute(lambda obj: slugify(obj.name))
    description = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    firmness = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Cheese.Firmness.choices]
    )

    class Meta:
        model = Cheese
```

`CheeseFactory`는 `Cheese`객체(모델 인스턴스)를 생성하며 이는 `Cheese.objects.create()`라고 생각해도 무방하다

- `name`: `FuzzyText()`를 사용하여 자동생성
- `slug`: `name`을 `slugify`
- `description`: 랜덤하게 생성된 문단
- `firmness`: 선택지중에서 랜덤하게 선택된다

**테스트용 더미데이터 생성**

```
python manage.py shell_plus
from everycheese.cheeses.tests.factories import CheeseFactory
cheese = CheeseFactory()
cheese
```

- 생성된 더미데이터는 admin에서 삭제한다.

##### 테스트용 데이터 생성기 사용법

**명시적인 필드값을 이용한 생성**

```python
cheese = CheeseFactory(name="Sample Cheese From Factory")
```

**대량 데이터 생성: 10개 생성 예**

```python
for x in range(10):
	CheeseFactory(name=f"Sample Cheese {x}")
```

**생성 데이터 확인**

```python
Cheese.objects.all()
```

**생성 데이터 삭제**

```python
Cheese.objects.filter(name__startswith='Sample').delete()
```



**Commit**

```
git status
git add -A
git commit -m "Add a cheese factory: test dummy data generator"
git push origin master
git log --oneline
```

##### 테스트 리팩터링

**1차**

`tests/test_models.py`

```python
import pytest
from ..models import Cheese
from .factories import CheeseFactory

# Connects our tests with our database
pytestmark = pytest.mark.django_db


def test___str__():
    # When
    cheese = CheeseFactory(name="Stracchino")

    # Then
    assert cheese.__str__() == "Stracchino"
    assert str(cheese) == "Stracchino"

```

**테스트실행**

```
coverage run -m pytest
```

**2차**

`tests/test_models.py`

```python
import pytest
from ..models import Cheese
from .factories import CheeseFactory

# Connects our tests with our database
pytestmark = pytest.mark.django_db


def test___str__():
    # When
    cheese = CheeseFactory(name="Stracchino")

    # Then
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name

```

**테스트실행**

```
coverage run -m pytest
```

**Commit**

```
git add -A
git commit -m "Refactore test___str__() with CheeseFactory"
git push origin master
git log --oneline
```

### APP에 새로운 기능 추가

#### 3rd-party App 추가

- Cheese model에 country field 추가

- 치즈가 기원된 국가: `country_of_origin`

  - 구현전략 #1: `CharField`로 정의하고 입력받는다.

    ```python
    country_of_origin = models.CharField("Country of Origin", max_length=255)
    ```

  - **구현전략 #2:  선택가능한 `CharField`로 정의한다.**

    ```python
    country_of_origin = models.CharField("Country of Origin", max_length=20, choices=COUNTRY_CHOICES, default=COUNTRY_UNSPECIFIED)
    ```

    `COUNTRY_CHOICES`는 선택가능 국가 리스트를 사실상 유지보수하기 힘드므로 3rd-party를 사용한다.

**Django 패키지 검색**

[Django Packages](https://djangopackages.org) : grid

**GitHub에서 사용법 익히기**

**PyPI에서 버젼 번호 가져오기** [PyPi](https://pypi.org/project/), [info](https://pypi.org/project/django-countries)

**패키지 설치**

`requirements/base.txt`

```
django-countries==6.1.2 # https://pypi.org/project/django-countries
pip install -r requirements/local.txt
```

로컬개발, 테스트, 운영환경 모두에서 사용할 수 있도록 base에 추가한다.

`settings/base.py`

```python
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_countries", # CountryField
]
```

#### Model 수정

`cheeses/models.py`

```python
from django_countries.fields import CountryField
class Cheese(TimeStampedModel) :
...
country_of_origin = CountryField("Country of Origin", blank=True)
```

`CountryField`는 `CharField`의 확장이다. Django에서는 empty값을 저장할때 NULL이 아닌 empty값을 사용하므로 null=True로 설정하지 않는다.

**마이그레이션**

```
python manage.py makemigrations cheeses
python manage.py migrate
```

**국가지정**

```
Cheddar - 영국
Gouda - 네덜란드
Camembert - 프랑스
Colby - 미국
```



#### 템플릿 수정

`templates/cheeses/cheese_detail.html`

```python
{% if cheese.country_of_origin %}
<p>Country of Origin: {{ cheese.country_of_origin.name }}
  <img src="{{ cheese.country_of_origin.flag }}"/>
</p>
{% endif %}
```



### Django-crash-starter

##### 이메일발송

settings/local.py: 로컬 개발환경 설정 - 실제 메일을 발송하는 대신 콘솔에 뿌려주는 Dummy

```python
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
```

settings/production.py: 운영환경 설정 - Mailgun으로 실제로 메일을 발송한다.

```python
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
```

