# Django Reference

## Setting



## Model



### Example

```python
from django.db import models

# 테이블 정의 w models.Model: 테이블이름은 APP이름_클래스이름 (기본값)
class Person(models.Model):
    # 컬럼 정의
    # "id" serial NOT NULL PRIMARY KEY: PK가 정의가 없을 경우 자동생성
    # id = models.AutoField(primary_key=True)
    # "name" varchar(30) NOT NULL
    name = models.CharField(max_length=30)
    
    class Meta:
        # 테이블 이름을 APP이름_클래스이름(기본값)말고 사용자가 직접정의
        db_table = "team_person"
        
    
```

### Field

#### Field Reference

##### options

###### null

False: NULL 저장 가능 여부

Char, Text 에는 NULL 사용하지 말 것

###### blank

False: blank 저장 가능 여부

###### choices

[choices](https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-options)

###### db_column

컬럼 이름 사용자 정의, 기본값은 필드이름

###### db_index

Ture일 경우, DB에 필드에 해당하는 인덱스 생성

###### db_tablespace

[db_tablespace](https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-options)

###### default

필드 기본값 callable일경우 레코드 생성시 마다 호출 된다.

###### editable

False일경우 admin이나 다른 ModelForm에 display되지 않는다. : default = True

###### error_messages

에러 메시지를 dict로 사용자 재정의 한다.

###### help_text

form 위젯에 추가로 도움말을 쵸시한다. 폼을 사용하지 않더라도 문서화에 유용하다.

###### primary_key

PK 지정 : null=False, unique=True를 의미한다.

###### unique

유니크 제약 지정 위반시 save()시, IntegrityError 발생

unique가 지정되면 묵시적으로 index를 생성하므로 db_index를 사용할 필요가 없다.

###### unique_for_date

title필드에 unique_for_date = "pub_date"라고 지정하면 같은일자에 동일한 title값을 가지는 레코드가 생성될 수 없음

###### unique_for_month

###### unique_for_year

###### verbose_name

읽는용도의 이름

###### validators

리스트 형태에 validator 지정

[validator](https://docs.djangoproject.com/en/3.0/ref/validators/)

##### 

##### Field Types

###### AutoField

class AutoField(**options)

자동증가하는 IntegerField 보통 직접 쓸일은 없음 PK인 id를 자동생성시 사용됨

###### BigAutoField

class BigAutoField(**options)

직접쓸일 없음

###### BigIntegerField

class BigIntegerField(**options)

numbers from `-9223372036854775808` to `9223372036854775807`.

###### BinaryField

class BinaryField(max_length=None, **options)

bytes, bytearray, memoryview 저장용 거의 쓸일 없음 이거 저장할거면 파일에 저장해야 함

###### BooleanField

class BooleanField(**options)

true/false : 체크박스, 기본값은 None

###### CharField

class CharField(max_length=None, **options)

TextInput

- max_length : 최대 길이 지정 가능

###### DateField

class DateField(auto_now=False, auto_now_add=False, **options)

datetime.date 객체용 

- auto_now : 현재시간 자동 설정 (수정일시 등에 사용) save()시 자동 업데이트 되고 QuerySet.update()등으로 다른 필드를 수정할때는 업데이트 안됨.
- auto_now_add: 현재시간 자동 설정(생성일시 사용) 수기로 필드값 설정불가.
- 둘다 동시 설정 불가

###### DateTimeField

class DateTimeField(auto_now=False, auto_now_add = False, **options)

datetime.datetime 객체용 

###### DecimalField

class DecimalField(max_digits=None, decimal_places=None, **options)

10진수, Decimal 객체용 

- max_digits: decimal_places이상 이어야 하며, 최대 자리수
- decimal_places: 허용된 최대 소수점 이하 자릿수
- ex) 999.99 는 max_digits = 5, decimal_places = 2

###### DurationField

class DurationField(**option)

시간의 기간값 timedelta

###### EmailField

class EmailField(max_length=254, **options)

CharFiled with EmailValidator

###### FileField

[FileField](https://docs.djangoproject.com/en/3.0/ref/models/fields/#registering-and-fetching-lookups)

class FileField(upload_to=None, max_length=100, **options)

pk로 지정 불가필드

- upload_to: 업로드 디렉토리 및 파일이름 

###### FloatField : 돈에 사용금지!!!

**돈에는 DecimalFiled를 사용할 것!!**

class FloatField(**option)

실수, float

###### ImageFiled

class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)

FileField로부터 상속받는다. 

###### IntegerField

class IntegerField(**options)

An integer. Values from `-2147483648` to `2147483647` are safe in all databases supported by Django.

###### GenericIPAddressField

class GenericIPAddressField(protocol='both', unpack_ipv4=False, **options)

IP주소를 스트링 포맷으로 저장(192.0.2.30 또는 2a02:42fe::4)

