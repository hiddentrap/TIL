# DJango Project

## Workflow

1. 특정 URL로 HTTP request 유입
2. URL resolving으로 해당 request를 특정 view function으로 매칭한다.
3. view function에서 해당 request를 처리하고 HTTP response를 리턴한다.

## Style Guid

[HackSoftware Styleguide](https://github.com/HackSoftware/Django-Styleguide)

단점

- 비지니스 로직을 모델에 다 때려넣다 보니..(근데 이런 방식은 Django 에서 추천하는 기본 패턴이다 [active record pattern](https://www.martinfowler.com/eaaCatalog/activeRecord.html) ) 규모가 큰 팀에서는 models.py 파일 하나에 코드가 엄청많이 있다보니 동시에 여러명이 작업하기가 매우 어려워진다. 

### OverView 2020.03.16

#### 비지니스 로직이 포함되야 할 것

- 모델 프로퍼티 (Exception 포함): @property 붙어있는 것들
- 모델 유효성 검증 메서드 (Exception 포함)
- 서비스 메서드 : DB저장
- Selectors 메서드 : DB 조회

#### 비지니스 로직이 포함되지 말아야 할 것

- API 및 VIEW
- Serializers 및 Forms
- Form 태그
- 모델 save 메서드

#### 모델 프로퍼티 vs 셀렉터

​	모델 프로퍼티가 다중 관계 (x: n)로 확장될 경우 Selector로 만드는게 낫다. 모델 프로퍼티가 list API에 추가될 경우 `select_related`로 풀기 쉽지 않은 N+1 문제를 초래할 수 있기 때문이다.

### Cookie Cutter : 프로젝트 생성툴

- 장점: 왠만한 패키지와 모듈들이 기본 세팅되서 프로젝트를 생성할 수 있다.
- 단점: Django 기본 Project Starter보다는 무겁고, 필요 없는 모듈들까지 설치된다.
- https://github.com/pydanny/cookiecutter-django

### Models

sample

```python
class Course(models.Model):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    attendable = models.BooleanField(default=True)

    students = models.ManyToManyField(
        Student,
        through='CourseAssignment',
        through_fields=('course', 'student')
    )

    teachers = models.ManyToManyField(
        Teacher,
        through='CourseAssignment',
        through_fields=('course', 'teacher')
    )

    slug_url = models.SlugField(unique=True)

    repository = models.URLField(blank=True)
    video_channel = models.URLField(blank=True, null=True)
    facebook_group = models.URLField(blank=True, null=True)

    logo = models.ImageField(blank=True, null=True)

    public = models.BooleanField(default=True)

    generate_certificates_delta = models.DurationField(default=timedelta(days=15))

    objects = CourseManager()

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date cannot be before start date!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def visible_teachers(self):
        return self.teachers.filter(course_assignments__hidden=False).select_related('profile')

    @property
    def duration_in_weeks(self):
        weeks = rrule.rrule(
            rrule.WEEKLY,
            dtstart=self.start_date,
            until=self.end_date
        )
        return weeks.count()

    @property
    def has_started(self):
        now = get_now()

        return self.start_date <= now.date()

    @property
    def has_finished(self):
        now = get_now()

        return self.end_date <= now.date()

    @property
    def can_generate_certificates(self):
        now = get_now()

        return now.date() <= self.end_date + self.generate_certificates_delta

    def __str__(self) -> str:
        return self.name
```

#### 유효성 검증

```python
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date cannot be before start date!")
```

​	유효성 검증은 `clean()`에 구현하며 모델 필드와 관계를 맺지 않는 확장에 대해서만 사용한다. clean()은 모델 인스턴스의 full_clean()에서 사용되며 full_clean()은 save()에 넣어 놓는게 좋다. 안그러면 각각 서비스에서 full_clean()을 호출해야 한다는 사실을 까먹는일이 발생한다.

#### 프로퍼티

​	visible_teachers()를 제외하고 모든 프로퍼티가 모델 필드에 직접 관계하고 있다. visible_teacher()는 selector로 고려하 필요하다.

##### 유효성 검증 가이드

- 유효성 검증이 non-relational model fields에만 의존한다면 clean()에 구현해서 full_clean() 에 포함시키고 이를 다시 save()에 포함시킨다.
- 유효성 검증이 복잡하고 관계확장이 이루어진다면, 해당 모델을 생성하는 서비스에 구현한다.
- cealn()과 서비스 양쪽에서 각각에 알맞는 유효성 검증을 수행해도 좋다.
- [Django's constraints](https://docs.djangoproject.com/en/2.2/ref/models/constraints/)를 사용할 수 있으면 사용하는게 좋다.

##### 프로퍼티 가이드

- non-relational model fields만 사용하면 프로퍼티로 만드는게 맞고
- visible_teachers() 처럼 spanning relationships가 필요하면 selector로 만드는게 맞다.

##### 메서드

- 여러 필드를 한번에 업데이트 하는 created_at 이나 created_by 같은 메서드가 필요하면 모델 메서드로 만들 수 있다
- 모든 모델 메서드는 서비스 안에서만 호출 되어야 한다.

##### 테스트

- 유효성 검증이나 프로퍼티와 같이 무엇인가 모델에 추가되었다면 테스트되어야 한다.

  유효성 검증 테스트 예제

  ```python
  from datetime import timedelta
  
  from django.test import TestCase
  from django.core.exceptions import ValidationError
  
  from project.common.utils import get_now
  
  from project.education.factories import CourseFactory
  from project.education.models import Course
  
  
  class CourseTests(TestCase):
      def test_course_end_date_cannot_be_before_start_date(self):
          start_date = get_now()
          end_date = get_now() - timedelta(days=1)
  
          course_data = CourseFactory.build()
          course_data['start_date'] = start_date
          course_data['end_date'] = end_date
  
          course = Course(**course_data)
  
          with self.assertRaises(ValidationError):
              course.full_clean()
  ```

  - get_new() 는 timezone을 인식한 datetime을 리턴한다.
  - CurseFactory.buidl()는 Course 모델을 생성하기 위한 모든 데이터를 담고 있는 dict를 리턴한다.
  - start_date와 end_date를 할당한다.
  - full_scan()을 호출하면 ValidationError가 나는지 평가한다.

  CourceFactory source

  ```python
  class CourseFactory(factory.DjangoModelFactory):
      name = factory.Sequence(lambda n: f'{n}{faker.word()}')
      start_date = factory.LazyAttribute(
          lambda _: get_now()
      )
      end_date = factory.LazyAttribute(
          lambda _: get_now() + timedelta(days=30)
      )
  
      slug_url = factory.Sequence(lambda n: f'{n}{faker.slug()}')
  
      repository = factory.LazyAttribute(lambda _: faker.url())
      video_channel = factory.LazyAttribute(lambda _: faker.url())
      facebook_group = factory.LazyAttribute(lambda _: faker.url())
  
      class Meta:
          model = Course
  
      @classmethod
      def _build(cls, model_class, *args, **kwargs):
          return kwargs
  
      @classmethod
      def _create(cls, model_class, *args, **kwargs):
          return create_course(**kwargs)
  ```

### Service

- app/services.py 모듈에 기술되어야 한다.

- keyword-only 파라메터를 받는다.

- 타입 어노테이션을 사용해야 한다. (mypy안사용해도 타입 어노테이션 사용할 것)

- 모델, 다른 서비스, 셀렉터를 사용한다.

- 간단하게 모델 생성이나, 복잡한 관점 분리, 외부 서비스나 타스크 호출등의 비지니스 로직을 수행한다.

- 사용자 생성 서비스 예

  ```python
  def create_user(
      *,
      email: str,
      name: str
  ) -> User:
      user = User(email=email)
      user.full_clean()
      user.save()
  
      create_profile(user=user, name=name)
      send_confirmation_email(user=user)
  
      return user
  ```

  모델을 생성하고 create_profile()과 send_confirmation_email() 이렇게 2개의 다른 서비스를 호출한다.

  #### Naming Convention

  ​	<action>_<entity>: create_user

### Selectors

- app/selectors.py 모듈에 기술되어야 한다.

- keyword-only 파라메터를 받는다

- 타입 어노테이션을 사용해야 한다. (mypy안사용해도 타입 어노테이션 사용할 것)

- 모델, 다른 서비스, 셀렉터를 사용한다.

- 데이터베이스로부터 데이터를 조회하는 로직을 수행한다.

- 사용자 목록 조회 셀렉터 예

  ```python
  def get_users(*, fetched_by: User) -> Iterable[User]:
      user_ids = get_visible_users_for(user=fetched_by)
  
      query = Q(id__in=user_ids)
  
      return User.objects.filter(query)
  ```

  get_visible_users_for() 는 또다른 selector이다.

  #### Naming Convention

  ​	<action>_<entity>: get_users

### APIs & Serializers

서비스와 셀럭터를 사용하는 API는 단순하고 유일해야 한다.

- 모델당 4개 API (CRUD) 즉, 오퍼레이션 당 1개 API
- 가장 심플한 APIView나 GenericAPIView를 사용해라
- API안에 비지니스 로직을 절대 집어 넣지 말고 Service나 Selector만 사용해라
- GET 또는 POST로 전달된 파라메터로부터 오브젝트를 뽑아내기 위해 serializer를 사용해라
  - InputSerializer, OutputSerializer
  - OutputSerializer는 필요하다면, ModelSerializer를 상속할 수 있다.
  - InputSerializer는 항상 Plain 한 Serializer여야 한다.
  - serializer사용은 최소화 하라
  - 중첩된 serializer라 필요하다면 inline_serializer util을 사용해라

#### Naming Convention

​	<entity><action>API: UserCreateApi, UserSendResetPasswordApi, UserDeactivateApi 등

- #### list API 예시

  ```python
  class CourseListApi(SomeAuthenticationMixin, APIView):
      class OutputSerializer(serializers.ModelSerializer):
          class Meta:
              model = Course
              fields = ('id', 'name', 'start_date', 'end_date')
  
      def get(self, request):
          courses = get_courses()
  
          serializer = self.OutputSerializer(courses, many=True)
  
          return Response(serializer.data)
  ```

- #### detail API 예시

  ```python
  class CourseDetailApi(SomeAuthenticationMixin, APIView):
      class OutputSerializer(serializers.ModelSerializer):
          class Meta:
              model = Course
              fields = ('id', 'name', 'start_date', 'end_date')
  
      def get(self, request, course_id):
          course = get_course(id=course_id)
  
          serializer = self.OutputSerializer(course)
  
          return Response(serializer.data)
  ```

- #### create API 예시

  ```python
  class CourseCreateApi(SomeAuthenticationMixin, APIView):
      class InputSerializer(serializers.Serializer):
          name = serializers.CharField()
          start_date = serializers.DateField()
          end_date = serializers.DateField()
  
      def post(self, request):
          serializer = self.InputSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
  
          create_course(**serializer.validated_data)
  
          return Response(status=status.HTTP_201_CREATED)
  ```

- #### update API 예시

  ```python
  class CourseUpdateApi(SomeAuthenticationMixin, APIView):
      class InputSerializer(serializers.Serializer):
          name = serializers.CharField(required=False)
          start_date = serializers.DateField(required=False)
          end_date = serializers.DateField(required=False)
  
      def post(self, request, course_id):
          serializer = self.InputSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
  
          update_course(course_id=course_id, **serializer.validated_data)
  
          return Response(status=status.HTTP_200_OK)
  ```

- #### 중첩된 serializer

  ```python
  class Serializer(serializers.Serializer):
      weeks = inline_serializer(many=True, fields={
          'id': serializers.IntegerField(),
          'number': serializers.IntegerField(),
      })
  ```

  inline_serializer()는 밑에 utils.py안에 있음

### Urls

- 1API 당 1URL, 1URL per action

- 도메인 별로 domain_patterns 리스트로 분리시키고 urlpatterns에 include 시킬 것

  ```python
  from django.urls import path, include
  
  from project.education.apis import (
      CourseCreateApi,
      CourseUpdateApi,
      CourseListApi,
      CourseDetailApi,
      CourseSpecificActionApi,
  )
  
  
  course_patterns = [
      path('', CourseListApi.as_view(), name='list'),
      path('<int:course_id>/', CourseDetailApi.as_view(), name='detail'),
      path('create/', CourseCreateApi.as_view(), name='create'),
      path('<int:course_id>/update/', CourseUpdateApi.as_view(), name='update'),
      path(
          '<int:course_id>/specific-action/',
          CourseSpecificActionApi.as_view(),
          name='specific-action'
      ),
  ]
  
  urlpatterns = [
      path('courses/', include((course_patterns, 'courses'))),
  ]
  ```

### Exception Handling

#### Raising Exceptions in Services / Selectors

애플리케이션의 HTTP 인터페이스와 코어 로직이 분리되어 있고 이 관점의 분리를 유지하기 위해서 서비스와 셀렉터에서 `rest_framework.exception class`를 사용하면 안된다.

서비스와 셀렉터는 예외처리를 위해 다음 중 하나를 사용한다.

- 파이썬 내장 예외처리 https://docs.python.org/3/library/exceptions.html

- `django.core.exceptions` 예외

- 둘 중 하나를 상속받은 Custom 예외

- 서비스에서 유효성 검증시 예외 발생 예제

  ```python
  from django.core.exceptions import ValidationError
  
  
  def create_topic(*, name: str, course: Course) -> Topic:
      if course.end_date < timezone.now():
         raise ValidationError('You can not create topics for course that has ended.')
  
      topic = Topic.objects.create(name=name, course=course)
  
      return topic
  ```

#### API에서 예외처리

​	서비스나 셀렉터에서 발생된 예외를 표준 HTTP응답으로 변환하기 위해서 발생된 예외를 잡아서 rest framework 가 이해할 수 있도록 해야한다.

이는 APIView의 `handle_exception`메서드에서 수행한다. 해당 메서드에서 Python/Django 예외를 Django Rest Framework 예외로 매핑시킨다.

기본적으로, DRF에 구현되어 있는 `handle_exception`메서드가 Django 내장 Http404가 `PermissionDenied` 예외를 처리하기 때문에 이는 처리할 필요가 없다.

예외처리 예제

```python
from rest_framework import exceptions as rest_exceptions

from django.core.exceptions import ValidationError


class CourseCreateApi(SomeAuthenticationMixin, APIView):
    expected_exceptions = {
        ValidationError: rest_exceptions.ValidationError
    }

    class InputSerializer(serializers.Serializer):
        ...

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_course(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
```

`get_error_message` 구현체

```python
def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc):
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg
```

이 코드를 ApiErrorsMixin으로 옮겨서 모든 API에서 중복 코드 작성을 예방한다.

ApiErrosMixin 예제

```python
from rest_framework import exceptions as rest_exceptions

from django.core.exceptions import ValidationError

from project.common.utils import get_error_message


class ApiErrorsMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    Without the mixin, they return 500 status code which is not desired.
    """
    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
```

예외처리 예제 개선판

```python
class CourseCreateApi(
    SomeAuthenticationMixin,
    ApiErrorsMixin,
    APIView
):
    class InputSerializer(serializers.Serializer):
        ...

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_course(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
```

위 코드는 utils.py에 있음

#### Error formatting

API에서 발생되는 에러 포매팅 표준화: 최종 사용자에게 javascript를 통해 보여주는 에러를 쉽게 만들기 위함

표준 시리얼라이저가 있고 그 중 한 필드에 에러가 있다면, 메세지는 아래와 같이 보여진다

```json
{
    "url": [
        "This field is required."
    ]
}
```

유효성 검증 에러 발생시 메세지: raise ValidationError('Something is wrong.')

```json
[
    "some error"
]
```

다른 에러 형식

```json
{
    "detail": "Method \"GET\" not allowed."
}
```

이렇게 3가지 에러 메시지 포매팅을 DRF가 제공하는 방법을 사용해서 일관된 형식으로 포매팅 하자.  https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling

그럼 이런식이 된다.

```json
{
  "errors": [
    {
      "message": "Error message",
      "code": "Some code",
      "field": "field_name"
    },
    {
      "message": "Error message",
      "code": "Some code",
      "field": "nested.field_name"
    },
    ]
}
```

ValidationError 발생시, field는 optional 이된다.

custom exception handler 예제

```python
from rest_framework.views import exception_handler


def exception_errors_format_handler(exc, context):
    response = exception_handler(exc, context)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    formatter = ErrorsFormatter(exc)

    response.data = formatter()

    return response
```

ErrorsFormatter()는 Utils.py에 있다.

구현된 exception handler 등록

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'project.app.handlers.exception_errors_format_handler',
    ...
}
```

ApiErrorsMixin과 결합하면 예측가는한 API 예외처리를 할 수 있다.

### Testing

#### 테스트 구조

모델, 서비스, 셀렉터&API /views 를 나눠서 테스트 한다.

```
project_name
├── app_name
│   ├── __init__.py
│   └── tests
│       ├── __init__.py
│       ├── models
│       │   └── __init__.py
│       │   └── test_some_model_name.py
│       ├── selectors
│       │   └── __init__.py
│       │   └── test_some_selector_name.py
│       └── services
│           ├── __init__.py
│           └── test_some_service_name.py
└── __init__.py
```

#### Naming Convention

- 테스트 파일 : test_the_name_of_the_thing_that_is_tested.py

- 테스트 케이스 : class TheNameOfTheThingThatIsTestedTests(TestCase)

  예제

  ```python
  def a_very_neat_service(*args, **kwargs):
      pass
  ```

  테스트 파일 이름

  ```
  project_name/app_name/tests/services/test_a_very_neat_service.py
  ```

  테스트 케이스 이름

  ```
  class AVeryNeatServiceTests(TestCase):
      pass
  ```

  utils.py 테스트 네이밍도 비슷

  ```
  project_name/common/utils.py
  project_name/common/tests/test_utils.py
  
  project_name/common/utils/files.py
  project_name/common/tests/utils/test_files.py
  ```

#### 테스트 예시 - django_styleguide

##### 샘플 모델

```python
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from djmoney.models.fields import MoneyField


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    description = models.TextField()

    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='EUR'
    )

    def __str__(self):
        return f'Item {self.id} / {self.name} / {self.price}'


class Payment(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    successful = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Payment for {self.item} / {self.user}'
```

##### 샘플 selectors

QuerySetType 구현을 위해 queryset_type.py 확인

```python
from django.contrib.auth.models import User

from django_styleguide.common.types import QuerySetType

from django_styleguide.payments.models import Item


def get_items_for_user(
    *,
    user: User
) -> QuerySetType[Item]:
    return Item.objects.filter(payments__user=user)
```

##### 샘플 services

```python
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django_styleguide.payments.selectors import get_items_for_user
from django_styleguide.payments.models import Item, Payment
from django_styleguide.payments.tasks import charge_payment


def buy_item(
    *,
    item: Item,
    user: User,
) -> Payment:
    if item in get_items_for_user(user=user):
        raise ValidationError(f'Item {item} already in {user} items.')

    payment = Payment.objects.create(
        item=item,
        user=user,
        successful=False
    )

    charge_payment.delay(payment_id=payment.id)

    return payment
```

##### services 테스트

프로젝트에서 가장 중요한 테스트이며 코드 대부분의 라인이 테스트되는 행위 테스트

- 철저한 방법으로 서비스 뒷단의 비지니스 로직이 커버될 수 잇는 테스트여야 한다.
- creating & reading 을 포함하는 database를 건드릴 수 있는 테스트여야 한다.
- 프로젝트 위부로 나가는 비동기 테스크 call을 비롯한 것은 mocking 되어야 한다.

주어진 테스트를 위해 필요한 상태를 생성하기 위해서는 아래 조합을 사용한다.

- Fakes https://github.com/joke2k/faker
- 필요한 오브젝트를 생성할 수 잇는 다른 서비스들
- 특별한 테스트 유틸리티나 헬퍼 메소드
- Factories https://factoryboy.readthedocs.io/en/latest/orms.html
- 아직 factories가 프로젝트에 도입되지 않았으면, 순수 Model.objects.create() calls

샘플 서비스 분석

```python
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django_styleguide.payments.selectors import get_items_for_user
from django_styleguide.payments.models import Item, Payment
from django_styleguide.payments.tasks import charge_payment


def buy_item(
    *,
    item: Item,
    user: User,
) -> Payment:
    if item in get_items_for_user(user=user):
        raise ValidationError(f'Item {item} already in {user} items.')

    payment = Payment.objects.create(
        item=item,
        user=user,
        successful=False
    )

    charge_payment.delay(payment_id=payment.id)

    return payment
```

- 유효성 검증을 위해 selector를 호출한다
- ORM 오브젝트를 생성한다
- 타스크를 호출한다.

샘플 서비스 테스트

```python
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django_styleguide.payments.services import buy_item
from django_styleguide.payments.models import Payment, Item


class BuyItemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Test User')
        self.item = Item.objects.create(
            name='Test Item',
            description='Test Item description',
            price=10.15
        )

        self.service = buy_item

    @patch('django_styleguide.payments.services.get_items_for_user')
    def test_buying_item_that_is_already_bought_fails(self, get_items_for_user_mock):
        """
        Since we already have tests for `get_items_for_user`,
        we can safely mock it here and give it a proper return value.
        """
        get_items_for_user_mock.return_value = [self.item]

        with self.assertRaises(ValidationError):
            self.service(user=self.user, item=self.item)

    @patch('django_styleguide.payments.services.charge_payment.delay')
    def test_buying_item_creates_a_payment_and_calls_charge_task(
        self,
        charge_payment_mock
    ):
        self.assertEqual(0, Payment.objects.count())

        payment = self.service(user=self.user, item=self.item)

        self.assertEqual(1, Payment.objects.count())
        self.assertEqual(payment, Payment.objects.first())

        self.assertFalse(payment.successful)

        charge_payment_mock.assert_called()
```

##### selectors 테스트

selectors 테스트 하는 것도 중요하다

샘플 selector 분석

```python
from django.contrib.auth.models import User

from django_styleguide.common.types import QuerySetType

from django_styleguide.payments.models import Item


def get_items_for_user(
    *,
    user: User
) -> QuerySetType[Item]:
    return Item.objects.filter(payments__user=user)
```

보시다시피 매우 직관적이고 단순한 selector이다 2~3개의 테스트로 커버할 수 있다

샘플 selector 테스트

```python
from django.test import TestCase
from django.contrib.auth.models import User

from django_styleguide.payments.selectors import get_items_for_user
from django_styleguide.payments.models import Item, Payment


class GetItemsForUserTests(TestCase):
    def test_selector_returns_nothing_for_user_without_items(self):
        """
        This is a "corner case" test.
        We should get nothing if the user has no items.
        """
        user = User.objects.create_user(username='Test User')

        expected = []
        result = list(get_items_for_user(user=user))

        self.assertEqual(expected, result)

    def test_selector_returns_item_for_user_with_that_item(self):
        """
        This test will fail in case we change the model structure.
        """
        user = User.objects.create_user(username='Test User')

        item = Item.objects.create(
            name='Test Item',
            description='Test Item description',
            price=10.15
        )

        Payment.objects.create(
            item=item,
            user=user
        )

        expected = [item]
        result = list(get_items_for_user(user=user))

        self.assertEqual(expected, result)
```

### Celery

http://www.celeryproject.org/

- 써드 파티 서비스와 커뮤니케이션 (sending emails, notifications, etc)
- HTTP사이클 밖에서 무거운 연산 작업 돌릴때
- 주기적인 타스크 (배치, Celery beat)

Celery는 프로젝트 로직과 다른 로직인것 처럼 다룬다: 비지니스 로직에 넣지 마라

예제

```python
from celery import shared_task

from project.app.services import some_service_name as service


@shared_task
def some_service_name(*args, **kwargs):
    service(*args, **kwargs)
```

서비스와 같은 이름을 갖는 실제 비지니스 로직을 담고 있는 태스크

#### 구조

##### 설정

https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

project/tasks/apps.py

```python
import os

from celery import Celery

from django.apps import apps, AppConfig
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')


app = Celery('project')


class TasksConfig(AppConfig):
    name = 'project.tasks'
    verbose_name = 'Celery Config'

    def ready(self):
        app.config_from_object('django.conf:settings', namespace="CELERY")
        app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    from celery.utils.log import base_logger
    base_logger = base_logger

    base_logger.debug('debug message')
    base_logger.info('info message')
    base_logger.warning('warning message')
    base_logger.error('error message')
    base_logger.critical('critical message')

    print('Request: {0!r}'.format(self.request))

    return 42
```

##### Tasks

태스크는 각각 app에 tasks.py에 있다.

API, 서비스, 셀렉터와 마찬가지로 tasks가 너무 커지면 도메인별로 나눈다. 즉

tasks/domain_a.py, tasks/domain_b.py처럼 나누고 tasks/`__init__`.py에서 import해서 Celery가 인식할 수 있게 해준다.

#### 주기적 태스크

[Celery Beat](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html) + django_celery_beat.schedulers:DatabaseScheduler + [django-celery=beat](https://github.com/celery/django-celery-beat) 사용

project.tasks.management.commands.setup_periodic_tasks.py

```python
from django.core.management.base import BaseCommand
from django.db import transaction

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask

from project.app.tasks import some_periodic_task


class Command(BaseCommand):
    help = f"""
    Setup celery beat periodic tasks.

    Following tasks will be created:

    - {some_periodic_task.name}
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print('Deleting all periodic tasks and schedules...\n')

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                'task': some_periodic_task
                'name': 'Do some peridoic stuff',
                # https://crontab.guru/#15_*_*_*_*
                'cron': {
                    'minute': '15',
                    'hour': '*',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                },
                'enabled': True
            },
        ]

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(
                **periodic_task['cron']
            )

            PeriodicTask.objects.create(
                name=periodic_task['name'],
                task=periodic_task['task'].name,
                crontab=cron,
                enabled=periodic_task['enabled']
            )
```

Few key things:

- We use this task as part of a deploy procedure.
- We always put a link to [`crontab.guru`](https://crontab.guru/) to explain the cron. Otherwhise it's unreadable.
- Everything is in one place.

### 그외

#### utils.py

```python
from rest_framework import serializers
from rest_framework import exceptions as rest_exceptions

from rest_framework.views import exception_handler
from rest_framework.settings import api_settings
from rest_framework import exceptions

from django.core.exceptions import ValidationError


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer, ), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc):
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg


class ApiErrorsMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    without the mixin, they return 500 status code which is not desired.
    """
    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)


class ErrorsFormatter:
    """
    The current formatter gets invalid serializer errors,
    uses DRF standart for code and messaging
    and then parses it to the following format:
    {
        "errors": [
            {
                "message": "Error message",
                "code": "Some code",
                "field": "field_name"
            },
            {
                "message": "Error message",
                "code": "Some code",
                "field": "nested.field_name"
            },
            ...
        ]
    }
    """
    FIELD = 'field'
    MESSAGE = 'message'
    CODE = 'code'
    ERRORS = 'errors'

    def __init__(self, exception):
        self.exception = exception

    def __call__(self):
        if hasattr(self.exception, 'get_full_details'):
            formatted_errors = self._get_response_json_from_drf_errors(
                serializer_errors=self.exception.get_full_details()
            )
        else:
            formatted_errors = self._get_response_json_from_error_message(message=str(self.exception))

        return formatted_errors

    def _get_response_json_from_drf_errors(self, serializer_errors=None):
        if serializer_errors is None:
            serializer_errors = {}

        if type(serializer_errors) is list:
            serializer_errors = {
                api_settings.NON_FIELD_ERRORS_KEY: serializer_errors
            }

        list_of_errors = self._get_list_of_errors(errors_dict=serializer_errors)

        response_data = {
            self.ERRORS: list_of_errors
        }

        return response_data

    def _get_response_json_from_error_message(self, *, message='', field=None, code='error'):
        response_data = {
            self.ERRORS: [
                {
                    self.MESSAGE: message,
                    self.CODE: code
                }
            ]
        }

        if field:
            response_data[self.ERRORS][self.FIELD] = field

        return response_data

    def _unpack(self, obj):
        if type(obj) is list and len(obj) == 1:
            return obj[0]

        return obj

    def _get_list_of_errors(self, field_path='', errors_dict=None):
        """
        Error_dict is in the following format:
        {
            'field1': {
                'message': 'some message..'
                'code' 'some code...'
            },
            'field2: ...'
        }
        """
        if errors_dict is None:
            return []

        message_value = errors_dict.get(self.MESSAGE, None)

        # Note: If 'message' is name of a field we don't want to stop the recursion here!
        if message_value is not None and\
           (type(message_value) in {str, exceptions.ErrorDetail}):
            if field_path:
                errors_dict[self.FIELD] = field_path
            return [errors_dict]

        errors_list = []
        for key, value in errors_dict.items():
            new_field_path = '{0}.{1}'.format(field_path, key) if field_path else key
            key_is_non_field_errors = key == api_settings.NON_FIELD_ERRORS_KEY

            if type(value) is list:
                current_level_error_list = []
                new_value = value

                for error in new_value:
                    # if the type of field_error is list we need to unpack it
                    field_error = self._unpack(error)

                    if not key_is_non_field_errors:
                        field_error[self.FIELD] = new_field_path

                    current_level_error_list.append(field_error)
            else:
                path = field_path if key_is_non_field_errors else new_field_path

                current_level_error_list = self._get_list_of_errors(field_path=path, errors_dict=value)

            errors_list += current_level_error_list

        return errors_list


def exception_errors_format_handler(exc, context):
    response = exception_handler(exc, context)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    formatter = ErrorsFormatter(exc)

    response.data = formatter()

    return response
```

#### queryset_type.py

```python
from typing import (
    Generic,
    Iterator,
    Any,
    TypeVar,
    Optional,
    Dict,
    Tuple,
    Union
)
from collections import Iterable


DjangoModel = TypeVar('DjangoModel')


class QuerySetType(Generic[DjangoModel], extra=Iterable):
    """
    This type represents django.db.models.QuerySet interface.
    Defined Types:
        DjangoModel - model instance
        QuerysetType[DjangoModel] - Queryset of DjangoModel instances
        Iterator[DjangoModel] - Iterator of DjangoModel instances
    """
    def __iter__(self) -> Iterator[DjangoModel]: ...

    def all(self) -> 'QuerySetType[DjangoModel]': ...

    def order_by(self, *args: Any) -> 'QuerySetType[DjangoModel]': ...

    def count(self) -> int: ...

    def filter(self, **kwargs: Any) -> 'QuerySetType[DjangoModel]': ...

    def exclude(self, **kwargs: Any) -> 'QuerySetType[DjangoModel]': ...

    def get(self, **kwargs: Any) -> DjangoModel: ...

    def annotate(self, **kwargs: Any) -> 'QuerySetType[DjangoModel]': ...

    def first(self) -> Optional[DjangoModel]: ...

    def update(self, **kwargs: Any) -> DjangoModel: ...

    def delete(self, **kwargs: Any) -> Tuple[int, Dict[str, int]]: ...

    def last(self) -> Optional[DjangoModel]: ...

    def exists(self) -> bool: ...

    def values(self, *args: Any) -> 'QuerySetType[DjangoModel]': ...

    def values_list(self, *args: Any) -> 'QuerySetType[DjangoModel]': ...

    def __getitem__(
        self,
        index: int
    ) -> Union[DjangoModel, "QuerySetType[DjangoModel]"]: ...

    def __len__(self) -> int: ...

    def __or__(
        self,
        qs: "QuerySetType[DjangoModel]"
    ) -> 'QuerySetType[DjangoModel]': ...

    def __and__(
        self,
        qs: "QuerySetType[DjangoModel]"
    ) -> 'QuerySetType[DjangoModel]': ...
```

### 개선판 by phalt 1.2.1

[ [Django API Domain Styleguide] 개선판 by phalt](https://github.com/phalt/django-api-domains)

https://phalt.github.io/django-api-domains 

### 목표

- 유연햔 설계 패턴
- Backend와 FrontEnd 프로젝트 분리

### 전략

- Django의 apps 을 도메인으로 간주한다.
- Django의 apps 을 도메인 간의 강력한 바운더리 컨텍스트를 지원하도록 구현한다.
- 비지니스 가치 뿐만 아니라 점진적으로 개발 속도 증가가 가능하도록 도메인이 분리될수 있도록 한다.
- 거대한 도메인에서 분리된 애플리케이션 서버롤 추출해 내는 노력을 줄이기 위해 스타일 가이드를 설계한다.
- 이 가이드는 API-based 애플리케이션을 위한 가이드이다.

### Domains

​	 [domain](https://en.wikipedia.org/wiki/Domain_(software_engineering)) 는 일종의 작은 소프트웨어이며, 애플리케이션에서 구분되는 비지니스 가치를 제공한다.

본 스타일 가이드에서 말하는 domain은 Django에서 app으로 간주한다. 그러므로 비지니스 도메인은 이를 반영하는 최소 하나의 구분되는 소프트웨어 도메인을 갖는다.

 이 가이드는 데이터베이스 테이블을 표현하는 Django [models](https://docs.djangoproject.com/en/2.1/topics/db/models/)(Django app pattern)의 주요 장점을 skinny model로 유지할 것이다. 

이 가이드는 또한, Django의 다른 어플리케이션으로 이식 가능한 패키지 앱을 유지한다. 이를 통해 도메인들을 다른 프로젝트나 코드 베이스로 이식 가능하도록 한다.

##### Examlples

​	이 가이드에서는 책에 대한 정보를 공유하는 book shop을 예로 들어 설명한다. 이는 books라는 비지니스 도메인으로 모델링 될 수 있고 소프트웨어 도메인 역시 books가 될 수 있다.

https://github.com/phalt/django-api-domains/tree/master/example_domain

##### Domain rules

- 도메인이 작업하기에 너무 커지면 쪼개야 한다.

  한 도메인은 4~6명의 개발자 (3쌍)가 편하게 작업할 수 있어야 한다. 만약 개발자들이 서로 작업 하는데 방해가 된다면, 소프트웨어가 이 스타일가이드에서 크게 벗어났는지 확인해보거나 도메인을 쪼개는 방안을 검토해봐야 한다.

- 도메인간의 강력한 bounded contexsts를 유지하기 위해서 이 문서의 스타일가이드에 집착할 필요가 있다.

  이는 개발 속도를 높이기 위해 도메인을 두개로 쪼갤 때에도 적용되지만 두 도메인은 여전히 도메인간 의존성을 유지한다. 만약 도메인간에 bounded context를 느슨하게 가져가면 바운더리는 풍화될 것이고 두 도메인을 독립적으로 작업할 수 있는 능력을 상실하게 된다.

#### StyleGuide

##### Visualisation

Apis ->  Services -> Modesl -> DB

​							  -> Interfaces

- 화살표는 의존성을 나타낸다.

  Apis 와 Interfaces는 도메인의 context boundary를 나타내며 외부로부터 도메인 내부를 보호한다.

- Services

  Services는 Models와 상호작용하며 도메인의 비지니스 로직을 처리한다. Services가 datastore와 Interface에 커뮤니케이션 하는지 아니면 다른 도메인에 커뮤니케이션 하는지는 Models에 따라 다르다.

- Models

  Models는 데이터베이스에 있는 데이터는 Models에 저장되며 이는 datastore에 의존적이다

- APIs

  Apis는 다른 도메인에서 service 기능을 사용할 수 있도록 publishing 한다. 이는 Services에 의존적이다.

- Interfaces

  도메인은 Interfaces를 통해 다른 도메인을 사용할 수 있다. 서비스는 다른 도메인과 통신하기 위해 interfaces에 의존적이다.

##### 파일구조

- 도메인은 반드시 다음 파일 구조를 따른다.

  - apis.py : 외부 공개용 functions, 접근 포인트, 표현 로직
  - interfaces.py : 다른 도메인 또는 외부 서비스와의 Intergration
  - models.py : 오브젝트 모델과 스토리지, 단순한 정보 로직

  urls.py, apps.py, migrations/* 와 같은 Django app의 표준 파일들은 허용된다.

-  [Django's pattern](https://docs.djangoproject.com/en/dev/#the-view-layer)에 있는 Views.py는 명시적으로 이 스타일가이드에서 허용되지 않는다.

  API-based 어플리케이션에 초점을 맞추고있으므로 Django의 views.py에 있는 대부분의 로직은 APIs 와 Services로 분리될 것이다.

- 좀 더 나은 파일 정리를 위해서 디렉토를 사용할 수 있다.

  예를 들어, apis.py를 아래와 같은 구조로 쪼갤 수 있다.

  ```
  apis/
    __init__.py
    rest.py
    graphql.py
  ```

  이 디렉토리의 `__init__.py`에서 포함되어 있는 파일들을 import한다.

  ```python
  # apis/__init__.py
  from .rest import *  # noqa
  from .graphql import *  # noqa
  ```

  이렇게 하면, apis의 모든 파일들을 쉽게 import 할 수 있다.

  ```python
  # example.py
  from domain.apis import Foo
  ```

  이는 네임스페이스를 정돈하고 도메인 정보를 빠짐없이 사용할 수 있게한다.

- 도메인에서 사용하지 않는다면 모든 파일들을 가지고 있을 필요는 없다. 예를들면, 다른 도메인에 대한 API 호출을 조정하는 도메인에는 데이터 스토어에 아무것도 저장하지 않기 때문에 모델이 필요하지 않다.
- 도메인은 이 스타일가이드 패턴에서 다루지 않는 코드 부분을 분리해내기 위해서 utils.py, enums.py, serializers.py와 같은 추가 파일들을 가질수 있다.

##### 절대경로 import or 상대경로 import

- 도메인 내부에 있는 파일들을 임포팅 한다면, 상대경로 import를 사용해야 한다.

- 같은 프로젝트의 다른 도메인에 있는 파일들을 임포팅 한다면, 절대경로 import를 사용해야 한다.

- 테스트에서 메인을 임포팅 한다면, 절대경로 import를 사용한다.

- 써드파티 패키지를 임포팅 한다면, 절대경로 import를 사용한다.

- 결국, 도메인 내부에 있는 파일들을 임포팅할때만 상대경로 import를 사용하고 나머지는 절대경로 import를 사용한다.

  이는 도메인을 패키징하거나 이동시키기 쉽게 하기 위함이다.

##### 로직 위치

​	종류에 따른 로직이 어디에 위치해야 하는지를 헷갈리는 거는 일반적이다.

많은 경우에 이는 결정하기 어려운 문제이고, 가장 좋은 조언은 패턴을 따르라고 집착해라. 

- **APIs** : ApIs.py

  표현과 관련한 로직

  "어디에서 이 데이터를 사용자에게 보여준담?" 또는 "API 스키마를 어디에 정의 한담?"

- **Services**: Services.py

  절차를 조정하고 트랜잭션 처리를 하는 로직

  "한 도메인에 있는 많은 모델들을 업데이트 하는 조정을 어디에 둬야 한담?" 또는 "어디서 다른 도메인으로 action하나를 디스패치 시킨담?"

- **Models**: Models.py

  정보에 관련한 로직

  "데이터를 어디에 저장한 담?" 또는 "저장하기 전처리 후처리 작업을 어디서 한담?"

- **Interface**: Interface.py

  다른 도메인으으로부터의 Input, 으로의 Output 데이터의 변환 처리

  "어디서 다른 도메인으로 붙는담?" 또는 "다른 도메인으로 보낼 데이터 포맷을 어떻게 바꾼담?"

#### Files

##### Example 설명

​	두 개의 도메인(books, authors)로 이루어진 서비스, 물론 하나의 도메인에 Books 와 Authors가 존재 할 수 있지만 예제를 위해 두개로 만든다. 그리고 또 하나, book과 author는 1:1 관계로 설정한다.

##### Modesl

## Project Start

- django-admin.py startproject superlists
- git init . : git 초기화
- echo 'db.sqlite3' >>  .gitignore : 버전관리 제외처리
- git add. : 스테이징
- git status : 스테이징 상태 확인
- git rm -r --cached superlists/`__pycache__` : 캐쉬파일 삭제
- echo '`__pycache__`' >> .gitignore : 버전관리 제외처리
- echo '*.pyc' >> .gitignore : 버전관리 제외처리
- git status : 스테이징 상태 확인
- git add .gitignore : 버전관리 제외처리 파일 스테이징 추가
- git commit -m 'first commit' : 스테이징 파일 커밋

### 앱 추가

- python3 manage.py startapp lists

## Project Structure

​	하나의 프로젝트는 여러 앱을 가질 수 있으며, 다른 사람이 만든 외부 앱도 사용할 수 있다. 

- superlists: 프로젝트 폴더 Root
  - db.sqlite3
  - functional_tests.py: Function Test (Use-Case)
  - lists
    - admin.py
    - `__init__`.py
    - migrations
      - `__init__`.py
    - templates : html 템플릿
    - models.py
    - tests.py : 단위 테스트
    - views.py
  - manage.py
  - superlists: Global Application
    - `__init__`.py
    - settings.py : Project 전역 설정
    - urls.py : URL 과 View Function 매핑 for Global, include로 Sub app의 urls.py 지정가능
    - wsgi.py

## Server Management

- python3 manage.py runserver : 서버 실행
- (서버 실행 중에 별도 터미널에서) python3 functional_tests.py : Functional Test 실행
- python3 manage.py test : 단위 테스트 실행

## Source Version Control

- git status : untracked된 파일들을 확인한다.
  - untracked된 파일이 있을경우,
    - git add lists : untracked된 파일을 스테이징한다.
    - git diff --staged : 커밋하려는 추가 코드를 확인한다.
    - git commit -m "commit reason"
    
  - untracked된 파일이 없을경우,

    - git diff : 커밋하려는 파일들의 변경 내역을 확인한다.

    - got commit -am "commit reason"

