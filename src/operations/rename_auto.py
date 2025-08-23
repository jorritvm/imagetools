"""
this operations helps you rename all files in a specified folder in an automated way.

the new file name is defined using a template string that can contain tags.
- you can add a sequence number based on the file name or the file modified time in different length using tags:
$seq_alpha_1, $seq_alpha_2, $seq_alpha_3 ,$seq_alpha_4, $seq_alpha_5
$seq_mtime_1, $seq_mtime_2, $seq_mtime_3 ,$seq_mtime_4, $seq_mtime_5

- you can add the file name without extension using the tag $name

- you can different representation of the mtime:
$mtime_date gives you the modified time as yyyymmdd
$mtime_date_sep gives you the modified time as yyyy-mm-dd
- you can different representation of the mtime:
$mtime_time gives you the modified time as hhmmss
$mtime_time_sep gives you the modified time as hh-mm-ss


- you can add the file extension using the tag $ext

- you can add a fixed piece of text anywhere in the new template without using any tags, just write it as is.
"""
import os
from datetime import datetime


def rename_auto_for_folder_path_operation(folder_path: str, new_file_name_template: str, callback):
    callback(f"Starting an auto rename action for folder: {folder_path}", 0)
    list_of_file_names = os.listdir(folder_path)
    list_of_file_paths = [os.path.join(folder_path, file_name) for file_name in list_of_file_names
                          if os.path.isfile(os.path.join(folder_path, file_name))]
    rename_auto_for_list_of_file_paths_operation(list_of_file_paths, new_file_name_template, callback)


def rename_auto_for_list_of_file_paths_operation(list_of_file_paths: list[str], new_file_name_template: str, callback):
    callback("Starting to rename files...", 0)
    total_files = len(list_of_file_paths)

    alpha_seq = create_alphabetical_sequence(list_of_file_paths)
    mtime_seq = create_mtime_sequence(list_of_file_paths)

    for i, file_path in enumerate(list_of_file_paths):
        # resolve the tags
        folder_path = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        mtime_float = os.path.getmtime(file_path)
        mtime_tags = breakdown_mtime(mtime_float)

        # template variable substitution
        new_file_name = new_file_name_template
        new_file_name = new_file_name.replace("$name", name)
        new_file_name = new_file_name.replace("$ext", ext)
        new_file_name = new_file_name.replace("$mtime_date_sep", mtime_tags['mtime_date_sep'])
        new_file_name = new_file_name.replace("$mtime_date", mtime_tags['mtime_date'])
        new_file_name = new_file_name.replace("$mtime_time_sep", mtime_tags['mtime_time_sep'])
        new_file_name = new_file_name.replace("$mtime_time", mtime_tags['mtime_time'])
        new_file_name = new_file_name.replace("$seq_alpha_1", f"{alpha_seq[file_path]:01d}")
        new_file_name = new_file_name.replace("$seq_alpha_2", f"{alpha_seq[file_path]:02d}")
        new_file_name = new_file_name.replace("$seq_alpha_3", f"{alpha_seq[file_path]:03d}")
        new_file_name = new_file_name.replace("$seq_alpha_4", f"{alpha_seq[file_path]:04d}")
        new_file_name = new_file_name.replace("$seq_alpha_5", f"{alpha_seq[file_path]:05d}")
        new_file_name = new_file_name.replace("$seq_mtime_1", f"{mtime_seq[file_path]:01d}")
        new_file_name = new_file_name.replace("$seq_mtime_2", f"{mtime_seq[file_path]:02d}")
        new_file_name = new_file_name.replace("$seq_mtime_3", f"{mtime_seq[file_path]:03d}")
        new_file_name = new_file_name.replace("$seq_mtime_4", f"{mtime_seq[file_path]:04d}")
        new_file_name = new_file_name.replace("$seq_mtime_5", f"{mtime_seq[file_path]:05d}")

        # create the new file path
        new_file_path = os.path.join(folder_path, new_file_name)
        # rename the file
        callback(f"Renaming {file_name} to {new_file_name}", int((i + 1) / total_files * 100))
        os.rename(file_path, new_file_path)

    callback("Finished!", 100)


def breakdown_mtime(mtime: float) -> dict[str, str]:
    """Break down the mtime into different formats."""
    mtime_dt = datetime.fromtimestamp(mtime)
    mtime_date = mtime_dt.strftime("%Y%m%d")
    mtime_date_sep = mtime_dt.strftime("%Y-%m-%d")
    mtime_time = mtime_dt.strftime("%H%M%S")
    mtime_time_sep = mtime_dt.strftime("%H-%M-%S")
    return {
        'mtime_date': mtime_date,
        'mtime_date_sep': mtime_date_sep,
        'mtime_time': mtime_time,
        'mtime_time_sep': mtime_time_sep
    }


def create_alphabetical_sequence(list_of_file_paths: list[str]) -> dict[str, int]:
    """
    Create an alphabetical sequence based on the file names starting at 1. The sequence is reset for each folder.
    """
    sorted_files = sorted(list_of_file_paths)
    return create_sequence(sorted_files)


def create_mtime_sequence(list_of_file_paths: list[str]) -> dict[str, int]:
    """
    Create a sequence based on the modified time of the files starting at 1. The sequence is reset for each folder.
    """

    # separate the list of file_paths into a dict of lists, where every key is a folder
    folder_dict = dict()
    for file_path in list_of_file_paths:
        folder_path = os.path.dirname(file_path)
        folder_dict.setdefault(folder_path, []).append(file_path)

    # then sort each of these dict items by mtime
    for folder_path, files in folder_dict.items():
        folder_dict[folder_path] = sorted(files, key=lambda x: os.path.getmtime(x))

    # then put these items together into a single list again
    sorted_files = []
    for folder_path, files in folder_dict.items():
        sorted_files.extend(files)

    # finally create the sequence based on the sorted files
    return create_sequence(sorted_files)


def create_sequence(sorted_files: list[str]) -> dict[str, int]:
    sequence = dict()
    folder_seq_counter = 1
    previous_folder = None
    for file_path in sorted_files:
        folder_path = os.path.dirname(file_path)
        # if we are in a new folder, reset the sequence counter
        if previous_folder is None or folder_path != previous_folder:
            folder_seq_counter = 1
        sequence[file_path] = folder_seq_counter
        # increment the sequence counter
        folder_seq_counter += 1
        previous_folder = folder_path
    return sequence
