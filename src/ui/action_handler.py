from PyQt6.QtWidgets import QDialog, QFileDialog

from operations.heic_to_jpg import heic_to_jpg_operation
from operations.takeout import takeout_operation
from ui.browser import Browser
from ui.designer.heic_to_jpg import Ui_heic_to_jpg
from ui.designer.takeout import Ui_takeout
from ui.folder_select import FolderSelectWidget


class ActionHandler:
    def __init__(self, folder_select: FolderSelectWidget, browser: Browser, action_buttons: dict, parent=None):
        self.folder_select = folder_select
        self.browser = browser
        self.action_buttons = action_buttons
        self.parent = parent
        self.setup_slots()

    def setup_slots(self):
        self.action_buttons['takeout'].pressed.connect(self.handle_takeout)
        self.action_buttons['heic_to_jpg'].released.connect(self.handle_heic_to_jpg)
        # self.btn_number.pressed.connect(self.numberButtonAction)
        # self.btn_rename.pressed.connect(self.renameButtonAction)
        # self.btn_resize.pressed.connect(self.resizeButtonAction)
        # self.btn_webalbum.pressed.connect(self.webAlbumButtonAction)
        # self.btn_upload.pressed.connect(self.uploadButtonAction)
        # self.btn_judge.pressed.connect(self.judgeButtonAction)

    def handle_takeout(self):
        # define a wrapper class for the dialog
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

        # create the dialog and show it,
        dlg = TakeoutDialog(self.folder_select.folder_edit.text(), self.parent)
        dlg.exec()
        # perform follow-up actions after closing
        if dlg.go_to_output:
            self.folder_select.force_set_directory(dlg.edit_output_path.text())

    def handle_heic_to_jpg(self):
        # define a wrapper class for the dialog
        class HeicToJpegDialog(QDialog, Ui_heic_to_jpg):
            def __init__(self, initial_folder: str, parent=None):
                QDialog.__init__(self, parent)
                self.setupUi(self)
                self.edit_folder_path.setText(initial_folder)
                self.go_to_output = False

                # slots
                self.btn_perform_action.clicked.connect(self.start_heic_to_jpg)
                self.btn_folder_select.clicked.connect(
                    lambda: self.edit_folder_path.setText(
                        QFileDialog.getExistingDirectory(self, 'Select Images Folder', self.edit_folder_path.text())
                    )
                )
                self.btn_close_redirect.clicked.connect(self.on_close_redirect)

            def start_heic_to_jpg(self):
                def callback(message, progress):
                    self.progress_bar.setValue(progress)
                    self.text_output.append(message)

                # fetch the input and clean the dialog log textedit
                folder_path = self.edit_folder_path.text()
                self.text_output.clear()
                # call the takeout operation
                return heic_to_jpg_operation(folder_path, callback)

            def on_close_redirect(self):
                self.go_to_output = True
                self.accept()

        # create the dialog and show it,
        dlg = HeicToJpegDialog(self.folder_select.folder_edit.text(), self.parent)
        dlg.exec()
        # perform follow-up actions after closing
        if dlg.go_to_output:
            self.folder_select.force_set_directory(dlg.edit_folder_path.text())

    # def handle_import(self):
    #     files = self.browser.get_selection()
    #     if len(files) == 0:
    #         QMessageBox.warning(self.parent, "No selection", "Create a selection first.")
    #     else:
    #         im = ImportImages(files, self.settings, self.folder_select.folder_edit.text())
    #         if im.exec():
    #             path = im.get_new_path()
    #             self.setFolder(path)
    #         im.close()

    # def numberButtonAction(self):
    #     files = self.browser.get_selection()
    #     if len(files) == 0:
    #         QMessageBox.warning(self, "No selection", "Create a selection first.")
    #     else:
    #         """create the dialog and extract the user's settings"""
    #         num = Number()
    #         if num.exec():
    #             settings = num.get_settings()
    #             track_changes = num.rename_files(files, settings)
    #             self.browser.update_elements(track_changes)
    #             num.close()
    #
    # def renameButtonAction(self):
    #     files = self.browser.get_selection()
    #     if len(files) == 0:
    #         QMessageBox.warning(self, "No selection", "Create a selection first.")
    #     else:
    #         """create the dialog"""
    #         ren = Rename(files, self.supervisor)
    #         ren.exec()
    #         ren.close()
    #
    #         """the dialog is ready now, we should update the application with the new filenames"""
    #         trackChanges = ren.getChanges()
    #         self.browser.update_elements(trackChanges)
    #
    # def resizeButtonAction(self):
    #     files = self.browser.get_selection()
    #     if len(files) == 0:
    #         QMessageBox.warning(self, "No selection", "Create a selection first.")
    #     else:
    #         """create the dialog"""
    #         res = Resize(files, self.supervisor, self.folder_select.folder_edit.text())
    #         res.exec()
    #         x = self.folder_select.folder_edit.text()
    #         res.close()
    #
    # def webAlbumButtonAction(self):
    #     files = self.browser.get_selection()
    #     if len(files) == 0:
    #         QMessageBox.warning(self, "No selection", "Create a selection first.")
    #     else:
    #         """create the dialog"""
    #         wa = WebAlbum(files, self.supervisor)
    #         wa.exec()
    #         wa.close()
    #
    # def uploadButtonAction(self):
    #     """create the dialog"""
    #     up = Upload(self.settings, self.folder_select.folder_edit.text())
    #     up.exec()
    #     up.close()
    #
    # def judgeButtonAction(self):
    #     files = self.browser.get_selection()
    #     if len(files) == 0:
    #         QMessageBox.warning(self, "No selection", "Create a selection first.")
    #     else:
    #         """create the dialog"""
    #         ju = Judge(files, self.supervisor)
    #         ju.exec()
    #         ju.close()
