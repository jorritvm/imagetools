from PyQt6.QtWidgets import QMessageBox

import ui.operation_handlers.created_to_mod_handler as created_to_mod_handler
import ui.operation_handlers.flat_to_tree_handler as flat_to_tree_handler
import ui.operation_handlers.heic_to_jpg_handler as heic_to_jpg_handler
import ui.operation_handlers.rename_auto_handler as rename_auto_handler
import ui.operation_handlers.rename_manual_handler as rename_manual_handler
import ui.operation_handlers.separate_media_handler as separate_media_handler
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
        self.operation_buttons['harvest_metadata'].released.connect(self.handle_harvest_metadata)
        self.operation_buttons['rename_auto'].released.connect(self.handle_rename_auto)
        self.operation_buttons['rename_manual'].released.connect(self.handle_rename_manual)
        self.operation_buttons['separate_media'].released.connect(self.handle_separate_media)

    def handle_takeout(self):
        takeout_handler.handle_takeout(self.main_window)

    def handle_heic_to_jpg(self):
        heic_to_jpg_handler.handle_heic_to_jpg(self.main_window)

    def handle_flat_to_tree(self):
        flat_to_tree_handler.handle_flat_to_tree(self.main_window)

    def handle_created_to_mod(self):
        created_to_mod_handler.handle_created_to_mod(self.main_window)

    def handle_harvest_metadata(self):
        QMessageBox.warning(
            self.main_window,
            "Harvest Metadata",
            "Due to recent changes in the Google API, this feature is currently unavailable."
        )

    def handle_rename_auto(self):
        rename_auto_handler.handle_rename_auto(self.main_window)

    def handle_rename_manual(self):
        rename_manual_handler.handle_rename_manual(self.main_window)

    def handle_separate_media(self):
        separate_media_handler.handle_separate_media(self.main_window)

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

    #

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
