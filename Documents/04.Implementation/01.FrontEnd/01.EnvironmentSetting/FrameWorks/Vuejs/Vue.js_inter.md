# VueJs Intermediate - Todo App

## Requirement

- [Chrome](https://www.google.com/intl/ko/chrome/)
  - [VueDevTool for Chrome](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
- [VScode](https://code.visualstudio.com/)
  - TSLint
  - Vetur
- [NodeJs](https://nodejs.org/en/)
- [Git](https://git-scm.com/downloads)

```
vue create vue-todo
cd vue-todo
npm run serve
```

## App 구현

### 컴포넌트 생성 및 등록

```
src/components/TodoHeader.vue
src/components/TodoInput.vue
src/components/TodoList.vue
src/components/TodoFotter.vue
```

`src/App.vue`

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <TodoInput></TodoInput>
    <TodoList></TodoList>
    <TodoFooter></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from './components/TodoHeader.vue'
import TodoInput from './components/TodoInput.vue'
import TodoList from './components/TodoList.vue'
import TodoFooter from './components/TodoFooter.vue'


export default {
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    'TodoHeader': TodoHeader,
    'TodoInput': TodoInput,
    'TodoList': TodoList,
    'TodoFooter': TodoFooter,
  }
}
</script>

// scope이 없으면 하위 컴포넌트까지 css가 적용된다.
<style>
body{
  text-align: center;
  background-color: #F6F6F6;
}
input{
  border-style: groove;
  width: 200;

}
button{
  border-style: groove;
}
.shadow {
  box-shadow: 5px 10px 10px rgba(0,0,0,0.03);
}
</style>

```

### 파비콘,아이콘,폰트,반응형 웹태그

[파비콘 생성태그](https://www.favicon-generator.org/)

[awsomefont](https://fontawesome.com/account/cdn)

[GoogleFonts](https://fonts.google.com/specimen/Ubuntu?query=ubuntu&sidebar.open&selection.family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700)

`public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="icon" href="<%= BASE_URL %>favicon.ico">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.13.0/css/all.css" integrity="sha384-Bfad6CLCknfcloXFOyFnlgtENryhrpZCe29RTifKEixXQZ38WheV+i/6YWSzkz3V" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Ubuntu" rel="stylesheet">
    <title><%= htmlWebpackPlugin.options.title %></title>
  </head>
  <body>
    <noscript>
      <strong>We're sorry but <%= htmlWebpackPlugin.options.title %> doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
    </noscript>
    <div id="app"></div>
    <!-- built files will be auto injected -->
  </body>
</html>

```

### TodoHeader

`components/TodoHeader.vue`

```vue
<template>
  <div>
      <header>
          <h1>TODO it!</h1>
      </header>
  </div>
</template>

// 파일 스코프
<style scoped>
h1{
    color: #2F3B52;
    font-weight: 900;
    /* 바깥여백: rem 폰트크기에 따른 배율 단위 */
    margin: 2.5rem 0 1.5rem
}

</style>
```

### TodoInput 

#### 구현

`components/TodoInput.vue`

```vue
<template>
  <div>
      <!-- v-model 2-way binding wth newTodoItem data -->
      <input type="text" v-model="newTodoItem">
      <!-- click event handling with addTodo method -->
      <button v-on:click="addTodo">add</button>
  </div>
</template>

<script>
export default {
    data: function(){
        return {
            newTodoItem: ""
        }
    },
    methods:{
        addTodo: function(){
            localStorage.setItem(this.newTodoItem, this.newTodoItem);
            this.newTodoItem = "";
        }
    }

}
</script>

<style>

</style>
```

[로컬 스토리지 setItem() API 가이드](https://developer.mozilla.org/en-US/docs/Web/API/Storage/setItem)

#### 리팩터링

- input 공백 처리 함수 분리
- 엔터키 처리
- 버튼 대신 span 태그
- css 및 fontawesome icon 적용

[fontawesome](https://fontawesome.com/)

`components/TodoInput.vue`

```vue
<template>
  <div class="inputBox shadow">
      <!-- v-model 2-way binding wth newTodoItem data -->
      <!-- keyboard event handling with addTodo method -->
      <input type="text" v-model="newTodoItem" v-on:keyup.enter="addTodo">
      <!-- click event handling with addTodo method -->
      <span class="addContainer" v-on:click="addTodo" >
          <!-- fontawsome icon apply: fas fa-plus -->
          <i class="fas fa-plus addBtn"></i>
      </span>
  </div>
</template>

<script>
export default {
    data: function(){
        return {
            newTodoItem: ""
        }
    },
    methods:{
        addTodo: function(){
            localStorage.setItem(this.newTodoItem, this.newTodoItem);
            this.clearInput();
        }, 
        clearInput: function(){
            this.newTodoItem = "";
        }
    }

}
</script>

<style scoped>
  input:focus {
    outline: none;
  }
  .inputBox {
    height: 50px;
    border-radius: 5px;
    line-height: 50px;
    background: white;
  }
  .inputBox input {
    border-style: none;
    font-size: 0.9rem;
  }
  .addContainer {
    display: block;
    float: right;
    width: 3rem;
    border-radius: 0 5px 5px 0;
    background: linear-gradient(to right, #6478FB, #8763FB);
  }
  .addBtn {
    color: white;
    vertical-align: middle;
  }
  .closeModalBtn {
    color: #42b983;
  }
</style>
```

### TodoList

#### 구현

`components/TodoList.vue`

```vue
<template>
  <div>
      <ul>
          <li v-for="todoItem in todoItems" v-bind:key='todoItem'>{{ todoItem }}</li>
      </ul>
  </div>
</template>

<script>
export default {
    data: function(){
        return {
            todoItems: []
        }
    },
    // created : 인스턴스 생성시점에 hook( call )
    created: function(){
        if(localStorage.length > 0){
            for (var i = 0; i < localStorage.length ; i++){
                if ((localStorage.key(i) !== "loglevel:webpack-dev-server") &&
                    (localStorage.key(i) !== "OTelJS.ClientId")){
                    this.todoItems.push(localStorage.key(i));
                    }
            }
        }
    }
}
</script>

<style>

</style>
```

#### 리팩터링

```vue
<template>
  <div>
      <ul>
          <li v-for="todoItem in todoItems" v-bind:key='todoItem' class="shadow">
            {{ todoItem }}
            <!-- click event Handling with removeTodo method -->
            <span class="removeBtn" v-on:click="removeTodo">
                <i class="fas fa-trash-alt"></i>
            </span>
            </li>
      </ul>
  </div>
</template>

<script>
export default {
    data: function(){
        return {
            todoItems: []
        }
    },
    methods:{
        removeTodo: function(){

        }
    },
    // created : 인스턴스 생성시점에 hook( call )
    created: function(){
        if(localStorage.length > 0){
            for (var i = 0; i < localStorage.length ; i++){
                if ((localStorage.key(i) !== "loglevel:webpack-dev-server") &&
                    (localStorage.key(i) !== "OTelJS.ClientId")){
                    this.todoItems.push(localStorage.key(i));
                    }
            }
        }
    }
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding-left: 0;
  margin-top: 0;
  text-align: left;
}
li {
  display: flex;
  min-height: 50px;
  line-height: 50px;
  margin: 0.5rem 0;
  padding: 0 0.9rem;
  border-radius: 5px;
  background: white;
}
.checkBtn {
  line-height: 45px;
  color: #62acde;
  margin-right: 5px;
}
.checkBtnCompleted {
  color: #b3adad;
}
.textCompleted {
  text-decoration: line-through;
  color: #b3adad;
}
.removeBtn {
  margin-left: auto;
  color: #de4343;
}

</style>
```

#### 삭제기능 구현

[MDN splice() API](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/splice)

```vue
<template>
  <div>
      <ul>
          <li v-for="(todoItem, index) in todoItems" v-bind:key='todoItem' class="shadow">
            {{ todoItem }}
            <!-- click event Handling with removeTodo method -->
            <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
                <i class="fas fa-trash-alt"></i>
            </span>
            </li>
      </ul>
  </div>
</template>

<script>
export default {
    data: function(){
        return {
            todoItems: []
        }
    },
    methods:{
        removeTodo: function(todoItem, index){
            localStorage.removeItem(todoItem);
            this.todoItems.splice(index, 1);
        }
    },
    // created : 인스턴스 생성시점에 hook( call )
    created: function(){
        if(localStorage.length > 0){
            for (var i = 0; i < localStorage.length ; i++){
                if ((localStorage.key(i) !== "loglevel:webpack-dev-server") &&
                    (localStorage.key(i) !== "OTelJS.ClientId")){
                    this.todoItems.push(localStorage.key(i));
                    }
            }
        }
    }
}
</script>
```



#### 완료기능 구현

`TodoInput.vue`

```javascript
  methods: {
    addTodo: function() {
      if (this.newTodoItem !== "") {
        var obj = { completed: false, item: this.newTodoItem };
        localStorage.setItem(this.newTodoItem, JSON.stringify(obj));
        this.clearInput();
      }
    },
    clearInput: function() {
      this.newTodoItem = "";
    }
  }
```

`TodoList.vue`

```vue
<template>
  <div>
    <ul>
      <li v-for="(todoItem, index) in todoItems" v-bind:key="todoItem.item" class="shadow">
        <i class="checkBtn fas fa-check" v-bind:class="{checkBtnCompleted: todoItem.completed}" 
        v-on:click="toggleComplete(todoItem)"></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <!-- click event Handling with removeTodo method -->
        <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
          <i class="fas fa-trash-alt"></i>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      todoItems: []
    };
  },
  methods: {
    removeTodo: function(todoItem, index) {
      localStorage.removeItem(todoItem);
      this.todoItems.splice(index, 1);
    },
    toggleComplete: function(todoItem) {
        todoItem.completed = !todoItem.completed;
        // 로컬 스토리지 데이터 갱신
        localStorage.removeItem(todoItem);
        localStorage.setItem(todoItem.item, JSON.stringify(todoItem));
    }
  },
```

### TodoFooter

`TodoFooter.vue`

```vue
<template>
  <div class="clearAllContainer">
      <span class="clearAllBtn" v-on:click="clearTodo">Clear All</span>
  </div>
</template>

<script>
export default {
    methods: {
        clearTodo: function(){
            localStorage.clear();
        }
    }
}
</script>

<style scoped>
.clearAllContainer {
  width: 8.5rem;
  height: 50px;
  margin: 0 auto;
  line-height: 50px;
  border-radius: 5px;
  background-color: white;
} 
.clearAllBtn {
  display: block;
  color: #e20303;
} 
</style>
```



## Refactoring

### 문제점진단

- 아이템 추가시 리스트 자동갱신 안됨
- Clear All로 삭제시 리스트 자동갱신 안됨
- TodoInput, TodoFooter에서는 event emit만 하고 App 컴포넌트에서 데이터 핸들링을 하고 그 결과를 App에서 TodoList 로 prop시킨다.
- App: Container: Business Loginc
- 나머지 : 표현단 : Presentor component

### 할 일 목록 표시 기능

TodoList의 데이터 load기능을 App으로 이동

`TodoList.vue`

```vue
<template>
  <div>
    <ul>
      <li v-for="(todoItem, index) in propsdata" v-bind:key="todoItem.item" class="shadow">
        <i
          class="checkBtn fas fa-check"
          v-bind:class="{checkBtnCompleted: todoItem.completed}"
          v-on:click="toggleComplete(todoItem)"
        ></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <!-- click event Handling with removeTodo method -->
        <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
          <i class="fas fa-trash-alt"></i>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ["propsdata"],
  methods: {
    removeTodo: function(todoItem, index) {
      localStorage.removeItem(todoItem);
      this.todoItems.splice(index, 1);
    },
    toggleComplete: function(todoItem) {
      todoItem.completed = !todoItem.completed;
      // 로컬 스토리지 데이터 갱신
      localStorage.removeItem(todoItem);
      localStorage.setItem(todoItem.item, JSON.stringify(todoItem));
    }
  }
};
</script>
```

`App.vue`

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <TodoInput></TodoInput>
    <!-- v-bind:내려보낼 프롭스 속성 이름 = "현재 위치의 데이터 이름" -->
    <TodoList v-bind:propsdata="todoItems"></TodoList>
    <TodoFooter></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from "./components/TodoHeader.vue";
import TodoInput from "./components/TodoInput.vue";
import TodoList from "./components/TodoList.vue";
import TodoFooter from "./components/TodoFooter.vue";

export default {
  data: function() {
    return {
      todoItems: []
    };
  },
  // created : 인스턴스 생성시점에 hook( call )
  created: function() {
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          this.todoItems.push(
            JSON.parse(localStorage.getItem(localStorage.key(i)))
          );
        }
      }
    }
  },
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    TodoHeader: TodoHeader,
    TodoInput: TodoInput,
    TodoList: TodoList,
    TodoFooter: TodoFooter
  }
};
</script>
```

### 할 일 추가 기능

`TodoInput.vue`

```vue
<template>
  <div class="inputBox shadow">
    <!-- v-model 2-way binding wth newTodoItem data -->
    <!-- keyboard event handling with addTodo method -->
    <input type="text" v-model="newTodoItem" v-on:keyup.enter="addTodo" />
    <!-- click event handling with addTodo method -->
    <span class="addContainer" v-on:click="addTodo">
      <!-- fontawsome icon apply: fas fa-plus -->
      <i class="fas fa-plus addBtn"></i>
    </span>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      newTodoItem: ""
    };
  },
  methods: {
    addTodo: function() {
      if (this.newTodoItem !== "") {
        this.$emit("addTodoItem", this.newTodoItem);
        this.clearInput();
      }
    },
    clearInput: function() {
      this.newTodoItem = "";
    }
  }
};
</script>
```

`App.vue`

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <!-- v-on:하위 컴포넌트에서 발생시킨 이벤트 이름 ="현재 컴포넌트의 메서드명" -->
    <TodoInput v-on:addTodoItem="addOneItem"></TodoInput>
    <!-- v-bind:내려보낼 프롭스 속성 이름 = "현재 위치의 데이터 이름" -->
    <TodoList v-bind:propsdata="todoItems"></TodoList>
    <TodoFooter></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from "./components/TodoHeader.vue";
import TodoInput from "./components/TodoInput.vue";
import TodoList from "./components/TodoList.vue";
import TodoFooter from "./components/TodoFooter.vue";

export default {
  data: function() {
    return {
      todoItems: []
    };
  },
  methods: {
    addOneItem: function(todoItem) {
      var obj = { completed: false, item: todoItem };
      localStorage.setItem(todoItem, JSON.stringify(obj));
      this.todoItems.push(obj);
    }
  },
  // created : 인스턴스 생성시점에 hook( call )
  created: function() {
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          this.todoItems.push(
            JSON.parse(localStorage.getItem(localStorage.key(i)))
          );
        }
      }
    }
  },
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    TodoHeader: TodoHeader,
    TodoInput: TodoInput,
    TodoList: TodoList,
    TodoFooter: TodoFooter
  }
};
</script>
```

### 할 일 삭제 기능

`TodoList.vue`

```vue
<template>
  <div>
    <ul>
      <li v-for="(todoItem, index) in propsdata" v-bind:key="todoItem.item" class="shadow">
        <i
          class="checkBtn fas fa-check"
          v-bind:class="{checkBtnCompleted: todoItem.completed}"
          v-on:click="toggleComplete(todoItem)"
        ></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <!-- click event Handling with removeTodo method -->
        <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
          <i class="fas fa-trash-alt"></i>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ["propsdata"],
  methods: {
    removeTodo: function(todoItem, index) {
        this.$emit('removeItem', todoItem, index);
    },
    toggleComplete: function(todoItem) {
      todoItem.completed = !todoItem.completed;
      // 로컬 스토리지 데이터 갱신
      localStorage.removeItem(todoItem);
      localStorage.setItem(todoItem.item, JSON.stringify(todoItem));
    }
  }
};
</script>
```

`App.vue`

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <!-- v-on:하위 컴포넌트에서 발생시킨 이벤트 이름 ="현재 컴포넌트의 메서드명" -->
    <TodoInput v-on:addTodoItem="addOneItem"></TodoInput>
    <!-- v-bind:내려보낼 프롭스 속성 이름 = "현재 위치의 데이터 이름" -->
    <TodoList v-bind:propsdata="todoItems" v-on:removeItem="removeOneItem"></TodoList>
    <TodoFooter></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from "./components/TodoHeader.vue";
import TodoInput from "./components/TodoInput.vue";
import TodoList from "./components/TodoList.vue";
import TodoFooter from "./components/TodoFooter.vue";

export default {
  data: function() {
    return {
      todoItems: []
    };
  },
  methods: {
    addOneItem: function(todoItem) {
      var obj = { completed: false, item: todoItem };
      localStorage.setItem(todoItem, JSON.stringify(obj));
      this.todoItems.push(obj);
    },
    removeOneItem: function(todoItem, index) {
      localStorage.removeItem(todoItem.item);
      this.todoItems.splice(index, 1);
    }
  },
  // created : 인스턴스 생성시점에 hook( call )
  created: function() {
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          this.todoItems.push(
            JSON.parse(localStorage.getItem(localStorage.key(i)))
          );
        }
      }
    }
  },
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    TodoHeader: TodoHeader,
    TodoInput: TodoInput,
    TodoList: TodoList,
    TodoFooter: TodoFooter
  }
};
</script>
```

