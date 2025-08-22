"""
Auto select operation selects images that have not been imported before.
It works closely together with the import images operation.
This is a UI only operation.
"""
import os

from PyQt6.QtWidgets import QMessageBox

from ui.browser import Browser
from ui.folder_select import FolderSelectWidget
from ui.settings import SettingsManager


def handle_auto_select(main_window):
    folder_select: FolderSelectWidget = main_window.folder_select
    browser: Browser = main_window.browser
    settings: SettingsManager = main_window.settings

    # get the current folder path
    folder_path = folder_select.folder_edit.text()
    if folder_path == "":
        return

    # compare files in folder to history of imported files from this folder
    file_names = set(os.listdir(folder_path))
    history = settings['auto_select_history'].get(folder_path, set())

    # get all values in set file_names that are not in set history
    first_time_seen_files = file_names - history

    # update the browser selection
    browser.add_file_names_to_selection(first_time_seen_files)

    # inform the user
    QMessageBox.information(
        main_window,
        "Auto Select",
        f"Auto selected {len(first_time_seen_files)} out of {len(file_names)} files."
    )
