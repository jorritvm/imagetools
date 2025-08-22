"""
Import images facilitates the process of importing images from a device into your library.
Images can be moved or copied.
The processed images will be tracked in the applications memory to facilitate auto-selection later on.
This is a UI only operation, completely packed in this module, there is no CLI or backend operation.
"""
import os
import shutil
from enum import Enum

from PyQt6.QtWidgets import QMessageBox, QDialog, QFileDialog

from ui.designer.import_images import Ui_import_images


class Mode(Enum):
    COPY = 'copy'
    MOVE = 'move'


def handle_import_images(main_window):
    # fetch the UI inputs
    browser_selection = main_window.browser.get_selection()
    browser_selection_file_paths = [file_info.absoluteFilePath() for file_info in browser_selection]
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()
    settings = main_window.settings

    # create the dialog and show it,
    dlg = ImportImagesDialog(folder_edit_text, browser_selection_file_paths, settings, main_window)
    dlg.exec()

    # perform follow-up actions after closing
    if dlg.go_to_output:
        folder_select.force_set_directory(dlg.edit_output_folder_path.text())
    else:
        folder_select.force_refresh()


class ImportImagesDialog(QDialog, Ui_import_images):
    def __init__(self, initial_folder: str, current_selection: list[str], settings, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.current_selection = current_selection
        self.edit_input_folder_path.setText(initial_folder)
        self.settings = settings
        self.go_to_output = False

        # slots
        self.btn_perform_action.clicked.connect(self.start_operation)
        self.btn_input_folder_select.clicked.connect(lambda: self.edit_input_folder_path.setText(
            QFileDialog.getExistingDirectory(self, 'Select Input Images Folder', self.edit_input_folder_path.text())))
        self.btn_output_folder_select.clicked.connect(lambda: self.edit_output_folder_path.setText(
            QFileDialog.getExistingDirectory(self, 'Select Destination Images Folder',
                                             self.edit_input_folder_path.text())))
        self.btn_close_redirect.clicked.connect(self.on_close_redirect)
        self.btn_close.clicked.connect(self.accept)

    def log(self, message: str, progress: int):
        """Log message and update progress bar"""
        self.progress_bar.setValue(progress)
        self.text_output.append(message)

    def start_operation(self):
        # collect parameters
        self.text_output.clear()
        output_folder_path = self.edit_output_folder_path.text()
        if self.rd_copy.isChecked():
            mode = Mode.COPY
        elif self.rd_move.isChecked():
            mode = Mode.MOVE
        else:
            QMessageBox.warning(self, "No mode selected", "Select copy or move.")
            return

        # determine file paths to process
        file_paths = []
        if self.rd_entire_folder.isChecked():
            # list all files in the input folder
            input_folder_path = self.edit_input_folder_path.text()
            file_paths = [os.path.join(input_folder_path, file_name) for file_name in os.listdir(input_folder_path)
                          if os.path.isfile(os.path.join(input_folder_path, file_name))]
        elif self.rd_selected_files_only.isChecked() and len(self.current_selection) > 0:
            file_paths = self.current_selection
        else:
            QMessageBox.warning(self, "No files selected", "Select entire folder or selected files.")

        self.import_images_operation(file_paths, output_folder_path, mode)
        self.mark_processed_for_autoselect(file_paths)

    def import_images_operation(self, file_paths: list[str], output_folder_path: str, mode: Mode):
        self.log("Starting import operation...", 0)
        self.log("Mode: " + mode.value, 0)
        self.log("Destination: " + output_folder_path, 0)

        # create output folder if it doesn't exist
        os.makedirs(output_folder_path, exist_ok=True)

        # move/copy all files
        total_files = len(file_paths)
        for i, file_path in enumerate(file_paths):
            progress = int((i + 1) / total_files * 100)
            file_name = os.path.basename(file_path)
            try:
                new_file_path = os.path.join(output_folder_path, file_name)
                if mode == Mode.COPY:
                    shutil.copy2(file_path, new_file_path)
                    self.log(f"Copied: {file_name}", progress)
                elif mode == Mode.MOVE:
                    shutil.move(file_path, new_file_path)
                    self.log(f"Moved: {file_name}", progress)
            except Exception as e:
                self.log(f"Error handling {file_name}: {str(e)}", progress)

    def mark_processed_for_autoselect(self, file_paths):
        """Update settings to remember processed files for auto-selection"""
        self.log("Marking processed files for auto-select history.", 100)
        for file_path in file_paths:
            folder_path = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            # ensure the folder path exists in history
            if folder_path not in self.settings['auto_select_history']:
                self.settings['auto_select_history'][folder_path] = set()
            self.settings['auto_select_history'][folder_path].add(file_name)

    def on_close_redirect(self):
        self.go_to_output = True
        self.accept()