### 할 일 완료 기능

`TodoList.vue`

```vue
<template>
  <div>
    <ul>
      <li v-for="(todoItem, index) in propsdata" v-bind:key="todoItem.item" class="shadow">
        <i
          class="checkBtn fas fa-check"
          v-bind:class="{checkBtnCompleted: todoItem.completed}"
          v-on:click="toggleComplete(todoItem, index)"
        ></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <!-- click event Handling with removeTodo method -->
        <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
          <i class="fas fa-trash-alt"></i>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ["propsdata"],
  methods: {
    removeTodo: function(todoItem, index) {
      this.$emit("removeItem", todoItem, index);
    },
    toggleComplete: function(todoItem, index) {
      this.$emit("toggleComplete", todoItem, index);
    }
  }
};
</script>
```

`App.vue`

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <!-- v-on:하위 컴포넌트에서 발생시킨 이벤트 이름 ="현재 컴포넌트의 메서드명" -->
    <TodoInput v-on:addTodoItem="addOneItem"></TodoInput>
    <!-- v-bind:내려보낼 프롭스 속성 이름 = "현재 위치의 데이터 이름" -->
    <TodoList
      v-bind:propsdata="todoItems"
      v-on:removeItem="removeOneItem"
      v-on:toggleComplete="toggleItem"
    ></TodoList>
    <TodoFooter></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from "./components/TodoHeader.vue";
