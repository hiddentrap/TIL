# PyQt5 GUI - QTDesigner

##### Event: Event, Signal, Timer -> Event Que -> Processed sequentially by Handler

사용자와 프로그램의 상호작용: 버튼클릭, 키입력, 마우스 클릭 등

##### Event Handler

사용자에 의해 발생된 Event(버튼클릭 등)를 처리하기위해 Event에 연결되는 함수

##### Signals

Event + Data

##### Slot: Signal Handler

예를들어, QT공식문서의 QMainWidow의 Signal 부분을 보면

void windowTitleChanged(const QString & title)로 미루어 보아

windowTitleChanged signal과 연결되는 slot은 title을 QString타입으로 받을 수 있다.

self.windowTitleChanged.connect(self.onWindowTitleChange) # signal과 slot 연결

self.windowTitleChanged.connect(lambda x: self.my_custom_fn(x, 25)) 처럼 파라메터를 추가할 수도 있음

## Multithreading

event는 쓰레드내에서 동기처리 그동안 OS와 GUI의 상호작용은 정지됨

GUI쓰레드와 워킹쓰레드를 분리시킬 필요가 있음 

**쓰레드: 메모리 공간 공유, 적은 리소스 소모, 쓰레드간 데이터 전달, 같은 메모리를 여러 쓰레드에서 읽고 쓸때 레이스 컨디션이나 세그폴트 발생가능. GIL은 PyQt에서는 큰이슈 안됨**

프로세스: 독립된 메모리 공간 점유(GIL의 완벽한 회피), 시작이 좀 느림, 더큰 메모리 오버헤드, 데이터 주고 받는게 복잡함

- QRunnable: 작업 컨테이너로 작업을 큐에 넣고 실행을 처리한다.

  ```python
  class Worker(QRunnable):
  """Worker Thread"""
  @pyqtSlot()
  def run(self)
  	pass
  ```

- QThreadPool: 작업을 다른 쓰레드로 전달하는 메서드

  ```python
  # __init__ block
  self.threadpool = QThreadPool()
  print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
  ```

- 쓰레드에 작업 실행

  ```python
  def _handler(self):
      worker = Worker()
      self.threadpool.start(worker)
  ```

- 데이터 리턴 from Thread job

  - .emit:

    - 사용자정의 signal은 QObject를 상속해서만 정의할 수 있는데 QRunnable은 QObject를 상속하지 않기때문에 QRunnable에서 직접 signal을 정의할 수 없다.

      ```python
      import traceback, sys
      
      class WorkerSignals(QObject):
          '''
          Defines the signals available from a running worker thread.
      
          Supported signals are:
      
          finished
              No data
          
          error
              `tuple` (exctype, value, traceback.format_exc() )
          
          result
              `object` data returned from processing, anything
      
          '''
          finished = pyqtSignal()
          error = pyqtSignal(tuple)
          result = pyqtSignal(object)
          
      class Worker(QRunnable):
          '''
          Worker thread
      
          Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
      
          :param callback: The function callback to run on this worker thread. Supplied args and 
                           kwargs will be passed through to the runner.
          :type callback: function
          :param args: Arguments to pass to the callback function
          :param kwargs: Keywords to pass to the callback function
      
          '''
      
          def __init__(self, fn, *args, **kwargs):
              super(Worker, self).__init__()
              # Store constructor arguments (re-used for processing)
              self.fn = fn
              self.args = args
              self.kwargs = kwargs
              self.signals = WorkerSignals()
      
          @pyqtSlot()
          def run(self):
              '''
              Initialise the runner function with passed args, kwargs.
              '''
      
              # Retrieve args/kwargs here; and fire processing using them
              try:
                  result = self.fn(
                      *self.args, **self.kwargs
                  )
              except:
                  traceback.print_exc()
                  exctype, value = sys.exc_info()[:2]
                  self.signals.error.emit((exctype, value, traceback.format_exc()))
              else:
                  self.signals.result.emit(result)  # Return the result of the processing
              finally:
                  self.signals.finished.emit()  # Done
      ```

      

  - .connect

    ```python
    def execute_this_fn(self):
        for n in range(0, 5):
            time.sleep(1)
        return "Done."
    
    def print_output(self, s):
        print(s)
    
    def thread_complete(self):
        print("THREAD COMPLETE!")
    
    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
    
        # Execute
        self.threadpool.start(worker) 
    ```

    

