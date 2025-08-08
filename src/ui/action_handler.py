from PyQt6.QtWidgets import QMessageBox

from ui.browser import Browser
from ui.folder_select import FolderSelectWidget


class ActionHandler:
    def __init__(self, folder_select: FolderSelectWidget, browser: Browser, action_buttons: dict, parent=None):
        self.folder_select = folder_select
        self.browser = browser
        self.action_buttons = action_buttons
        self.parent = parent
        self.setup_slots()

    def setup_slots(self):
        self.action_buttons['import'].pressed.connect(self.handle_import)
        # self.btn_number.pressed.connect(self.numberButtonAction)
        # self.btn_rename.pressed.connect(self.renameButtonAction)
        # self.btn_resize.pressed.connect(self.resizeButtonAction)
        # self.btn_webalbum.pressed.connect(self.webAlbumButtonAction)
        # self.btn_upload.pressed.connect(self.uploadButtonAction)
        # self.btn_judge.pressed.connect(self.judgeButtonAction)

    def handle_import(self):
        files = self.browser.get_selection()
        if len(files) == 0:
            QMessageBox.warning(self.parent, "No selection", "Create a selection first.")
        else:
            im = ImportImages(files, self.settings, self.folder_select.folder_edit.text())
            if im.exec():
                path = im.get_new_path()
                self.setFolder(path)
            im.close()

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