import TodoInput from "./components/TodoInput.vue";
import TodoList from "./components/TodoList.vue";
import TodoFooter from "./components/TodoFooter.vue";

export default {
  data: function() {
    return {
      todoItems: []
    };
  },
  methods: {
    addOneItem: function(todoItem) {
      var obj = { completed: false, item: todoItem };
      localStorage.setItem(todoItem, JSON.stringify(obj));
      this.todoItems.push(obj);
    },
    removeOneItem: function(todoItem, index) {
      localStorage.removeItem(todoItem.item);
      this.todoItems.splice(index, 1);
    },
    toggleItem: function(todoItem, index) {
      this.todoItems[index].completed = !this.todoItems[index].completed
      // 로컬 스토리지 데이터 갱신
      localStorage.removeItem(todoItem);
      localStorage.setItem(todoItem.item, JSON.stringify(todoItem));
    }
  },
  // created : 인스턴스 생성시점에 hook( call )
  created: function() {
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          this.todoItems.push(
            JSON.parse(localStorage.getItem(localStorage.key(i)))
          );
        }
      }
    }
  },
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    TodoHeader: TodoHeader,
    TodoInput: TodoInput,
    TodoList: TodoList,
    TodoFooter: TodoFooter
  }
};
</script>
```

### 할 일 모두 삭제 기능

`TodoFooter.vue`

```vue
<template>
  <div class="clearAllContainer">
      <span class="clearAllBtn" v-on:click="clearTodo">Clear All</span>
  </div>
