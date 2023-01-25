#!/usr/bin/python
############################################################################
#    Copyright (C) 2013 by Jorrit Vander Mynsbrugge                        #
#    jorrit.vm@gmail.com                                                   #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

#python imports
import os
import sys
import time
import pickle

#pyqt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#application code imports
from resource import *
from core.about_run import *
from core.settings_run import *
from core.folderSelect import *
from core.thumbnailBrowser import *
from threadedResizer.threadedResizer import *
from msilib.schema import SelfReg

from imageoperations.Import import *
from imageoperations.Number import *
from imageoperations.Rename import *
from imageoperations.Resize import *
from imageoperations.WebAlbum import *
from imageoperations.Upload import *
from imageoperations.Judge import *


class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)
       
        self.settings = self.getSettings()
        self.supervisor = Supervisor(self.settings['nThreads'], self)
        
        self.widgetLeft = folderSelectWidget()
        self.thumbnailBrowser = thumbnailBrowser(self.supervisor, self.settings['path'])
        self.setupUi()
        self.widgetLeft.selectionChanged.connect(self.thumbnailBrowser.changeFolder)
        self.setupToolButtons()
        self.setFolder(self.settings['path'])


    def debugButton(self):
        pass
         
     
    def setFolder(self, path):
        self.widgetLeft.uiPath.setText(path)
        self.widgetLeft.uiPath.returnPressed.emit()
    
    #===========================================================================
    # DIALOG HANDLING
    #===========================================================================

    def getSettings(self):
        #get settings
        values = dict()
        if not os.path.exists("settings.bin"):
            values['nThreads'] = 1
            values['saveThumbs'] = False
            values['defaultLocation'] = "c:/temp"
            values['path'] = ""  
        else:
            try:
                fi = open("settings.bin", 'rb')
                values = pickle.load(fi)
            finally:
                fi.close()
        return values
    
    def saveSettings(self):
        flag = False
        try:
            fi = open("settings.bin", 'wb')
            pickle.dump(self.settings, fi)
            flag = True
        except:
            flag = False
            QMessageBox.critical(self,"ERROR", "There was an error saving these settings...")
        finally:
            fi.close()

        return flag

    def showSettings(self):
        self.settingsDialog = SettingsRun(self.settings)
        # ---
        #not yet implemented
        self.settingsDialog.saveThumbsCheck.setDisabled(True)
        self.settingsDialog.label_2.setDisabled(True)
        # ---
        self.settingsDialog.accepted.connect(self.acceptSettings)
        self.settingsDialog.rejected.connect(self.rejectSettings)
        self.settingsDialog.exec_()
        
    def acceptSettings(self):
        temp = self.settingsDialog.dictValues()
        for key,value in temp.items():
            self.settings[key] = value
        flag = self.saveSettings()
        if flag:
            QMessageBox.warning(self,"Warning", "You must restart Imagetools for changes to take effect...")
        self.settingsDialog.close()
        
    def rejectSettings(self):
        self.settingsDialog.close()
    
    def closeEvent(self, event):
        #saving settings
        self.settings['path'] = self.widgetLeft.uiPath.text()
        self.saveSettings()
    
    def showAbout(self):
        about = AboutRun()
        about.exec_()
        about.close()
        

    #===========================================================================
    # TOOL BUTTONS ACTIONS
    #===========================================================================
    
    def setupToolButtons(self):
        self.uiBtnImport.pressed.connect(self.importButtonAction)
        self.uiBtnNumber.pressed.connect(self.numberButtonAction)
        self.uiBtnRename.pressed.connect(self.renameButtonAction)
        self.uiBtnResize.pressed.connect(self.resizeButtonAction)
        self.uiBtnWebAlbum.pressed.connect(self.webAlbumButtonAction)
        self.uiBtnUpload.pressed.connect(self.uploadButtonAction)
        self.uiBtnJudge.pressed.connect(self.judgeButtonAction)
        
        self.uiBtnAutoSelect.setDisabled(True)
        self.uiBtnRotate.setDisabled(True)
        
    
    def importButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            im = Import(files, self.settings, self.widgetLeft.uiPath.text()) 
            if im.exec_():
                path = im.getNewPath()
                self.setFolder(path)
            im.close()
        
    
    def numberButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog and extract the user's settings"""
            num = Number()
            settings = None
            if num.exec_():
                settings = num.getSettings()
                
                """start the rename procedure"""
                trackChanges = num.renameFiles(files, settings)
                self.thumbnailBrowser.updateElements(trackChanges)
                num.close()
       
    def renameButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog"""
            ren = Rename(files, self.supervisor)
            ren.exec_()
            ren.close()
           
            """the dialog is ready now, we should update the application with the new filenames"""
            trackChanges = ren.getChanges()
            self.thumbnailBrowser.updateElements(trackChanges)
       
  
    def resizeButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog"""
            res = Resize(files, self.supervisor, self.widgetLeft.uiPath.text())
            res.exec_()
            x = self.widgetLeft.uiPath.text()
            res.close()
         
    def webAlbumButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog"""
            wa = WebAlbum(files, self.supervisor)
            wa.exec_()
            wa.close()
           
    def uploadButtonAction(self):
        """create the dialog"""
        up = Upload(self.settings, self.widgetLeft.uiPath.text()) 
        up.exec_()
        up.close()
        
    def judgeButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog"""
            ju = Judge(files, self.supervisor) 
            ju.exec_()
            ju.close()

            
    #===========================================================================
    # SET UP UI
    #===========================================================================
        
    def setupUi(self):

        self.centralWidget = QWidget(self)
        self.setWindowTitle("Imagetools")
        
        #=======================================================================
        # """create toolbuttons"""
        #=======================================================================
        self.uiBtnAutoSelect = QPushButton("1. Auto Select")
        self.uiBtnImport = QPushButton("2. Import")
        self.uiBtnRotate = QPushButton("3. Rotate")
        self.uiBtnNumber = QPushButton("4. Number")
        self.uiBtnJudge = QPushButton("5. Judge")
        self.uiBtnRename = QPushButton("6. Rename")
        self.uiBtnResize = QPushButton("7. Resize")
        self.uiBtnWebAlbum = QPushButton("8. Web Album")
        self.uiBtnUpload = QPushButton("9. Upload")
        BtnList = [self.uiBtnAutoSelect, self.uiBtnImport, self.uiBtnRotate, self.uiBtnNumber, self.uiBtnJudge, self.uiBtnRename, self.uiBtnResize, self.uiBtnWebAlbum, self.uiBtnUpload]
                
        """layout buttons 3x3"""
        self.groupActions = QGroupBox("Actions")
        self.uiLayoutBtns = QGridLayout(self.groupActions)
        i = 0
        for Btn in BtnList:
            x = i % 3
            y = int(i/3)
            self.uiLayoutBtns.addWidget(Btn,y,x)
            i += 1
        self.uiLayoutBtns.setContentsMargins(4,4,4,4)
        self.uiLayoutBtns.setSpacing(4)
        self.groupActions.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum))
     
        self.uiLayoutRight = QVBoxLayout()
        self.uiLayoutRight.addWidget(self.thumbnailBrowser)
        self.uiLayoutRight.addWidget(self.groupActions)
        self.uiLayoutRight.setContentsMargins(0,0,0,0)
        
        self.widgetRight = QWidget()
        self.widgetRight.setLayout(self.uiLayoutRight)
        
        
        #=======================================================================
        # """globale layout"""
        #=======================================================================
        """vertical splitter (left | right)"""
        self.hsplitter = QSplitter()
        self.hsplitter.addWidget(self.widgetLeft)
        self.hsplitter.addWidget(self.widgetRight)
                  
        """setting the central widget and its contents"""
        self.setCentralWidget(self.centralWidget)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.addWidget(self.hsplitter)
        
        """size"""
        self.resize(800, 600)
        self.hsplitter.setSizes([150,300]) #this gives us a nice startup size distribution
        #sizepol = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        #self.uiTree.setSizePolicy(sizepol)
        
        self.setWindowIcon(QIcon(":/appicon.ico"))
        
        """create menubar"""
        settingsAction = QAction("&Settings", self)
        settingsAction.triggered.connect(self.showSettings)
        exitAction = QAction('&Exit', self)        
        exitAction.triggered.connect(qApp.quit)
        aboutAction = QAction('&About', self)        
        aboutAction.triggered.connect(self.showAbout)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(settingsAction)
        fileMenu.addAction(exitAction)
        helpMenu = menubar.addMenu("&Help")
        helpMenu .addAction(aboutAction)
        
        debugAction = QAction("&Debug", self)
        debugAction.triggered.connect(self.debugButton)
        helpMenu.addAction(debugAction)
        

if __name__ == "__main__":
    
    import sys
    app = QApplication(sys.argv)
    
    main = MainWindow()
    main.show()
    
    sys.exit(app.exec_())
        


