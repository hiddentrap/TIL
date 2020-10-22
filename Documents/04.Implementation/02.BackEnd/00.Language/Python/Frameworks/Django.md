# Django

https://github.com/cookiecutter/cookiecutter

https://medium.com/@cristobalcl/how-to-start-a-python-project-with-django-in-2020-803122721b23

```shell
# Python version
pyenv install 3.8.2
pyenv shell 3.8.2

# Create a Django project
export PROJECT_NAME=the_project

pip install --user Django
django-admin startproject $PROJECT_NAME

cd $PROJECT_NAME
mv $PROJECT_NAME/ config
find . -type f -name '*.py' -exec sed -i "s/$PROJECT_NAME/config/g" '{}' \;

# Version control
git init
curl https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore --output .gitignore
git add .
git commit -m "First commit"

# Python environment for the project
pyenv local 3.8.2
git add .
git commit -m "Set Python version for the project"

# Beautiful dependency and packaging management
poetry init -n
poetry add Django
git add .
git commit -m "Add poetry"

# Don't mess with the repo
poetry add -D pre-commit
poetry run pre-commit install
poetry run pre-commit sample-config > .pre-commit-config.yaml
cat >> .pre-commit-config.yaml << EOF
- repo: https://github.com/psf/black
  rev: stable
  hooks:
    - id: black
      language_version: python3.6
EOF

poetry run pre-commit run --all-files
# Fail?
poetry run pre-commit run --all-files
# Ok!

git add .
git commit -m "Add pre-commit with Black"
```



- Linting & Typechecking & Testing
- Skeleton of Clean Architecture
- Deployment
- CI/CD
- Documentation generation
- Version control
- Issue Tracker
- Package Managing : Poerty
  - https://python-poetry.org/



1. 프로젝트 의존성에 전역 파이썬 시스템을 사용하지 말라

   : 가상환경을 사용해서 격리 시킬 것

   : virtualenv or Docker

2. requirements.txt에 package목록 및 버전정보 작성할 것

   :pip-tools

   :dependency를 소스까지 다운로드 해놓을 것. pip help download

3. 함수기반 view말고 클래스 기반 view를 사용할 것

   :템플릿 네임 https://github.com/phpdude/django-template-names

4. Fat Models, Skinny Views를 지향할 것

   : 비지니스 로직은 작게 작게 메서드로 쪼개서 모델에 때러넣는 것이다.

   : 사용자에게 메일 보내기 기능이 필요하면 컨트롤러/view에 로직을 때려넣지 말고 모델에 이메일 기능을 넣어 확장시켜라

   :http://django-best-practices.readthedocs.io/en/latest/applications.html#make-em-fat

   :일반적으로 모델은 하나의 오브젝트나 엔티티를 나타내므로 단수의 이름을 갖는다

5. 설정파일 관리를 잘해라

   :700라인 이상 넘어가면 유지보수하기 어려워진다

   :dev, production, staging 설정파일을 쪼개놓고 커스텀 로더를 만들어라

   ​	:https://github.com/sobolevn/django-split-settings

6. app의 목적은 한 두줄의 짧은 문장으로 설명가능해야 한다.

   : 예시) 사용자를 등록하고 이메일로 계정을 활성화시킨다

   프로젝트 전체 구조

   ```sh
   root@c5b96c395cfb:/test# tree -L 3
   .
   ├── deploy
   │   ├── chef
   │   └── docker
   │       ├── devel
   │       └── production
   ├── docs
   ├── logs
   ├── manage.py
   ├── media
   ├── project
   │   ├── __init__.py
   │   ├── apps
   │   │   ├── auth
   │   │   ├── blog
   │   │   ├── faq
   │   │   ├── pages
   │   │   ├── portal
   │   │   └── users
   │   ├── conf
   │   ├── settings.py
   │   ├── static
   │   ├── templates
   │   ├── urls.py
   │   └── wsgi.py
   └── static
       └── admin
           ├── css
           ├── fonts
           ├── img
           └── js
   
   ```

   그 중 portal app의 구조

   ```shell
   root@c5b96c395cfb:/test# tree project/apps/portal/
   project/apps/portal/
   ├── __init__.py
   ├── admin.py
   ├── apps.py
   ├── management
   │   ├── __init__.py
   │   └── commands
   │       ├── __init__.py
   │       └── update_portal_feeds.py
   ├── migrations
   │   └── __init__.py
   ├── models.py
   ├── static
   │   └── portal
   │       ├── css
   │       ├── img
   │       └── js
   ├── templates
   │   └── portal
   │       └── index.html
   ├── templatetags
   │   ├── __init__.py
   │   └── portal.py
   ├── tests.py
   ├── urls.py
   └── views.py
   ```

7. 템플릿 네이밍

   ```
   [application]/[model]_[function].html
   address_book/contact_list.html
   address_book/contact_detail.html
   ```

   

8. python manage.py collectstatic

9. assets never expire policy https://css-tricks.com/strategies-for-cache-busting-css/

10. https://docs.djangoproject.com/en/1.10/howto/custom-management-commands/

   https://github.com/django-extensions/django-extensions

11. https://github.com/phpdude/django-macros-url

https://github.com/phpdude/docker-django-webpack-skeleton

11. 견고하고 실패하지 않는 DB 커넥션을 설정해라
12. cached loading 켜라
13. 캐쉬에 세션을 저장해라. DB에저장하지 말고 memcash 옵션 활성화 또는 Redis같은거 써라
14. 애플리케이션과 라이브러리는 분리해라
15. 팀플릿은 한군데 몰아놔라

16. 



https://www.upgrad.com/blog/django-project-ideas-topics-beginners/