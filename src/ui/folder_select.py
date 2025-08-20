import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class FolderSelectWidget(QWidget):
    """
    FolderSelectWidget is a QWidget that allows the user to select a folder from the file system
    using a tree, or an auto-complete address bar.
    """
    selectionChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setup the left pane of the application's main window
        self.setup_ui()
        self.setup_slots()
        self.folder_memory = FolderMemory()

    """UI and slots setup section"""

    def setup_ui(self):
        # create both widgets of the left pane
        self.folder_tree = QTreeView()  # create directory browser
        self.folder_edit = TabSensitiveLineEdit()  # create path input lineEdit

        # file system model
        self.fsm = QFileSystemModel(self)
        self.fsm.setRootPath("")
        self.fsm.setFilter(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)

        # modify the treeview to show only the first column
        self.folder_tree.setModel(self.fsm)
        for i in range(3):
            self.folder_tree.setColumnHidden(i + 1, True)
        self.folder_tree.header().hide()

        # link the selection model to an instance variable for later use
        self.tree_selection_model = self.folder_tree.selectionModel()
        # if the current item is changed, only expand up to the new item
        self.tree_selection_model.currentChanged.connect(self.expand_to_current)

        # set up a completer used by the lineEdit
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setModel(self.fsm)

        # set minimum popup height
        self.popup = self.completer.popup()
        self.popup.setMinimumSize(QSize(0, 100))
        self.folder_edit.setCompleter(self.completer)
        self.folder_edit.tabPressed.connect(self.tab_action)

        # set buttons
        self.prev_btn = QPushButton()
        self.next_btn = QPushButton()

        self.prev_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack))
        self.next_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))

        self.prev_btn.setMaximumWidth(20)
        self.next_btn.setMaximumWidth(20)

        # connect the button signals
        self.prev_btn.pressed.connect(self.to_previous_directory)
        self.next_btn.pressed.connect(self.to_next_directory)

        line_edit_layout = QHBoxLayout()
        line_edit_layout.addWidget(self.folder_edit)
        line_edit_layout.addWidget(self.prev_btn)
        line_edit_layout.addWidget(self.next_btn)
        line_edit_layout.setSpacing(2)

        ui_layout_left = QVBoxLayout()
        ui_layout_left.addLayout(line_edit_layout)
        ui_layout_left.addWidget(self.folder_tree)
        ui_layout_left.setContentsMargins(0, 0, 0, 0)

        self.setLayout(ui_layout_left)

    def setup_slots(self):
        self.folder_edit.returnPressed.connect(self.set_directory_upon_edit)
        self.folder_tree.clicked.connect(self.set_directory_upon_select)
        self.folder_tree.doubleClicked.connect(self.open_folder_in_os)

    """navigation section: clicking in the tree, entering the path in the edit, or using back & forward buttons"""

    def force_refresh(self):
        self.set_directory_upon_edit()

    def force_set_directory(self, str):
        self.folder_edit.setText(str)
        self.set_directory_upon_edit()

    def set_directory_upon_edit(self):
        # get the path
        path = QFileInfo(self.folder_edit.text()).absoluteFilePath()
        self.folder_memory.add(path)
        # set the tree
        self.set_dir_tree(path)
        # emit
        abspath = self.folder_edit.text()
        self.selectionChanged.emit(abspath)

    def set_directory_upon_select(self, model_index):
        # get the path
        path = self.fsm.filePath(model_index)
        self.folder_memory.add(path)
        # set the edit
        self.folder_edit.setText(path)
        # emit
        abspath = self.folder_edit.text()
        self.selectionChanged.emit(abspath)

    def to_previous_directory(self):
        # get the path
        self.folder_memory.backward()
        path = self.folder_memory.current()
        # set the edit
        self.folder_edit.setText(path)
        # set the tree
        self.set_dir_tree(path)
        # emit
        abspath = self.folder_edit.text()
        self.selectionChanged.emit(abspath)

    def to_next_directory(self):
        self.folder_memory.forward()
        path = self.folder_memory.current()
        # set the edit
        self.folder_edit.setText(path)
        # set the tree
        self.set_dir_tree(path)
        # emit
        abspath = self.folder_edit.text()
        self.selectionChanged.emit(abspath)

    def set_dir_tree(self, path: str):
        if QFileInfo(path).isDir():
            model_index = self.fsm.index(path)
            if self.fsm.fileName(model_index) != "":
                self.tree_selection_model.setCurrentIndex(model_index, QItemSelectionModel.SelectionFlag.ClearAndSelect)

    """helper functions for this module"""

    def tab_action(self):
        """update the completer with the subfolders of the folder on which we clicked TAB"""
        prefix = self.completer.completionPrefix()
        text = self.folder_edit.text()
        if prefix != text:
            # a different option is chosen with the arrows in the dropdown
            next = text
        else:
            next = self.completer.currentCompletion()
        if QFileInfo(next).isDir():
            next = next + "\\"
        self.folder_edit.setText(next)
        self.completer.setCompletionPrefix(next)

    def expand_to_current(self, current_model_index: QModelIndex, old_model_index: QModelIndex):
        """make sure the tree expands to the correct filepath and old paths are collapsed"""
        old_path = self.fsm.filePath(old_model_index)
        new_path = self.fsm.filePath(current_model_index)

        if old_path in new_path:
            # either the new path is a subfolder of the new path...
            self.folder_tree.expand(current_model_index)
        elif new_path in old_path:
            # or the new path is a parent folder...
            index = old_model_index
            while old_path != new_path:
                self.folder_tree.collapse(index)
                index = self.fsm.parent(index)
                old_path = self.fsm.filePath(index)
        else:
            # ...or we start collapsing until they have the same joined path
            index = old_model_index
            while index != QModelIndex():
                self.folder_tree.collapse(index)
                index = self.fsm.parent(index)
                tempPath = self.fsm.filePath(index)
                if tempPath in new_path:
                    # here they have common path, so we break the collapse loop
                    break
            # and even if the loop continues all the way up the tree, this still works out fine for us..."""

            # time to expand the new path
            self.folder_tree.expand(current_model_index)

        # resize width of column every time expansion/collapsing happens
        self.folder_tree.resizeColumnToContents(0)
        # make the first column wider
        self.folder_tree.setColumnWidth(0, 500)

    def open_folder_in_os(self, model_index):
        os.startfile(self.fsm.filePath(model_index))


class TabSensitiveLineEdit(QLineEdit):
    """TabSensitiveLineEdit is a QLineEdit that emits a signal when the tab key is pressed."""
    tabPressed = pyqtSignal()

    def __init__(self, *args):
        QLineEdit.__init__(self, *args)

    def event(self, event):
        # emit new signal when tab key is pressed
        if (event.type() == QEvent.Type.KeyPress) and (event.key() == Qt.Key.Key_Tab):
            self.tabPressed.emit()
            return True

        # finally, pass event to parent
        return QLineEdit.event(self, event)

    def mousePressEvent(self, e):
        self.selectAll()


class FolderMemory:
    """
    FolderMemory is a class that keeps track of the last visited folders.
    It allows the user to navigate back and forth through the folder history.
    """

    def __init__(self):
        self.paths = []
        self.index = -1

    def add(self, path):
        self.paths = self.paths[0:self.index + 1]
        self.paths.append(path)
        self.index += 1

    def backward(self):
        self.index = max(self.index - 1, 0)
        return self.index

    def forward(self):
        self.index = min(self.index + 1, len(self.paths) - 1)
        return self.index

    def current(self):
        try:
            return self.paths[self.index]
        except IndexError:
            return ""
