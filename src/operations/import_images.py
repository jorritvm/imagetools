from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from resources.uipy.import_images import Ui_Import
import os.path
import shutil


class ImportImages(QDialog, Ui_Import):
    
    def __init__(self, files, settings, root,  parent=None):
        QDialog.__init__(self, parent)
    
        self.files = files
        self.root = root
        self.settings = settings
        self.total = len(self.files)
        self.progress = 0

        self.setupUi(self)
        self.setup_slots()
    
        self.preset_values()
        
        self.fh = FileHandler()
        self.fh.next_done.connect(self.next_done)

    def log(self, txt):
        self.text.append(txt)
        
    def setup_slots(self):
        self.btn_import.clicked.connect(self.start_import)
        self.btn_goto.clicked.connect(self.accept)
        self.btn_folder_select.clicked.connect(self.folder_select)
    
    def preset_values(self):
        tmp = self.files[0].lastModified()
        yyyymmdd = tmp.toString("yyyy-MM-dd")
        x = os.path.normcase(os.path.join(self.settings['default_location'], yyyymmdd))
        self.edit_destination.setText(x)

    def folder_select(self):
        x = QFileDialog.getExistingDirectory(self, 'Select Folder', self.edit_destination.text())
        if x != "":
            self.edit_destination.setText(x)
        
    def update_progress_bar(self):
        self.progress += 1
        x = self.progress / self.total * 100
        self.progress_bar.setValue(x)
        
    def start_import(self):
        self.abort = False
        
        # copy or move?
        mode = ""
        if self.radio_move.isChecked():
            mode = "move"
        if self.radio_copy.isChecked():
            mode = "copy"
        self.log("Mode set to " + mode)
            
        # create the directory
        self.log("Creating main directory..")
        new_path = self.edit_destination.text()
        fi = self.files[0]
        dirp = fi.dir()
        
        if dirp.mkpath(new_path):
            self.log("Directory created...")
        else:
            self.abort = True
            self.log("Creating directory failed...")
                    
        if not self.abort:
            self.mode = mode
            self.manage_files()
    
    def manage_files(self):
        """ send the move/copy command to the filehandler thread
        when it is done, it will give a signal back to next_done
        which will in turn again invoke this method"""
        if len(self.files) > 0:
            fi = self.files.pop()
            destination_dir = self.edit_destination.text()
            
            self.log('Handling ' + fi.fileName())
            self.fh.initialize(fi, destination_dir, self.mode)
            self.fh.start()
        else:
            self.btn_import.setDisabled(True)
            self.log("FINISHED")

    def next_done(self, s):
        self.log(s + " handled..")
        self.update_progress_bar()
        self.manage_files()
        
    def get_new_path(self):
        return self.edit_destination.text()
    
    
class FileHandler(QThread):
    
    next_done = pyqtSignal(str)
    
    def __init__(self,  parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
    
    def initialize(self, fi, destination_dir, mode):
        self.fi = fi
        self.destination_dir = destination_dir
        self.mode = mode

    def run(self):
        fi = self.fi
        fi_old = fi.absoluteFilePath()
        fi_new = QFileInfo(QDir(self.destination_dir), fi.fileName()).absoluteFilePath()

        if self.mode == "copy":
            shutil.copy2(fi_old, fi_new)
        if self.mode == "move":
            shutil.move(fi_old, fi_new)

        self.next_done.emit(fi.fileName())
