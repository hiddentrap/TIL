# Django Coding

## FunctionalTest(w in memory db) 작성

: End-to-End Test(w real db)

/functional_tests.py

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 사용자는 서버 자산관리를 위해 관리 페이지로 이동한다.
        self.browser.get('http://localhost:8000')

        # 사용자는 페이지 타이틀과 헤더에서 Asset Inventory를 확인한다.
        self.assertIn('Asset Inventory', self.browser.title)
        self.fail('Finish the test!')

        # 사용자는 새로운 서버 자산을 등록하기 위해 입력 창을 찾는다.

        # 사용자는 서버명 텍스트 박스에 서버명"SERVER01"을 입력한다.

        # 사용자는 엔터를 입력하고, 페이지의 서버 리스트는 업데이트 된다.
        # 1: SERVER01


if __name__ == '__main__':
    unittest.main()

```

python functional_tests.py

유즈케이스 테스트는 실패한다.

## 어플리케이션 추가

```
python manage.py startapp servers
```

## 어플리케이션 등록 to Django

/settings.py

```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'servers',
]
```



## UnitTest 작성

app/tests.py

```python
from servers.views import home_page


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        # Given Nothing
        # When
        found = resolve('/')

        # Then
        self.assertEqual(found.func, home_page)

```

python manage.py test

단위 테스트는 실패한다.

## VIEW 작성

app/views.py

단위 테스트를 통과할 수 있는 최소 코드 작성

```python
def home_page():
    pass
```

python manage.py test

단위 테스트는 실패한다.

## URL 매핑

app/urls.py

단위 테스트를 통과할 수 있는 최소 코드 작성

```python
from servers import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
]
```

python manage.py test

단위 테스트는 성공한다.

또 다른 단위 테스트를 작성하고 반복한다.