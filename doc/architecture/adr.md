# Architecture decision records

## ADR 1: Use of pyuic instead of ui.loadUI

There are 2 ways to load a Qt Designer UI file in PyQt:

- Using `uic.loadUi()`

```python
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)  # loads UI into *this* instance
        self.my_button.clicked.connect(self.do_something)
```

- Using `pyuic` to convert the `.ui` file into a Python class

```commandline
pyuic6 mainwindow.ui -o ui_mainwindow.py
```

```python
from PyQt6.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.my_button.clicked.connect(self.do_something)
```

This project uses the second method for the following reasons:

- faster application startup time, because XML has been parsed beforehand
- XML parsing is rare, and has been automated using a bat/py script in the scripts/ folder
- having the python code in the project allows for IDE autocompletion