##### 완성예제

```python
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
        


class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
    
        self.counter = 0
    
        layout = QVBoxLayout()
        
        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)
    
        layout.addWidget(self.l)
        layout.addWidget(b)
    
        w = QWidget()
        w.setLayout(layout)
    
        self.setCentralWidget(w)
    
        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
    
    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n*100/4)
            
        return "Done."
 
    def print_output(self, s):
        print(s)
        
    def thread_complete(self):
        print("THREAD COMPLETE!")
 
    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        
        # Execute
        self.threadpool.start(worker) 

        
    def recurring_timer(self):
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)
    
    
app = QApplication([])
window = MainWindow()
app.exec_()
```

## MVC ModelView Model View

https://www.learnpyqt.com/courses/model-views/modelview-architecture/

##### Model

데이터 구조

데이터 저장소(DB or File or Network 리소스)와 ViewController간의 인터페이스로 동작

모델은 데이터를 포함하고 VIEW와의 표준화된 API를 통해서 VIEW가 데이터를 소비하고 사용자에게 표현할수 있게 한다. 복수의 View는 같은 데이터를 공유할수 있고 다른 여러 방법으로 표현할 수 있다.

데이터나 레퍼런스를 저장하고 개개의 또는 범위의 레코드 및 관련 메타데이터를 반환하고 디스플레이하는 명령어들

##### View

사용자에게 데이터 표현, 1 source mutiple view 도 가능

모델로부터 데이터를 요청하고 반환되는 데이터를 위젯에 디스플레이한다.

##### Controller

사용자로부터 입력을 받아서 명령으로 모델이나 뷰에 전달

Qt에서는 뷰와 컨트롤러의 경계가 살짝 모호하다.

Qt는 사용자로부터 OS를 통해 이벤트를 입력받아서 이를 위젯(컨트롤러)에 위임하여 처리한다. 근데, 위젯이 현재 상태를 뷰에 넣어서 사용자에게 표현도 해준다.

따라서 ModelView = Model, View+Controller 라고 생각하자.

### Example with QListView, QLineEdit

| objectName       | Type          | Description                                                  |
| ---------------- | ------------- | ------------------------------------------------------------ |
| `todoView`       | `QListView`   | The list of current todos                                    |
| `todoEdit`       | `QLineEdit`   | The text input for creating a new todo item                  |
| `addButton`      | `QPushButton` | Create the new todo, adding it to the todos list             |
| `deleteButton`   | `QPushButton` | Delete the current selected todo, removing it from the todos list |
| `completeButton` | `QPushButton` | Mark the current selected todo as done                       |

Qt가 제공하는 모델 베이스: lists, trees, tables

QListView - QAbstractListModel

```python
tick = QtGui.QImage('tick.png')

class TodoModel(QtCore.QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        # [(bool, str), (bool, str), (bool, str)]
        self.todos = todos or [] # 데이터 스토어 todos가 true면 todos아니면 []

    def data(self, index, role): #  필수구현
        '''View에서 오는 요청을 핸들링하고 적당한 결과를 리턴한다.
        index: 뷰가 요청하는 데이터의 위치정보로 .row()와 .column()으로 접근가능
        QList에서 column은 항상 0을 리턴
        role: 뷰가 요청하는 데이터의 목적 타입을 가리킨다. 
        '''
        if role == Qt.DisplayRole:# 디스플레이용 데이터 요청이면
            _, text = self.todos[index.row()]
            return text
        
       if role == Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return tick # or QtGui.QColor('green')

    def rowCount(self, index): # 필수구현
        return len(self.todos)
    
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.model = TodoModel()
        self.load()
        self.todoView.setModel(self.model)
        
        self.addButton.pressed.connect(self.add)
        self.deleteButton.pressed.connect(self.delete)
        self.completeButton.pressed.connect(self.complete)

    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.todoEdit.text()
        if text: # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.        
            self.model.layoutChanged.emit() # or dataChanged()
            # Empty the input
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes() # return list of index
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal 
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def load(self):
        try:
            with open('data.db', 'r') as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

    def save(self):
        with open('data.db', 'w') as f:
            data = json.dump(self.model.todos, f)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
```

