from dataclasses import dataclass

from PyQt6.QtWidgets import QDialog, QFileDialog, QInputDialog

from operations.ftp_upload import ftp_upload_operation
from ui.designer.ftp_upload import Ui_ftp_upload
from ui.settings import SettingsManager

NEW_TAG: str = "<new>"


def handle_ftp_upload(main_window):
    # fetch the UI inputs
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()

    # create the dialog and show it,
    dlg = FtpUploadDialog(folder_edit_text, main_window.settings, main_window)
    dlg.exec()


class FtpUploadDialog(QDialog, Ui_ftp_upload):
    """Dialog for uploading images via FTP. Also manages FTP credential presets."""

    def __init__(self, initial_folder: str, settings: SettingsManager, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edit_folder_path.setText(initial_folder)
        self.settings = settings
        self.current_preset_name: str = NEW_TAG
        self.refresh_preset_data()

        # slots
        self.btn_perform_action.clicked.connect(self.start_operation)
        self.btn_folder_select.clicked.connect(
            lambda: self.edit_folder_path.setText(
                QFileDialog.getExistingDirectory(self, 'Select Images Folder', self.edit_folder_path.text())
            )
        )
        self.btn_close.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.save_preset)
        self.btn_load.clicked.connect(self.load_preset)
        self.btn_delete.clicked.connect(self.delete_preset)

    def start_operation(self):
        self.text_log.clear()

        def callback(message, progress):
            self.progress_bar.setValue(progress)
            self.text_log.append(message)

        ip = self.edit_ip.text()
        port = int(self.spin_port.text())
        user = self.edit_user.text()
        password = self.edit_password.text()
        remote_folder_path = self.edit_remote_folder_path.text()
        source_folder_path = self.edit_folder_path.text()

        ftp_upload_operation(ip, port, user, password, remote_folder_path, source_folder_path, callback)

    def refresh_preset_data(self):
        """Load the values of a saved prest onto the UI fields."""
        # load the list of preset names
        self.combo_preset.clear()
        self.combo_preset.addItem(NEW_TAG)
        for preset in self.settings['ftp_presets'].values():
            self.combo_preset.addItem(preset.name)

        i = self.combo_preset.findText(self.current_preset_name)
        if i > 0:
            self.combo_preset.setCurrentIndex(i)

        # load the specific preset values
        preset_name = self.combo_preset.currentText()
        if preset_name == NEW_TAG:
            self.edit_ip.clear()
            self.spin_port.setValue(21)  # default FTP port
            self.edit_user.clear()
            self.edit_password.clear()
            self.edit_remote_folder_path.clear()
        else:
            preset = self.settings['ftp_presets'][preset_name]
            self.edit_ip.setText(preset.ip)
            self.spin_port.setValue(preset.port)
            self.edit_user.setText(preset.user)
            self.edit_password.setText(preset.password)
            self.edit_remote_folder_path.setText(preset.remote_folder_path)

    def load_preset(self):
        self.current_preset_name = self.combo_preset.currentText()
        self.refresh_preset_data()

    def save_preset(self):
        """Save the current UI field values as a new preset or overwrite an existing one."""
        # decide on the preset name
        preset_name = QInputDialog.getText(self,
                                           'Preset name',
                                           'Give a name for this new preset',
                                           text=self.combo_preset.currentText())[0]
        if preset_name == "":
            return

        # save new preset
        new_preset = FtpPreset(preset_name,
                               self.edit_ip.text(),
                               int(self.spin_port.text()),
                               self.edit_user.text(),
                               self.edit_password.text(),
                               self.edit_remote_folder_path.text())
        self.settings['ftp_presets'][preset_name] = new_preset

        # refresh the combobox
        self.current_preset_name = preset_name
        self.refresh_preset_data()

    def delete_preset(self):
        preset_name = self.combo_preset.currentText()
        if preset_name != NEW_TAG:
            # remove the item from the settings["ftp_presets'] dict that matches the key
            self.settings['ftp_presets'].pop(preset_name)
            self.current_preset_name = NEW_TAG
            self.refresh_preset_data()


@dataclass
class FtpPreset:
    name: str
    ip: str
    port: int
    user: str
    password: str
    remote_folder_path: str
