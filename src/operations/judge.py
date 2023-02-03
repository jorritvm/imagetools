'''
Created on 27-okt.-2013

@author: jorrit
'''

import os
import shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Judge(QDialog):
    
    def __init__(self, files, supervisor, parent=None):
        QDialog.__init__(self,  parent)
        self.showMaximized()
        self.setModal(True)
        self.setWindowTitle("Judge images: click 1 to 9 for side by side, A B T for selections, enter to confirm, escape to cancel...")
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
                    
        self.files = files
        self.supervisor = supervisor
        self.supervisor.newItemReady.connect(self.processNextResizedItem)
        self.showCount = 3
        
        self.thumbs = dict() #key = filename #value = QImage
        self.startResize()
        
        self.marked = dict()
        self.currentlyJudging = self.files[0] #fi object
        self.currentlyJudgingReady = False
        self.setupJudgingReady = False
        
        self.fh = FileHandler()
        self.fh.nextDone.connect(self.writeResult)     
        
    
    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_1 :
            self.adaptCount(1)
        if e.key() == Qt.Key_2 :
            self.adaptCount(2)
        if e.key() == Qt.Key_3 :
            self.adaptCount(3)
        if e.key() == Qt.Key_4 :
            self.adaptCount(4)
        if e.key() == Qt.Key_5 :
            self.adaptCount(5)
        if e.key() == Qt.Key_6 :
            self.adaptCount(6)
        if e.key() == Qt.Key_7 :
            self.adaptCount(7)
        if e.key() == Qt.Key_8 :
            self.adaptCount(8)
        if e.key() == Qt.Key_9 :
            self.adaptCount(9)
        if e.key() == Qt.Key_Right :
            self.move("right")
        if e.key() == Qt.Key_Left :
            self.move("left")
        if e.key() == Qt.Key_A :
            self.markImage("Sel_A")
        if e.key() == Qt.Key_B :
            self.markImage("Sel_B")
        if e.key() == Qt.Key_T :
            self.markImage("Trash")
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            self.writeResult()
        if e.key() == Qt.Key_Escape:
            self.reject()
    
    def sbText(self, txt):
        self.sb.clearMessage()
        self.sb.showMessage(txt)
        
    def adaptCount(self, i):
        self.showCount = i
        self.setupJudgingReady = False
        self.setupJudging()  
        
    def move(self,direction):
        o  = self.files.index(self.currentlyJudging)
        if direction == "right":
            try:
                self.currentlyJudging = self.files[o+1]
                self.currentlyJudgingReady = False
                self.setupJudgingReady = False
                self.setupJudging()                
            except:
                pass #at the end of the list there aren't any to the right
                o  = self.files.index(self.currentlyJudging)
        if direction == "left":
            if o > 0: #at the beginning of the list there aren't any to the left
                self.currentlyJudging = self.files[o-1]
                self.currentlyJudgingReady = False
                self.setupJudgingReady = False
                self.setupJudging()                
    
    def markImage(self, dirname):
        fi = self.currentlyJudging
        fn = fi.fileName()
        self.marked[fn] = (fi, dirname)
        self.move("right")
            
    def startResize(self):
        q = []
        h = self.height()
        for fi in self.files:
            q.append([fi, h, True]) #smooth
        self.currentlyProcessing = self.supervisor.add_items(q, True) # prior
        self.supervisor.process_queue()
    
    
    def processNextResizedItem(self, ticket, img):
        for item in self.currentlyProcessing:
            if item[3] == ticket:
                fn = item[0].fileName()
                self.thumbs[fn] = img
        self.setupJudging()        
        
        
    def readyForJudging(self, fi):
        ready = True
        if not self.currentlyJudgingReady:
            o  = self.files.index(fi)
            p = o + self.showCount
            
            for i in range(o,p):
                try:
                    fi = self.files[i]
                    if fi.fileName() in self.thumbs.keys():
                        pass
                    else:
                        ready = False
                except: 
                    pass # in case we want to go outside of self.files bounds
        return ready #we are ready to show all these thumbs based on the count and current judging item   
    
           
    def setupJudging(self):
        if not self.currentlyJudgingReady:
            #print("not ready to judge: "+ self.currentlyJudging.fileName())
            self.currentlyJudgingReady = self.readyForJudging(self.currentlyJudging)
        
        if not self.setupJudgingReady: #we haven't shown the currently requested pictures yet
            if self.currentlyJudgingReady:
                while self.layout.count():
                    child = self.layout.takeAt(0) #werkt niet
                    while child.count():
                        child.takeAt(0).widget().deleteLater() 
                    del child                  
                
                o  = self.files.index(self.currentlyJudging)
                for i in range(self.showCount):
                    p = o + i
                    a = self.size().width() / self.showCount - 25
                    b = self.size().height() - 45
                    lbltop = QLabel()
                    lbltop.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum))
                    lbl = QLabel("End of list...")
                    try:
                        fn = self.files[p].fileName()
                        myPixmap = QPixmap.fromImage(self.thumbs[fn])    
                        myScaledPixmap = myPixmap.scaled(a,b, Qt.KeepAspectRatio)
                        lbl.setPixmap(myScaledPixmap)
                        if fn in self.marked.keys():
                            lbltop.setText(fn + " - " + self.marked[fn][1])
                        else: 
                            lbltop.setText(fn)
                    except:
                        pass #when we get to the end of the list there aren't any more items to the right
                    lout = QVBoxLayout()
                    lout.addWidget(lbltop)
                    lout.addWidget(lbl)
                    self.layout.addLayout(lout)

                self.setupJudgingReady = True
            
            
    def writeResult(self):
        if len(self.marked) > 0:
           
            item = self.marked.popitem()[1]
            fi = item[0]
            destDir = os.path.join(fi.absolutePath(),item[1]) 

            self.fh.initialize(fi, destDir, "move")
            self.fh.start()
        else:
            self.accept()
          
                    
class FileHandler(QThread):
    
    nextDone = pyqtSignal()
    
    def __init__(self,  parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
    
    def initialize(self, fi, destDir, mode):
        self.fi = fi
        self.destDir = destDir
        self.mode = mode

    def run(self):
        fi = self.fi
        fi_old = fi.absoluteFilePath()
        fi_new = QFileInfo(QDir(self.destDir), fi.fileName()).absoluteFilePath()
        fi_cr2_old = fi.absolutePath() + "/" +  fi.baseName() + ".CR2"
        fi_cr2_new = QFileInfo(QDir(self.destDir), fi.baseName() + ".CR2").absoluteFilePath()

        # create the directory
        dirp = fi.dir()
        if dirp.mkpath(self.destDir):
            pass
        else:
            print("Creating directory failed...")
         
        #moving the files
        if self.mode == "copy":
            shutil.copy2(fi_old, fi_new)
            if os.path.exists(fi_cr2_old):
                shutil.copy2(fi_cr2_old, fi_cr2_new)
        if self.mode == "move":
            shutil.move(fi_old, fi_new)
            if os.path.exists(fi_cr2_old):
                shutil.move(fi_cr2_old, fi_cr2_new)
        
        self.nextDone.emit()
             

        
        
        
           
            