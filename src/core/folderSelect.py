# from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class FolderSelectWidget(QWidget):

    selectionChanged = pyqtSignal(str)
                
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setup the left pane of the application's main window
        self.create_elements()
        self.setup_tree()
        self.setup_edit()
        self.setup_edit_tree_link()
        self.create_layout()
        
        self.tree_selection_model.selectionChanged.connect(self.handle_selection_change)
         
    def create_elements(self):
        """
        create both widgets of the left pane
        :return:
        """
        self.ui_tree = QTreeView()  # create directory browser
        self.ui_path = JLineEdit()  # create path input lineEdit

    def setup_tree(self):
        # file system model
        self.fsm = QFileSystemModel(self)
        self.fsm.setRootPath("")
        self.fsm.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
   
        # modify the treeview to show only the first column
        self.ui_tree.setModel(self.fsm)
        for i in range(3):
            self.ui_tree.setColumnHidden(i + 1, True)
        self.ui_tree.header().hide()

        # link the selection model to an instance variable for later use
        self.tree_selection_model = self.ui_tree.selectionModel()
        
        # add a horizontal scrollbar to the tree
        self.ui_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # todo: this probably can be deleted
 
        # if the current item is changed, only expand up to the new item
        self.tree_selection_model.currentChanged.connect(self.expand_to_current)

    def setup_edit(self):
        # set up a completer used by the lineEdit
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setModel(self.fsm)
        
        # set minimum popup height
        self.popup = self.completer.popup()
        self.popup.setMinimumSize(QSize(0,100))
        self.ui_path.setCompleter(self.completer)
        self.ui_path.tabPressed.connect(self.tabAction)
        
        # set clear button
        self.erase_path_btn = QPushButton("x")
        self.erase_path_btn.setMaximumWidth(20)
        
        # connect this new button to clearing the lineEdit
        self.erase_path_btn.pressed.connect(self.ui_path.clear)

    def setup_edit_tree_link(self):
        # link edit --> tree
        self.ui_path.returnPressed.connect(self.set_ui_tree)
        
        # link tree --> edit
        self.tree_selection_model.currentChanged.connect(self.set_file_path)

    def set_file_path(self, current_model_index, old_model_index):
        self.ui_path.setText(self.fsm.filePath(current_model_index))

    def set_ui_tree(self):
        path = self.ui_path.text()
        if QFileInfo(path).isDir():
            model_index = self.fsm.index(path)
            if self.fsm.fileName(model_index) != "":
                self.tree_selection_model.setCurrentIndex(model_index, QItemSelectionModel.ClearAndSelect)
    
    def tabAction(self):
        prefix = self.completer.completionPrefix()
        text = self.ui_path.text()
        if prefix != text:
            #a different option is chosen with the arrows in the dropdown
            next = text
        else: 
            next = self.completer.currentCompletion()
        if QFileInfo(next).isDir():
            next = next + "\\"
        self.ui_path.setText(next)
        self.completer.setCompletionPrefix(next)

    def expand_to_current(self, current_model_index, old_model_index):
        oldPath = self.fsm.filePath(old_model_index)
        newPath = self.fsm.filePath(current_model_index)
 
        if oldPath in newPath:
            """either the new path is a subfolder of the new path..."""
            self.ui_tree.expand(current_model_index)
        elif newPath in oldPath:
            """or the new path is a parent folder..."""
            index = old_model_index
            while oldPath != newPath:
                self.ui_tree.collapse(index)
                index = self.fsm.parent(index)
                oldPath = self.fsm.filePath(index)  
        else:
            """...or we start collapsing until they have the same joined path"""
            index = old_model_index
            while index != QModelIndex():
                self.ui_tree.collapse(index)
                index = self.fsm.parent(index)
                tempPath = self.fsm.filePath(index)
                if tempPath in newPath:
                    """here they have common path, so we break the collapse loop"""
                    break
            """and even if the loop continues all the way up the tree, this still works out fine for us..."""
            
            """time to expand the new path"""
            self.ui_tree.expand(current_model_index)
                
        """resize width of column every time expansion/collapsing happens"""
        self.ui_tree.resizeColumnToContents(0)
        """make the first column wider"""
        self.ui_tree.setColumnWidth(0, 500)
        
       
    def handle_selection_change(self, new, old):
        """since the selection model is annoying we make sure it always selects the 'current' item"""
        current_model_index = self.tree_selection_model.currentIndex()
        """although this is messy, just go with it ;-) """
        if len(new.indexes()) > 0:
            selectedModelIndex = new.indexes()[0]
            if current_model_index != selectedModelIndex:
                self.tree_selection_model.select(current_model_index, QItemSelectionModel.Clear)
                self.tree_selection_model.select(current_model_index, QItemSelectionModel.Select)
                
        abspath =  self.ui_path.text()
        self.selectionChanged.emit(abspath)


    def create_layout(self):
        line_edit_layout = QHBoxLayout()
        line_edit_layout.addWidget(self.ui_path)
        line_edit_layout.addWidget(self.erase_path_btn)
        line_edit_layout.setSpacing(2)
        
        ui_layout_left = QVBoxLayout()
        ui_layout_left.addLayout(line_edit_layout)
        ui_layout_left.addWidget(self.ui_tree)
        ui_layout_left.setContentsMargins(0, 0, 0, 0)

        self.setLayout(ui_layout_left)


class JLineEdit(QLineEdit):
    tabPressed = pyqtSignal()
    
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)

    def event(self, event):
        # emit new signal when tab key is pressed
        if (event.type() == QEvent.KeyPress) and (event.key() == Qt.Key_Tab):
            self.tabPressed.emit()
            return True

        # finally, pass event to parent
        return QLineEdit.event(self, event)
