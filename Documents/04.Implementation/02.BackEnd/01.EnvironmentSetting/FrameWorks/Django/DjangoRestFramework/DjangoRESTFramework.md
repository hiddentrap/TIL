# Django RESET Framework

Front-End와 Back-End를 분리하면 얻을 수 있는 장점

- 프론트 엔드는 빠르게 변화하지만 백엔드는 재개발을 잘하지 않는다.
- one source multi use
- API는 외부 공개도 가능하다.

단점

- 모놀리스틱 보다 설정이 더 필요하다.

## Concepts, C1

### 목표

- APIs와 HTTP 프로토콜의 소개

### 용어정리

- web APIs: endpoints, resources, HTTP verbs, HTTP status codes, REST
- URLs: 인터넷에 있는 자원의 주소, ex) https://www.google.com /about/
  -  **scheme** : Https, Http, ftp, smtp and so on
  - **hostname**: www.google.com
  - (optional) **path**: /about/
- A **Client** **requests** information and a **server** responds with a **response** over **HTTP**
- client - server connecton flow
  1. Get IP address with domain name via Domain Name Service
  2. TCP Connects (신뢰성, 순서보장, 에러체킹 on Application Layer) handshake
     1. Send SYN asking for connection
     2. receive SYN-ACK with connection parameter
     3. Send ACK back to confirm the connection
  3. Communication via HTTP
- **HTTP Verbs**: 모든 웹페이지는 URL과 함께 승인되는 행위 목록을 가지고 있고 이를 HTTP Verbs라 한다.
  - CRUD(Create, Read, Update, Delete) - HTTP Verbs(POST, GET, PUT, DELETE)
- **Endpoints**: APIs가 사용가능한 actions 목록, **URLs + HTTP Verbs**
  - https://www.mysite.com/api/users: 
    - **GET** returns all users as list aka. **collection**
    - **POST** adds user
  - https://www.mysite.com/api/users/<id>: 
    - **GET** returns a single user
    - **DELETE** removes a single user
- **HTTP**: TCP 연결을 맺은 양단간의 요청-응답 프로토콜
  - HTTP message = request/response-status line + headers + optional body data
- **Stauts Codes**: 상태코드
  - 2xx 성공: 요청성공, 200 OK, 201 Created
  - 3xx 리다이렉션: 요청이 이동됨, 301 Moved permanently
  - 4xx 클라이언트 에러: 보통 잘못된 URL 요청, 404 Not Found
  - 5xx 서버 에러: 요청 해석 에러, 500 Server Error
- **Statelessness**: 무상태 프로토콜
  - 하나의 요청/응답 쌍은 이전의 요청/응답 쌍과 완전하게 무관하다.
  - state라 불리는 과거에 행해진 상호작용을 저장하지 않는다.
- **REST**: RESTful API는 최소한, 
  - HTTP처럼 무상태이다.
  - 일반적인 HTTP verbs (GET, POST, PUT, DELETE etc)를 지원한다.
  - JSON 또는 XML 포맷으로 데이터를 리턴한다.

## APP: Library, C2

### 목표

- 전통적인 Django App인 Library에 Django REST Framework API를 추가함으로써 차이점 살펴보기 

#### 전통적인 Django APP

##### 프로젝트 생성

###### Conda 가상환경 생성

Anaconda prompt as administrator: 

```shell
conda create -n hellodjango python=3.8
conda activate hellodjango
```

###### Django 설치

Anaconda prompt as administrator: 

```shell
pip install django
```

###### Django 프로젝트 생성

Anaconda prompt as administrator: 

```shell
django-admin startproject library_project
```

###### DB마이그레이션 및 서버실행

```
(library) $ python manage.py migrate
(library) $ python manage.py runserver
```



##### APP 생성

```
(library) $ python manage.py startapp books
```

