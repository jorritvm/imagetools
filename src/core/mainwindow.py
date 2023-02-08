from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# written by hand instead of the qt designer, but using the same style of creating a second super class

class Ui_mainwindow(object):
    def setupUi(self, second):
        self.centralWidget = QWidget(self)
        self.setWindowTitle("Imagetools")

        # =======================================================================
        # """create toolbuttons"""
        # =======================================================================
        self.uiBtnAutoSelect = QPushButton("1. Auto Select")
        self.uiBtnImport = QPushButton("2. Import")
        self.uiBtnRotate = QPushButton("3. Rotate")
        self.uiBtnNumber = QPushButton("4. Number")
        self.uiBtnJudge = QPushButton("5. Judge")
        self.uiBtnRename = QPushButton("6. Rename")
        self.uiBtnResize = QPushButton("7. Resize")
        self.uiBtnWebAlbum = QPushButton("8. Web Album")
        self.uiBtnUpload = QPushButton("9. Upload")
        BtnList = [self.uiBtnAutoSelect, self.uiBtnImport, self.uiBtnRotate, self.uiBtnNumber, self.uiBtnJudge,
                   self.uiBtnRename, self.uiBtnResize, self.uiBtnWebAlbum, self.uiBtnUpload]

        """layout buttons 3x3"""
        self.groupActions = QGroupBox("Actions")
        self.uiLayoutBtns = QGridLayout(self.groupActions)
        i = 0
        for Btn in BtnList:
            x = i % 3
            y = int(i / 3)
            self.uiLayoutBtns.addWidget(Btn, y, x)
            i += 1
        self.uiLayoutBtns.setContentsMargins(4, 4, 4, 4)
        self.uiLayoutBtns.setSpacing(4)
        self.groupActions.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum))

        self.uiLayoutRight = QVBoxLayout()
        self.uiLayoutRight.addWidget(self.thumbnailBrowser)
        self.uiLayoutRight.addWidget(self.groupActions)
        self.uiLayoutRight.setContentsMargins(0, 0, 0, 0)

        self.widgetRight = QWidget()
        self.widgetRight.setLayout(self.uiLayoutRight)

        # =======================================================================
        # """global layout"""
        # =======================================================================
        """vertical splitter (left | right)"""
        self.hsplitter = QSplitter()
        self.hsplitter.addWidget(self.widget_left)
        self.hsplitter.addWidget(self.widgetRight)

        """setting the central widget and its contents"""
        self.setCentralWidget(self.centralWidget)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.addWidget(self.hsplitter)

        """size"""
        self.resize(800, 600)
        self.hsplitter.setSizes([150, 300])  # this gives us a nice startup size distribution
        # sizepol = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # self.ui_tree.setSizePolicy(sizepol)

        self.setWindowIcon(QIcon(":/appicon.ico"))

        """create menubar"""
        settingsAction = QAction("&Settings", self)
        settingsAction.triggered.connect(self.settings.show_settings)
        exitAction = QAction('&Exit', self)
        exitAction.triggered.connect(qApp.quit)
        aboutAction = QAction('&About', self)
        aboutAction.triggered.connect(self.show_about)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(settingsAction)
        fileMenu.addAction(exitAction)
        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(aboutAction)

        debugAction = QAction("&Debug", self)
        debugAction.triggered.connect(self.debug)
        helpMenu.addAction(debugAction)
