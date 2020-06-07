





# WebPack

비슷한 web task manager로, grunt, glup 같은게 있으나 WebPack을 많이 씀

## 설치

[강좌 리포지토리](https://github.com/joshua1988/LearnWebpack)

[웹팩 핸드북](https://joshua1988.github.io/webpack-guide/guide.html)

## NodeJs, NPM

NPM: Node Package Manager: 자바스크트립트 패키지 관리자

NPM 시작

[NPM](https://joshua1988.github.io/webpack-guide/build/npm-module-install.html#npm-전역-설치-경로)

```
node -v // node 버전확인
npm -v // npm 버전확인
npm init -y
```

라이브러리 설치

```
npm install jquery
```

NPM을 사용하는 이유와 장점

- 라이브러리 버전 및 의존성 관리
- CDN이 아닌 로컬에 설치할 수 있음

## NPM

### 설치명령어

```
npm install gulp // 지역설치
npm uninstall gulp
npm install gulp --global // 전역설치 %USERPROFILE%\AppData\Roaming\npm\node_modules
```

- 전역설치 : 프로젝트에서 사용할 라이브러리를 불러올 때 사용하는 것이 아니라 시스템 레벨에서 사용할 자바스크립트 라이브러릴 설치할 때 사용 
- 지역설치 옵션 2가지
  - npm install jquery --save-prod // npm i jquery : dependencies 설치
  - npm install jquery --save-dev // npm i jquery -D : devDependencies 설치
- dependencies와 devDependencies의 차이
  - depenedencies: jquery, jquery-ui, react, angular, vue, chart등 애플리케이션 동작에 필요한 라이브러리
  - devDependencies: webpack, js-compression, sass등 개발할때 도움을 주는 개발용 보조 라이브러리 

```
npm run builde : devDependencies 의 라이브러리는 제외
```



## 웹팩시작

웹팩이란 최신 프런트엔드 프레임워크에서 가장 많이 사용되는 모듈 번들러. 모듈 번들러란 웹 어플리케이션을 구성하는 자원(HTML, CSS, Javascript, Images 등)을 모두 각각의 모듈로 보고 이를 조합해서 병합된 하나의 결과물을 만드는 도구

### 모듈번들링

웹 애플리케이션을 구성하는 몇십, 몇백개의 자원들을 하나의 파일로 병합 및 압축 해주는 동작

### 튜토리얼

```
npm init -y // npm 초기화
npm i webpack webpack-cli -D // 개발용 라이브러리 설치
npm i lodash // JS 유틸리티 라이브러리 설치
```

`index.html`

```html
<html>
  <head>
    <title>Webpack Demo</title>
    <script src="https://unpkg.com/lodash@4.16.6"></script>
  </head>
  <body>
    <script src="src/index.js"></script>
  </body>
</html>
```

`src/index.js`

```javascript
function component() {
  var element = document.createElement('div');

  /* lodash is required for the next line to work */
  element.innerHTML = _.join(['Hello','webpack'], ' ');

  return element;
}

document.body.appendChild(component());
```

웹팩 빌드를 위한 구성 및 빌드

`index.js`

```javascript
import _ from 'lodash';

function component() {
    var element = document.createElement('div');
  
    /* lodash is required for the next line to work */
    element.innerHTML = _.join(['Hello','webpack'], ' ');
  
    return element;
  }
  
  document.body.appendChild(component());
```

`index.html`

```html
<html>
  <head>
    <title>Webpack Demo</title>
    <!-- <script src="https://unpkg.com/lodash@4.16.6"></script> -->
  </head>
  <body>
    <!-- <script src="src/index.js"></script> -->
    <script src="./dist/main.js"></script>
  </body>
</html>
```

`package.json` 추가

```json
{
  "name": "getting-started",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "webpack --mode=none"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "webpack": "^4.43.0",
    "webpack-cli": "^3.3.11"
  },
  "dependencies": {
    "lodash": "^4.17.15"
  }
}

```

--entry=src/index.js --output=public/output.js

```
npm run build
```

mode는 production, development, none 3가지 존재

웹팩 설정파일 추가

`webpack.config.js`

```javascript
// webpack.config.js
// `webpack` command will pick up this config setup by default
var path = require('path');

module.exports = {
  mode: 'none',
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  }
};
```

[node path api](https://nodejs.org/api/path.html)

`package.json`

```javascript
{
  "name": "getting-started",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "webpack"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "webpack": "^4.43.0",
    "webpack-cli": "^3.3.11"
  },
  "dependencies": {
    "lodash": "^4.17.15"
  }
}
```

[즉시실행함수](https://developer.mozilla.org/ko/docs/Glossary/IIFE)

## 웹팩소개

[유튭](https://www.youtube.com/watch?v=WQue1AN93YU)

웹팩에서 지칭하는 모듈이라는 개념은 자바스크립트 모듈에만 국한되지 않고 웹 애플리케이션을 구성하는 모든 자원을 의미. 웹 애플리케이션을 제작하려면 HTML, CSS, Javascript, Images, Font 등 많은 파일들이 필요 이 하나 하나가 모두 모듈



웹 개발 작업 자동화 도구

- HTML, CSS, JS 압축
- 이미지 압축
- CSS 전처리기 변환

이를 위해 Grunt나 Gulp같은 도구들이 등장 + 모듈관리 = WebPack

웹 애플리케이션의 빠른 로딩 속도와 높은 성능

서버로 요청하는 파일 숫자를 줄이기 + 나중에 필요한 자원들은 나중에 요청하는 레이지 로딩(Lazy Loading)

### 해결하려는 문제

- 자바스크립트 변수 유효 범위 문제
- 브라우저별 HTTP 요청 숫자의 제약: 평균 동시 요청 가능 갯수 6개
- 사용하지 않는 코드의 관리
- 다이나믹 로딩, 레이지 로딩



## 바벨&ES6

[바벨 공식 사이트](https://babeljs.io/)

바벨 : 자바스크립트 컴파일러로 ES6 문법을 하위 버전 문법으로 변환하여 브라우저 호환성을 높여줌

### ES6 문법

[ES6 Modules 문법 소개](https://joshua1988.github.io/es6-online-book/modules.html)

```
export 변수, 함수
export var pi = 3.14;
export function sum(a,b) {
    return a+b;
}
```

```
import { 불러올 변수 또는 함수 이름 } from '파일 경로';
import { pi } from './math.js'
import { sum } from './math.js';

console.log(pi);
sum(10, 20);
```



## 웹팩속성

[웹팩 4가지 주요속성](https://joshua1988.github.io/webpack-guide/concepts/overview.html)

### entry

웹팩에서 웹 자원을 변환하기 위해 필요한 최초 진입점이자 자바스크립트 경로

```
// webpack.config.js
module.exporters = {
    entry: './src/index.js'
}
```



### output

웹팩을 돌리고 난 결과물의 파일 경로

```
// webpack.config.js
module.exports = {
    output: {
        filename: 'bundle.js'
    }
}


  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  }
```

브라우져 캐싱때문에 '[chunkhash].bundle.js' 같이 사용할 수도 있다.

### loader

웹팩이 웹 애플리케이션을 파일 관계를 파악할 때 자바스크립트 파일이 아닌 웹 자원(HTML, CSS, Images, 폰트 등)들을 자바스크립트 파일 안으로 들어올 수 있도록 변환할 수 있도록 도와주는 속성

```
// webpack.config.js
module.exports = {
    modlue: {
        rules: []
    }
}
```

### 실습

```
npm init -y
npm i webpack webpack-cli css-loader style-loader mini-css-extract-plugin -D
```

`index.html`

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>CSS & Libraries Code Splitting</title>
  </head>
  <body>
    <header>
      <h3>CSS Code Splitting</h3>
    </header>
    <div>
      <!-- 웹팩 빌드 결과물이 잘 로딩되면 아래 p 태그의 텍스트 색깔이 파란색으로 표시됨 -->
      <p>
        This text should be colored with blue after injecting CSS bundle
      </p>
    </div>
    <!-- 웹팩의 빌드 결과물을 로딩하는 스크립트 -->
    <script src="./dist/bundle.js"></script>
  </body>
</html>
```

`base.css`

```
p {
  color : blue;
}
```

`index.js`

```
import './base.css';
```

`webpack.config.js`

```javascript
var path = require('path');

module.exports = {
  mode: 'none',
  entry: './index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
}
```

`package.json`

```json
{
  "name": "code-splitting",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "webpack"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "css-loader": "^3.5.3",
    "mini-css-extract-plugin": "^0.9.0",
    "style-loader": "^1.2.1",
    "webpack": "^4.43.0",
    "webpack-cli": "^3.3.11"
  }
}

```

npm run build

### 설정파일분석

`webpack.config.js`

```javascript
var path = require('path');

module.exports = {
  mode: 'none', // production, development, none
  entry: './index.js',
  output: {
    filename: 'bundle.js', // [name][chunkhash].js
    path: path.resolve(__dirname, 'dist')
  },
  module: { //loader
    rules: [
      {
        test: /\.css$/, // css 확장자의 모든 파일을 대상으로 
        use: ['style-loader', 'css-loader', 'sass-loader'] 
          // css-loader와 style-loader 사용 순서중요 오른쪽부터 적용
      }
    ]
  },
}
```

css-loader : css를 javascript에 넣을 수 있도록함

style-loader: javascript에 들어온 css를 head태그안에 inline으로 넣어서 적용시킴

CSS 파일을 별도로 분리하기 위해 MiniCssExtractPlugin 플로그인 설정 추가

`webpack.config.js`

```javascript
var path = require("path");
var MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  mode: "none",
  entry: "./index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist"),
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [{ loader: MiniCssExtractPlugin.loader }, "css-loader"],
      },
    ],
  },
  plugins: [new MiniCssExtractPlugin()],
};

```

dist/main.css 생성됨

index.html에 <link rel="stylesheet" href="./dist/main.css"> 추가

### plugin

웹팩의 기본적인 동작에 추가적인 기능을 제공하는 속성. 로더랑 비교하면 로더는 파일을 해석하고 변환하는 과정에 관여하는 반면, 플러그인은 해당 결과물의 형태를 바꾸는 역할

```
module.exports={
    plugins: []
}

var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    plugins: [
        new HtmlWebpackPlugin(), // 웹팩으로 빌드한 결과물로 HTML 파일을 생성해주는 플러그인
        new webpack.ProgressPlugin() // 웹팩의 빌드 진행율을 표시해주는 플러그인
    ]
}
```

- split-chunks-plugin
- clean-webpack-plugin
- image-webpack-loader
- webpack-bundle-analyzer-plugin

### 리뷰

[관련문서](https://joshua1988.github.io/webpack-guide/concepts/wrapup.html)

## 참고자료

[로더](https://webpack.js.org/loaders/)

[플러그인](https://webpack.js.org/plugins/)

## 웹팩데브서버

빌드 없이 결과 확인

웹 애플리케이션을 개발하는 과정에서 유용하게 쓰이는 도구, 웹팩의 빌드 대상 파일이 변경 되었을 때 매번 웹팩 명령어를 실행하지 않아도 코드만 변경하고 코드만 변경하고 저장하면 웹팩으로 빌드 후 브라우저를 새로고침 해줌

매번 명령어를 치는 시간과 브라우저를 새로 고침하는 시간 뿐만 아니라 웹팩 빌드 시간 또한 줄여주기 때문에 웹팩 기반의 웹 애플리케이션 개발에 필수

파일레벨로 빌드 결과를 내지 않고 메모리 레벨에서만 동작

[관련문서](https://joshua1988.github.io/webpack-guide/devtools/webpack-dev-server.html)

```
npm init -y
npm i webpack webpack-cli webpack-dev-server html-webpack-plugin -D
```

`package.json`

```
{
  // ...
  "scripts": {
    "dev": "webpack-dev-server"
  },
}
```

`index.html`

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Webpack Dev Server</title>
  </head>
  <body>
    <!-- 빌드 결과물이 정상적으로 로딩되면 아래 div 태그의 텍스트가 변경됨 -->
    <div class="container">
      TBD..
    </div>
    <!-- HTML Webpack Plugin에 의해 웹팩 빌드 내용이 아래에 추가됨 -->
  </body>
</html>
```

`index.js`

```javascript
var div = document.querySelector('.container');
div.innerText = 'Webpack loaded!!';
```

`webpack.config.js`

```javascript
var path = require('path');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  mode: 'none',
  entry: './index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  devServer: {
    port: 9000,
  },
  plugins: [
    new HtmlWebpackPlugin({
      // index.html 템플릿에 빌드 결과물의 include 태그들을 추가해줌
      template: 'index.html',
    }),
  ],
};
```

[튜토리얼](https://joshua1988.github.io/webpack-guide/tutorials/webpack-dev-server.html)

[HtmlWebpackPlugin](https://webpack.js.org/plugins/html-webpack-plugin/)

## 실전 설정파일

```javascript
var path = require('path')
var webpack = require('webpack')

module.exports = {
  mode: 'production',
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/', // CDN 배포시 사용 속성
    filename: 'build.js'
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ],
      },      
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map' // 빌드 소스와 실제파일 소스를 연결하여 디버깅을 도움
}

// webpack v3까지 v4는 필요 없음
// if (process.env.NODE_ENV === 'production') {
//   module.exports.devtool = '#source-map'
//   // http://vue-loader.vuejs.org/en/workflow/production.html
//   module.exports.plugins = (module.exports.plugins || []).concat([
//     new webpack.DefinePlugin({
//       'process.env': {
//         NODE_ENV: '"production"'
//       }
//     }),
//     new webpack.optimize.UglifyJsPlugin({
//       sourceMap: true,
//       compress: {
//         warnings: false
//       }
//     }),
//     new webpack.LoaderOptionsPlugin({
//       minimize: true
//     })
//   ])
// }
```