- admin.py: Django 내장 Admin app 설정파일
- apps.py: app 설정파일
- migrations/: 데이트베이스 변경에 대한 마이그레이션 파일 저장 폴더
- models.py: 데이터베이스 모델 정의
- tests.py: app에 국한된 테스트
- views.py: web app에 대한 request/responst 로직처리
- urls.py (수동생성필요): app에 대한 url 라우팅 정의



###### 프로젝트에 APP설치

`library_project/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'books.apps.BooksConfig',
]
```

###### Model 추가

`books/models.py`

```python
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title

```

**마이그레이션**: 추후 디버깅 편의를 위해서 makemigrations할때는 APP별로 해주는게 좋다

```
(library) $ python manage.py makemigrations books
(library) $ python manage.py migrate
```



###### 프로젝트 관리자 생성

```
(library) $ python manage.py createsuperuser
```

###### 내장 Admin에 Model 등록

`books/admin.py`

```python
from django.contrib import admin

from books.models import Book

admin.site.register(Book)
```

```
(library) $ python manage.py runserver
http://127.0.0.1:8000/admin/
Django for Beginners
Build websites with Python and Django
William S. Vincent
978-198317266
```



###### View 생성

`books/views.py`

```python
from django.views.generic import ListView

from .models import Book


class BookListView(ListView):
    model = Book

    template_name = 'book_List.html'
```



###### URLs 생성

프로젝트 레벨: `library_project/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
]
```

App 레벨: `books/urls.py`

```python
from django.urls import path

from .views import BookListView

urlpatterns = [
    path('', BookListView.as_view(), name='home')
]
```

사용자가 홈페이지 접속시 `library_project/urls.py`에 의해서 `books/urls.py`로 가게된다. 거기에서 `BookListView로` 연결되게 되고 다시 `book_list.html`로 이동한다.

- `books/templates/books/book_list.html`



###### 템플릿 생성

`books/templates/books/book_list.html`

```html
<h1>All books</h1>
{% for book in object_list %}
    <ul>
        <li>Title: {{ book.title }}</li>
        <li>Subtitle: {{ book.subtitle }}</li>
        <li>Author: {{ book.author }}</li>
        <li>ISBN: {{ book.isbn }}</li>
    </ul>
{% endfor %}
```



#### Django REST Framework

##### 설치

```
pip install djangorestframework
```

`settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd party
    'rest_framework',
    
    # Local
    'books.apps.BooksConfig',
    
]
```

결국, API는 모든 책들의 리스트를 JSON으로 반환하는 하나의 endpoint (URLs + HTTP Verbs)를 노출한다. 그래서

URL route, View, serializer file이 필요하다. 다른 app들이 추가되어도 모든 API와 API관련 파일들을 포함할 수 있는 API용 app을 만들 수 있다. (API APP에는 Model이 필요 없다.)



##### API APP 생성

```
python manage.py startapp api
```



###### APP 등록

`library_porject/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',

    # Local
    'books.apps.BooksConfig',
    'api.apps.ApiConfig',

]
```



###### Serializers 생성

Object to JSON 변환기

`api/serializers.py`

```python
from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'subtitle', 'author', 'isbn')
```



###### View 생성

`api/views.py`

```python
from rest_framework import generics
from books.models import Book
from .serializers import BookSerializer


class BookAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```



###### URL 생성

`library_project/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('api/', include('api.urls')),
]
```

`api/urls.py`

```python
from django.urls import path
from .views import BookAPIView

urlpatterns = [
    path('', BookAPIView.as_view()),
]
```



##### 실행

```
python manage.py runserver
curl http://127.0.0.1:8000/api/
```



## APP: Todo w React, C3 ~ C4

### 목표

- Todo API를 만들어서 React 프론트엔드와 연결해보기

### BackEnd-APIs

Django 설치, Django REST Framework 설치

`todo/backend` 폴더생성



#### 개발 환경설정

##### Conda 가상환경 생성

Anaconda prompt as administrator: 

```shell
conda create -n backend python=3.8
conda activate backend
```

##### Django 설치

Anaconda prompt as administrator: 

```shell
pip install django
```

