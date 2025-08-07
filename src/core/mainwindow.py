""" UI written by hand instead of the qt designer, but using the same 'trick' of creating a second super class """

from pyprojroot import here

from core.folder_select import *
from core.thumbnail_browser import ThumbnailBrowser


class Ui_mainwindow(object):
    def setup_ui(self):
        self.setup_widgets()
        self.setup_btn_tweaks()
        self.setup_menu_bar()
        self.setup_various()

    def setup_widgets(self):
        """ create left widget"""
        self.folder_select = FolderSelectWidget()

        """ create the right widget"""
        # create toolbuttons & organise them in a 3x3 layout
        self.btn_auto_select = QPushButton("1. Auto Select")
        self.btn_import = QPushButton("2. Import")
        self.btn_rotate = QPushButton("3. Rotate")
        self.btn_number = QPushButton("4. Number")
        self.btn_judge = QPushButton("5. Judge")
        self.btn_rename = QPushButton("6. Rename")
        self.btn_resize = QPushButton("7. Resize")
        self.btn_webalbum = QPushButton("8. Web Album")
        self.btn_upload = QPushButton("9. Upload")
        list_buttons = [self.btn_auto_select, self.btn_import, self.btn_rotate, self.btn_number, self.btn_judge,
                        self.btn_rename, self.btn_resize, self.btn_webalbum, self.btn_upload]
        group_actions = QGroupBox("Actions")
        layout_buttons = QGridLayout(group_actions)
        i = 0
        for btn in list_buttons:
            x = i % 3
            y = int(i / 3)
            layout_buttons.addWidget(btn, y, x)
            i += 1
        layout_buttons.setContentsMargins(4, 4, 4, 4)
        layout_buttons.setSpacing(4)
        group_actions.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum))

        # create the thumbnailbrowser
        # self supervisor and self.settings must exist in subclass (templating)
        self.t_browser = ThumbnailBrowser(self.supervisor, self.settings['path'], self.settings['image_size'])

        # combine thumbnailbrowser and buttonbox using a vlayout into the right widget
        layout_right = QVBoxLayout()
        layout_right.addWidget(self.t_browser)
        layout_right.addWidget(group_actions)
        layout_right.setContentsMargins(0, 0, 0, 0)
        self.widget_right = QWidget()
        self.widget_right.setLayout(layout_right)

        """combine left and right into the central widget"""
        self.hsplitter = QSplitter()
        self.hsplitter.addWidget(self.folder_select)
        self.hsplitter.addWidget(self.widget_right)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        gridLayout = QGridLayout(self.centralWidget)
        gridLayout.addWidget(self.hsplitter)

    def setup_btn_tweaks(self):
        # todo: remove when features are added
        self.btn_auto_select.setDisabled(True)
        self.btn_rotate.setDisabled(True)

    def setup_menu_bar(self):
        """create menu_bar"""
        self.action_settings = QAction("&Settings", self)
        self.action_exit = QAction('&Exit', self)
        self.action_about = QAction('&About', self)
        self.action_changelog = QAction('&Changelog', self)

        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu('&File')
        menu_file.addAction(self.action_settings)
        menu_file.addAction(self.action_exit)
        menu_help = menu_bar.addMenu("&Help")
        menu_help.addAction(self.action_about)
        menu_help.addAction(self.action_changelog)
        # todo: remove debug button and related code
        action_debug = QAction("&Debug", self)
        action_debug.triggered.connect(self.debug)
        menu_help.addAction(action_debug)

    def setup_various(self):
        self.setWindowTitle("Imagetools by JVM")
        self.setWindowIcon(QIcon(str(here("src/resources/appicon.ico"))))
        self.resize(800, 600)
        self.hsplitter.setSizes([150, 300])  # this gives us a nice startup size distribution
