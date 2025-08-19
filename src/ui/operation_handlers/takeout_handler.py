"""
This operation handler is responsible for the 'takeout' operation
The handle_ function is called from the main window when a button is clicked
It spawns a user dialog to configure the operation, using a separate execution thread because the operation is long-running
It handles the operation termination (closing the dialog) by triggering a main application state refresh
"""
from PyQt6.QtCore import QThread, QObject, pyqtSignal
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
        self.worker_thread = None

        # slots
        self.btn_takeout.clicked.connect(self.start_operation)
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

    def start_operation(self):
        # fetch the input and clean the dialog log textedit
        input_path = self.edit_input_path.text()
        output_path = self.edit_output_path.text()
        self.text_output.clear()

        # create worker + thread
        self.worker_thread = QThread()
        self.worker = TakeoutWorker(input_path, output_path)
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


class TakeoutWorker(QObject):
    """ Worker for the takeout operation to keep UI responsive."""
    progress = pyqtSignal(str, int)  # message, progress
    finished = pyqtSignal()

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        def callback(message, progress):
            self.progress.emit(message, progress)

        # run your heavy function in this thread
        takeout_operation(self.input_path, self.output_path, callback)
        self.finished.emit()
