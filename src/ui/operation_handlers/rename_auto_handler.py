"""
This operation handler is responsible for the 'rename auto' operation
The handle_ function is called from the main window when a button is clicked
It spawns a user dialog to configure the operation, and execute it
It handles the operation termination (closing the dialog) by triggering a main application state refresh
"""
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox

from operations.rename_auto import rename_auto_for_folder_path_operation, rename_auto_for_list_of_file_paths_operation
from ui.designer.rename_auto import Ui_rename_auto


def handle_rename_auto(main_window):
    # fetch the UI inputs
    browser_selection = main_window.browser.get_selection()
    browser_selection_file_paths = [file_info.absoluteFilePath() for file_info in browser_selection]
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()

    # create the dialog and show it,
    dlg = RenameAutoDialog(folder_edit_text, browser_selection_file_paths, main_window)
    dlg.exec()

    # perform follow-up actions after closing
    if dlg.go_to_output:
        folder_select.force_set_directory(dlg.edit_folder_path.text())
    else:
        folder_select.force_refresh()


class RenameAutoDialog(QDialog, Ui_rename_auto):
    def __init__(self, initial_folder: str, current_selection: list[str], parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edit_folder_path.setText(initial_folder)
        self.go_to_output = False
        self.current_selection = current_selection

        # slots
        self.btn_perform_action.clicked.connect(self.start_operation)
        self.btn_folder_select.clicked.connect(
            lambda: self.edit_folder_path.setText(
                QFileDialog.getExistingDirectory(self, 'Select Images Folder', self.edit_folder_path.text())
            )
        )
        self.btn_close_redirect.clicked.connect(self.on_close_redirect)

    def start_operation(self):
        self.text_output.clear()

        def callback(message, progress):
            self.progress_bar.setValue(progress)
            self.text_output.append(message)

        # call entrypoint for folder or files depending on ui configuration
        new_file_name_template = self.edit_template.text()
        if self.rd_selected_files_only.isChecked():
            # user selected to process only selected files
            if len(self.current_selection) == 0:
                QMessageBox.warning(self, "No selection", "Create a selection first.")
                return
            rename_auto_for_list_of_file_paths_operation(self.current_selection, new_file_name_template, callback)
        else:
            # user selected to process entire folder
            folder_path = self.edit_folder_path.text()
            rename_auto_for_folder_path_operation(folder_path, new_file_name_template, callback)

    def on_close_redirect(self):
        self.go_to_output = True
        self.accept()
