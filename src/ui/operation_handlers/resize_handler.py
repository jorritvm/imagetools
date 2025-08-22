"""
This operation handler is responsible for the 'resize' operation
The handle_ function is called from the main window when a button is clicked
It spawns a user dialog to configure the operation, and execute it
It handles the operation termination (closing the dialog) by triggering a main application state refresh
"""
import os

from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox

from operations.resize import resize_folder_path_operation, resize_list_of_file_paths_operation
from ui.designer.resize import Ui_resize


def handle_resize(main_window):
    # fetch the UI inputs
    browser_selection = main_window.browser.get_selection()
    browser_selection_file_paths = [file_info.absoluteFilePath() for file_info in browser_selection]
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()

    # create the dialog and show it,
    dlg = ResizeDialog(folder_edit_text, browser_selection_file_paths, main_window)
    dlg.exec()

    # perform follow-up actions after closing
    if dlg.go_to_output:
        destination_folder_path = os.path.join(dlg.edit_folder_path.text(), dlg.edit_subfolder_name.text())
        folder_select.force_set_directory(destination_folder_path)
    else:
        folder_select.force_refresh()


class ResizeDialog(QDialog, Ui_resize):
    def __init__(self, initial_folder: str, current_selection: list[str], parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edit_folder_path.setText(initial_folder)
        self.current_selection = current_selection
        self.go_to_output = False

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
        folder_path = self.edit_folder_path.text()
        subfolder_name = self.edit_subfolder_name.text().strip()
        if not subfolder_name:
            subfolder_name = "."
        prefix = self.edit_prefix.text().strip()
        if not prefix:
            prefix = "none"
        suffix = self.edit_suffix.text().strip()
        if not suffix:
            suffix = "none"
        size = self.spin_size.value()
        quality = self.spin_quality.value()

        if self.rd_selected_files_only.isChecked():
            # user selected to process only selected files
            if len(self.current_selection) == 0:
                QMessageBox.warning(self, "No selection", "Create a selection first.")
                return
            resize_list_of_file_paths_operation(self.current_selection,
                                                subfolder_name,
                                                prefix, suffix,
                                                size, quality, callback)
        else:
            # user selected to process entire folder
            resize_folder_path_operation(folder_path,
                                         subfolder_name,
                                         prefix, suffix,
                                         size, quality, callback)

    def on_close_redirect(self):
        self.go_to_output = True
        self.accept()
