"""
the ftp upload operations uploads an entire folder to an FTP.
- no support for TLS yet
"""

import os
from ftplib import FTP


def ftp_upload_operation(ip: str, port: int, user: str, password: str, destination_folder_name: str,
                         source_folder_path: str, callback) -> None:
    """Uploads an entire folder to an FTP server."""
    # verify if folder_to_upload exists and is a directory
    if not os.path.isdir(source_folder_path):
        callback(f"The folder to upload '{source_folder_path}' does not exist or is not a directory.", 100)
        return

    # connect to the FTP server
    callback("Connecting to FTP server...", 0)
    ftp = FTP()
    ftp.connect(ip, port)
    ftp.login(user, password)

    # Ensure the target directory exists, create it if necessary (including nested folders), and move to it
    callback("Creating the target directory on the server...", 0)
    folders = destination_folder_name.strip('/').split('/')
    for folder in folders:
        try:
            ftp.cwd(folder)
        except Exception:
            ftp.mkd(folder)
            ftp.cwd(folder)

    # Walk through the local folder and upload files, creating subfolders as needed
    total = get_file_count_of_tree(source_folder_path)
    i = 1
    for root, dirs, files in os.walk(source_folder_path):
        # Create and enter any required subfolder
        relative_folder_path = os.path.relpath(root, source_folder_path).replace("\\", "/")
        server_folder_path = destination_folder_name + (
            "/" + relative_folder_path if relative_folder_path != "." else "")
        if relative_folder_path != '.':
            try:
                callback(f"Creating server folder {server_folder_path}", int(i / total * 100))
                ftp.mkd(relative_folder_path)
            except Exception:
                pass
            ftp.cwd(server_folder_path)
        # Upload all files in the current folder
        for file_name in files:
            callback(f"Uploading {file_name}", int(i / total * 100))
            local_file_path = os.path.join(root, file_name)
            with open(local_file_path, 'rb') as f:
                ftp.storbinary(f'STOR ' + file_name, f)
            i += 1
        # Move back to the parent folder
        if relative_folder_path != '.':
            ftp.cwd(destination_folder_name)

    ftp.quit()
    callback("Finished.", 100)


def get_file_count_of_tree(folder_path: str) -> int:
    """Returns the total number of files in a folder and its subfolders."""
    total_files = 0
    for _, _, files in os.walk(folder_path):
        total_files += len(files)
    return total_files
