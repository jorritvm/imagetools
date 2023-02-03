'''
Created on 8-okt.-2013

@author: jorrit
'''
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threadedResizer.threadedResizer import Supervisor


class thumbnailBrowser(QWidget):
    def __init__(self, supervisor, path, parent=None):
        QWidget.__init__(self, parent)
        
        self.listView = CustomQListWidget()
        self.setupListView()
        
        self.detailView = QTreeWidget
        self.setupDetailView()

        self.setupUi()
        self.setupExternalOpen()
        self.setupZoomButtons()    
        self.setupSelectionButtons()
        
        self.setSupervisor(supervisor)
        
        self.rootFolder = ""
        self.changeFolder(path)       
    
    #===========================================================================
    # UI SETUP CODE 
    #=========================================================================== 
        
    def setupUi(self):
        """create selectionbox buttons"""
        self.uiBtnAdd = QPushButton("Add")
        self.uiBtnRemove = QPushButton("Remove")
        self.uiBtnAddAll = QPushButton("Add All")
        self.uiBtnClear = QPushButton("Clear")
        BtnList2 = [self.uiBtnAdd, self.uiBtnRemove, self.uiBtnAddAll, self.uiBtnClear]

        """layout buttons"""
        self.groupSelection = QGroupBox("Selection")
        self.uiLayoutBtns2 = QHBoxLayout(self.groupSelection)
        for Btn in BtnList2:
            self.uiLayoutBtns2.addWidget(Btn)
        self.uiLayoutBtns2.setContentsMargins(4,4,4,4)
        self.uiLayoutBtns2.setSpacing(4)

        """create browser buttons"""
        self.uiThumb = QPushButton("T")
        self.uiDetail = QPushButton("D")
        self.uiZoomIn = QPushButton("+")
        self.uiZoomOut = QPushButton("-")
        BtnList3 = [self.uiThumb, self.uiDetail, self.uiZoomOut, self.uiZoomIn]

        """layout buttons"""
        self.groupBrowser = QGroupBox("Browser")
        self.uiLayoutBtns3 = QHBoxLayout(self.groupBrowser)
        for Btn in BtnList3:
            Btn.setMaximumWidth(25)
            self.uiLayoutBtns3.addWidget(Btn)
        self.uiLayoutBtns3.setContentsMargins(4,4,4,4)
        self.uiLayoutBtns3.setSpacing(4)
        self.groupBrowser.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred))
                             
        """rechtse layout"""
        self.uiLayoutBtns4 = QHBoxLayout()
        self.uiLayoutBtns4.addWidget(self.groupSelection)
        self.btnSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.uiLayoutBtns4.addItem(self.btnSpacer)
        self.uiLayoutBtns4.addWidget(self.groupBrowser)
        
        self.uiLayoutRight = QVBoxLayout()
        self.uiLayoutRight.addWidget(self.listView)
        self.uiLayoutRight.addLayout(self.uiLayoutBtns4)
        self.uiLayoutRight.setContentsMargins(4,4,4,4)
        
        self.setLayout(self.uiLayoutRight)    
    
    def setupListView(self):
        """change the viewmode to iconmode instead of listmode"""
        self.listView.setViewMode(QListView.IconMode)
        
        """set the icon size"""
        self.listView.iconSizes = [50,100,150,200,250,300,350]
        self.listView.iconSizePosition = 2
        self.listView.setIconMaxSize()
        
        """add some spacing around the elements"""
        self.listView.setSpacing(10)
        
        """wrap the items when there are too many to layout horizontally"""
        self.listView.setWrapping(True)
        
        """set the automatic resize to adjust instead of fixed"""
        self.listView.setResizeMode(QListView.Adjust)
        
        """set the view to allow multiple selection"""
        self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
    
    def setupDetailView(self):
        pass

    def setupExternalOpen(self):
        self.listView.itemDoubleClicked.connect(self.externalOpen)
    
    def externalOpen(self, item):
        fi = QFileInfo()
        fi.setFile(QDir(self.rootFolder), item.text())
        link = fi.absoluteFilePath()
        os.startfile(link)

    #===========================================================================
    # ZOOM BUTTONS ACTIONS
    #===========================================================================

    def setupZoomButtons(self):
        """python 3.0 style connections"""
        self.uiZoomIn.pressed.connect(lambda: self.listView.adjustIconSize("+"))
        self.uiZoomOut.pressed.connect(lambda: self.listView.adjustIconSize("-"))
  
    #===========================================================================
    # SELECTION BUTTONS ACTIONS
    #===========================================================================
    
    def setupSelectionButtons(self):
        self.uiBtnAdd.pressed.connect(self.addButtonAction)
        self.uiBtnRemove.pressed.connect(self.removeButtonAction)
        self.uiBtnAddAll.pressed.connect(self.addAllButtonAction)
        self.uiBtnClear.pressed.connect(self.clearButtonAction)   
           
    def addButtonAction(self):
        view = self.listView
        for i in range(view.count()):
            item = view.item(i)
            if view.isItemSelected(item):
                item.setBackgroundColor(QColor(Qt.green))
        
    def removeButtonAction(self):
        view = self.listView
        for i in range(view.count()):
            item = view.item(i)
            if view.isItemSelected(item):
                item.setBackgroundColor(QColor(Qt.white))
    
    def addAllButtonAction(self):
        view = self.listView
        for i in range(view.count()):
            item = view.item(i)
            item.setBackgroundColor(QColor(Qt.green))  
       
    def clearButtonAction(self):
        view = self.listView
        for i in range(view.count()):
            item = view.item(i)
            item.setBackgroundColor(QColor(Qt.white))
    
    #===========================================================================
    # SUPERVISOR USAGE (multithreaded thumbnail generation) 
    #===========================================================================    
    
    def setSupervisor(self, supervisor):
        self.supervisor = supervisor
        self.supervisor.newItemReady.connect(self.imageReady)

    def imageReady(self, ticket, img): #img is in QImage format
        #check of dit ticket van ons is
        for item in self.currentlyProcessing:
            if item[3] == ticket:
                name = os.path.basename(item[0].absoluteFilePath())
                for i in range(self.listView.count()):
                    if self.listView.item(i).text() == name:
                        self.listView.item(i).setIcon(QIcon(QPixmap.fromImage(img)))             
   
    
    #===========================================================================
    # CORE THUMBNAILBROWSER FEATURES 
    #=========================================================================== 
            
    def changeFolder(self, path):
        self.rootFolder = path
        self.listView.clear()
        self.supervisor.clear_queue()

        """set a directory model with appropriate filters to get the image info"""
        self.dirModel = QDir(path)
        self.dirModel.setNameFilters(["*.jpg","*.jpeg","*.png","*.bmp"])

        """create the DATA the model will use"""
        self.images = self.dirModel.entryList()
        self.absolutePathImages = list()
        for fileName in self.images:
            self.absolutePathImages.append(self.dirModel.absoluteFilePath(fileName))   
        
        q = []
        for file in self.absolutePathImages:
            q.append([QFileInfo(file), 400, False]) # not smooth
            px = QPixmap(480,270) #take this dummy thumbnail large enough
            px.fill(QColor(255,255,255)) #makes sure it's white 
            x = QListWidgetItem(QIcon(px), os.path.basename(file))
            self.listView.addItem(x) 
            
        self.currentlyProcessing = self.supervisor.add_items(q, False) # not prior
        self.supervisor.process_queue()
    

    def getSelection(self): 
        """returns list of QFileInfo objetcs"""
        x = []
        view = self.listView
        for i in range(view.count()):
            item = view.item(i)
            if item.backgroundColor() == QColor(Qt.green):
                fi = QFileInfo()
                fi.setFile(QDir(self.rootFolder), item.text())
                x.append(fi)
        return x
        
    def updateElements(self, changes):
        print(changes)
        for old,new in changes.items():
            fi_old = QFileInfo(old)
            fi_new = QFileInfo(new)                       
            if self.rootFolder == fi_old.absolutePath():
                view = self.listView
                for i in range(view.count()):
                    item = view.item(i)
                    if item.text() == fi_old.fileName():
                        #print("found it")
                        item.setText(fi_new.fileName())
        
        
    
class CustomQListWidget(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self,parent)
        
    
    #===========================================================================
    # ZOOM ACTIONS
    #===========================================================================
    def adjustIconSize(self,direction):
        if direction == "+":
            newPos = self.iconSizePosition + 1 
        elif direction == "-":
            newPos = self.iconSizePosition - 1
        
        """make sure we don't try to go out of bounds of our sizes list"""
        if newPos < 0 or newPos > len(self.iconSizes)-1:
            newPos = self.iconSizePosition

        self.iconSizePosition = newPos
        self.setIconMaxSize()
        
    
    def setIconMaxSize(self):
        """here we really set the iconSize, the view will update automaticly"""
        size = self.iconSizes[self.iconSizePosition]
        self.setIconSize(QSize(size,size*9/16))
        self.setGridSize(QSize(size+0,size*9/16+25))
        