</template>

<script>
export default {
    methods: {
        clearTodo: function(){
            this.$emit('clearAll')
        }
    }
}
</script>
```

`App.vue`

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <!-- v-on:하위 컴포넌트에서 발생시킨 이벤트 이름 ="현재 컴포넌트의 메서드명" -->
    <TodoInput v-on:addTodoItem="addOneItem"></TodoInput>
    <!-- v-bind:내려보낼 프롭스 속성 이름 = "현재 위치의 데이터 이름" -->
    <TodoList
      v-bind:propsdata="todoItems"
      v-on:removeItem="removeOneItem"
      v-on:toggleComplete="toggleItem"
    ></TodoList>
    <TodoFooter
    v-on:clearAll="clearAllItems"
    ></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from "./components/TodoHeader.vue";
import TodoInput from "./components/TodoInput.vue";
import TodoList from "./components/TodoList.vue";
import TodoFooter from "./components/TodoFooter.vue";

export default {
  data: function() {
    return {
      todoItems: []
    };
  },
  methods: {
    addOneItem: function(todoItem) {
      var obj = { completed: false, item: todoItem };
      localStorage.setItem(todoItem, JSON.stringify(obj));
      this.todoItems.push(obj);
    },
    removeOneItem: function(todoItem, index) {
      localStorage.removeItem(todoItem.item);
      this.todoItems.splice(index, 1);
    },
    toggleItem: function(todoItem, index) {
      this.todoItems[index].completed = !this.todoItems[index].completed
      // 로컬 스토리지 데이터 갱신
      localStorage.removeItem(todoItem);
      localStorage.setItem(todoItem.item, JSON.stringify(todoItem));
    }, 
    clearAllItems: function(){
      localStorage.clear();
      this.todoItems = [];
    }
  },
  // created : 인스턴스 생성시점에 hook( call )
  created: function() {
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          this.todoItems.push(
            JSON.parse(localStorage.getItem(localStorage.key(i)))
          );
        }
      }
    }
  },
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    TodoHeader: TodoHeader,
    TodoInput: TodoInput,
    TodoList: TodoList,
    TodoFooter: TodoFooter
  }
};
</script>
```

## 사용자 경험 개선

### 모달 컴포넌트 등록

