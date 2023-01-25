'''
Created on 11-sep.-2013

@author: jorrit
'''
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class folderSelectWidget(QWidget):
    #===========================================================================
    # TREE AND EDIT WIDGET
    #===========================================================================
    
    selectionChanged = pyqtSignal(str)
                
    def __init__(self,parent = None):
        QWidget.__init__(self, parent)
        self.createElements()
        self.setupTree()
        self.setupEdit()
        self.setupEditTreeLink()
        self.createLayout()
        
        self.treeSelectionModel.selectionChanged.connect(self.handleSelectionChange)
         
    def createElements(self):        
        """create directory browser"""
        self.uiTree = QTreeView()
        """create path input lineedit"""
        self.uiPath = JLineEdit()        

    
    def setupTree(self):
        """file system model"""
        self.fsm = QFileSystemModel(self)
        self.fsm.setRootPath("")
        self.fsm.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
   
        """modify the treeview to show only the first column"""                
        self.uiTree.setModel(self.fsm)
        for i in range(3):
            self.uiTree.setColumnHidden(i+1, True)
        self.uiTree.header().hide()

        """link the selection model to an instance variable for later use"""
        self.treeSelectionModel = self.uiTree.selectionModel()
        
        """add a horizontal scrollbar to the tree"""
        self.uiTree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn) #this probably can be deleted  
 
        """if the current item is changed, only expand up to the new item"""
        self.treeSelectionModel.currentChanged.connect(self.expandToCurrent) 

      
    def setupEdit(self):
        """completer used by the lineedit"""
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setModel(self.fsm)
        
        """set minimum popup height"""
        self.popup = self.completer.popup()
        self.popup.setMinimumSize(QSize(0,100))
        self.uiPath.setCompleter(self.completer)
        self.uiPath.tabPressed.connect(self.tabAction)
        
        """set clear button"""
        self.erasePathButton = QPushButton("x")
        self.erasePathButton.setMaximumWidth(20)
        
        """connection"""
        self.erasePathButton.pressed.connect(self.uiPath.clear)
        
        
    def setupEditTreeLink(self):
        """edit --> tree"""
        txt = self.uiPath.text()
        self.uiPath.returnPressed.connect(self.setUiTree)
        
        """tree --> edit"""
        self.treeSelectionModel.currentChanged.connect(self.setFilePath)
             
       
    def setFilePath(self, currentModelIndex, oldModelIndex):
        self.uiPath.setText(self.fsm.filePath(currentModelIndex))
       
       
    def setUiTree(self):
        path = self.uiPath.text()
        check = QFileInfo(path).isDir()
        if check:
            modelIndex = self.fsm.index(path)
            if self.fsm.fileName(modelIndex) !=  "":
                self.treeSelectionModel.setCurrentIndex(modelIndex, QItemSelectionModel.ClearAndSelect) #strong stuff
                                      
    
    def tabAction(self):
        prefix = self.completer.completionPrefix()
        text = self.uiPath.text()
        if prefix != text:
            #a different option is chosen with the arrows in the dropdown
            next = text
        else: 
            next = self.completer.currentCompletion()
        if QFileInfo(next).isDir():
            next = next + "\\"
        self.uiPath.setText(next)
        self.completer.setCompletionPrefix(next)
    
    
    def expandToCurrent(self, currentModelIndex, oldModelIndex):
        oldPath = self.fsm.filePath(oldModelIndex)
        newPath = self.fsm.filePath(currentModelIndex)
 
        if oldPath in newPath:
            """either the new path is a subfolder of the new path..."""
            self.uiTree.expand(currentModelIndex)
        elif newPath in oldPath:
            """or the new path is a parent folder..."""
            index = oldModelIndex
            while oldPath != newPath:
                self.uiTree.collapse(index)
                index = self.fsm.parent(index)
                oldPath = self.fsm.filePath(index)  
        else:
            """...or we start collapsing until they have the same joined path"""
            index = oldModelIndex
            while index != QModelIndex():
                self.uiTree.collapse(index)
                index = self.fsm.parent(index)
                tempPath = self.fsm.filePath(index)
                if tempPath in newPath:
                    """here they have common path, so we break the collapse loop"""
                    break
            """and even if the loop continues all the way up the tree, this still works out fine for us..."""
            
            """time to expand the new path"""
            self.uiTree.expand(currentModelIndex)
                
        """resize width of column every time expansion/collapsing happens"""
        self.uiTree.resizeColumnToContents(0)
        """make the first column wider"""
        self.uiTree.setColumnWidth(0,500)
        
       
    def handleSelectionChange(self, new, old):
        """since the selection model is annoying we make sure it always selects the 'current' item"""
        currentModelIndex = self.treeSelectionModel.currentIndex()
        """although this is messy, just go with it ;-) """
        if len(new.indexes()) > 0:
            selectedModelIndex = new.indexes()[0]
            if currentModelIndex != selectedModelIndex:
                self.treeSelectionModel.select(currentModelIndex, QItemSelectionModel.Clear)
                self.treeSelectionModel.select(currentModelIndex, QItemSelectionModel.Select)
                
        abspath =  self.uiPath.text()
        self.selectionChanged.emit(abspath)


    def createLayout(self):
        lineEditLayout = QHBoxLayout()
        lineEditLayout.addWidget(self.uiPath)
        lineEditLayout.addWidget(self.erasePathButton)
        lineEditLayout.setSpacing(2)
        
        self.uiLayoutLeft = QVBoxLayout()
        self.uiLayoutLeft.addLayout(lineEditLayout)
        self.uiLayoutLeft.addWidget(self.uiTree)
        self.uiLayoutLeft.setContentsMargins(0,0,0,0)
        self.setLayout(self.uiLayoutLeft)            
               
class JLineEdit(QLineEdit):
    """it's important to define new style pyqt signals in the class declaration space, not the constructor!!!"""
    tabPressed = pyqtSignal()
    
    def __init__(self, *args):
        """call the superclass's constructor"""
        QLineEdit.__init__(self, *args)
        
        
    def event(self, event):
        #this class has new signals to act when certain keys are pressed 
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Tab):
            self.tabPressed.emit()
            return True

        return QLineEdit.event(self, event) #pass event of to parent if we don't need it
