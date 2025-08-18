"""
Rename manual is a pure UI operation.
As such all of the logic is contained in this module.
There is no separate operation module for the file system operations.
Relies more heavily on PyQt6 QFileInfo and QFile API instead of the Python standard library.
"""

from PyQt6.QtCore import QFileInfo, QFile
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QMessageBox

from threaded_resizer.threaded_resizer import Supervisor, ImageResizeTask
from ui.designer.rename_manual import Ui_rename_manual


def handle_rename_manual(main_window):
    folder_select = main_window.folder_select
    browser_selection: list[QFileInfo] = main_window.browser.get_selection()
    resize_supervisor = main_window.supervisor  # this module will use the same threaded resize as the browser
    if len(browser_selection) == 0:
        QMessageBox.warning(main_window, "No selection", "Create a selection first.")
    else:
        """create the dialog"""
        dlg = RenameManualDialog(browser_selection, resize_supervisor)
        dlg.exec()
        folder_select.force_refresh()


class RenameManualDialog(QDialog, Ui_rename_manual):
    def __init__(self, browser_selection: list[QFileInfo], supervisor: Supervisor, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.files = browser_selection  # QFileInfo objects
        self.supervisor = supervisor  # threaded resizer

        # slots
        self.edit_new_name.textEdited.connect(self.adjust_preview)
        self.edit_separator.textEdited.connect(self.adjust_preview)
        self.spin_skip_left.valueChanged.connect(self.adjust_preview)
        self.btn_save_next.clicked.connect(self.save_next)
        self.btn_skip_next.clicked.connect(self.go_to_next_image)
        self.supervisor.newItemReady.connect(self.display_thumbnail)

        self.image_index = 0
        self.load_image()

    def load_image(self):
        if len(self.files) > 0:
            file_info = self.files[self.image_index]
            self.lbl_old_file_name.setText(file_info.baseName())
            self.lbl_extension.setText(file_info.completeSuffix())
            self.edit_new_name.clear()
            self.edit_new_name.setFocus()
            self.show_thumbnail(file_info)

    def show_thumbnail(self, file_info):
        self.lbl_preview_image.setText("creating preview...")
        request = [ImageResizeTask(file_info, self.height(), True)]  # True for fast transformation mode
        self.reply = self.supervisor.add_items(request, prior=True)  # true for priorty
        self.supervisor.process_queue()

    def display_thumbnail(self, ticket, img):
        # check that the current active file matches the thumbnail reply
        if self.reply[0].ticket == ticket:
            self.lbl_preview_image.setPixmap(QPixmap.fromImage(img))

    def adjust_preview(self):
        """create the virtual new filename and show a preview on the dialog"""
        left_keep = self.spin_skip_left.value()
        old_name = self.lbl_old_file_name.text()
        old_name_keep = old_name[:left_keep]
        separator = self.edit_separator.text()
        new_part = self.edit_new_name.text()
        extension = "." + self.lbl_extension.text()
        new_file_name = old_name_keep + separator + new_part + extension
        self.lbl_preview_file_name.setText(new_file_name)

    def save_next(self):
        """get new filename"""
        new_file_name = self.lbl_preview_file_name.text()

        if new_file_name == '':
            QMessageBox.warning(self, "Invalid filename", "You need to enter a new filename first!")
        else:
            """create file object"""
            file_info = self.files[self.image_index]
            file = QFile(file_info.absoluteFilePath())
            new_file_name = file_info.absolutePath() + "/" + new_file_name

            if file.rename(new_file_name):
                self.go_to_next_image()
            else:
                QMessageBox.warning(self, "Invalid filename", "Rename failed.")

    def go_to_next_image(self):
        new_index = self.image_index + 1
        if new_index >= len(self.files):
            QMessageBox.information(self, "End of selection", "End of selection reached.")
        else:
            self.image_index = new_index
            self.load_image()
