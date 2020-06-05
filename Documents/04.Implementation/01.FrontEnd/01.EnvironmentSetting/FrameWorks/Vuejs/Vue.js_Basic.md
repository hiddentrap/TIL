# Vue.js_Basic

[정리필요](https://velog.io/@jakeseo_me/Vue.js-간단정리-1-기본-사용)

## Requirement

- [https://www.google.com/intl/ko/chrome/](https://www.google.com/intl/ko/chrome/)
- [https://code.visualstudio.com/](https://code.visualstudio.com/)
  - Vetur : Vue Tool Chain
  - Night Owl : 코드강조
  - Material Icon Theme : 아이콘 테마
  - Live Server
  - ESLint
  - Prettier
  - Auto Close Tag
  - Atom Keymap, Eclipse Keymap and so on : 단축키 맵
- [https://nodejs.org/ko/](https://nodejs.org/ko/)
- [https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)

## Refer GIT

- [https://github.com/joshua1988/learn-vue-js](https://github.com/joshua1988/learn-vue-js)

## Vue.js 소개

### 기존 개발방식

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app"></div>

    <script>
      var div = document.querySelector("#app");
      var str = "hello world";
      div.innerHTML = str;

      str = "hello world!!!";
      div.innerHTML = str;
    </script>
  </body>
</html>

```

DOM을 직접 읽어서 수정

### Reactivity

데이터의 변화를 감지하여 자동으로 화면에 반영

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app"></div>

    <script>
      var div = document.querySelector("#app");
      var viewModel = {};
      // 객체의 동작을 재정의 하는 API
      // Object.defineProperty(대상객체, 객체의속성, {정의할내용})
      Object.defineProperty(viewModel, "str", {
        // 속성에 접근했을 때의 동작을 정의
        get: function () {
          console.log("접근");
        },
        // 속성에 값을 할당했을 때의 동작을 정의
        set: function (newValue) {
          console.log("할당", newValue);
          div.innerHTML = newValue;
        },
      });
    </script>
  </body>
</html>

```

[https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty)

### Reactivity Library

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app"></div>

    <script>
      var div = document.querySelector("#app");
      var viewModel = {};
      // 객체의 동작을 재정의 하는 API
      // Object.defineProperty(대상객체, 객체의속성, {정의할내용})
      (function () {
        function init() {
          Object.defineProperty(viewModel, "str", {
            // 속성에 접근했을 때의 동작을 정의
            get: function () {
              console.log("접근");
            },
            // 속성에 값을 할당했을 때의 동작을 정의
            set: function (newValue) {
              console.log("할당", newValue);
              render(newValue);
            },
          });
        }

        function render(value) {
          div.innerHTML = value;
        }

        init();
      })();
    </script>
  </body>
</html>

```

즉시실행함수로 감싸는 이유: 스코프를 숨기기

[https://developer.mozilla.org/ko/docs/Glossary/IIFE](https://developer.mozilla.org/ko/docs/Glossary/IIFE)

### Reactivity를 Vuejs로

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Getting Started</title>
  </head>
  <body>
    <div id="app">{{message}}</div>

    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      new Vue({
        el: "#app",
        data: {
          message: "Hello Vue.js",
        },
      });
    </script>
  </body>
</html>

```

## 인스턴스

인스턴스는 뷰료 개발할때 필수료 생성해야 하는 코드

```html
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
        var vm = new Vue({
            el: '#app',
            data:{
                message: 'hi'
            }
        });

    </script>
```

### 인스턴스와 생성자함수

```javascript
function Person(name, job){
    this.name = name;
    this.job = job;
}
```

[https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Obsolete_Pages/Core_JavaScript_1.5_Guide/Creating_New_Objects/Using_a_Constructor_Function](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Obsolete_Pages/Core_JavaScript_1.5_Guide/Creating_New_Objects/Using_a_Constructor_Function)

[https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Object/constructor](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Object/constructor)

### 인스턴스 옵션 속성

```javascript
new Vue({
    el:,
    template:,
    data:,
    methods:,
    created:,
    watch:,
})
```

- el: 인스턴스가 그려지는 화면의 시작점 (특점 HTML 태그)
- template: 화면에 표시할 요소(HTML, CSS 등)
- data: 뷰의 반응성(Reactivity)가 반영된 데이터 속성
- methods: 화면의 동작과 이벤트 로직을 제어하는 메서드
- created: 뷰의 라이프 사이클과 관련된 속성
- watch: data에서 정의한 속성이 변화했을 때 추가 동작을 수행할 수 있게 정의하는 속성

## 컴포넌트

컴포넌트는 화면의 영역을 구분하여 개발할 수 있는 뷰의 기능입니다. 컴포넌트 기반으로 화면을 개발하게 되면 코드의 **재사용성이** 올라가고 빠르게 화면을 제작할 수 있습니다.

### 전역 컴포넌트 등록

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
        <app-header></app-header>
        <app-content></app-content>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
        // Vue.component('컴포넌트 이름', 컴포넌트 내용);
        Vue.component('app-header',{
            template: '<h1>Header</h1>'
        });

        Vue.component('app-content',{
            template: '<div>content</div>'
        });
        new Vue({
            el: '#app'
        });
    </script>
  </body>
</html>

```

실무에서 전역컴포넌트는 사용할일이 거의 없다.

### 지역 컴포넌트 등록

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <app-header></app-header>
      <app-content></app-content>
      <app-footer></app-footer>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      // 전역: Vue.component('컴포넌트 이름', 컴포넌트 내용);
      Vue.component("app-header", {
        template: "<h1>Header</h1>",
      });

      Vue.component("app-content", {
        template: "<div>content</div>",
      });
      new Vue({
        el: "#app",
        components: {
          // 지역: '컴포넌트 이름': 컴포넌트 내용,
          "app-footer": {
            template: "<footer>footer</footer>",
          },
        },
      });
    </script>
  </body>
</html>

```

app-footer

### 전역&지역 컴포넌트 차이

플러그인 라이브러리: 전역 컴포넌트 - 모든 인스턴스에서 사용가능

일반적인 경우 : 지역 컴포넌트 - 등록된 인스턴스에서만 사용가능

### 컴포넌트와 인스터스의 관계

인스턴스 = Root 컴포넌트

일반적인 경우 : 인스턴스는 1개만씀

## 컴포넌트 통신

뷰 컴포넌트는 각각 고유한 데이터 유효 범위를 갖는다. 따라서, 컴포넌트 간에 데이터를 주고 받기 위해선 규칙을 따라야 한다.

컴포넌트는 트리 구조를 갖는다: 직계로만 통신 가능

하위 컴포넌트 -> 상위컴포넌트: 이벤트 발생으로 전달

상위컴포넌트 -> 하위컴포넌트 : props 전달

### 규칙이 필요한 이유

데이터 흐름추적이 용이해진다.

### props: 상위->하위

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <!-- <app-header v-bind:프롭스 속성 이름="상위 컴포넌트의 데이터 이름"> -->
      <app-header v-bind:propsdata="message"></app-header>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      var appHeader = {
        template: "<h1>{{propsdata}}</h1>",
        props: ["propsdata"],
      };

      new Vue({
        el: "#app",
        components: {
          "app-header": appHeader,
        },
        data: {
          message: "hi",
        },
      });
    </script>
  </body>
</html>

```

상위컴포넌트(Root)의 data: message가 바뀌면 하위컴포넌트(app-header)의 props: propsdata도 바뀜

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <!-- <app-header v-bind:프롭스 속성 이름="상위 컴포넌트의 데이터 이름"> -->
      <app-header v-bind:propsdata="message"></app-header>
      <app-content v-bind:propsnum="num"></app-content>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      var appHeader = {
        template: "<h1>{{propsdata}}</h1>",
        props: ["propsdata"],
      };

      var appContent = {
        template: "<div>{{propsnum}}</div>",
        props: ["propsnum"],
      };

      new Vue({
        el: "#app",
        components: {
          "app-header": appHeader,
          "app-content": appContent,
        },
        data: {
          message: "hi",
          num: 10,
        },
      });
    </script>
  </body>
</html>

```

### event emit: 하위->상위

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <!-- <app-header v-on:하위 컴포넌트에서 발생한 이벤트 이름="상위 컴포넌트의 메서드 이름"> -->
      <p>{{ num }}</p>
      <app-header v-on:pass="logText"></app-header>
      <app-content v-on:increase="addNum"></app-content>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      var appHeader = {
        template: "<button v-on:click='passEvent'>click me</button>",
        methods: {
          passEvent: function () {
            this.$emit("pass");
          },
        },
      };

      var appContent = {
        template: "<button v-on:click='addNumber'>add</button>",
        methods: {
          addNumber: function () {
            this.$emit("increase");
          },
        },
      };
      new Vue({
        el: "#app",
        components: {
          "app-header": appHeader,
          "app-content": appContent,
        },
        methods: {
          logText: function () {
            console.log("hi");
          },
          addNum: function () {
            this.num = this.num + 1;
            console.log(this.num);
          },
        },
        data: {
          num: 10,
        },
      });
    </script>
  </body>
</html>

```

### 동일레벨 컴포넌트 통신

공통조상 컴포넌트까지 올려서 다시 내려야함: event emit + props

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      {{ num }}
      <app-header v-bind:propsnum="num"></app-header>
      <app-content v-on:pass="deliverNum"></app-content>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      var appHeader = {
        template: "<div>header</div>",
        props: ["propsnum"],
      };
      var appContent = {
        template:
          "<div>content<button v-on:click='passNum'>pass</button></div>",
        methods: {
          passNum: function () {
            this.$emit("pass", 10);
          },
        },
      };

      new Vue({
        el: "#app",
        data: {
          str: "hi",
        },
        components: {
          "app-header": appHeader,
          "app-content": appContent,
        },
        data: {
          num: 0,
        },
        methods: {
          deliverNum: function (value) {
            this.num = value;
          },
        },
      });
    </script>
  </body>
</html>

```

## 뷰라우터

뷰 라우터는 뷰 라이브러리를 이용하여 싱글 페이지 애플리케이션을 구현할 때 사용하는 라이브러리

[https://router.vuejs.org/installation.html](https://router.vuejs.org/installation.html)

```
<script src="https://unpkg.com/vue-router/dist/vue-router.js">
or
npm install vue-router
```

### 기본형태

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div id="app">

    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
    <script>
        var router = new VueRouter({

        });

        new Vue({
            el: '#app',
            router: router,
        });
    </script>
</body>
</html>
```

### 라우터 뷰

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <router-view></router-view>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
    <script>
      var LoginComponent = {
        template: "<div>login</div>",
      };

      var MainComponent = {
        template: "<div>main</div>",
      };
      var router = new VueRouter({
        // 페이지의 라우팅 정보
        routes: [
          // 로그인 페이지
          {
            // 페이지의 url
            path: "/login",
            // 해당 url에서 표시될 컴포넌트
            component: LoginComponent,
          },
          // 메인 페이지
          {
            path: "/main",
            component: MainComponent,
          },
        ],
      });

      new Vue({
        el: "#app",
        router: router,
      });
    </script>
  </body>
</html>

```

### 라우터 링크

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
        <div>
            <!-- <a>태그로 변환됨 -->
            <router-link to="/login">Login</router-link>
            <router-link to="/main">Main</router-link>
        </div>
      <router-view></router-view>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
    <script>
      var LoginComponent = {
        template: "<div>login</div>",
      };

      var MainComponent = {
        template: "<div>main</div>",
      };
      var router = new VueRouter({
        // 페이지의 라우팅 정보
        routes: [
          // 로그인 페이지
          {
            // 페이지의 url
            path: "/login",
            // 해당 url에서 표시될 컴포넌트
            component: LoginComponent,
          },
          // 메인 페이지
          {
            path: "/main",
            component: MainComponent,
          },
        ],
      });

      new Vue({
        el: "#app",
        router: router,
      });
    </script>
  </body>
</html>

```

VueRouter.mode: URL의 해쉬 값 제거 속성

- 'history': http://127.0.0.1:5500/playground/router.html/main
- defualt: http://127.0.0.1:5500/playground/router.html#/main

VueRouter.routes: 라우팅 할 URL과 컴포넌트 값 지정

[라우터 네비게이션 가이드 관련 설명](https://joshua1988.github.io/web-development/vuejs/vue-router-navigation-guards/)

<router-view> 컴포넌트가 뿌려지는 영역

<router-link to ="이동할 URL">  : <a>태그로 변환되서 나옴

## axios: http 통신 라이브러리

[Ajax 위키백과 링크](https://ko.wikipedia.org/wiki/Ajax)

[Vue Resource Github: 이제 안씀 옛날거](https://github.com/pagekit/vue-resource)

뷰에서 권고하는 HTTP 통신 라이브러리: Axios. Promise 기반의 HTTP통신 라이브러리이며 상대적으로 다른 HTTP통신 라이브러리들에 비해 무선화가잘되어 있고 API가 다양하다.

[Axios Github](https://github.com/axios/axios)

자바스크립트의 비동기 처리 패턴

1. callback : [자바스크립트 비동기 처리와 콜백 함수](https://joshua1988.github.io/web-development/javascript/javascript-asynchronous-operation/)
2. promise : [자바스크립트 Promise 이해하기](https://joshua1988.github.io/web-development/javascript/promise-for-beginners/) 
3. promise + generator
4. async & await : [자바스크립트 async와 await](https://joshua1988.github.io/web-development/javascript/js-async-await/)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Axios</title>
</head>
<body>
  <div id="app">
    <button v-on:click="getData">get user</button>
    <div>
      {{ users }}
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
  <script>
    new Vue({
      el: '#app',
      data: {
        users: []
      },
      methods: {
        getData: function() { 
          var vm = this;
          axios.get('https://jsonplaceholder.typicode.com/users/')
            .then(function(response) {
              console.log(response.data);
              vm.users = response.data;
            })
            .catch(function(error) {
              console.log(error);
            });
        }
      }
    })
  </script>
</body>
</html>
```

[jason데이터 테스트](https://jsonplaceholder.typicode.com/)

[자바스크립트 동작 원리](https://joshua1988.github.io/web-development/translation/javascript/how-js-works-inside-engine/)

[프런트엔드 개발자가 알아야 하는 HTTP프로토콜](https://joshua1988.github.io/web-development/http-part1/)

[구글 크롬 개발자 도구 공식 문서](https://developers.google.com/web/tools/chrome-devtools/)

## 뷰 템플릿 문법

뷰의 템플릿 문법이란 뷰로 화면을 조작하는 방법: 데이터 바인딩 + 디렉티브

데이터 바인딩: 뷰 인스턴스에서 정의한 속성들을 화면에 표시하는 방법 ex) {{ 속성 }}

디렉티브: <span v-if="show"> 처럼 html 태그에 v- 속성 문법

### 데이터 바인딩

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <p>{{num}}</p>
      <p>{{doubleNum}}</p>
      {{str}}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      new Vue({
        el: "#app",
        data: {
          str: "hi",
          num: 10,
        },
        computed: {
          doubleNum: function () {
            return this.num * 2;
          },
        },
      });
    </script>
  </body>
</html>

```

### 뷰 디렉티브

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <p v-bind:id="uuid" v-bind:class="name">{{num}}</p>
      <p>{{doubleNum}}</p>
      <div v-if="loading">
          Loading...
      </div>
      <div v-else>
          test user has benn logged in
      </div>
      <div v-show="loading">
          Loading...
      </div>
      <div>
          <input type="text" v-model="message" placeholder="edit me">
          <p>Message is: {{ message }}</p>
      </div>
      {{str}}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      new Vue({
        el: "#app",
        data: {
          str: "hi",
          num: 10,
          uuid: "abc1234",
          name: "text-blue",
          loading: false,
          message: '',

        },
        computed: {
          doubleNum: function () {
            return this.num * 2;
          },
        },
      });
    </script>
  </body>
</html>

```

v-if: dom 삭제

v-show: disaply:none 설정

[Form Input Binding 공식문서](https://vuejs.org/v2/guide/forms.html#ad)

### methods속성, v-on(키마이벤트)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <button v-on:click="logText">click me</button>
      <input type="text" v-on:keyup.enter='logText'>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      new Vue({
        el: "#app",
        methods: {
          logText: function () {
            console.log("clicked");
          },
        },
      });
    </script>
  </body>
</html>

```

### watch 속성

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      {{ num }}
      <button v-on:click="addNum">increase</button>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      new Vue({
        el: "#app",
        data: {
          num: 10,
        },
        watch: {
          num: function () {
            this.logText();
          },
        },
        methods: {
          addNum: function () {
            this.num = this.num + 1;
          },
          logText: function () {
            console.log("changed");
          },
        },
      });
    </script>
  </body>
</html>

```

watch 속성의 function은 (newVlaue, oldValue)를 기본적으로 받을 수 있음

### watch vs computed

[watch 속성과 computed 속성 차이점](https://vuejs.org/v2/guide/computed.html#ad)

watch: 무거운 로직, 매번 실행되는게 부담스러운 로직

computed: 단순한 값에 대한 계산, validation

일반적인경우는 보통 computed를 쓰는게 좋음

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
</head>
<body>
  <div id="app">
    {{ num }}
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    new Vue({
      el: '#app',
      data: {
        num: 10
      },
      computed: {
        doubleNum: function() {
          return this.num * 2;
        }
      },
      watch: {
        num: function(newValue, oldValue) {
          this.fetchUserByNumber(newValue);
        }
      },
      methods: {
        fetchUserByNumber: function(num) {
          // console.log(num);
          axios.get(num);
        }
      }
    });
  </script>
</body>
</html>
```

### computed

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
  <style>
  .warning {
    color: red;
  }
  </style>
</head>
<body>
  <div id="app">
    <p v-bind:class="{ warning:isError }">Hello</p>
    <p v-bind:class="errorTextColor">Hello</p>
  </div>
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    new Vue({
      el: '#app',
      data: {
        // cname: 'blue-text',
        isError: false
      },
      computed: {
        errorTextColor: function() {
          // if (isError) {
          //   return 'warning'
          // } else {
          //   return null;
          // }
          return this.isError ? 'warning' : null;
        }
      }
    });
  </script>
</body>
</html>
```

## VueCLI

[https://cli.vuejs.org/](https://cli.vuejs.org/)

```
npm install -g @vue/cli
```

%USERPROFILE%\AppData\Roaming\npm\node_modules

[https://stackoverflow.com/questions/5926672/where-does-npm-install-packages](https://stackoverflow.com/questions/5926672/where-does-npm-install-packages)

[웹 개발시 알아두면 좋은 리눅스 명령어](https://joshua1988.github.io/web-development/linux-commands-for-beginners/)

```
Vue CLI 3.x
vue create '프로젝트 폴더 위치'
vue create vue-cli
cd vue-cli
npm run serve
build
lint
```

### CLI 프로젝트 폴더구조 등

public/index.html : npm run serve시 실행됨 -> main.js -> App.vue

### 싱글파일 컴포넌트

.vue: html, javascript, css를 한 파일에서 관리

```vue
<template>
  <!-- HTML: template -->
  <div>header</div>
</template>

<script>
export default {
  // Javascript: methods
  methods: {
    addNum: function() {},
  },
};
</script>

<style>
/* CSS */
</style>
```

```
<hello-world></hello-world>
<HelloWorld/>
```

### 프로젝트 시작시 코드정리

- components/HelloWorld.vue 삭제
- src/App.vue 내용 전체 삭제
- vue [Tap]

```vue
<template>
  <div>
    {{ str }}
  </div>
</template>

<script>
export default {
  // namespace 를 function()으로 감춰줘야 한다.
  data: function(){
    return {
      str: 'hi'
    }
  }
}
</script>

<style>

</style>
```

### 컴포넌트 등록하기

컴포넌트 이름은 최소 두단어로 파스칼케이스로 AppHeader.vue

`src/App.vue`

```vue
<template>
  <div>
    <app-header></app-header>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
export default {
  // namespace 를 function()으로 감춰줘야 한다.
  data: function(){
    return {
      str: 'hi'
    }
  }, 
  components:{
    'app-header': AppHeader,
  },
}
</script>

<style>

</style>
```

`src/components/AppHeader.vue`

```vue
<template>
  <header>
      <h1>Header</h1>
  </header>
</template>

<script>
export default {

}
</script>

<style>

</style>
```

### props 구현

`src/App.vue`

```vue
<template>
  <div>
    <app-header v-bind:propsdata="str"></app-header>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
export default {
  // namespace 를 function()으로 감춰줘야 한다.
  data: function(){
    return {
      str: 'Header'
    }
  }, 
  components:{
    'app-header': AppHeader,
  },
}
</script>

<style>

</style>
```

`src/components/AppHeader.vue`

```vue
<template>
  <header>
      <h1>{{ propsdata }}</h1>
  </header>
</template>

<script>
export default {
    props: ['propsdata']

}
</script>

<style>

</style>
```

### event emit 구현

`src/App.vue`

```vue
<template>
  <div>
    <app-header v-bind:propsdata="str" v-on:renew="renewStr"></app-header>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
export default {
  // namespace 를 function()으로 감춰줘야 한다.
  data: function(){
    return {
      str: 'Header'
    }
  }, 
  components:{
    'app-header': AppHeader,
  },
  methods:{
    renewStr: function(){
      this.str = 'hi';
    },
  },
}
</script>

<style>

</style>
```

`src/components/AppHeader.vue`

```vue
<template>
  <header>
      <h1>{{ propsdata }}</h1>
      <button v-on:click="sendEvent">send</button>
  </header>
</template>

<script>
export default {
    props: ['propsdata'],
    methods: {
        sendEvent: function(){
            this.$emit('renew')
        },
    },
}
</script>

<style>

</style>
```

## 사용자 입력폼 만들기

```
vue create vue-form 
default
```

### HTML 작업

`src/App.vue`

```html
<template>
<div>
  <form action="">
    <div>
      <label for="username">id: </label>
      <input id="username" type="text">
    </div>
    <div>
      <label for="password">pw: </label>
      <input id="password" type="password">
    </div>
    <button>login</button>
  </form>
</div>
</template>

<script>
export default {

}
</script>

<style>

</style>
```

### v-model & submit

[이벤트 버블링과 캡쳐링](https://joshua1988.github.io/web-development/javascript/event-propagation-delegation/)

`src/App.vue`

```html
<template>
<div>
  <form v-on:submit="submitForm">
    <div>
      <label for="username">id: </label>
      <input id="username" type="text" v-model="username">
    </div>
    <div>
      <label for="password">pw: </label>
      <input id="password" type="password" v-model="password">
    </div>
    <button type="submit">login</button>
  </form>
</div>
</template>

<script>
export default {
  data: function(){
    return {
      username: '',
      password: '',
    }
  },
  methods:{
    submitForm: function(event){
      event.preventDefault(); // 서브밋시 새로고침 방지
      console.log(this.username, this.password)
    },
  },
}
</script>

<style>

</style>
```

### axios & form 구현

```
npm i axios
```

`src/App.vue`

```vue
<template>
<div>
  <form v-on:submit.prevent="submitForm">
    <div>
      <label for="username">id: </label>
      <input id="username" type="text" v-model="username">
    </div>
    <div>
      <label for="password">pw: </label>
      <input id="password" type="password" v-model="password">
    </div>
    <button type="submit">login</button>
  </form>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data: function(){
    return {
      username: '',
      password: '',
    }
  },
  methods:{
    submitForm: function(){
      // event.preventDefault(); // 서브밋시 새로고침 방지
      console.log(this.username, this.password)
      var url = 'https://jsonplaceholder.typicode.com/users';
      var data = {
        username: this.username, 
        passworld: this.passworld
      }
      axios.post(url, data)
      .then(function(response){
        console.log(response);
      })
      .catch(function(error){
        console.log(error);
      });
    },
  },
}
</script>

<style>

</style>
```

### 자동완성

```html
<template>
    <div class="wrap">
  <div id="app" 
       v-on:keyup.down="selectValue('down')"
       v-on:keyup.up="selectValue('up')">
    <div class="search">
      <input class="s" placeholder="'장'을 써보세요" 
             v-on:input="searchQuery=event.target.value">
      <ul class="r" tabindex="0" 
          v-bind:class="{ show: isActive }"
          v-on:mouseover="removeValue">
        <li tabindex="-1" 
            v-for="(el, index) in filterList" 
            v-on:click="changeValue(el.name)"
            v-on:keyup.enter="selectValue('enter', el.name)">
          <span>{{ el.name }}</span>
        </li>
      </ul>
      <p>Console: <strong>On</strong></p>
    </div>
  </div>
</div>
</template>
<script>
    var names = [
  { name: '김건모 잘못된 만남' },
  { name: '홍길동' },
  { name: '손오공' },
  { name: '공민지' },
  { name: '장동건' },
  { name: '장희빈' },
  { name: '고추장' },
  { name: '된장' },
  { name: '장장' },
  { name: '희야' },
];

var app = new Vue({
  el: '#app',
  data: {
    isActive: false,
    searchQuery: '',
    names: names,
  },
  methods: {
    changeValue(str) {
      console.log(`change value: ${str}`);
      this.isActive = false;
      document.querySelector('.s').value = str;
    },
    selectValue(keycode, str) {
      if (this.isActive === true) {
        const hasClass = document.querySelector('.r').classList.contains('key');
        if (keycode === 'down') {
          if (!hasClass) {
            const thisEl = document.querySelectorAll('.r li')[0];
            document.querySelector('.r').classList.add('key');
            thisEl.classList.add('sel');
            thisEl.focus();
          } else {
            const lastEl = document.querySelector('.r li:last-child');
            const thisEl = document.querySelector('.r li.sel');
            const nextEl = thisEl.nextElementSibling;
            if (!lastEl.classList.contains('sel')) {
              thisEl.classList.remove('sel');
              nextEl.classList.add('sel');
              nextEl.focus();
            }
          }
        }
        if (keycode === 'up' && hasClass) {
          const firstEl = document.querySelectorAll('.r li')[0];
          const thisEl = document.querySelector('.r li.sel');
          const prevEl = thisEl.previousElementSibling;
          if (!firstEl.classList.contains('sel')) {
            thisEl.classList.remove('sel');
            prevEl.classList.add('sel');
            prevEl.focus();
          } else {
            document.querySelector('.s').focus();
          }
        }
        if (keycode === 'enter' && hasClass) {
          this.changeValue(str);
        }
      }
    },
    removeValue() {
      if (document.querySelector('.r').classList.contains('key')) {
        document.querySelector('.r').classList.remove('key');
        document.querySelector('.r li.sel').classList.remove('sel');
      }
    },
  },
  computed: {
    filterList() {
      const str = this.searchQuery;
      const reg = /[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9|\s]/.test(str);
      console.log(`typing value: ${str}`);
      if (reg === false && str !== '' && str !== ' ') {
        this.isActive = true;
        return this.names.filter((el) => {
          return el.name.match(str);
        });
      } else {
        this.isActive = false;
      }
    },
  },
});
</script>
<style>
    html, body {
  height: 100%;
}
body {
  background-color: #ddd;
  font-size: 14px;
  color: #333;
}
strong {
  font-weight: bold;
}
.wrap {
  display: table;
  padding: 200px 20px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
#app {
  display: table-cell;
  vertical-align: middle;
  text-align: center;
  .search {
    position: relative;
    margin: 0 auto;
    width: 100%;
    max-width: 600px;
    .s {
      padding: 10px 20px;
      width: 100%;
      max-width: 600px;
      height: 60px;
      box-sizing: border-box;
      box-shadow: 0 0 3px rgba(#000, 0.2);
      border: 1px solid #888;
      font-size: 16px;
    }
    .r {
      display: none;
      position: absolute;
      left: 0;
      top: 60px;
      width: 100%;
      height: 156px;
      overflow-y: auto;
      &.show {
        display: block;
      }
      li {
        margin-top: -1px;
        padding: 0 20px;
        width: 100%;
        height: 40px;
        background-color: #fff;
        box-sizing: border-box;
        border: 1px solid #888;
        outline: none;
        font-size: 16px;
        line-height: 40px;
        cursor: pointer;
        &:hover, &.sel {
          background-color: darken(#fff, 5%);
        }
      }
    }
    p {
      padding: 10px 0;
      text-align: right;
      font-size: 12px;
    }
  }
}
</style>
```



## Refer

- [Vue 공식문서](https://vuejs.org/v2/guide/)
- [Vue 스타일가이드](https://vuejs.org/v2/style-guide/)
- [Vue Cookbook](https://vuejs.org/v2/cookbook/)
- [Vuex 공식문서](https://vuex.vuejs.org/)
- [VueRouter 공식문서](https://router.vuejs.org/)
- [Vue CLI 공식문서](https://cli.vuejs.org/)
- [https://moonspam.github.io/Vuejs-Autocomplete/](https://moonspam.github.io/Vuejs-Autocomplete/)