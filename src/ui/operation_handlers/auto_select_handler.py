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

    # Get the current folder path
    folder_path = folder_select.folder_edit.text()
    if folder_path == "":
        return

    # Get both sets of file names: the folder and the folder history
    file_names = set(os.listdir(folder_path))
    history = settings['auto_select_history'].get(folder_path, set())

    # Clean up history: remove files no longer in the folder
    history.intersection_update(file_names)

    # Select files not yet in history
    first_time_seen_files = file_names - history
    browser.add_file_names_to_selection(first_time_seen_files)

    # inform the user
    QMessageBox.information(
        main_window,
        "Auto Select",
        f"Auto selected {len(first_time_seen_files)} out of {len(file_names)} files."
    )
