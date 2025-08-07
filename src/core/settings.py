import os
import pickle

from PyQt6.QtCore import QSize, QPoint
from PyQt6.QtWidgets import *
from pyprojroot import here

import constants
from resources.uipy.settings import Ui_SettingsDialog


class SettingsManager(dict):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.settings_folder_path = here(constants.SETTINGS_FOLDER_NAME)
        self.create_settings_folder()

        self.settings_file_path = os.path.join(self.settings_folder_path, constants.SETTINGS_FILE_NAME)
        self.load_settings()

    def generate_default_settings(self):
        self['n_threads'] = int(os.cpu_count() / 2)
        self['save_thumbs'] = False
        self['default_location'] = "c:/temp"
        self['path'] = ""
        self['image_size'] = 2
        self['app_size'] = QSize(800, 600)
        self['app_pos'] = QPoint(100, 100)

    def create_settings_folder(self):
        """Create the settings folder if it does not exist."""
        try:
            if not self.settings_folder_path.exists():
                os.makedirs(self.settings_folder_path, exist_ok=True)
        except OSError as e:
            QMessageBox.critical(self.parent, "ERROR", "There was an error creating the settings folder...")

    def load_settings(self):
        if not os.path.exists(self.settings_file_path):
            self.generate_default_settings()
        else:
            try:
                with open(self.settings_file_path, 'rb') as file:
                    self.update(pickle.load(file))  # merge pure dict in this empty subclassed dict
            except Exception as e:
                QMessageBox.critical(self.parent, "ERROR",
                                     "There was an error loading the settings file...\n" +
                                     "Reverting to default settings.\n" +
                                     str(e))
                self.generate_default_settings()

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

    # def closeEvent(self, ev):
    #     ev.accept()  # redundant
