"""
To structure images it is convenient to group them into folders by date.
This script will take all files in a folder and move them into subfolders named by their 'date modified' (=mtime).
For date folders the ISO8601 format is used: YYYY-MM-DD.
"""

import os
from datetime import datetime


def flat_to_tree_operation(folder_path: str, callback) -> None:
    if not os.path.exists(folder_path) and not os.path.isdir(folder_path):
        callback(f"The specified folder does not exist: {folder_path}", 100)
        return

    callback(f"Starting to organize files in {folder_path}", 0)

    folder_contents = os.listdir(folder_path)
    total = len(folder_contents)
    for i, file_name in enumerate(folder_contents):
        file_path = os.path.join(folder_path, file_name)

        # skip dirs
        if not os.path.isfile(file_path):
            continue

        # get the date in the proper format as a string
        timestamp = os.path.getmtime(file_path)
        time = datetime.fromtimestamp(timestamp)
        iso_date = str(time.year) + "-" + str(time.month).zfill(2) + "-" + str(time.day).zfill(2)
        destination_folder_path = os.path.join(folder_path, iso_date)

        # create the destination folder if it does not exist
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)

        # move the file to the destination folder
        destination_file_path = os.path.join(destination_folder_path, file_name)
        callback(f"Moving {file_name} to {iso_date}", int(100 * i / total))
        os.rename(file_path, destination_file_path)

    callback("Finished!", 100)
