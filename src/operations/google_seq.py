"""
The google seq operation ensures your pictures are shown in the same order in google photos as on your local system.

Details:
- online photo albums dont sort by name but by date taken, and if that does not exist they use mtime
- if the file names indicate the correct sequence, this operation will overwrite the mtime and remove the exif date taken to respect that sequence
- warning: the original mtime will be lost
"""

import os

from PIL import Image


def google_seq_operation(folder_path: str, callback) -> None:
    """Adjusts file metadata to ensure correct sequence in Google Photos."""
    callback("Starting google_seq operation...", 0)

    # Ensure the folder exists
    if not os.path.isdir(folder_path):
        callback(f"Error: '{folder_path}' is not a valid directory.", 100)
        return

    # List all files in the folder, sorted alphabetically
    list_of_file_names = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
                                key=lambda x: x.lower())
    if not list_of_file_names:
        callback(f"No files found in the directory '{folder_path}'.", 100)
        return

    # Get the mtime of the first file
    first_file_path = os.path.join(folder_path, list_of_file_names[0])
    base_mtime = os.path.getmtime(first_file_path)

    # Update mtime for each file, incrementing by 1 second
    total = len(list_of_file_names)
    for index, file_name in enumerate(list_of_file_names):
        try:
            file_path = os.path.join(folder_path, file_name)
            remove_exif(file_path)
            new_mtime = base_mtime + index
            os.utime(file_path, (new_mtime, new_mtime))
            callback(f"Modified {file_name}", int((index / total) * 100))
        except OSError:
            callback(f"Error modifying file: {file_name}", int((index / total) * 100))

    callback("Finished.", 100)


def remove_exif(file_path):
    """Removes EXIF metadata from a JPEG file."""
    if not file_path.lower().endswith(('.jpg', '.jpeg')):
        return
    try:
        with Image.open(file_path) as img:
            img_no_exif = Image.new(img.mode, img.size)
            img_no_exif.paste(img)
            img_no_exif.save(file_path, "jpeg")
    except Exception as e:
        raise e
