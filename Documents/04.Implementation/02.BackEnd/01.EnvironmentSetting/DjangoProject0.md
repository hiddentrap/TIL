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

