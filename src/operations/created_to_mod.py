"""
This operation helps you overwrite the append and modified time of all jpg files in a specified folder of for a
given list of files with their created time.

This is useful for ensuring that the modified time reflects the original creation time.
"""

import os


def created_to_mod_for_folder_path_operation(folder_path: str, callback) -> None:
    if os.path.exists(folder_path):
        callback(f"Storing modified time as created time for all jpg files in folder: {folder_path}", 0)
        list_of_file_names = os.listdir(folder_path)
        list_of_file_paths = [os.path.join(folder_path, file_name) for file_name in list_of_file_names
                              if os.path.isfile(os.path.join(folder_path, file_name))]
        created_to_mod_for_list_of_files_operation(list_of_file_paths, callback)


def created_to_mod_for_list_of_files_operation(list_of_file_paths: list[str], callback) -> None:
    callback("Starting to set modified time as created time for all listed jpg files...", 0)

    total_files = len(list_of_file_paths)
    for i, file_path in enumerate(list_of_file_paths):
        root, ext = os.path.splitext(file_path)

        if ext.lower() == ".jpg":
            ctime = os.path.getctime(file_path)
            os.utime(file_path, (int(ctime), int(ctime)))
            callback("Set modified time as created time for file: " + file_path,
                     int((i + 1) / total_files * 100))

    callback("Finished!", 100)
