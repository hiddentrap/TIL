# Python TDD

## Web Functional Test

### Selenium

> selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH

```python
pip install webdriver-manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```

## URL View Mapping Test

```python
    def test_root_url_resolves_to_home_page_view(self):
        # Given Nothing

        # When
        found = resolve('/')

        # Then
        self.assertEqual(found.func, home_page)
```



## HTML Test

### Isolated way

```python
    def test_home_page_returns_correct_html(self):
        # Given
        request = HttpRequest()

        # When
        response = home_page(request)
        html = response.content.decode('utf8')

        # Then
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>서버관리</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
```

### Django way

```python
    def test_uses_home_template(self):
        # Given Nothing

        # When
        response = self.client.get('/')

        # Then
        self.assertTemplateUsed(response, 'servers.html')
```

## Type Test: Type Annotation

[참고하여 정리필요](https://seorenn.tistory.com/77)

```
mypy test.py
```

## Mocking Framework 사용금지

​	Mocking Framework(mock.patch, monkeypatching, unittest.mock)을 사용하는 대신 Fake(추상화) Class를 만들어 사용하는 것이 낫다.

Fake(추상화) Class : 테스트에서만 사용할 수 있는 외부 컴포넌트 대체 동작 구현체 

Fake(추상화) Class를 사용한 테스트

스텁 = dummy : 아직 완성되지 않은 하부 모듈 대신 사용하는 모듈

```python
class FakeFileSystem(list): 

    def copy(self, src, dest): 
        self.append(('COPY', src, dest))

    def move(self, src, dest):
        self.append(('MOVE', src, dest))

    def delete(self, dest):
        self.append(('DELETE', src, dest))


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source = {"sha1": "my-file" }
    dest = {}
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    synchronise_dirs(reader.pop, filesystem, "/source", "/dest")

    assert filesystem == [("COPY", "/source/my-file", "/dest/my-file")]


def test_when_a_file_has_been_renamed_in_the_source():
    source = {"sha1": "renamed-file" }
    dest = {"sha1": "original-file" }
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    synchronise_dirs(reader.pop, filesystem, "/source", "/dest")

    assert filesystem == [("MOVE", "/dest/original-file", "/dest/renamed-file")]

```

