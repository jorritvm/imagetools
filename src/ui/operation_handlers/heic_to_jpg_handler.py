from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtWidgets import QDialog, QFileDialog

from operations.heic_to_jpg import heic_to_jpg_operation
from ui.designer.heic_to_jpg import Ui_heic_to_jpg


def handle_heic_to_jpg(main_window):
    # fetch the UI inputs
    folder_select = main_window.folder_select
    folder_edit_text = folder_select.folder_edit.text()

    # create the dialog and show it
    dlg = HeicToJpegDialog(folder_edit_text, parent=main_window)
    dlg.exec()

    # perform follow-up actions after closing
    if dlg.go_to_output:
        folder_select.force_set_directory(dlg.edit_folder_path.text())


class HeicToJpegDialog(QDialog, Ui_heic_to_jpg):
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
        # fetch the input and clean the dialog log textedit
        folder_path = self.edit_folder_path.text()
        self.text_output.clear()

        # create worker + thread
        self.worker_thread = QThread()
        self.worker = HeicToJpegtWorker(folder_path)
        self.worker.moveToThread(self.worker_thread)

        # connect signals
        self.worker.progress.connect(self.on_progress)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        # start background thread
        self.worker_thread.start()

    def on_progress(self, message, progress):
        self.progress_bar.setValue(progress)
        self.text_output.append(message)

    def on_close_redirect(self):
        self.go_to_output = True
        self.accept()


class HeicToJpegtWorker(QObject):
    """ Worker for the takeout operation to keep UI responsive."""
    progress = pyqtSignal(str, int)  # message, progress
    finished = pyqtSignal()

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        def callback(message, progress):
            self.progress.emit(message, progress)

        # run your heavy function in this thread
        heic_to_jpg_operation(self.folder_path, callback)
        self.finished.emit()
