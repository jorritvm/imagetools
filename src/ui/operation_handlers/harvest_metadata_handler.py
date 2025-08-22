from PyQt6.QtWidgets import QMessageBox


def handle_harvest_metadata(main_window):
    QMessageBox.warning(
        main_window,
        "Harvest Metadata",
        "Due to recent changes in the Google API, this feature is currently unavailable."
    )
