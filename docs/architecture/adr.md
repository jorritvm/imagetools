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
        * [Use of this core operation from a CLI entrypoint:](#use-of-this-core-operation-from-a-cli-entrypoint-1)
    * [Adding a catalog module to the project](#adding-a-catalog-module-to-the-project)
    * [FolderSelect - Catalog - Browser interaction](#folderselect---catalog---browser-interaction)

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

## Adding a catalog module to the project to persist metadata

Over time it became apparent that persisted metadata handling was required.

- To select pictures that were previously not imported a tracking mechanism of pictures was needed.
- To avoid regenerating thumbnails for pictures that were already processed, a cache was needed.

#### Q: Store metadata centrally or distributed per picture folder?

- The metadata will be stored in the separate picture folders.
- This allows for easy backup meaning it will be available on other devices using imagetools too.

#### Q: Store metadata in text or binary format?

- The textual metadata will become part of a single JSON file (metadata.json) stored in every folder.
- The thumbnails will be stored as jpg in a subfolder (.thumbs)

#### Q: How to avoid rewriting the entire metadata store for every change?

- The textual metadata will be updated in bulk or when the folder changes and some entry is 'dirty'
- The thumbnails will be updated as they are generated. They are cleaned up when the folder is changed.

## FolderSelect - Catalog - Browser interaction

Interaction workflow:

- User interaction changes folder
- FolderSelect triggers folder_change in catalog
- Catalog cleans up old folder metadata
- Catalog loads new folder metadata from disk
- Catalog triggers folder_change in browser
- Browser loads new folder metadata from catalog (thumb or details view)
- If browser requested thumbnail view catalog will start generating missing thumbnails
- If a thumbnail is generated it will be stored in the catalog and sent to the browser

## Catalog - Operations interaction:

The catalog will only be used when using the UI interface. Not when using the CLI.
(This means modules like auto-select, which rely on persisted metadata, cannot be implemented in the CLI interface.) 
