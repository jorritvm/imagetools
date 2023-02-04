import os
import pickle

from PyQt5.QtWidgets import *
# from resources.uipy.settings import *
from pyprojroot import here

from src.resources.uipy.settings import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    
    def __init__(self, values, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.to_dialog(values) #values is a dict of settings
                
    def to_dialog(self, values):
        self.nthreadsBox.setValue(values['n_threads'])
        self.saveThumbsCheck.setChecked(values['saveThumbs'])
        self.rootfolderEdit.setText(values['defaultLocation'])  
    
    def to_dict(self):
        values = dict()
        values['n_threads'] = self.nthreadsBox.value()
        values['saveThumbs'] = self.saveThumbsCheck.isChecked()
        values['defaultLocation'] = self.rootfolderEdit.text() 
        return values
            
    def closeEvent(self, ev):
        ev.accept() #redundant


class SettingsManager(dict):
    def __init__(self, parent):
        self.parent = parent
        self.load_settings()

    def load_settings(self):
        fpfn_settings = here("src/settings/settings.bin")
        if not fpfn_settings.exists():
            self['n_threads'] = int(os.cpu_count() / 2)
            self['saveThumbs'] = False
            self['defaultLocation'] = "c:/temp"
            self['path'] = ""
        else:
            try:
                fi = open(fpfn_settings, 'rb')
                self.update(pickle.load(fi))  # merge pure dict in this empty subclassed dict
            finally:
                fi.close()

    def save_settings(self):
        try:
            fpfn = here("src/settings/settings.bin")
            fcon = open(fpfn, 'wb')
            pickle.dump(self.copy(), fcon)  # only pure dict can be pickled
            flag = True
        except:
            flag = False
            QMessageBox.critical(self.parent, "ERROR", "There was an error saving these settings...")
            os.rename(fpfn, here("src/settings/settings_broken.bin"))
        finally:
            fcon.close()
        return flag

    def show_settings(self):
        self.settingsDialog = SettingsDialog(self)
        # ---
        # not yet implemented
        self.settingsDialog.saveThumbsCheck.setDisabled(True)
        self.settingsDialog.label_2.setDisabled(True)
        # ---
        self.settingsDialog.accepted.connect(self.accept_settings)
        self.settingsDialog.rejected.connect(self.reject_settings)
        self.settingsDialog.exec_()

    def accept_settings(self):
        temp = self.settingsDialog.to_dict()
        for key, value in temp.items():
            self[key] = value
        flag = self.save_settings()
        if flag:
            QMessageBox.warning(self.parent, "Warning", "You must restart Imagetools for changes to take effect...")
        self.settingsDialog.close()

    def reject_settings(self):
        self.settingsDialog.close()


