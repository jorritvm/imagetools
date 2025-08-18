from PyQt6.QtWidgets import QDialog, QFileDialog

from operations.created_to_mod import created_to_mod_for_folder_path_operation, \
    created_to_mod_for_list_of_files_operation
from ui.designer.created_to_mod import Ui_created_to_mod


def handle_created_to_mod(main_window):
    # fetch the UI inputs
    browser_selection = main_window.browser.get_selection()
    browser_selection_file_paths = [file_info.absoluteFilePath() for file_info in browser_selection]
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()

    # create the dialog and show it,
    dlg = CreatedToModDialog(folder_edit_text, browser_selection_file_paths, main_window)
    dlg.exec()

    # perform follow-up actions after closing
    if dlg.go_to_output:
        folder_select.force_set_directory(dlg.edit_folder_path.text())
    else:
        folder_select.force_refresh()


class CreatedToModDialog(QDialog, Ui_created_to_mod):
    def __init__(self, initial_folder: str, current_selection: list[str], parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edit_folder_path.setText(initial_folder)
        self.go_to_output = False
        self.current_selection = current_selection

        # slots
        self.btn_perform_action.clicked.connect(self.start_created_to_mod)
        self.btn_folder_select.clicked.connect(
            lambda: self.edit_folder_path.setText(
                QFileDialog.getExistingDirectory(self, 'Select Images Folder', self.edit_folder_path.text())
            )
        )
        self.btn_close_redirect.clicked.connect(self.on_close_redirect)

    def start_created_to_mod(self):
        self.text_output.clear()

        def callback(message, progress):
            self.progress_bar.setValue(progress)
            self.text_output.append(message)

        # call entrypoint for folder or files depending on ui configuration

        if self.rd_selected_files_only.isChecked():
            # user selected to process only selected files
            if len(self.current_selection) == 0:
                QMessageBox.warning(self, "No selection", "Create a selection first.")
                return
            created_to_mod_for_list_of_files_operation(self.current_selection, callback)
        else:
            # user selected to process entire folder
            folder_path = self.edit_folder_path.text()
            created_to_mod_for_folder_path_operation(folder_path, callback)

    def on_close_redirect(self):
        self.go_to_output = True
        self.accept()
