from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox

from operations.created_to_mod import created_to_mod_for_folder_path_operation, \
    created_to_mod_for_list_of_files_operation
from operations.flat_to_tree import flat_to_tree_operation
from operations.heic_to_jpg import heic_to_jpg_operation
from operations.takeout import takeout_operation
from ui.browser import Browser
from ui.designer.created_to_mod import Ui_created_to_mod
from ui.designer.flat_to_tree import Ui_flat_to_tree
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
        self.action_buttons['flat_to_tree'].released.connect(self.handle_flat_to_tree)
        self.action_buttons['created_to_mod'].released.connect(self.handle_created_to_mod)
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

    def handle_flat_to_tree(self):
        # define a wrapper class for the dialog
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

        # create the dialog and show it,
        dlg = FlatToTreeDialog(self.folder_select.folder_edit.text(), self.parent)
        dlg.exec()
        # perform follow-up actions after closing
        if dlg.go_to_output:
            self.folder_select.force_set_directory(dlg.edit_folder_path.text())
        else:
            self.folder_select.force_refresh()

    def handle_created_to_mod(self):
        # define a wrapper class for the dialog
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

        # create the dialog and show it,
        current_selection = [file_info.absoluteFilePath() for file_info in self.browser.get_selection()]
        dlg = CreatedToModDialog(self.folder_select.folder_edit.text(), current_selection, self.parent)
        dlg.exec()
        # perform follow-up actions after closing
        if dlg.go_to_output:
            self.folder_select.force_set_directory(dlg.edit_folder_path.text())
        else:
            self.folder_select.force_refresh()

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
