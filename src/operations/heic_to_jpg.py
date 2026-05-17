"""
Iphone pictures are taken in .heic format, which is not supported by many applications.
This operation converts those .heic files into .jpg files while preserving the EXIF data and modified date.
It will also remove the original .heic files.

Iphone live photos also come with an associated .mov or .mp4 file that have the same base name and nearly the same modified time.
This operation will also remove those files.

Summary of workflow:
1. convert all heic in a folder into jpg & keep exif -  #
2. set jpg modified date equal to heic's
3. remove heic
4. remove .mov/.mp4 with same name and nearly same modified time

The operations relies on imagemagick being available on %PATH% (magick.exe)
"""

import datetime
import multiprocessing as mp
import os
import shutil
import subprocess
from typing import Optional

TIME_WINDOW_FOR_LIVE_PHOTO: int = 300  # in seconds, 300 seconds = 5 minutes


def iter_all_files(folder_path: str):
    for current_folder, _, file_names in os.walk(folder_path):
        for file_name in file_names:
            yield current_folder, file_name, os.path.join(current_folder, file_name)


def iter_all_folders(folder_path: str):
    for current_folder, _, file_names in os.walk(folder_path):
        yield current_folder, file_names


def heic_to_jpg_operation(folder_path: str, callback) -> None:
    if not check_if_imagemagick_is_installed(callback):
        return

    if not os.path.isdir(folder_path):
        callback(f"The specified folder does not exist: {folder_path}", 100)
        return

    perform_all_jpg_to_heic_conversion(folder_path, callback)
    copy_stats_to_new_jpg_files(folder_path, callback)
    cleanup_live_files(folder_path, callback)
    cleanup_json_files(folder_path, callback)
    cleanup_heic_files(folder_path, callback)

    callback("Finished!", 100)


def check_if_imagemagick_is_installed(callback):
    callback("Checking availability of imagemagick on your system...", 0)
    if shutil.which("magick") is None:
        callback("Imagemagick is not installed or not found in PATH. Please install it first.", 100)
        return False
    callback("Imagemagick has been found in PATH. Continuing.", 100)
    return True


def perform_all_jpg_to_heic_conversion(folder_path: str, callback) -> None:
    callback("Converting HEIC to JPEG recursively using parallel application of imagemagick..", 0)
    heic_files_to_convert = []
    for _, _, file_path in iter_all_files(folder_path):
        file_path_root, file_name_ext = os.path.splitext(file_path)
        jpg_file = file_path_root + ".jpg"
        if file_name_ext.lower() == ".heic" and not os.path.exists(jpg_file):
            heic_files_to_convert.append(file_path)

    if not heic_files_to_convert:
        return

    with mp.Pool() as pool:
        pool.map(convert_heic_to_jpg, heic_files_to_convert)


def convert_heic_to_jpg(heic_file_path: str) -> None:
    """this is the task performed by any multiprocessing worker, it converts a single heic file to jpg"""
    if heic_file_path.lower().endswith(".heic"):
        pwd = os.getcwd()
        src_folder = os.path.abspath(os.path.dirname(heic_file_path))
        os.chdir(src_folder)
        command = [
            "magick",
            heic_file_path,
            "-set",
            "filename:base",
            "%[basename]",
            "%[filename:base].jpg",
        ]
        subprocess.call(command)
        os.chdir(pwd)


def copy_stats_to_new_jpg_files(folder_path: str, callback) -> None:
    callback("Copying stats to new JPG files...", 33)
    for _, _, file_path in iter_all_files(folder_path):
        file_path_root, file_name_ext = os.path.splitext(file_path)
        if file_name_ext.lower() == ".heic":
            jpg_file = file_path_root + ".jpg"
            if os.path.exists(jpg_file):
                shutil.copystat(file_path, jpg_file)


