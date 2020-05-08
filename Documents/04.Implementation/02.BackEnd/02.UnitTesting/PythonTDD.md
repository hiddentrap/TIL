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

