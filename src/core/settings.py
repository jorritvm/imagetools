import os
import pickle

from PyQt6.QtCore import QSize, QPoint
from PyQt6.QtWidgets import *
from pyprojroot import here
from resources.uipy.settings import Ui_SettingsDialog


class SettingsManager(dict):
    def __init__(self, parent):
        self.parent = parent
        self.load_settings()

    def _create_settings_folder(self):
        """Create the settings folder if it does not exist."""
        fpfn = here("settings")
        try:
            if not fpfn.exists():
                os.makedirs(fpfn, exist_ok=True)
        except OSError as e:
            QMessageBox.critical(self.parent, "ERROR", "There was an error creating the settings folder...")

    def load_settings(self):
        self._create_settings_folder()
        fpfn_settings = here("settings/settings.bin")
        if not fpfn_settings.exists():
            self['n_threads'] = int(os.cpu_count() / 2)
            self['save_thumbs'] = False
            self['default_location'] = "c:/temp"
            self['path'] = ""
            self['image_size'] = 2
            self['app_size'] = QSize(800, 600)
            self['app_pos'] = QPoint(100, 100)
        else:
            try:
                fi = open(fpfn_settings, 'rb')
                self.update(pickle.load(fi))  # merge pure dict in this empty subclassed dict
            finally:
                fi.close()

    def save_settings(self):
        try:
            fpfn = here("settings/settings.bin")
            fcon = open(fpfn, 'wb')
            pickle.dump(self.copy(), fcon)  # only pure dict can be pickled
            flag = True
        except:
            flag = False
            QMessageBox.critical(self.parent, "ERROR", "There was an error saving these settings...")
            os.rename(fpfn, here("settings/settings_broken.bin"))
        finally:
            fcon.close()
        return flag

    def show_settings(self):
        self.settingsDialog = SettingsDialog(self)
        # todo: --- not yet implemented ---
        self.settingsDialog.check_save_thumbs.setDisabled(True)
        self.settingsDialog.label_2.setDisabled(True)
        # ---------------------------
        self.settingsDialog.accepted.connect(self.accept_settings)
        self.settingsDialog.rejected.connect(self.reject_settings)
        self.settingsDialog.exec()

    def accept_settings(self):
        temp = self.settingsDialog.to_dict()
        for key, value in temp.items():
            self[key] = value
        if self.save_settings():
            QMessageBox.warning(self.parent, "Warning", "You must restart Imagetools for changes to take effect...")
        self.settingsDialog.close()

    def reject_settings(self):
        self.settingsDialog.close()


class SettingsDialog(QDialog, Ui_SettingsDialog):

    def __init__(self, values, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.to_dialog(values)  # values is a dict of settings

    def to_dialog(self, values):
        self.box_nthreads.setValue(values['n_threads'])
        self.check_save_thumbs.setChecked(values['save_thumbs'])
        self.edit_root_folder.setText(values['default_location'])

    def to_dict(self):
        values = dict()
        values['n_threads'] = self.box_nthreads.value()
        values['save_thumbs'] = self.check_save_thumbs.isChecked()
        values['default_location'] = self.edit_root_folder.text()
        return values

    def closeEvent(self, ev):
        ev.accept()  # redundant