##### Django 프로젝트 생성

Anaconda prompt as administrator: 

```shell
django-admin startproject todo_project
```

##### App 생성

```shell
python manage.py startapp todos
```

##### DB마이그레이션 및 서버실행

```
python manage.py migrate
python manage.py runserver
```

##### App 등록

`todo_project/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local
    'todos.apps.TodosConfig',
]
```

##### 서버 동작확인

```
python manage.py runserver
```



#### Model 등록

`todos/models.py`

```python
from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title
```

##### DB마이그레이션 및 서버실행

```
python manage.py makemigrations todos
python manage.py migrate
```

##### Admin App 등록

`todos/admin.py`

```python
from django.contrib import admin

from .models import Todo

admin.site.register(Todo)
```

##### 관리자 생성

```
python manage.py createsuperuser
Learn HTTP
Second item
1st todo
```



#### Django REST Framework

```
pip install djangorestframework
```

`todo_project/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',

    # Local
    'todos.apps.TodosConfig',
]
```

```python
# django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}
```

[Django REST Framework Settings](http://www.django-rest-framework.org/api-guide/settings/)

접근설정: Any 로 재정의 해봄



#### Test 작성

`todos/tests.py`

```python
from django.test import TestCase
from .models import Todo


class TodoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Todo.objects.create(title='first todo', body='a body here')

    def test_title_content(self):
        todo = Todo.objects.get(id=1)

        expected_object_name = f'{todo.title}'
        self.assertEquals(expected_object_name, 'first todo')

    def test_body_content(self):
        todo = Todo.objects.get(id=1)

        expected_object_name = f'{todo.body}'
        self.assertEquals(expected_object_name, 'a body here')

```



#### Serializers 생성

`todos/serializers.py`

```python
from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'body',)

```



#### View 생성

`todos/views.py`

```python
from rest_framework import generics

from .models import Todo
from .serializers import TodoSerializer


class ListTodo(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class DetailTodo(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

```



#### URL 생성

`todo_project/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('todos.urls')),
]
```

`todos/urls.py`

```python
from django.urls import path
from .views import ListTodo, DetailTodo

urlpatterns = [
    path('<int:pk>/', DetailTodo.as_view()),
    path('', ListTodo.as_view()),
]
```



#### 서버 동작확인

```
python manage.py runserver
http://127.0.0.1:8000/api/
http://127.0.0.1:8000/api/1/
```



#### CORS

Cross-Origin Resource Sharing: 클라이언트가 다른 도메인에 있는(a.com vs b.com 또는 a.com:3000 vs a.com:4000) API와 커뮤니케이션하는 경우 잠재적인 보안위협이 존재한다.

따라서 다른 도메인과 커뮤니케이션 할 경우에는 서버에 클라이언트로 하여금 크로스 도메인 요청을 허용하는 특정 HTTP 헤더를 초함해야 한다.

이 프로젝트는 프론트 엔드와 백엔드가 분리되어서 서로 다른 포트에서 동작하므로 설정이 필요하다.

가장 쉽게 해결하는 방법은 Django REST Framework 에서 권장하는 방법으로 적당한 HTTP 헤더를 자동으로 포함해줄 수 있도록 설정에서 미들웨어를 사용하도록 하는 것이다.

해당 미들웨어는 django-cors-headers다

##### 미들웨어 APP 설치

```
pip install django-cors-headers
```

- APP 등록
- 미들웨어 설정추가: CommonMiddleWare위에 설정해준다. (미들웨어는 Top-Bottom 순으로 로드된다.)
- CORS 화이트 리스트 설정 : 3000port는 React의 기본 포트다.

`todo_project/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'corsheaders',

    # Local
    'todos.apps.TodosConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:8000',
)

```



##### 

### FrontEnd-React

#### NodeJS 설치

[NodeJS](https://nodejs.org/en/)

#### NVM 설치

[NVM for Windows](https://github.com/coreybutler/nvm-windows/releases)

#### React App 생성

```
npx create-react-app frontend
npm start
```

#### API Data Mocking

`todo/frontend/src/App.js`

```react
import React, { Component } from 'react';

const list = [
    {
        "id":1,
        "title":"1st todo",
        "body":"Learn Django properly."
    },
    {
        "id":2,
        "title":"Second item",
        "body":"Learn Python."
    },
    {
        "id":3,
        "title":"Learn HTTP",
        "body":"It's important."
    }
]

class App extends Component {
    constructor(props) {
        super(props)
        this.state = { list };
    }

    render(){
        return(
            <div>
                {this.state.list.map(item => (
                    <div key={item.id}>
                        <h1>{item.title}</h1>
                        <p>{item.body}</p>
                    </div>
                ))}
            </div>
        );
    }
}

export default App;

```

#### BackEnd + FrontEnd

API서버에 Get 요청을 보내서 Mocking데이터 대신 실제 데이터를 가져오는데는 2가지 방법이 있다. 내장 Fetch API와 axios. 근데 보통 axios쓴다.

##### axios 설치

```
npm install axios
```

보통 npm 명령어 뒤에 --save 플래그를 붙여서 package.json에 의존성을 저장하려고 하는데 최근 버전의 npm에서는 기본적으로 붙기 때문에 --save플래그를 생략해서 쓴다.

##### App.js 수정

- axios를 이용해서 GET request를 한다. 이를 위해서 getTodos 함수를 만든다.
- mocking된 list를 제거한다

`src/App.js`

```react
import React, {Component} from 'react';
import axios from 'axios';

class App extends Component {
    state = {
        todos: []
    };

    componentDidMount() {
        this.getTodos();
    }

    getTodos() {
        axios
            .get('http://127.0.0.1:8000/api/')
            .then(res => {
                this.setState({todos: res.data});
            })
            .catch(err => {
                console.log(err);
            });
    }

    render() {
        return (
            <div>
                {this.state.todos.map(item => (
                    <div key={item.id}>
                        <h1>{item.title}</h1>
                        <p>{item.body}</p>
                    </div>
                ))}
            </div>
        );
    }
}

export default App;

```



## APP: Blog, C5 ~ C9

### 목표

- 완전한 CRUD 기능을 비롯한 권한, 인증, viewsets, 라우터, 문서화 기능을 갖춘 Blog API 만들어보기
- CRUD APIs
- Log-in, Log-out APIs
- Sign up for accounts APIs 
- Viewsets
- Routers
- Documentation



#### Blog API 개발

##### 개발 환경설정

```
conda create -n blogapi python=3.8
conda activate blogapi
pip install django
django-admin startproject blog_project
python manage.py startapp posts

blog/project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local
    'posts.apps.PostsConfig',
]

python manage.py migrate
```



##### Model 생성

`posts/models.py`

```python
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

```

```
python manage.py makemigrations posts
python manage.py migrate
```

##### Admin 등록

`posts/admin.py`

```python
from django.contrib import admin

from .models import Post

admin.site.register(Post)

```

```
python manage.py createsuperuser
python manage.py runserver

admin
Hello World!
This is my first blog post.
```

##### Tests 작성

로그인된 사용자가 포스팅 할 수 있는지 테스트

`posts/tests.py`

```python
from django.test import TestCase

from django.contrib.auth.models import User

from .models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 사용자 생성
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc123'
        )
        testuser1.save()

        # 사용자 포스팅
        test_post = Post.objects.create(
            author=testuser1, title='Blog title', body='Body content...'
        )
        test_post.save()

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        author = f'{post.author}'
        title = f'{post.title}'
        body = f'{post.body}'

        self.assertEqual(author, 'testuser1')
        self.assertEqual(title, 'Blog title')
        self.assertEqual(body, 'Body content...')

```

```
python manage.py test
```

##### REST API 작성 (R)

- REST Framework 설치
- 데이터 직렬화 ( to JSON)을 위한 serializers.py
- 로직 적용을 위한 views.py
- URL 라우팅을 위한 urls.py

```
pip install djangorestframework

blog_project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd
    'rest_framework',

    # Local
    'posts.apps.PostsConfig',
]

REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.AllowAny'
	]
}
```

##### Serializer 작성

`posts/serializers.py`

```python
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'body', 'created_at',)
        model = Post

```



##### View 작성

- ListAPIView : read-only endpoint **collection**
- RetrieveAPIView: read-only **single** endpoint
- ListCreateAPIView: **read-write** endpoint
- RetrieveUpdateDestroyAPIView: **read**, **updated** or **deleted** **single** endpoint

`posts/views.py`

```python
from rest_framework import generics

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

```



##### URL 작성

`blog_project/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
]

```

API 버저닝은 좋은 전략이다. 수정을 많이 하면 다양한 API소비자느 이를 업데이트 하는데 지연시간이 생길수 있기 때문인데. 버저닝을 하면 v2가 런칭되는 동안 v1을 사용할 수 있기 때문이다. 

`posts/urls.py`

```python
from django.urls import path
from .views import PostList, PostDetail

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view()),
    path('', PostList.as_view()),
]

```

```
python manage.py runserver

Allow 항목을 확인해보면 사용가능한 action을 알수 있다.
GET: 조회, POST: 여러개 포스팅, PUT: 하나 포스팅/수정, DELETE: 삭제
```

#### 

#### 접근권한 설정

- 프로젝트 레벨
- 뷰 레벨
- 모델 레벨

##### 테스트용 사용자 생성

```
admin에서 새로운 사용자 testuser 생성
```

##### API에 로그인 추가

`blog_project/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

http://127.0.0.1:8000/api/v1/ : 오른쪽 상단에 log-in 관련 생김
```

현재는 `blog_project/settings.py`에 기본접근권한이 `AllowAny`로 설정되어 있어 로그인하지 않아도 접근

##### View Level Permission

`posts/views.py`

```python
from rest_framework import generics, permissions

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

http://127.0.0.1:8000/api/v1/ : 로그인 하지 않고는 접근 불가 HTTP 403 Forbidden
```

##### Project Level Permission

- AllowAny - 인증여부와 관계없이 누구나 접근가능
- IsAuthenticated - 로그인된 사용자만 접근가능
- IsAdminUser - 관리자만 접근가능
- IsAuthenticatedOrReadOnly - 누구나 보기 가능 but, 쓰기, 수정, 삭제는 로그인된 사용자만 가능

`blog_project/settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

```

##### 사용자정의 Permission

특정 블로그 포스트의 작성자만 해당 포스트를 수정하거나 삭제할 수 있도록.  다른 사용자에게는 Read-Only

단, 관리자는 모든 포스트에 CRUD권한을 갖는다.

이를 위해서, Custom Permission은 `rest_framework의` `permissions.BasePermission의` `has_object_permission(self, request, view, obj)`를 오버라이딩 해야 한다.

`posts/permissions.py`

```python
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # 포스트 작성자에게만 쓰기 권한부여
        return obj.author == request.user

```

`SAFE_METHODS`: GET, OPTIONS, HEAD 포함하는 튜플: read request 이므로 모두 True

그렇지 않으면, write request (생성, 수정, 삭제) 작성자만 가능하도록 함.

View에 적용

`posts/views.py`

```python
from rest_framework import generics, permissions

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

```



#### 사용자 인증

사용자 등록 + 로그인 + 로그아웃

전통적인 모놀리스틱환경에서는 세션기반 쿠키 패턴으로 구현한다.

HTTP는 무상태 프로토콜이므로 사용자가 인증되었는지 다음 요청에서 확인할 수 있는 방법이 없다. 따라서 매 HTTP요청마다 유니크한 식별자를 함께 전달해야 한다. 이를 구현하는 공통적인 접근방법은 없다.

Django REST Framework는 4가지 방법을 제공한다. 또, JSON Web Tokens과 같은 기능을 제공하는 많은 3rd 패키지가 존재하기도 한다.

4가지 방법에 대한 장단점을 비교해보고 사용자 등록, 로그인, 로그아웃을 위한 API를 만들어본다.



##### 기본인증

클라이언트가 HTTP요청을 만들때마다 **인증신용정보를** 보내도록 강제한다.

1. 클라이언트는 HTTP요청을 만든다
2. 서버는 HTTP에 401(Unauthorized) 상태코드와 인증방법을 기술하는 WWW-Authenticate  HTTP 헤더를 포함하여 보낸다
3. 클라이언트는 인증 HTTP 헤더를 통해 인증신용정보를 보낸다.
4. 서버는 인증신용정보를 체크해서 200 OK나, 403 Forbidden 상태코드를 응답한다.
5. 한번 승인되면 클라이언트는 다음 요청부터 HTTP헤더에 인증된 신용정보를 포함해서 보낸다.

**인증신용정보는** 아이디:패스워드를 Base64 인코딩한 Plain 값이다.

- 장점

  - 단순하다

- 단점

  - 모든 요청마다 서버는 사용자 이름과 패스워드를 찾아서 검증해야 한다 (비효율적임)
  - 인증신용정보가 Plain값으로 왔다리 갔다리 하기 때문에 보안에 취약하다.

  이런 이유에서, 기본인증은 HTTPS로 감싸서 사용해야 한다.



##### 세션인증

전통적인 Django 마냥 모놀리스식 웹사이트는 세션과 쿠키를 조합한 인증 스키마를 대안으로 사용해왔다. 인증신용정보(아이디/패스워드)로 클라이언트 인증을 하고 쿠키에 저장되는 세션 ID를 서버로부터 받는다. 그 후에는 HTTP 요청 헤더에 이 세션 ID를 함께 전달한다.

서버는 수신된 세션ID로 신용정보를 포함한 사용자의 모든 정보를 포함하고 있는 세션 오브젝트를 검색한다.

이 방법은 stateful하다. 서버(세션 오브젝트)와 클라이언트(세션 아이디) 양쪽에서 모두 기록이 유지되어야 하기 때문이다.

1. 사용자는 인증정보를 입력한다 (ID/PASS)
2. 서버는 해당 인증정보를 검증하고 유효할경우 DB에 저장되는 세션 객체를 생성한다(요새는 메모리)
3. 서버는 클라이언트에 세션 ID를(세션 객체가 아니다) 전송한다. 그리고 그 세션 ID는 브라우저의 쿠키에 저장된다.
4. 그 후의 모든 요청은 HTTP 헤더에 세션 ID를 포함하고 DB에 의해 검증되면 요청이 처리된다.
5. 사용자가 애플리케이션에서 로그아웃하면 세션ID는 서버와 클라이언트 모두에서 삭제된다.
6. 사용자가 다시 로그인하게되면 새로운 세션 ID가 생성되고 클라이언트의 쿠키에 저장된다. 

Django REST Framework의 기본설정은 기본인증과 세션인증의 조합이다. Django의 전통적인 세션 기반 인증 시스템이 사용되고 세션 ID가 HTTP 헤더에 포함되어 각 요청마다 기본인증을 통해 전달된다.

- 장점
  - 사용자 인증정보가 기본인증처럼 매 요청/응답 사이클마다 전송되지 않고 한번만 전송되므로 좀더 안전하다. 
  - 서버가 매번 사용자 인증정보를 검증하지 않고 매번 세션 ID로 세션 객체를 빠르게 확인하기 때문에 더 효율적이다. 
- 단점
  - 세션ID는 로그인이 수행된 브라우저 내부에서만 유효하다( 여러 도메인에서는 동작하지 않는다) 이는 여러 프론트 앤드를 지원하는 API가 필요할때 명백한 문제가 된다.
  - 세션 객체는 여러 서버로 구성된 대형 사이트에서 최신 상태로 유지되어야 한다. 서버간 세션객체의 정확성을 어떻게 유지할 것인가?
  - 이증이 필요치 않을때도 매 요청마다 쿠키가 전송된다. 이는 비효율적이다

결국, 프론트 엔드가 여러개인 API일 경우 세션기반 인증 체계를 사용하는 것은 좋지 않다.



##### 토큰인증***

토큰: 헤더(암호화방식, 타입 등) + 페이로드(서버에 보낼 사용자 데이터 등) + 유효체크값(헤더+페이로드+비밀키를 base64인코딩)

single page applications으로 인해 최근에 가장 인기있는 방법이다.

토큰 기반 인증은 stateless이다. 클라이언트가 처음에 사용자 인증정보를 서버로 한번 보낸다. 서버는 이를 검증해서 유니크한 토큰이 생성되고 클라이언트에 의해 쿠키나 로컬저장소에 저장된다. 이 토큰은 매 HTTP 요청 헤더에 포함되어 전달되고 서버는 토큰으로 사용자가 인증되었는지 체크한다 사용한다. 서버는 사용자의 기록을 유지하지 않고 단지 토큰이 유효한지 아닌지만 기록한다.

쿠키는 서버 정보를 읽을때 사용된다. 사이즈가 작고 4kb 매 HTTP 요청과 함께 자동으로 보내진다.

로컬 저장소는 클라이언트 정보를 위해 설계되었고 훨씬 크다 5120KB 그리고 토큰은 쿠키와 로컬 저장소 양쪽에 저장되고 XSS공격에 취약하다. 현재 가장 베스트 프랙티스는 토큰을 쿠키에 저장할때 httpOnly 와 Secure 쿠키 플래그를 함께 저장하는것이다.

- 장점
  - 토큰은 클라이언트에 저장되므로 서버는 세션 객체를 최신상태로 유지할 필요가 없다.
  - 토큰은 여러 프론트엔드로 공유될 수 있지만 세션은 아니다
- 단점
  - 토큰은 사용자 정보를 포함하기 때문이 토큰이 커지는 것은 퍼포먼스 이슈를 유발할 수 있다.

Django REST Framework의 내장 토큰인증은 의도적으로 단순하기 때문에 토큰 만료 기간을 설정할 수 있다. 또한 사용자 하나당 토큰 한개만 생성할 수 있다. 

JWTs는 클라이언트에 고유한 토큰을 생성하고 유효기간을 설정학 수 있고 서버 또는 3rd 파티 서비스 Auth0같은 데서 생성할 수 있다. 또 JWT는 암호화 됤수 있어서 HTTPS가 아닌 HTTP에서도 안전하게 만들수 있따.

###### 토큰인증 설정

`blog_project/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd
    'rest_framework',
    'rest_framework.authtoken',

    # Local
    'posts.apps.PostsConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}`

python manage.py migrate
```

###### 사용자 생성,로그인아웃

**Django-Rest-Auth**

로그인, 로그아웃, 패스워드 리셋 API

```
pip install django-rest-auth
```

`blog_project/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    # Local
    'posts.apps.PostsConfig',
]
```

URL설정

`blog_project/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
]


http://127.0.0.1:8000/api/v1/rest-auth/login/
http://127.0.0.1:8000/api/v1/rest-auth/logout/
http://127.0.0.1:8000/api/v1/rest-auth/password/reset
http://127.0.0.1:8000/api/v1/rest-auth/password/reset/confirm
```

사용자 등록

```
pip install django-allauth
```

blog_project/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth',
    'rest_auth.registration',

    # Local
    'posts.apps.PostsConfig',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1

python manage.py migrate
```

URL설정

`blog_project/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
]


http://127.0.0.1:8000/api/v1/rest-auth/registration/
```

추후, 프론트 엔드에서 http://127.0.0.1:8000/api/v1/rest-auth/login/ 이 API를 통해 로그인을해서 발급받는 토큰을 쿠키나 로컬저장소에 저장해서 사용한다.

#### Viewsets and Routers

Viewset 하나로 여러개의 관련된 view를 대체할 수 있고 라우터는 URL을 자동생성할 수 있다.

목표: 여러개의 view와 URL을 더 적은 코드의 viewsets과 라우터로 래픽토링

현재까지의 API목록

| API                               | Method |
| --------------------------------- | ------ |
| /                                 | GET    |
| /:pk/                             | GET    |
| /rest-auth/registration           | POST   |
| /rest-auth/login                  | POST   |
| /rest-auth/logout                 | GET    |
| /rest-auth/password/reset         | POST   |
| /rest-auth/password/reset/confirm | POST   |

##### 사용자관리

###### Serializers

`posts/serializers.py`

```python
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'body', 'created_at',)
        model = Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)

```

###### Views

`posts/views.py`

```python
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, UserSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

```

Post와 User모델의 코드 패턴이 똑같다는것을 알 수 있다.

###### URLs

`posts/urls.py`

```python
from django.urls import path
from .views import PostList, PostDetail, UserList, UserDetail

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view()),
    path('', PostList.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]

 http://127.0.0.1:8000/api/v1/users/
```

##### Refactoring

###### Viewsets

viewset은 관련된 여러 뷰들을 하나의 클래스로 묶는것이다. 즉, 하나의 viewset으로 여러개의 view를 대체할 수 있다. 현재 4개의 view가 있다. 이를 2개의 viewset으로 대체해보자

단점은 뷰셋에 익숙하지 않은 신규 개발자들한테 가독성이 좀 떨어질 수 있다는 것이다.

`posts/views.py`

```python
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

```

ModelViewSet = list view + detail view

###### Routers

라우터는 viewsets과 함께 동작하며 URL패턴을 자동생성한다.

지금까지 만든 4개의 URL패턴을 viewset하나당 하나의 라우터로 수정한다.

3가지 종류의 라우터가 있다: SimpleRouter, DefaultRouter, CustomRouter

`posts/urls.py`

```python
from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, PostViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('', PostViewSet, basename='posts')

urlpatterns = router.urls

```

처음에는 그냥 view와 url로 시작하고 api가 복잡해지면서 중복된 코드가 반복되면 viewset과 router를 고려하자

#### 스키마 및 문서

스키마: 기계가 읽는 API 개요 문서

문서화: 스키마에 정보를 덧붙여서 사람이 읽고 사용할 수 있도록 함

현재까지의 API목록

| API                               | Method |
| --------------------------------- | ------ |
| /                                 | GET    |
| /:pk/                             | GET    |
| users/                            | GET    |
| users/:pk/                        | GET    |
| /rest-auth/registration           | POST   |
| /rest-auth/login                  | POST   |
| /rest-auth/logout                 | GET    |
| /rest-auth/password/reset         | POST   |
| /rest-auth/password/reset/confirm | POST   |

##### 스키마

Core API를 사용해서 API스키마를 만들어서 문서화 준비를 한다.

```
pip install coreapi pyyaml
```

`blog_project/urls.py`

```python
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Blog API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('schema/',schema_view),
]

```

##### 문서화

django-rest-swagger 사용

```
pip install django-rest-swagger
```

`blog_project.settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth',
    'rest_auth.registration',

    # Local
    'posts.apps.PostsConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

```

`blog_project/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

API_TITLE = 'Blog API'
API_DESCRIPTION = 'A Web API for creating and editing blog posts.'

schema_view = get_swagger_view(title=API_TITLE)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('swagger-docs/', schema_view),
]

```

```
'staticfiles' is not a registered tag library. Must be one of
해당문제는 {% load staticfiles %}이 태그가 django3.0에서 {% load static %} 이걸로 바껴서 그럼
site-packages/rest_framework_swagger/templates/rest_framework_swagger에가서 index.html을 직접 수정해줘야 함
```

**로그인/로그아웃 버튼을 위한 설정** :잘안되네 공식문서 참고바람

`blog_project/settings.py`

```python
SWAGGER_SETTINGS = {
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}
```

