"""
This module contains constants used throughout the application.
The usage is straightforward: import the constants you need from this module.
"""

from PyQt6.QtCore import Qt

SETTINGS_FOLDER_NAME: str = "settings"
SETTINGS_FILE_NAME: str = "settings.bin"
INITIAL_WINDOW_WIDTH: int = 1000
INITIAL_WINDOW_HEIGHT: int = 800
INITIAL_WINDOW_POSITION_X: int = 100
INITIAL_WINDOW_POSITION_Y: int = 100
BROWSER_THUMBNAIL_SIZES: list[int] = list(range(50, 750, 50))  # 50px to 700px in steps of 50px
BROWSER_DEFAULT_THUMBNAIL_SIZE: int = 2  # corresponds to 150px in the BROWSER_THUMBNAIL_SIZES list
IMAGE_FILTERS: list[str] = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]  # list of file filters (strings) for image files
THUMBNAIL_SELECTION_COLOR = Qt.GlobalColor.darkCyan  # color used for selected thumbnails in the browser
INITIAL_IMAGES_COUNT_TO_JUDGE: int = 3  # initial number of images to judge in the JudgeDialog
JUDGE_MARKER_A_COLOR = Qt.GlobalColor.green  # color for imaged marked with marker A
JUDGE_MARKER_B_COLOR = Qt.GlobalColor.cyan  # color for images marked with marker B
JUDGE_MARKER_T_COLOR = Qt.GlobalColor.red  # color for images marked with marker T (trash)

JUDGE_FOLDER_NAME_MARKER_A: str = "sel_a"
JUDGE_FOLDER_NAME_MARKER_B: str = "sel_b"
JUDGE_FOLDER_NAME_MARKER_T: str = "trash"