[vue2 modal example](https://codesandbox.io/s/github/vuejs/vuejs.org/tree/master/src/v2/examples/vue-20-modal-component?from-embed=&file=/style.css:0-1063)

`components/common/Modal.vue`

```vue
<template>
  <transition name="modal">
        <div class="modal-mask">
          <div class="modal-wrapper">
            <div class="modal-container">

              <div class="modal-header">
                <slot name="header">
                  default header
                </slot>
              </div>

              <div class="modal-body">
                <slot name="body">
                  default body
                </slot>
              </div>
            </div>
          </div>
        </div>
      </transition>
</template>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 300px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

</style>
```

`TodoInput.vue`

```vue
<template>
  <div class="inputBox shadow">
    <!-- v-model 2-way binding wth newTodoItem data -->
    <!-- keyboard event handling with addTodo method -->
    <input type="text" v-model="newTodoItem" v-on:keyup.enter="addTodo" />
    <!-- click event handling with addTodo method -->
    <span class="addContainer" v-on:click="addTodo">
      <!-- fontawsome icon apply: fas fa-plus -->
      <i class="fas fa-plus addBtn"></i>
    </span>
    <Modal v-if="showModal" @close="showModal = false">
      <!--
      you can use custom content here to overwrite
      default content
      -->
      <h3 slot="header">경고!
          <i class="closeModalBtn fas fa-times" @click="showModal=false"></i>
      </h3>
      <p slot="body">무언가를 입력하세요.</p>
      <p slot="footer">copyright</p>
      
    </Modal>
  </div>
</template>

<script>
import Modal from "./common/Modal.vue";

export default {
  data: function() {
    return {
      newTodoItem: "", 
      showModal: false
    };
  },
  methods: {
    addTodo: function() {
      if (this.newTodoItem !== "") {
        this.$emit("addTodoItem", this.newTodoItem);
        this.clearInput();
      } else {
      }
    },
    clearInput: function() {
      this.newTodoItem = "";
    }
  },
  components: {
    Modal: Modal
  }
};
</script>
```

### Slot

Modal 컴포넌트를 TodoInput 컴포넌트에 등록해서 사용

slot 영억은 TodoInput(상위) 컴포넌트에서 재정의 가능

### 트랜지션 구현

[Vue Transition Classes](https://vuejs.org/v2/guide/transitions.html#Transition-Classes)

`TodoInput.vue`

```vue
<template>
  <div>
    <transition-group name="list" tag="ul">
      <li v-for="(todoItem, index) in propsdata" v-bind:key="todoItem.item" class="shadow">
        <i
          class="checkBtn fas fa-check"
          v-bind:class="{checkBtnCompleted: todoItem.completed}"
          v-on:click="toggleComplete(todoItem, index)"
        ></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <!-- click event Handling with removeTodo method -->
        <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
          <i class="fas fa-trash-alt"></i>
        </span>
      </li>
    </transition-group>
  </div>
</template>

<style scoped>
/* 리스트 아이템 트랜지션 효과 */
.list-enter-active,
.list-leave-active {
  transition: all 1s;
}
.list-enter, .list-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateY(30px);
}
</style>
```

## ES6 for Vue.js

- ES6 = ECMAScript 2015 이크마스크립트
- ES5 = ECMAScript 2009

### Babel

- 구 버전 브라우저 중에서 ES6를 지원하지 않는 브라우저가 있으므로 각 브라우저에 호환 가능한 ES5로 변환하는 컴파일러

```javascript
babel for webpack
module: {
    loaders: [{
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
            presets: ['es2015']
        }
    }]
 },
```

### const & let - 변수선언

- 블록 단위{ }로 변수의 범위가 제한됨

  - 기존 자바스크립트(ES5)는 { }는 상관없이 스코프가 설정됨

  ```javascript
  var sum = 0;
  for (var i = 1; i <= 5; i++) {
      sum = sum + 1;
  }
  console.log(sum); // 15
  console.log(i); // 6
  ```

  - Hosting이란 선언한 함수와 변수를 해석기가 가장 상단에 있는 것처럼 인식한다.
  - **js 해석기는 코드의 라인 순서와 관계 없이 함수선언식과 변수를 위한 메모리 공간을 먼저 확보한다.**
  - 따라서, function a()와 var 는 코드의 최상담으로 끌어 올려진 것(hoisted) 처럼 보인다.

  ```javascript
  function willBeOveridden() {
      return 10;
  }
  willBeOveridden(); // 5
  function willBeOveridden() {
      return 5;
  }
  ```

  

- const : 한번 선언한 값에 대해서 변경할 수 없음 (상수 개념)

  - 그럼에도 객체 내부는 변경할 수 있음

  ```javascript
  const a = {};
  a.num = 10;
  const b = [];
  b.push(200);
  ```

  

- let: 한번 선언한 값에 대해서 다시 선언할 수 없음

```javascript
function f() {
    {
        let x;
        {
            // 새로운 블록안에 새로운 x의 스코프가 생김
            const x = "sneaky";
            x = "foo"; // 위에 이미 const로 x를 선언했으므로 다시 값을 대입하면 에러 발생
        }
        // 이전 블록 범위로 돌아왔기 때문에 'let x'에 해당하는 메모리에 값을 대입
        x = "bar";
        let x = "inner"; // Uncaught SyntaxError: Identifier 'x'; has already been seclared
    }
}
```

#### Refactoring with const & let

`App.vue`

```vue
const obj = { completed: false, item: todoItem };

for (let i = 0; i < localStorage.length; i++) {
```



### 화살표함수

#### Arrow Function

- 함수를 정의할 때 function 이라는 키워드를 사용하지 않고 => 로 대체
- 흔히 사용하는 **콜백 함수**의 문법을 간결화

```javascript
// ES5 함수 정의 방식
var sum = function(a,b) {
    return a + b;
};

// ES6 함수 정의 방식
var sum = (a,b) => {
    return a + b;
}

sum (10, 20);

// ES5
var arr = ["a", "b", "c"];
arr.forEach(function(value) {
    console.log(value); // a, b, c
});

// ES6
var arr = ["a", "b", "c"];
arr.forEach((value) => {console.log(value)}); // a, b, c
```

[바벨 온라인 에디터](https://babeljs.io/repl/)

### 향상된 객체 리터럴

객체의 속성을 메서드로 사용할 때 function 예약어를 생략하고 생성가능

```javascript
var dictionary ={
    words: 100,
    // ES5
    lookup: function() {
        console.log("find worlds");
    },
    // ES6
    lookup(){
        console.log("find words");
    }
};
```

리팩터링예

`App.vue`

```vb
<script>
import TodoHeader from "./components/TodoHeader.vue";
import TodoInput from "./components/TodoInput.vue";
import TodoList from "./components/TodoList.vue";
import TodoFooter from "./components/TodoFooter.vue";

export default {
  data() {
    return {
      todoItems: []
    };
  },
  methods: {
    addOneItem(todoItem) {
      const obj = { completed: false, item: todoItem };
      localStorage.setItem(todoItem, JSON.stringify(obj));
      this.todoItems.push(obj);
    },
    removeOneItem(todoItem, index) {
      localStorage.removeItem(todoItem.item);
      this.todoItems.splice(index, 1);
    },
    toggleItem(todoItem, index) {
      this.todoItems[index].completed = !this.todoItems[index].completed
      // 로컬 스토리지 데이터 갱신
      localStorage.removeItem(todoItem);
      localStorage.setItem(todoItem.item, JSON.stringify(todoItem));
    }, 
    clearAllItems(){
      localStorage.clear();
      this.todoItems = [];
    }
  },
  // created : 인스턴스 생성시점에 hook( call )
  created() {
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          this.todoItems.push(
            JSON.parse(localStorage.getItem(localStorage.key(i)))
          );
        }
      }
    }
  },
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    TodoHeader: TodoHeader,
    TodoInput: TodoInput,
    TodoList: TodoList,
    TodoFooter: TodoFooter
  }
};
</script>
```

객체의 속성명과 값 명이 동일할 때 아래와 같이 축약가능

```javascript
var figures = 10;
var dictionary = {
	figures
};
```

리팩터링 예

`App.vue`

```vue
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    TodoHeader,
    TodoInput,
    TodoList,
    TodoFooter
  }
```

### Modules

자바스크립트 모듈화 방법

- 자바스크립트 모듈 로더 라이브러리(AMD, Commons JS)기능을 js언어 자체에서 지원
- 호출되기 전까지는 코드 실행과 동작을 하지 않는 특징이 있음

```javascript
// libs/math.js
export function sum(x, y){
    return x + y;
}
export var pi = 3.141593;

// main.js
import {sum} from 'libs/math.js';
sum(1, 2);
```

## Vuex 

### 소개

상태관리 라이브러리

- 복잡한 애플리케이션의 컴포넌트들을 효율적으로 관리하는 Vuex 라이브러리 소개
- Vuex 라이브러리의 등장 배경인 Flux 패턴 소개
- Vuex 라이브러리의 주요 속성인 state(data), getters(computed), mutations(methods), actions(async methods) 학습
- Vuex를 더 쉽게 코딩할 수 있는 방법인 Helper 기능 소개
- Vuex로 프로젝트를 구조화화는 방법과 모듈 구조화 방법 소개

#### Vuex란?

- 무수히 많은 컴포넌트의 데이터를 관리하기 위한 상태 관리 패턴이자 라이브러리
- React의 Flux 패턴에서 기인함
- Vue.js 중고급 개발자로 성장하기 위한 필수 관문

#### Flux란?

- MVC 패턴의 복잡한 데이터 흐름 문제를 해결하는 개발 패턴 - Unidirectional data flow (단방향 데이터 흐름)
  - Action -> Dispatcher -> Model(Store) -> View -> Action -> Dispatcher -> ...
    - MVC 패턴
      - Controller -> Model <->View
      - 문제점
        - 기능 추가 및 변경에 따라 생기는 문제점을 예측할 수가 없음
        - 앱이 복잡해지면서 생기는 업데이트 루프
  - Action : 화면에서 발생하는 이벤트 또는 사용자의 입력
  - Dispatcher: 데이터를 변경하는 방법, 메서드
  - Model : 화면에 표시할 데이터
  - View : 사용자에게 비춰지는 화면

#### Vuex 필요성

[자바스크립트 비동기 처리와 콜백 함수](https://joshua1988.github.io/web-development/javascript/javascript-asynchronous-operation/)

[자바스크립트 Promise](https://joshua1988.github.io/web-development/javascript/promise-for-beginners/)

- 복잡한 애플리케이션에서 컴포넌트의 개수가 많아지면 컴포넌트 간에 데이터 전달이 어려워진다.

- 이벤트 버스로 해결?

  - 어디서 이벤트를 보냈는지 혹은 어디서 이벤트를 받았는지 알기 어려움

    ```
    // Login.vue
    eventBus.$emit('fetch', loginInfo);
    
    // List.vue
    eventBus.$on('display', data => this.displayOnScreen(data));
    
    // Chart.vue
    eventBus.$emit('refreshData', chartData);
    
    컴포넌트 간 데이터 전달이 명시적이지 않음
    ```

    

#### Vuex 해결할 수 있는 문제

- MVC 패턴에서 발생하는 구조적 오류
- 컴포넌트 간 데이터 전달 명시
- 여러 개의 컴포넌트에서 같은 데이터를 업데이트 할 때 동기화 문제



#### Vuex 컨셉

- State : 컴포넌트 간에 공유하는 데이터 data()
- VIew : 데이터를 표시하는 화면 template
- Action : 사용자의 입력에 따라 데이터를 변경하는 methods
- State -> View -> Actions : Data() -> template -> methods

#### Vuex 구조

컴포넌트 -(Dispatch)-> 비동기 로직(with Backend API) -(commit)-> 동기 로직(with Devtools) -(Mutate)-> 상태 -(Render)-> 컴포넌트...

### Vuex 기술요소

#### 설치 및 등록

```javascript
npm install vuex --save
```

`src/store/store.js`

```javascript
import Vue from 'vue'
import Vuex from 'vuex'

// Vue의 모든 영역에 플러그인 추가
Vue.use(Vuex);

export const store = new Vuex.Store({

});
```

`src/main.js`

```javascript
import Vue from 'vue'
import App from './App.vue'
import { store } from './store/store'

Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')

```

- state: 여러 컴포넌트에 공유되는 데이터 data
- getters : 연산된 state 값을 접근하는 속성 computed
- mutations: state 값을 변경하는 이벤트 로직, 메서드 methods
- actions: 비동기 처리 로직을 선언하는 메서드 async methods

#### state와 getters

state: 여러 컴포넌트 간에 공유할 데이터 - 상태

```vue
// Vue
data: {
	messgae: 'Hello Vue.js!'
}

// Vuex
state: {
	message: 'Hello Vue.js!'
}

<!-- Vue -->
<p>{{ message }}</p>

<!-- Vuex -->
<p>{{ this.$store.state.message }}</p>
```

getters: state 값을 접근하는 속성이자 computed() 처럼 미리 연산된 값을 접근하는 속성

```javascript
// store.js
state: {
    num: 10
},
getters: {
    getNumber(state) {
        return state.num;
    },
    doubleNumber(state){
        return state.num * 2;
    }
}

<p>{{ this.$store.getters.getNumber }}</p>
<p>{{ this.$store.getters.doubleNumber }}</p>
```

#### state이용 refactoring

`TodoList.vue`

```vue
<template>
  <div>
    <transition-group name="list" tag="ul">
      <li v-for="(todoItem, index) in this.$store.state.todoItems" v-bind:key="todoItem.item" class="shadow">
        <i
          class="checkBtn fas fa-check"
          v-bind:class="{checkBtnCompleted: todoItem.completed}"
          v-on:click="toggleComplete(todoItem, index)"
        ></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <!-- click event Handling with removeTodo method -->
        <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
          <i class="fas fa-trash-alt"></i>
        </span>
      </li>
    </transition-group>
  </div>
</template>
```

store/store.js

```javascript
import Vue from "vue";
import Vuex from "vuex";

// Vue의 모든 영역에 플러그인 추가
Vue.use(Vuex);

const storage = {
  fetch() {
    const arr = [];
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          arr.push(JSON.parse(localStorage.getItem(localStorage.key(i))));
        }
      }
    }
    return arr;
  },
};

export const store = new Vuex.Store({
  state: {
    todoItems: storage.fetch(),
  },
});

```

#### mutations

- state의 값을 변경할 수 있는 유일한 방법이자 메서드

  - state를 직접 변경하는 경우 어느 컴포넌트에서 해당 state를 변경했는지 추적이 어려워지기 때문
  - 반응성, 디버깅, 테스팅 혜택을 얻기 위함

- 뮤테이션은 commit() 으로 동작시킨다.

  ```javascript
  // store.js
  state: { num:10 }
  mutations: {
      printNumbers(state){
          return state.num
      },
      sumNumbers(state, anotherNum){
          return state.num + anotherNum;
      }
  }
  
  // App.vue
  this.$store.commit('printNumbers');
  this.$store.commit('sumNubmers',20);
  ```

- state를 변경하기 위해 mutations를 동작시킬 때 인자(payload)를 전달할 수 있음

  ```javascript
  // store.js
  state: { storeNum: 0},
  mutations: {
      modifyState(state, payload) {
          console.log(payload.str);
          return state.storeNum += payload.num;
      }
  }
  
  // App.vue
  this.$store.commit('modifyState', {
      str: 'passed from payload',
      num: 20
  });
  ```

#### mutations이용 refactoring

`App.vue`

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <TodoInput></TodoInput>
    <TodoList></TodoList>
    <TodoFooter></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from "./components/TodoHeader.vue";
import TodoInput from "./components/TodoInput.vue";
import TodoList from "./components/TodoList.vue";
import TodoFooter from "./components/TodoFooter.vue";

export default {
  components: {
    // 컴포넌트 태그명 : 컴포넌트 내용
    TodoHeader,
    TodoInput,
    TodoList,
    TodoFooter
  }
};
</script>


<style>
body {
  text-align: center;
  background-color: #f6f6f6;
}
input {
  border-style: groove;
  width: 200;
}
button {
  border-style: groove;
}
.shadow {
  box-shadow: 5px 10px 10px rgba(0, 0, 0, 0.03);
}
</style>

```

`store.js`

```javascript
import Vue from "vue";
import Vuex from "vuex";

// Vue의 모든 영역에 플러그인 추가
Vue.use(Vuex);

const storage = {
  fetch() {
    const arr = [];
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          arr.push(JSON.parse(localStorage.getItem(localStorage.key(i))));
        }
      }
    }
    return arr;
  },
};

export const store = new Vuex.Store({
  state: {
    todoItems: storage.fetch(),
  },
  mutations: {
    addOneItem(state, todoItem) {
      const obj = { completed: false, item: todoItem };
      localStorage.setItem(todoItem, JSON.stringify(obj));
      state.todoItems.push(obj);
    },
    removeOneItem(state, payload) {
      localStorage.removeItem(payload.todoItem.item);
      state.todoItems.splice(payload.index, 1);
    },
    toggleItem(state, payload) {
      console.log("hi");
      state.todoItems[payload.index].completed = !state.todoItems[payload.index]
        .completed;
      // 로컬 스토리지 데이터 갱신
      localStorage.removeItem(payload.todoItem);
      localStorage.setItem(
        payload.todoItem.item,
        JSON.stringify(payload.todoItem)
      );
    },
    clearAllItems(state) {
      localStorage.clear();
      state.todoItems = [];
    },
  },
});

```

#### actions

- 비동기 처리 로직을 선언하는 메서드. 비동기 로직을 담당하는 mutations
  - state값의 변화를 추적하기 어렵기 때문에 mutations 속성에는 동기 처리 로직만 넣어야 한다.
- 데이터 요청, Promise, ES6 async과 같은 비동기 처리는 모두 actions에 선언

```javascript
// store.js
state: {
    num: 10
},
mutations: {
    doubleNumber(state){
        state.num * 2;
    }
},
actions: {
    delayDoubleNumber(context) { // context로 store의 메서드와 속성 접근
    	context.commit('doubleNumber');
    }
}

// App.vue
this.$store.dispatch('delayDoubleNumber');


// store.js
mutations: {
    addCounter(state) {
        state.counter++
    },
},
actions: {
    delayedAddCounter(context) {
        setTimeout(() => context.commit('addCounter'), 2000);
    }
}

// App.vue
methods: {
    incrementCounter() {
        this.$store.dispatch('delayedAddCounter');
    }
}


//store.js
mutations: {
    setData(state, fetchedData){
        state.product = fetchedData;
    }
},
actions: {
    fetchProductData(context){
        return axios.get('https://domain.com/products/1')
                    .then(response => context.commit('setData', response));
    }
}

// App.vue
methods: {
    getProduct() {
        this.$store.dispatch('fetchProductData');
    }
}
```

### Vuex 헬퍼함수

#### Helper

- state -> mapState
- getters -> mapGetters
- mutations -> mapMutations
- actions -> mapActions

#### 사용법

헬퍼를 사용하고자 하는 vue 파일에서 아래와 같이 해당 헬퍼를 로딩

```vue
// App.vue
import { mapState } from 'vuex'
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'
import { mapActions } from 'vuex'

export default {
    computed() { ...mapState(['num']), ...mapGetters(['countedNum'])},
     methods: { ...mapMutations(['clickBtn']), ...mapActions(['asyncClickBtn'])}
}
```

... : Object Spread Operator

#### mapState, mapGetters

mapState

Vuex에 선언한 state 속성을 뷰 컴포넌트에 더 쉽게 연결해주는 헬퍼

```vue
// App.vue
import { mapState } from 'vuex'

computed(){
    ...mapState(['num'])
    // num() { return this.$store.state.num; }
}

// store.js
state: {
    num: 10
}


<!-- <p>{{ this.$store.state.num }}</p> -->
<p>{{ this.num }}</p>
```

mapGetters

Vuex에 선언한 getters 속성을 뷰 컴포넌트에 더 쉽게 연결해주는 헬퍼

```
// App.vue
import { mapGetters } from 'vuex'

computed() { ...mapGetters(['reverseMessage'])}

// stroe.js
getters: {
    reverseMessage(state){
        return state.msg.split(''),reverse().join('');
    }
}

<!-- <p>{{ this.$store.getters.reverseMessage }}</p> -->
<p>{{ this.reverseMessgae }}</p>
```

#### Refactoring with above

`store.js`

```javascript
  getters: {
      storedTodoItems(state){
          return state.todoItems;
      }
  },
```

`TodoList.vue`

```vue
<template>
  <div>
    <transition-group name="list" tag="ul">
      <li
        v-for="(todoItem, index) in this.storedTodoItems"
        v-bind:key="todoItem.item"
        class="shadow"
      >
        <i
          class="checkBtn fas fa-check"
          v-bind:class="{checkBtnCompleted: todoItem.completed}"
          v-on:click="toggleComplete(todoItem, index)"
        ></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <!-- click event Handling with removeTodo method -->
        <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
          <i class="fas fa-trash-alt"></i>
        </span>
      </li>
    </transition-group>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  methods: {
    removeTodo(todoItem, index) {
      this.$store.commit("removeOneItem", { todoItem, index });
    },
    toggleComplete(todoItem, index) {
      this.$store.commit("toggleItem", { todoItem, index });
    }
  },
  computed:{
    // todoItems(){
    //   return this.$store.getters.storedTodoItems;
    // },
    ...mapGetters(['storedTodoItems']),
  }
};
</script>
```

#### mapMutations, mapActions

mapMutations

Vuex에 선언한 mutations 속성을 뷰 컴포넌트에 더 쉽게 연결해주는 헬퍼

```javascript
// App.vue
import { mapMutations } from 'vuex'
methods: {
    ...mapMutations(['clickBtn']),
        authLogin() {}, 
        displayTable() {}
}

// stroe.js
mutations: {
    clickBtn(state){
        alert(state.msg);
    }
}

<button @click="clickBtn">popup message</button>
```

mapActions

Vuex에 선언한 actions 속성을 뷰 컴포넌트에 더 쉽게 연결해주는 헬퍼

```javascript
// App.vue
import { mapActions } from 'vuex'

methods: {
    ...mapActions(['delayClickBtn']),
}
    
//store.js
actions:{
    delayClickBtn(contexT){
        setTimeout(() => context.commit('clciBtn'), 20000);
    }
}
    
    
<button @click="delayClickBtn">delay popup message</button>
```

헬퍼의 유연한 문법

Vuex에 선언한 속성을 그대로 컴포넌트에 연결하는 문법

```
...mapMutations([
    'clickBtn',
    'addNubmer' // 인자 선언안해도 자동적으로 넘겨준
])
```

Vuex에 선언한 속성을 컴포넌트의 특정 메서드에다가 연결하는 문법

```
...mapMutations({
    popupMsg: 'clciBtn' // 컴포넌트 메서드명 : store의 뮤테이션 명
})
```

#### Refactoring with above

`TodoList.vue`

```vue
<template>
  <div>
    <transition-group name="list" tag="ul">
      <li
        v-for="(todoItem, index) in this.storedTodoItems"
        v-bind:key="todoItem.item"
        class="shadow"
      >
        <i
          class="checkBtn fas fa-check"
          v-bind:class="{checkBtnCompleted: todoItem.completed}"
          v-on:click="toggleComplete({todoItem, index})"
        ></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <!-- click event Handling with removeTodo method -->
        <span class="removeBtn" v-on:click="removeTodo({todoItem, index})">
          <i class="fas fa-trash-alt"></i>
        </span>
      </li>
    </transition-group>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  methods: {
    ...mapMutations({
      removeTodo: 'removeOneItem',
      toggleComplete: 'toggleItem',
    }),
    // removeTodo(todoItem, index) {
    //   this.$store.commit("removeOneItem", { todoItem, index });
    // },
    // toggleComplete(todoItem, index) {
    //   this.$store.commit("toggleItem", { todoItem, index });
    // }
  },
  computed:{
    // todoItems(){
    //   return this.$store.getters.storedTodoItems;
    // },
    ...mapGetters(['storedTodoItems']),
  }
};
</script>
```

TodoFooter.vue

```vue
<template>
  <div class="clearAllContainer">
      <span class="clearAllBtn" v-on:click="clearTodo">Clear All</span>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
    methods: {
      ...mapMutations({
        clearTodo: 'clearAllItems',
      }),
        // clearTodo(){
        //     this.$store.commit('clearAllItems');
        // }
    }
}
</script>
```

#### 헬퍼함수 정리

`store.js`

```javascript
import Vue from "vue";
import Vuex from "vuex";