def cleanup_live_files(folder_path: str, callback) -> None:
    callback("Cleaning up live files (associated MOV/MP4 files)...", 66)
    heic_files = [(current_folder, file_name) for current_folder, file_names in iter_all_folders(folder_path)
                  for file_name in file_names if os.path.splitext(file_name)[1].lower() == ".heic"]
    total = len(heic_files)

    for i, (current_folder, file_name) in enumerate(heic_files, start=1):
        file_path = os.path.join(current_folder, file_name)
        file_path_root, _ = os.path.splitext(file_path)
        sibling_files = os.listdir(current_folder)
        callback(f"Cleaning up live files for: {file_name}", int(100 * i / total))

        # remove the mov_file named exactly like the heic file if it exists and has no associated json
        mov_file_path = file_path_root + ".mov"
        if os.path.exists(mov_file_path):
            # delete_if_within_same_period(os.path.join(flat_folder, jpg_file),
            #                              os.path.join(flat_folder, mov_file))
            delete_if_without_json(mov_file_path, sibling_files)

        # remove the mp4_file named exactly like the heic file if it exists and has no associated json
        mp4_file_path = file_path_root + ".mp4"
        if os.path.exists(mp4_file_path):
            # delete_if_within_same_period(os.path.join(flat_folder, jpg_file),
            #                              os.path.join(flat_folder, mp4_file))
            delete_if_without_json(mp4_file_path, sibling_files)


def cleanup_json_files(folder_path: str, callback) -> None:
    callback("Cleaning up JSON files...", 90)
    all_media_files = [(current_folder, file_name) for current_folder, file_names in iter_all_folders(folder_path)
                       for file_name in file_names if os.path.splitext(file_name)[1].lower() in [".jpg", ".mov", ".png", ".heic", ".mp4"]]
    total = len(all_media_files)

    for i, (current_folder, file_name) in enumerate(all_media_files, start=1):
        sibling_files = os.listdir(current_folder)
        callback(f"Cleaning up JSON files for: {file_name}", int(100 * i / total))
        json_file = find_matching_json(file_name, sibling_files, current_folder)
        if json_file:
            os.remove(json_file)


def cleanup_heic_files(folder_path: str, callback) -> None:
    # remove the heic if the jpg exists
    callback("Cleaning up HEIC files...", 66)
    heic_files = [file_path for _, _, file_path in iter_all_files(folder_path)
                  if os.path.splitext(file_path)[1].lower() == ".heic"]
    total = len(heic_files)
    for i, file_path in enumerate(heic_files, start=1):
        file_path_root, _ = os.path.splitext(file_path)
        callback(f"Cleaning up HEIC file: {os.path.basename(file_path)}", int(100 * i / total))
        jpg_file_path = file_path_root + ".jpg"
        if os.path.exists(jpg_file_path):
            os.remove(file_path)


def find_matching_json(file_name: str, all_files: list[str], folder_path: str) -> Optional[str]:
    """
    Finds the matching json file for a given file name.
    This can be non-trivial because google keeps adding and changing suffixes.
    Eg.
    IMG_9174.MOV                             <--> IMG_9174.MOV.supplemental-metadata.json
    f047a342-32c9-4dba-b40b-b448578b1208.mp4 <--> f047a342-32c9-4dba-b40b-b448578b1208.mp4.suppl.json

    :param file_name: mov, mp4 or jpg file name for which to find a matching json file
    :param all_files: list of all files in the folder
    :param folder_path: path to the folder where the files are located
    :return: the matching json file path if found, otherwise None
    """
    for file_i in all_files:
        if file_i.lower().startswith(file_name.lower()) and file_i.lower().endswith(".json"):
            return os.path.join(folder_path, file_i)
    return None


def delete_if_within_same_period(jpg_file, mov_file):
    """jpg_file, mov_file must be absolute file path"""
    jpg_modified_time = os.path.getmtime(jpg_file)
    mov_modified_time = os.path.getmtime(mov_file)

    jpg_modified_datetime = datetime.datetime.fromtimestamp(jpg_modified_time)
    mov_modified_datetime = datetime.datetime.fromtimestamp(mov_modified_time)

    time_difference = abs(jpg_modified_datetime - mov_modified_datetime)

    if time_difference.total_seconds() <= TIME_WINDOW_FOR_LIVE_PHOTO:
        basename = os.path.basename(mov_file)
        os.remove(mov_file)


def delete_if_without_json(file_path, all_files):
    """mov_file must be absolute file path"""
    file_name = os.path.basename(file_path)
    folder_path = os.path.dirname(file_path)
    json_file = find_matching_json(file_name, all_files, folder_path)
    if not json_file:
        os.remove(file_path)
