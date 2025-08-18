# from operations.created_to_mod import created_to_mod_for_folder_path_operation, \
#     created_to_mod_for_list_of_files_operation
# from operations.flat_to_tree import flat_to_tree_operation
# from operations.heic_to_jpg import heic_to_jpg_operation
# from ui.designer.created_to_mod import Ui_created_to_mod
# from ui.designer.flat_to_tree import Ui_flat_to_tree
# from ui.folder_select import FolderSelectWidget

import ui.operation_handlers.created_to_mod_handler as created_to_mod_handler
import ui.operation_handlers.flat_to_tree_handler as flat_to_tree_handler
import ui.operation_handlers.heic_to_jpg_handler as heic_to_jpg_handler
import ui.operation_handlers.takeout_handler as takeout_handler


class OperationHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.operation_buttons = main_window.operation_buttons
        self.setup_slots()

    def setup_slots(self):
        self.operation_buttons['takeout'].pressed.connect(self.handle_takeout)
        self.operation_buttons['heic_to_jpg'].released.connect(self.handle_heic_to_jpg)
        self.operation_buttons['flat_to_tree'].released.connect(self.handle_flat_to_tree)
        self.operation_buttons['created_to_mod'].released.connect(self.handle_created_to_mod)
        # self.btn_number.pressed.connect(self.numberButtonAction)
        # self.btn_rename.pressed.connect(self.renameButtonAction)
        # self.btn_resize.pressed.connect(self.resizeButtonAction)
        # self.btn_webalbum.pressed.connect(self.webAlbumButtonAction)
        # self.btn_upload.pressed.connect(self.uploadButtonAction)
        # self.btn_judge.pressed.connect(self.judgeButtonAction)

    def handle_takeout(self):
        takeout_handler.handle_takeout(self.main_window)

    def handle_heic_to_jpg(self):
        heic_to_jpg_handler.handle_heic_to_jpg(self.main_window)

    def handle_flat_to_tree(self):
        flat_to_tree_handler.handle_flat_to_tree(self.main_window)

    def handle_created_to_mod(self):
        created_to_mod_handler.handle_created_to_mod(self.main_window)

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
