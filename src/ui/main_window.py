from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QGroupBox, QSizePolicy, QSplitter, \
    QHBoxLayout, QWidget
from pyprojroot import here

import ui.constants as constants
from threaded_resizer.threaded_resizer import Supervisor
from ui.about import AboutDialog
from ui.action_handler import ActionHandler
from ui.browser import Browser
from ui.folder_select import FolderSelectWidget
from ui.settings import SettingsManager


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.settings = SettingsManager(self)
        self.supervisor = Supervisor(self.settings['n_threads'], self)
        self.action_buttons: dict = dict()

        self.setup_widgets()
        self.setup_menu_bar()
        self.setup_various()
        self.setup_slots()

        self.actionHandler = ActionHandler(self.folder_select,
                                           self.browser,
                                           self.action_buttons)

        # restore latest settings
        self.setFolder(self.settings['path'])
        self.resize(self.settings['app_size'])
        self.move(self.settings['app_position'])

    def setup_widgets(self):
        # create the left section
        self.folder_select = FolderSelectWidget()

        # create the middle section
        self.browser = Browser(self.supervisor, self.settings['path'], self.settings['image_size'])

        # create the right section
        self.action_buttons['takeout'] = QPushButton("Takeout")
        self.action_buttons['heic2jpg'] = QPushButton("Heic 2 JPG")
        self.action_buttons['flat2tree'] = QPushButton("Flat 2 Tree")
        self.action_buttons['auto_select'] = QPushButton("Auto Select")
        self.action_buttons['import'] = QPushButton("Import")
        self.action_buttons['rotate'] = QPushButton("Rotate")
        self.action_buttons['number'] = QPushButton("Number")
        self.action_buttons['judge'] = QPushButton("Judge")
        self.action_buttons['rename'] = QPushButton("Rename")
        self.action_buttons['resize'] = QPushButton("Resize")
        self.action_buttons['webalbum'] = QPushButton("Web Album")
        self.action_buttons['ftp_upload'] = QPushButton("FTP Upload")
        self.action_buttons['archive'] = QPushButton("Archive")
        self.action_buttons['cleanup'] = QPushButton("Cleanup")
        self.action_buttons['make_sequential'] = QPushButton("Make Sequential")
        self.action_buttons['prefix_mtime'] = QPushButton("Prefix MTime")
        self.action_buttons['separate_video'] = QPushButton("Separate Video")
        self.action_buttons['harvest_metadata'] = QPushButton("Harvest Metadata")
        self.group_actions = QGroupBox("Actions")
        layout_buttons = QVBoxLayout(self.group_actions)
        for btn in self.action_buttons.values():
            btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum))
            btn.setMinimumHeight(20)
            btn.setMinimumWidth(100)
            layout_buttons.addWidget(btn)

        """combine left, middle and right into the central widget"""
        self.right_of_splitter = QWidget()
        self.middle_right = QHBoxLayout(self.right_of_splitter)
        self.middle_right.addWidget(self.browser)
        self.middle_right.addWidget(self.group_actions)
        self.hsplitter = QSplitter(self)
        self.hsplitter.addWidget(self.folder_select)
        self.hsplitter.addWidget(self.right_of_splitter)
        self.setCentralWidget(self.hsplitter)
        self.folder_select.setContentsMargins(10, 0, 0, 10)
        self.middle_right.setContentsMargins(0, 0, 10, 10)

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
        self.setWindowIcon(QIcon("ui/resources/appicon.ico"))
        self.resize(constants.INITIAL_WINDOW_WIDTH, constants.INITIAL_WINDOW_HEIGHT)
        self.hsplitter.setSizes([100, 300])  # this gives us a nice startup size distribution

    def setup_slots(self):
        self.folder_select.selectionChanged.connect(self.browser.change_folder)
        self.action_settings.triggered.connect(self.settings.show_settings_dialog)
        self.action_exit.triggered.connect(self.close)
        self.action_about.triggered.connect(self.show_about)
        self.action_changelog.triggered.connect(self.show_changelog)

    def setFolder(self, path):
        self.folder_select.folder_edit.setText(path)
        self.folder_select.folder_edit.returnPressed.emit()

    @pyqtSlot()
    def show_about(self):
        dlg = AboutDialog(str(here("README.md")))
        dlg.exec()
        dlg.close()

    @pyqtSlot()
    def show_changelog(self):
        dlg = AboutDialog(str(here("NEWS.md")))
        dlg.exec()
        dlg.close()

    def closeEvent(self, event):
        self.settings['path'] = self.folder_select.folder_edit.text()
        self.settings['image_size'] = self.browser.thumbs_view.icon_size_position
        self.settings['app_size'] = self.size()
        self.settings['app_position'] = self.pos()
        self.settings.save_settings()

    def debug(self):
        print("paths")
        print(self.folder_select.folder_memory.paths)
        print("index")
        print(self.folder_select.folder_memory.index)
