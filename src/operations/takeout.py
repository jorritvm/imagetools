"""
Google photo users can download a takeout archive of their pictures as a single zip file.
Downloaded files have their 'mtime' modified by google to the time of download which isn't useful for organizing pictures.
Luckily these takeout archives contain a .json file for each picture with the original metadata.
This operation allows you transform that zipfile into a folder of picture with 'mtime' adapted using that json metadata.

input:
- absolute path to a zipfile or a folder containing the unzipped files, or empty string
- absolute path to a folder where the unzipped files should be stored, or already is
- a callback triggered upon every file processed (message: str, progress: int (0-100))

operation & side effects:
- does not delete the original zip file
- will create the required output folder
- will unzip all files in the zip archive
- will read the json files and set the modified time of the corresponding picture files
- will not delete the json files

output:
- the absolute path to the folder where the final files are stored
"""

import json
import os
import shutil


def takeout_operation(takeout_zip_file_path: str, output_folder_path: str, callback) -> str:
    """if it's a zipfile unzip then modify mtime, if it's a folder just modify mtime"""

    # if no zip file is provided, only process the output folder
    if ((not takeout_zip_file_path or takeout_zip_file_path == "None") and
            os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        callback(f"No zip file provided, processing provided output folder: {output_folder_path}", 0)
        modify_mtime(output_folder_path, callback)
        return output_folder_path

    # if a zip file is provided, validate input and perform both unzip and mtime modification
    safe_to_process = True
    if not os.path.exists(takeout_zip_file_path):
        callback(f"The specified input path does not exist: {takeout_zip_file_path}", 100)
        safe_to_process = False
    if os.path.isfile(takeout_zip_file_path) and not takeout_zip_file_path.endswith('.zip'):
        callback(f"The specified input path is not a zip file: {takeout_zip_file_path}", 100)
        safe_to_process = False
    if os.path.isfile(output_folder_path):
        callback(f"The specified output path is a file, not a folder: {output_folder_path}", 100)
        safe_to_process = False
    if os.path.exists(output_folder_path) and os.listdir(output_folder_path):
        callback(f"The specified output folder is not empty: {output_folder_path}", 100)
        safe_to_process = False

    if safe_to_process:
        if not os.path.exists(output_folder_path):
            callback(f"Creating output folder: {output_folder_path}", 0)
            os.makedirs(output_folder_path, exist_ok=True)
        unzip_takeout_files(takeout_zip_file_path, output_folder_path, callback)
        move_all_files_to_output_folder(output_folder_path, callback)
        modify_mtime(output_folder_path, callback)
        return output_folder_path


def unzip_takeout_files(takeout_zip_file_path, output_folder_path, callback):
    """
    Unzips the takeout zip file into the specified output folder.
    If the output folder does not exist, it will be created.
    """
    callback(f"Unzipping {takeout_zip_file_path}", 0)
    shutil.unpack_archive(takeout_zip_file_path, output_folder_path, 'zip')
    callback(f"Unzipped files to {output_folder_path}", 100)


def move_all_files_to_output_folder(output_folder_path, callback):
    """
    All files that have been unzipped will end up in subfolders below output_folder_path.
    They must be moved to the output folder.
    """
    callback(f"Moving all files upward to {output_folder_path}", 0)
    for root, dirs, files in os.walk(output_folder_path, topdown=False):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            destination_file = os.path.join(output_folder_path, file_name)
            if source_file != destination_file:
                shutil.move(source_file, destination_file)
                callback(f"Moved {source_file} to {destination_file}", 0)
        # Remove empty folders except the output folder itself
        if root != output_folder_path and not os.listdir(root):
            os.rmdir(root)
            callback(f"Removed empty folder {root}", 0)
    callback("All files moved to output folder", 100)


def modify_mtime(folder_path, callback):
    """Reads all json files in the specified folder and modifies the mtime of the corresponding picture files"""
    # look up all json files
    all_files = os.listdir(folder_path)
    json_files = list()
    for file_name in all_files:
        root, ext = os.path.splitext(file_name)
        file_name_full = os.path.join(folder_path, file_name)
        if ext.lower() == ".json":
            json_files.append(file_name_full)

    # read json files and make file-modified pairs
    info = dict()
    for json_file in json_files:
        # get image file title
        with open(json_file) as file:
            js = json.load(file)
        key = js["title"]

        # quick hack in case of duplicate filenames which the json does not know!
        if "(1)" in json_file:
            base, ext = os.path.splitext(key)
            key = f"{base}(1){ext}"

        # get timestamp from json
        val = js["photoTakenTime"]["timestamp"]
        info[key] = val

    # set file modified date according to date in json
    total = len(info)
    for i, (key, val) in enumerate(info.items()):
        image_file_path = os.path.join(folder_path, key)

        if os.path.exists(image_file_path):
            # update stats onto the file
            os.utime(image_file_path, (int(val), int(val)))
            callback(f"Changed mtime for {key}", int(100 * i / total))

    callback("Finished!", 100)