// Vue의 모든 영역에 플러그인 추가
Vue.use(Vuex);

export const store = new Vuex.Store({

    state: {
        price: 100
    },
    getters: {
        originalPrice(state){
            return state.price;
        },
        doublePrice(state){
            return state.price * 2;
        },
        triplePrice(state){
            return state.price * 3;
        }
    }
});
```

`com.vue`

```vue
<template>
  <div id="root">
    <p>{{originalPrice }}</p>
    <p>{{doublePrice }}</p>
    <p>{{triplePrice }}</p>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
      ...mapGetters(['originalPrice','doublePrice','triplePrice']),
    // originalPrice() {
    //     return this.$stroe.getters.originalPrice;
    // },
    // doublePrice() {
    //     return this.$stroe.getters.doublePrice;
    // },
    // triplePrice() {
    //     return this.$stroe.getters.triplePrice;
    // }
  }
};
</script>
<style>
</style>
```

### 프로젝트 구조화 및 모듈화

#### 스토어 속성 모듈화1

```javascript
//store.js
import Vue from 'vue'
import Vuex from 'vuex'

export const stroe = new Vuex.Stroe({
    state: {},
    getters: {},
    mutations: {},
    actions: {}
});
```

를 모듈화하면

```javascript
import Vue from 'vue'
import Vuex from 'vuex'
import * as getters from 'store/getters.js'
import * as mutations from 'store/mutations.js'
import * as actions from 'store/actions.js'

