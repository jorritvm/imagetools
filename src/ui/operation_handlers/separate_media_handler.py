from PyQt6.QtWidgets import QDialog, QFileDialog

from operations.separate_media import separate_media_operation
from ui.designer.separate_media import Ui_separate_media


def handle_separate_media(main_window):
    # fetch the UI inputs
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()

    # create the dialog and show it,
    dlg = SeparateMediaDialog(folder_edit_text, main_window)
    dlg.exec()

    # perform follow-up actions after closing
    if dlg.go_to_output:
        folder_select.force_set_directory(dlg.edit_folder_path.text())
    else:
        folder_select.force_refresh()


class SeparateMediaDialog(QDialog, Ui_separate_media):
    def __init__(self, initial_folder: str, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edit_folder_path.setText(initial_folder)
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
        move_what = None
        if self.rd_both.isChecked():
            move_what = "both"
        elif self.rd_images.isChecked():
            move_what = "images"
        elif self.rd_videos.isChecked():
            move_what = "videos"
        image_subfolder_name = self.edit_image_subfolder_name.text()
        video_subfolder_name = self.edit_video_subfolder_name.text()

        separate_media_operation(folder_path,
                                 move_what,
                                 callback,
                                 video_subfolder_name,
                                 image_subfolder_name)

    def on_close_redirect(self):
        self.go_to_output = True
        self.accept()
