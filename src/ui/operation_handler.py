"""This module links the UI operation button presses to the correct operation handler."""

from ui import main_window
from ui.operation_handlers.auto_select_handler import handle_auto_select
from ui.operation_handlers.created_to_mod_handler import handle_created_to_mod
from ui.operation_handlers.flat_to_tree_handler import handle_flat_to_tree
from ui.operation_handlers.ftp_upload_handler import handle_ftp_upload
from ui.operation_handlers.harvest_metadata_handler import handle_harvest_metadata
from ui.operation_handlers.heic_to_jpg_handler import handle_heic_to_jpg
from ui.operation_handlers.import_images import handle_import_images
from ui.operation_handlers.judge_handler import handle_judge
from ui.operation_handlers.rename_auto_handler import handle_rename_auto
from ui.operation_handlers.rename_manual_handler import handle_rename_manual
from ui.operation_handlers.resize_handler import handle_resize
from ui.operation_handlers.separate_media_handler import handle_separate_media
from ui.operation_handlers.takeout_handler import handle_takeout
from ui.operation_handlers.web_album_handler import handle_web_album


class OperationHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.btns = main_window.operation_buttons
        self.setup_slots()

    def setup_slots(self):
        self.btns['auto_select'].pressed.connect(lambda: handle_auto_select(self.main_window))
        self.btns['import_images'].pressed.connect(lambda: handle_import_images(self.main_window))
        self.btns['takeout'].pressed.connect(lambda: handle_takeout(self.main_window))
        self.btns['heic_to_jpg'].released.connect(lambda: handle_heic_to_jpg(main_window))
        self.btns['flat_to_tree'].released.connect(lambda: handle_flat_to_tree(self.main_window))
        self.btns['created_to_mod'].released.connect(lambda: handle_created_to_mod(self.main_window))
        self.btns['harvest_metadata'].released.connect(lambda: handle_harvest_metadata(self.main_window))
        self.btns['rename_auto'].released.connect(lambda: handle_rename_auto(self.main_window))
        self.btns['rename_manual'].released.connect(lambda: handle_rename_manual(self.main_window))
        self.btns['separate_media'].released.connect(lambda: handle_separate_media(self.main_window))
        self.btns['judge'].released.connect(lambda: handle_judge(self.main_window))
        self.btns['resize'].released.connect(lambda: handle_resize(self.main_window))
        self.btns['web_album'].released.connect(lambda: handle_web_album(self.main_window))
        self.btns['ftp_upload'].released.connect(lambda: handle_ftp_upload(self.main_window))
        self.btns['import_images'].released.connect(lambda: handle_import_images(self.main_window))
