from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QGroupBox, QSizePolicy, QSplitter, \
    QHBoxLayout, QWidget

from threaded_resizer.threaded_resizer import Supervisor
from ui.browser import Browser
from ui.folder_select import FolderSelectWidget
from ui.settings import SettingsManager


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.settings = SettingsManager(self)
        self.supervisor = Supervisor(self.settings['n_threads'], self)
        self.setup_widgets()
        # self.setup_btn_tweaks()
        # self.setup_menu_bar()
        # self.setup_various()
        # self.setup_slots()
        #
        # # restore latest settings
        # self.setFolder(self.settings['path'])
        # self.resize(self.settings['app_size'])
        # self.move(self.settings['app_position'])

    def setup_widgets(self):
        # create the left section
        self.folder_select = FolderSelectWidget()

        # create the middle section
        self.browser = Browser(self.supervisor, self.settings['path'], self.settings['image_size'])

        # create the right section
        self.actions = dict()
        self.actions['takeout'] = QPushButton("Takeout")
        self.actions['heic2jpg'] = QPushButton("Heic 2 JPG")
        self.actions['flat2tree'] = QPushButton("Flat 2 Tree")
        self.actions['auto_select'] = QPushButton("Auto Select")
        self.actions['import'] = QPushButton("Import")
        self.actions['rotate'] = QPushButton("Rotate")
        self.actions['number'] = QPushButton("Number")
        self.actions['judge'] = QPushButton("Judge")
        self.actions['rename'] = QPushButton("Rename")
        self.actions['resize'] = QPushButton("Resize")
        self.actions['webalbum'] = QPushButton("Web Album")
        self.actions['ftp_upload'] = QPushButton("FTP Upload")
        self.actions['archive'] = QPushButton("Archive")
        self.actions['cleanup'] = QPushButton("Cleanup")
        self.actions['make_sequential'] = QPushButton("Make Sequential")
        self.actions['prefix_mtime'] = QPushButton("Prefix MTime")
        self.actions['separate_video'] = QPushButton("Separate Video")
        self.actions['harvest_metadata'] = QPushButton("Harvest Metadata")
        self.group_actions = QGroupBox("Actions")
        layout_buttons = QVBoxLayout(self.group_actions)
        for btn in self.actions.values():
            btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum))
            btn.setMinimumHeight(30)
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
        self.setContentsMargins(10, 10, 10, 10)

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

    def setup_slots(self):
        self.folder_select.selectionChanged.connect(self.browser.change_folder)
        self.btn_import.pressed.connect(self.import_btn_action)
        self.btn_number.pressed.connect(self.numberButtonAction)
        self.btn_rename.pressed.connect(self.renameButtonAction)
        self.btn_resize.pressed.connect(self.resizeButtonAction)
        self.btn_webalbum.pressed.connect(self.webAlbumButtonAction)
        self.btn_upload.pressed.connect(self.uploadButtonAction)
        self.btn_judge.pressed.connect(self.judgeButtonAction)
        self.action_settings.triggered.connect(self.settings.show_settings_dialog)
        self.action_exit.triggered.connect(self.close)
        self.action_about.triggered.connect(self.show_about)
        self.action_changelog.triggered.connect(self.show_changelog)

    def setFolder(self, path):
        self.folder_select.folder_edit.setText(path)
        self.folder_select.folder_edit.returnPressed.emit()

    def show_about(self):
        dlg = AboutDialog("README.md")
        dlg.exec()
        dlg.close()

    def show_changelog(self):
        dlg = AboutDialog("NEWS.md")
        dlg.exec()
        dlg.close()

    def closeEvent(self, event):
        self.settings['path'] = self.folder_select.folder_edit.text()
        self.settings['image_size'] = self.browser.thumbs_view.icon_size_position
        self.settings['app_size'] = self.size()
        self.settings['app_pos'] = self.pos()
        self.settings.save_settings()

    def import_btn_action(self):
        files = self.browser.get_selection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else:
            im = ImportImages(files, self.settings, self.folder_select.folder_edit.text())
            if im.exec():
                path = im.get_new_path()
                self.setFolder(path)
            im.close()

    def numberButtonAction(self):
        files = self.browser.get_selection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else:
            """create the dialog and extract the user's settings"""
            num = Number()
            if num.exec():
                settings = num.get_settings()
                track_changes = num.rename_files(files, settings)
                self.browser.update_elements(track_changes)
                num.close()

    def renameButtonAction(self):
        files = self.browser.get_selection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else:
            """create the dialog"""
            ren = Rename(files, self.supervisor)
            ren.exec()
            ren.close()

            """the dialog is ready now, we should update the application with the new filenames"""
            trackChanges = ren.getChanges()
            self.browser.update_elements(trackChanges)

    def resizeButtonAction(self):
        files = self.browser.get_selection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else:
            """create the dialog"""
            res = Resize(files, self.supervisor, self.folder_select.folder_edit.text())
            res.exec()
            x = self.folder_select.folder_edit.text()
            res.close()

    def webAlbumButtonAction(self):
        files = self.browser.get_selection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else:
            """create the dialog"""
            wa = WebAlbum(files, self.supervisor)
            wa.exec()
            wa.close()

    def uploadButtonAction(self):
        """create the dialog"""
        up = Upload(self.settings, self.folder_select.folder_edit.text())
        up.exec()
        up.close()

    def judgeButtonAction(self):
        files = self.browser.get_selection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else:
            """create the dialog"""
            ju = Judge(files, self.supervisor)
            ju.exec()
            ju.close()

    def debug(self):
        print("paths")
        print(self.folder_select.folder_memory.paths)
        print("index")
        print(self.folder_select.folder_memory.index)
