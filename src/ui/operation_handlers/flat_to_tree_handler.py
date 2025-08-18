from PyQt6.QtWidgets import QDialog, QFileDialog

from operations.flat_to_tree import flat_to_tree_operation
from ui.designer.flat_to_tree import Ui_flat_to_tree


def handle_flat_to_tree(main_window):
    # fetch the UI inputs
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()

    # create the dialog and show it,
    dlg = FlatToTreeDialog(folder_edit_text, parent=main_window)
    dlg.exec()

    # perform follow-up actions after closing
    if dlg.go_to_output:
        folder_select.force_set_directory(dlg.edit_folder_path.text())
    else:
        folder_select.force_refresh()


class FlatToTreeDialog(QDialog, Ui_flat_to_tree):
    def __init__(self, initial_folder: str, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edit_folder_path.setText(initial_folder)
        self.go_to_output = False

        # slots
        self.btn_perform_action.clicked.connect(self.start_flat_to_tree)
        self.btn_folder_select.clicked.connect(
            lambda: self.edit_folder_path.setText(
                QFileDialog.getExistingDirectory(self, 'Select Images Folder', self.edit_folder_path.text())
            )
        )
        self.btn_close_redirect.clicked.connect(self.on_close_redirect)

    def start_flat_to_tree(self):
        def callback(message, progress):
            self.progress_bar.setValue(progress)
            self.text_output.append(message)

        # fetch the input and clean the dialog log textedit
        folder_path = self.edit_folder_path.text()
        self.text_output.clear()
        # call the takeout operation
        return flat_to_tree_operation(folder_path, callback)

    def on_close_redirect(self):
        self.go_to_output = True
        self.accept()