export const store = new Vuex.Stroe({
    state: {},
    getters: getters,
    mutations: mutations,
    actions: actions
});

```

#### 적용

`store.js`

```javascript
import Vue from "vue";
import Vuex from "vuex";
import * as getters from './getters'
import * as mutations from './mutations'

// Vue의 모든 영역에 플러그인 추가
Vue.use(Vuex);

const storage = {
  fetch() {
    const arr = [];
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          arr.push(JSON.parse(localStorage.getItem(localStorage.key(i))));
        }
      }
    }
    return arr;
  },
};

export const store = new Vuex.Store({
  state: {
    todoItems: storage.fetch(),
  },
  getters,
  mutations
});

```

`getters.js`

```javascript
export const storedTodoItems = (state) => {
  return state.todoItems;
};

```

`mutations.js`

```javascript
const addOneItem = (state, todoItem) => {
  const obj = { completed: false, item: todoItem };
  localStorage.setItem(todoItem, JSON.stringify(obj));
  state.todoItems.push(obj);
};
const removeOneItem = (state, payload) => {
  localStorage.removeItem(payload.todoItem.item);
  state.todoItems.splice(payload.index, 1);
};
const toggleItem = (state, payload) => {
  state.todoItems[payload.index].completed = !state.todoItems[payload.index]
    .completed;
  // 로컬 스토리지 데이터 갱신
  localStorage.removeItem(payload.todoItem);
  localStorage.setItem(payload.todoItem.item, JSON.stringify(payload.todoItem));
};
const clearAllItems = (state) => {
  localStorage.clear();
  state.todoItems = [];
};

