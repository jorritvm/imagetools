"""
Recursively walk trough a folder of combined image/video files and
separate them into subfolders based on their media type.

You can choose to put movies in subfolders, or images in subfolders, or both
"""

import os

OPTIONS = ['images', 'videos', 'both']
IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic']
MOV_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.mpeg', '.mpg']


def separate_media_operation(folder_path: str,
                             move_what_type: str,
                             callback,
                             movie_subfolder_name: str = 'movs',
                             image_subfolder_name: str = 'pics',
                             ):
    if move_what_type.lower() not in OPTIONS:
        callback("move_what_type must be one of 'images', 'videos', or 'both'", 100)
        return

    # recursively walk through the folder and separate files
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if move_what_type.lower() in ['images', 'both'] and is_image(file_name):
                target_folder = os.path.join(root, image_subfolder_name)
            elif move_what_type.lower() in ['videos', 'both'] and is_movie(file_name):
                target_folder = os.path.join(root, movie_subfolder_name)
            else:
                continue

            # create the target folder if it does not exist
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # move the file
            new_file_path = os.path.join(target_folder, file_name)
            if not os.path.exists(new_file_path):
                os.rename(file_path, new_file_path)
                callback(f"Moved {file_name} to {target_folder}", 100)
            else:
                callback(f"File {file_name} already exists in {target_folder}, skipping", 100)
    callback("Finished!", 100)


def is_movie(file_name: str) -> bool:
    """Check if the file is a movie based on its extension."""
    return any(file_name.lower().endswith(ext) for ext in MOV_EXTENSIONS)


def is_image(file_name: str) -> bool:
    """Check if the file is an image based on its extension."""
    return any(file_name.lower().endswith(ext) for ext in IMG_EXTENSIONS)
