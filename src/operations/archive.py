"""
The archive operation will zip subfolders in the current folder if the zip files don't exist yet.
No version check will occur. If the subfolder was updated but the zip file already exists, it will be skipped.
"""

import os
from zipfile import ZipFile, ZIP_STORED


def archive_operation(folder_path: str, callback) -> None:
    """Archives subfolders in the specified folder into zip files."""
    callback("Starting archive operation...", 0)
    entries = os.listdir(folder_path)
    list_of_folder_names = [d for d in entries if os.path.isdir(os.path.join(folder_path, d))]
    list_of_file_names = [f for f in entries if os.path.isfile(os.path.join(folder_path, f))]

    total = len(list_of_folder_names)
    for i, folder_name in enumerate(list_of_folder_names):
        zip_file_name = folder_name + '.zip'
        if zip_file_name in list_of_file_names:
            callback(f"Skipping folder: {folder_name}", int((i / total) * 100))
        else:
            callback(f"Archiving folder: {folder_name}", int((i / total) * 100))
            zip_file_path = os.path.join(folder_path, zip_file_name)
            source_folder_path = os.path.join(folder_path, folder_name)

            with ZipFile(zip_file_path, 'w', ZIP_STORED, True) as zip_file:
                zip_folder_to_zipfile(source_folder_path, zip_file)

    callback("Finished.", 100)


def zip_folder_to_zipfile(folder_path, zip_file: ZipFile) -> None:
    """Recursively adds a folder and its contents to a ZipFile, preserving folder structure."""
    top_folder_name = os.path.basename(folder_path)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            abs_path = os.path.join(root, file)
            # Make the arcname relative, starting with the top folder name
            archive_name = os.path.join(top_folder_name, os.path.relpath(abs_path, folder_path))
            zip_file.write(abs_path, arcname=archive_name)
