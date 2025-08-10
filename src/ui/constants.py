"""
This module contains constants used throughout the application.
The usage is straightforward: import the constants you need from this module.
"""
SETTINGS_FOLDER_NAME: str = "settings"
SETTINGS_FILE_NAME: str = "settings.bin"
INITIAL_WINDOW_WIDTH: int = 1000
INITIAL_WINDOW_HEIGHT: int = 800
INITIAL_WINDOW_POSITION_X: int = 100
INITIAL_WINDOW_POSITION_Y: int = 100
BROWSER_THUMBNAIL_SIZES: list[int] = list(range(50, 750, 50))  # 50px to 700px in steps of 50px
BROWSER_DEFAULT_THUMBNAIL_SIZE: int = 2  # corresponds to 150px in the BROWSER_THUMBNAIL_SIZES list
IMAGE_FILTERS = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]  # list of file filters (strings) for image files
