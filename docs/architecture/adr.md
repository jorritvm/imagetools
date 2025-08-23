# Architecture decision records

<!-- In pycharm you can insert a TOC using the ALT+INSERT hotkey-->
<!-- TOC -->

* [Architecture decision records](#architecture-decision-records)
    * [Use of pyuic instead of ui.loadUI](#use-of-pyuic-instead-of-uiloadui)
    * [Use of the style guide as described in style_guide.md](#use-of-the-style-guide-as-described-in-style_guidemd)
    * [Use of uv for dependency management](#use-of-uv-for-dependency-management)
    * [Clear separation of UI and CLI for operations](#clear-separation-of-ui-and-cli-for-operations)
        * [Core logic of an operation:](#core-logic-of-an-operation)
        * [Use of this core operation from a CLI entrypoint:](#use-of-this-core-operation-from-a-cli-entrypoint)
        * [Use of this core operation from a UI entrypoint:](#use-of-this-core-operation-from-a-ui-entrypoint)

<!-- TOC -->

## Use of pyuic instead of ui.loadUI

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

## Use of the style guide as described in style_guide.md

This project follows the style guide as described in `doc/style_guide/style_guide.md`.

## Use of uv for dependency management

The project uses `uv` for dependency management, which is a modern alternative to `pip`.   
It is used to install dependencies and manage the virtual environment.  
The developer should provide a fallback solution by creating a requirements.txt file for users wanting to use pip.

## Clear separation of UI and CLI for operations

The application must provide a UI and CLI interface to its operations to the user.  
All operations must be executable from the CLI, except those that are clearly UI only.

The CLI interface must be self-documenting (e.g. using argparse) and provide a help message.  
The UI interface must be intuitive and require no additional documentation.

The operations must accept callback parameters that depend on the context in which they are used.  
Example:

#### Core logic of an operation:

```python
import shutil
import os


def copy_images(image_paths, dest_folder, progress_callback=None):
    total = len(image_paths)
    for idx, src_path in enumerate(image_paths, start=1):
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_folder, filename)
        shutil.copy2(src_path, dest_path)
        if progress_callback:
            progress_callback(idx, total, filename)
```

#### Use of this core operation from a CLI entrypoint:

```python
def cli_progress(idx, total, filename):
    print(f"[{idx}/{total}] Copied {filename}")


if __name__ == "__main__":
    files = ["img1.jpg", "img2.jpg", "img3.jpg"]
    copy_images(files, "/tmp/copied", progress_callback=cli_progress)
```

#### Use of this core operation from a UI entrypoint:

Simple single thread version:

```python
def ui_progress(idx, total, path):
    progress_bar.setValue(int(idx / total * 100))
    status_label.setText(f"Copying {os.path.basename(path)}...")


# Somewhere in your button handler:
copy_images(selected_files, dest_folder, progress_callback=ui_progress)
```

However, if the operation is long running, it should be run in a separate thread to avoid blocking the UI.Use threads
and not async.

* A worker thread executes the core operation.
* It defines a callback method that emits a signal
* The signals are linked to the slots in the main UI thread.

```python
class CopyWorker(QObject):
    progress = pyqtSignal(int, int, str)
    finished = pyqtSignal()

    def __init__(self, image_paths, dest_folder):
        super().__init__()
        self.image_paths = image_paths
        self.dest_folder = dest_folder

    def run(self):
        def qt_progress(idx, total, filename):
            self.progress.emit(idx, total, filename)

        copy_images(self.image_paths, self.dest_folder, progress_callback=qt_progress)
        self.finished.emit()
```


