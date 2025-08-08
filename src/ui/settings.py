import os
import pickle

from PyQt6.QtCore import QSize, QPoint
from PyQt6.QtWidgets import QDialog, QMessageBox
from pyprojroot import here

from ui import constants
from ui.designer.settings import Ui_SettingsDialog


class SettingsManager(dict):
    """
    SettingsManager is a subclass of dict that manages the UI application settings.

    It adds functionality to load and save settings to a file, and display settings in a dialog.
    If there are problems during loading or saving, it will revert to default settings to avoid crashing the application.

    Note: can't use @pyqtSlot decorator on slots because self is not a QObject (but that's OK)
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.settings_folder_path = here(constants.SETTINGS_FOLDER_NAME)
        self.settings_file_path = os.path.join(self.settings_folder_path, constants.SETTINGS_FILE_NAME)
        self.create_settings_folder()
        self.load_settings()

    def generate_default_settings(self) -> None:
        """Generate default settings. Changes the SettingsManager's state directly."""
        self['n_threads'] = os.cpu_count() - 1
        self['save_thumbs'] = False
        self['default_location'] = "c:/temp"
        self['path'] = ""
        self['image_size'] = 2
        self['app_size'] = QSize(800, 600)
        self['app_position'] = QPoint(100, 100)

    def create_settings_folder(self):
        """Create the settings folder if it does not exist."""
        try:
            if not self.settings_folder_path.exists():
                os.makedirs(self.settings_folder_path, exist_ok=True)
        except OSError as e:
            QMessageBox.critical(self.parent, "ERROR", "There was an error creating the settings folder...")

    def load_settings(self) -> None:
        """
        Load settings from the settings file.
        If the file does not exist, generate default settings.
        Changes the SettingsManager's state directly
        """
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

    def save_settings(self) -> bool:
        """
        Save the current settings to the settings file.
        :return: True if settings were saved, False otherwise.
        """
        try:
            with open(self.settings_file_path, 'wb') as file:
                pickle.dump(self.copy(), file)  # use copy because only pure dict can be serialized with pickle
                flag = True
        except IOError as e:
            QMessageBox.critical(self.parent, "ERROR", "There was an error saving these settings...")
            flag = False
        return flag

    def show_settings_dialog(self, clicked: bool = False) -> None:
        self.settingsDialog = SettingsDialog(self, self.parent)
        self.settingsDialog.accepted.connect(self.accept_settings)
        self.settingsDialog.rejected.connect(self.reject_settings)
        self.settingsDialog.exec()

    def accept_settings(self) -> None:
        temp = self.settingsDialog.to_dict()
        for key, value in temp.items():
            self[key] = value
        if self.save_settings():
            QMessageBox.warning(self.parent, "Warning", "You must restart Imagetools for changes to take effect...")
        self.settingsDialog.close()

    def reject_settings(self) -> None:
        self.settingsDialog.close()


class SettingsDialog(QDialog, Ui_SettingsDialog):
    """
    SettingsDialog is a QDialog that allows the user to view and modify UI application settings.
    """

    def __init__(self, values: SettingsManager, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.to_dialog(values)  # values is a dict of settings

    def to_dialog(self, values: SettingsManager) -> None:
        self.box_nthreads.setValue(values['n_threads'])
        self.check_save_thumbs.setChecked(values['save_thumbs'])
        self.edit_root_folder.setText(values['default_location'])

    def to_dict(self) -> dict:
        values = dict()
        values['n_threads'] = self.box_nthreads.value()
        values['save_thumbs'] = self.check_save_thumbs.isChecked()
        values['default_location'] = self.edit_root_folder.text()
        return values
