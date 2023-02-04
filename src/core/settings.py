from PyQt5.QtWidgets import *
from resources.uipy.settings import *
from pyprojroot import here
import pickle

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


class SettingsManager():

    def __init__:
        pass

    def get_settings(self):
        values = dict()
        fpfn_settings = here("src/settings/settings.bin")
        if not fpfn_settings.exists():
            values['n_threads'] = int(os.cpu_count() / 2)
            values['saveThumbs'] = False
            values['defaultLocation'] = "c:/temp"
            values['path'] = ""
        else:
            try:
                fi = open(fpfn_settings, 'rb')
                values = pickle.load(fi)
            finally:
                fi.close()
        return values

    def save_settings(self):
        try:
            fi = open(here("src/settings/settings.bin"), 'wb')
            pickle.dump(self.settings, fi)
            flag = True
        except:
            flag = False
            QMessageBox.critical(self, "ERROR", "There was an error saving these settings...")
        finally:
            fi.close()

        return flag

    def show_settings(self):
        self.settingsDialog = SettingsDialog(self.settings)
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
            self.settings[key] = value
        flag = self.save_settings()
        if flag:
            QMessageBox.warning(self, "Warning", "You must restart Imagetools for changes to take effect...")
        self.settingsDialog.close()

    def reject_settings(self):
        self.settingsDialog.close()