- protocol : both, IPv4, IPv6
- unpack_ipv4: true면 ::ffff:192.0.2.1로 저잘될께 192.0.2.1로 저장됨 both에서만 먹힘
- blank를 허용하려면 null도 허용해야함

###### NullBooleanField 없다쳐라.

class NullBooleanField(**optons)

###### PositiveIntegerField

class PositiveIntegerField(**options)

0이상인 값 values from `0` to `2147483647`

###### PositiveSmallIntegerField

 Values from `0` to `32767` 

###### SlugField

class SlugField(max_length=50, **options)

신문사 용어로 문자, 숫자, _, - 로만 이루어진 짧은 라벨로 URL에서 사용된다.

묵시적으로 db_index가 True로 활성화된다. 

- allow_unicode : unicdoe 사용

###### SmallAutoField 

쓸일 없음

###### SmallIntegerField

Values from `-32768` to `32767` 

###### TextField

large text field

###### TimeField

class TimeField(auto_now=False, auto_now_add=False, **options 

datetime.time 객체용

###### URLField

class URLField(max_length=200)

CharField with URLValidator

###### UUIDField

class UUIDFiled(**options)

UUID 클래스 저장용 char(32) PK를 위한 AutoFiled의 대안

```python
import uuid
from django.db import models

class MyUUIDModel(models.Model):
    id = models.UUIDField(promary_key = True,
                         default=uuid.uuid4, editable=False)
```



#### Relationship fields

[참조](https://brunch.co.kr/@ddangdol/1)

###### OnetoManyField

ForeignKey

class ForeginKey(to, on_delete, **options)

다 대 일 관계에서 사용

```python
from django.db import models

class Car(models.Model):
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )
    # ...

class Manufacturer(models.Model):
    # ...
    pass
```

ForeignKye에 대해 index가 자동생성되므로 원하지 않을경우 db_index=False 

- on_delete: 외래키가 참조하는 객체가 삭제될때의 동작
  - CASCADE : 현재 객체 삭제
  - PROTECT : 참조 객체 삭제 금지
  - SET_NULL : 외래키만 null로 변경 단, null = True로 설정되어 있어야함
  - SET_DEFAULT : 외래키를 기본값으로 변경 단, 기본값이 설정되어 있어야함
  - SET()
  - DO_NOTHING: 아무것도 않한다.
- limit_choices_to: ModelForm 랜더링할때 사용, 선택할수 있는값 제한
- to_field: 외래키 참조필드 지정



###### ManytoManyField

class ManyToManyField(to, **options)

다 대 다 관계 

- 두모델중 한모델에만 존재해야 하며 어느 모델에 있던 관계없다. ( 더 큰 모델에 있는게 맞는거 같음)

```python
# models.py
from django.db import models

class User(models.Model):
    id = models.Autofield(primary=True)
    name = models.Charfield(max_length=10)
    
class Star(models.Model):
    id = models.Autofield(primary=True)
    followers = models.ManyToManyField(User, related_name="following")
    
star = Star.objects.all().first()
following_user_list = star.followers.all()

user = User.objects.all().first()
following_start_list = user.following.all()

```

- 중간 테이블을 정의할 수도 있음

```python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
    
class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.manyToManyField(Person, through='Membership')
    
    def __str__(self):
        return self.name
    
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.charField(max_length=64)
    
    
ringo = Person.objects.create(name="Ringo Starr")
paul = Person.objects.create(name="Paul McCartney")
beatles = Group.objects.crate(name="The Beatles")
m1 = Membership(person=ringo, group=beatles,date_joined=date(1962,8,16), invite_reason="Needed a new drummer.")
m1.save()
beatles.members.all()
ringo.group_set.all()
m2 = Membership.objects.create(person=paul, group=beatles, date_joined=date(1960,8,1),invite_reason="Wanted to form a band.")
beatles.members.all()

일반적인 다대다 필드와는 다르게 add(), create(), set()을 사용하여 관계를 만들수는 없다
beatles.members.add(john)
beatles.members.create(name="George Harrison")
beatles.members.set([john, paul, ringo, george])
```

중개모델 제약

중간 모델에는 원본 모델에 대한 외래 키가 하나만 포함되야한다(예제에서 Group). 또는 Django에서 ManyToManyField.through_fields를 사용해서 관계에 사용해야 하는 외래 키를 명시적으로 지정해야 한다. 두 개 이상의 외래 키가 있고 through_fields를 정의하지 않는다면, 유효성 검증 오류가 발생한다. 외래 키에 대한 비슷한 제한사항이 대상 모델(예제에서 Person)에도 적용된다.

중개 모델을 통해 다대다 관계를 가지고 있는 모델의 경우 동일한 모델에 대한 두 개의 외래 키가 허용되지만 다대다 관계와는 다른 측면으로 처리된다. 두 개 이상의 외래 키가 있는 경우, 위처럼 through_fields를 지정해야 한다. 그렇지 않으면 유효성 검증 에러가 발생한다.

중개 모델을 사용하여 자신의 모델로부터 다대다 관계를 정의할 때는 symmetrical=False를 사용해야 한다



왜일까? **Person**과 **Group** 간의 관계를 만들 수 없다. **Membership** 모델 관계에 필요한 모든 세부 정보를 지정해야 한다. 간단한 **add**, **create** 및 할당 호출은 추가 세부사항을 지정하는 방법을 제공하지 않는다. 결과적으로 중간 모델을 사용한 다대다 관계에서는 비활성화된다. 이런 관계의 유형을 생성하기 위한 유일한 방법은 중간 모델의 인스턴스를 생성하는 것이다.



비슷한 이유로 **remove()** 메서드가 비활성화된다. 예를 들면, 중간 모델에 의해 정의된 사용자 정의 테이블을 통해 (model1, model2)의 유일성이 적용되지 않은 경우 remove() 호출은 지워야 할 중간 모델 인스턴스에 대한 충분한 정보를 제공하지 않는다.

```
beatles.members.remove(ringo) # 안먹힘

하지만, clear() 메서드를 사용하여 모든 인스턴스에 다대다 관계를 삭제할 수 있다.
beatles.members.clear()
```

중간 모델의 인스턴스를 생성하여 다대다 관계를 설정하면 쿼리를 실행할 수 있다. 일반적인 다대다 관계같이 다대다 관계 모델의 속성을 사용하여 쿼리 할 수 있다.

```
Group.objects.filter(members__name__startwith='Paul')

중간 모델을 사용할 때 해당 속성에 대해서도 쿼리 할 수 있다.
Person.objects.filter(group__name='The Beatles', membership__date_joined__gt=date(1961,1,1))

회원의 정보에 접근이 필요할 경우 직접 Membership 모델에 쿼리 하여 수행할 수 있다.
ringos_membership=Membership.objects.get(group=beatles, person=ringo)
ringos_membership.date_joined
ringos_membership.invite_reason

같은 정보에 접근하는 다른 방법은 Person 객체에서 다대다 reverse relationship를 쿼리 하는 것이다.
ringos_membership = ringo.membership_set.get(group=beatles)
ringos_membership.date_joined
ringos_membership.invite_reason
```

###### OnetoOneField

개념적으로 ForeignKey with unique=True와 동일

객체확장에 유용, 상속개념

한 모델에 여러 개의 OneToOneFiled 타입 정의 가능

다른 앱의 모델과 관계하는 것도 가능

```python
from django.db import models
from geography.models import Zipcode

class Restaurant(models.Model):
    zip_code = models.ForeignKey(ZipCode,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,)

```

- parent_link: 다른 구현체 모델로부터 상속된 모델일 경우 True



#### Primary key fields

- 장고는 오직 한 개의 필드에만 primary_key=True 지정가능

- 지정하지 않을경우 다음 코드가 자동 추가됨

  ```python
  id = models.AutoField(primary_key=True)
  ```

- 여러 필드를 PK로 구성해야 하는경우, `AutoField`를 PK로 쓰고 Meta로 제약할 수 밖에없다.

  ```python
  class Hop(models.Model):
      migration = models.ForeignKey('Migration')
      host = models.ForeignKey(User, related_name='host_set')
  
      class Meta:
          unique_together = (("migration", "host"),)
  ```

  

### Meta options

#### abstract

[abstract-base-class](https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes)

abstract = True : 추상화 클래스

#### db_table

테이블 이름 사용자 정의

db_table = "user_table_name"

#### db_tablespace

[tablespace?](https://docs.djangoproject.com/en/3.0/topics/db/tablespaces/)

#### default_manager_name

objects대신 다른 이름으로 쓰려면 지정

#### default_related_name

?

#### get_latest_by

시간으로 정렬할때 기준 필드

```
# Latest by ascending order_date
get_latest_by = "order_date"

# Latest by priority descending, order_date ascending
get_latest_by = ['-priority', 'order_date']
```

#### managed

기존 디비나 다른 방법으로 생성된 테이블을 장고의 데이터베이스 라이프 사이클에서 제외 시킬때 사용 migrate나 flush 명령어에 영향받지 않도록. 

기본은 managed = True 포함, False 제외

[참고](https://docs.djangoproject.com/en/3.0/ref/models/options/)

#### order_with_respect_to

#### ordering

[쿼리표현](https://docs.djangoproject.com/ko/3.0/ref/models/expressions/)

ordering = ['-pub_date'] 디센딩 ['pub_date'] 어센딩

```
from django.db.models import F

ordering = [F('author').asc(nulls_last=True)]
```

https://docs.djangoproject.com/ko/3.0/ref/models/options/

https://docs.djangoproject.com/en/3.0/topics/db/models/#meta-options

## View