export { addOneItem, removeOneItem, toggleItem, clearAllItems}
```

#### 스토어 속성 모듈화2

앱이 비대해져서 1개의 store로는 관리가 힘들 때 modules 속성 사용

```javascript
// store.js
import Vue from 'vue'
import Vuex from 'vuex'
import todo from 'modules/todo.js'

export const stroe = new Vuex.Store({
    modules:{
    moduleA: todo, // 모듈명칭 : 모듈파일명
    todo // todo: todo
    }
});

//todo.js
const state ={}
const getters = {}
const mutations = {}
const actions = {}
```

#### 적용

`store/modules/todoApp.js`

```javascript
const storage = {
  fetch() {
    const arr = [];
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (
          localStorage.key(i) !== "loglevel:webpack-dev-server" &&
          localStorage.key(i) !== "OTelJS.ClientId"
        ) {
          // Json -> Object
          arr.push(JSON.parse(localStorage.getItem(localStorage.key(i))));
        }
      }
    }
    return arr;
  },
};

const state = {
  todoItems: storage.fetch(),
};

const getters = {
  storedTodoItems(state) {
    return state.todoItems;
  },
};

const mutations = {
  addOneItem(state, todoItem) {
    const obj = { completed: false, item: todoItem };
    localStorage.setItem(todoItem, JSON.stringify(obj));
    state.todoItems.push(obj);
  },
  removeOneItem(state, payload) {
    localStorage.removeItem(payload.todoItem.item);
    state.todoItems.splice(payload.index, 1);
  },
  toggleItem(state, payload) {
    state.todoItems[payload.index].completed = !state.todoItems[payload.index]
      .completed;
    // 로컬 스토리지 데이터 갱신
    localStorage.removeItem(payload.todoItem);
    localStorage.setItem(
      payload.todoItem.item,
      JSON.stringify(payload.todoItem)
    );
  },
  clearAllItems(state) {
    localStorage.clear();
    state.todoItems = [];
  },
};


export default {
    state,
    getters,
    mutations,
}
```

`store.js`

```javascript
import Vue from "vue";
import Vuex from "vuex";
import todoApp from './modules/todoApp'

// Vue의 모든 영역에 플러그인 추가
Vue.use(Vuex);

export const store = new Vuex.Store({
    modules:{
        todoApp
    }
});

```

