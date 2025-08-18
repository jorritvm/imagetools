from PyQt6.QtWidgets import QDialog, QFileDialog

from operations.takeout import takeout_operation
from ui.designer.takeout import Ui_takeout


def handle_takeout(main_window):
    # fetch the UI inputs
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()

    # create the dialog and show it
    dlg = TakeoutDialog(folder_edit_text, parent=main_window)
    dlg.exec()

    # perform follow-up actions after closing
    if dlg.go_to_output:
        folder_select.force_set_directory(dlg.edit_output_path.text())


class TakeoutDialog(QDialog, Ui_takeout):
    def __init__(self, initial_output_folder: str, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edit_output_path.setText(initial_output_folder)
        self.go_to_output = False

        # slots
        self.btn_takeout.clicked.connect(self.start_takeout)
        self.btn_output_select.clicked.connect(
            lambda: self.edit_output_path.setText(
                QFileDialog.getExistingDirectory(self, 'Select Output Folder', self.edit_output_path.text())
            )
        )
        self.btn_input_select.clicked.connect(
            lambda: self.edit_input_path.setText(
                QFileDialog.getOpenFileName(self, 'Select Input File', self.edit_input_path.text(),
                                            "Zip Files (*.zip);;All Files (*)")[0]
            )
        )
        self.btn_close_redirect.clicked.connect(self.on_close_redirect)

    def start_takeout(self):
        def callback(message, progress):
            self.progress_bar.setValue(progress)
            self.text_output.append(message)

        # fetch the input and clean the dialog log textedit
        input_path = self.edit_input_path.text()
        output_path = self.edit_output_path.text()
        self.text_output.clear()
        # call the takeout operation
        return takeout_operation(input_path, output_path, callback)

    def on_close_redirect(self):
        self.go_to_output = True
        self.accept()