### Example with QTableView, pandas, numpy

QTableView, QtreeView = QAbstractTableModel, QStandardItemModel

#### with list : 비추 컬럼 갯수가 다르게 들어가서 예외 발생 가능성 있음

```python
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role): # 필수
        if role == Qt.BackgroundRole and index.column() == 2:
        # See below for the data structure.
        	return QtGui.QColor('blue')
        
        if role == Qt.TextAlignmentRole:
        value = self._data[index.row()][index.column()]

        	if isinstance(value, int) or isinstance(value, float):
            	# Align right, vertical middle.
           		return Qt.AlignVCenter + Qt.AlignRight
            
        if role == Qt.ForegroundRole:
        	value = self._data[index.row()][index.column()]

        	if (
            	(isinstance(value, int) or isinstance(value, float))
            	and value < 0
        	):
            	return QtGui.QColor('red')
        
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            # Get the raw value
        	value = self._data[index.row()][index.column()]

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value

            if isinstance(value, str):
                # Render strings with quotes
                return '"%s"' % value

            # Default (anything not captured above: e.g. int)
            return value
        
        if role == Qt.DecorationRole:
        	value = self._data[index.row()][index.column()]
            # 달력 그림 붙이기
        	if isinstance(value, datetime):
            	return QtGui.QIcon('calendar.png')
            
            # 체크, x표시 붙이기
       		if isinstance(value, bool):
            	if value:
                	return QtGui.QIcon('tick.png')
            	return QtGui.QIcon('cross.png')
            
            # 컬러사각형 붙이기
            if (isinstance(value, int) or isinstance(value, float)):
        		value = int(value)

        		# Limit to range -5 ... +5, then convert to 0..10
        		value = max(-5, value)  # values < -5 become -5
        		value = min(5, value)   # valaues > +5 become +5
        		value = value + 5       # -5 becomes 0, +5 becomes + 10
        		return QtGui.QColor(COLORS[value])

    def rowCount(self, index): # 필수
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index): # 필수
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = [
          [4, 9, 2],
          [1, 0, 0],
          [3, 5, 0],
          [3, 3, 2],
          [7, 8, 9],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()
```

| Role                   | Type                                    |
| ---------------------- | --------------------------------------- |
| `Qt.BackgroundRole`    | `QBrush` (also `QColor`)                |
| `Qt.CheckStateRole`    | `Qt.CheckState`                         |
| `Qt.DecorationRole`    | `QIcon`, `QPixmap`, `QColor`            |
| `Qt.DisplayRole`       | `QString` (also `int`, `float`, `bool`) |
| `Qt.FontRole`          | `QFont`                                 |
| `Qt.SizeHintRole`      | `QSize`                                 |
| `Qt.TextAlignmentRole` | `Qt.Alignment`                          |
| `Qt.ForegroundRole`    | `QBrush` (also `QColor`)=               |

### with numpy 

int나 float의 type을 python 껄로 바까줘야함 예를들어 numpy의 int는 numpy.int32임

```python
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import numpy as np


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Note: self._data[index.row()][index.column()] will also work
            value = self._data[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = np.array([
          [1, 9, 2],
          [1, 0, -1],
          [3, 5, 2],
          [3, 3, 2],
          [5, 8, 9],
        ])

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()
```

### with Pandas

```python
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame([
          [1, 9, 2],
          [1, 0, -1],
          [3, 5, 2],
          [3, 3, 2],
          [5, 8, 9],
        ], columns = ['A', 'B', 'C'], index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()
```

