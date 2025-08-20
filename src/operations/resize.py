"""
The resize operation resizes images to the desired output size.
It uses a multithreaded approach to go as fast as possible.
To avoid needing a PyQt QApplication, we're not using the threaded_resizer, nor the QImage class.
- You can provide a folder and it will resize all the jpeg in that folder or you provide a list of files to resize.
- You have to specify the desired output folder, use "." for the current image folder
- You can specify a filename prefix and a filename suffix. If you specify 'none' that will be replaced by "".
- You can specify a jpg quality index from 0 to 100, where 100 is the best quality, default is 85
"""
import concurrent.futures
import os

from PIL import Image

MAX_WORKERS = 1  # If set to None the amount of system cores will be used


def resize_folder_path_operation(folder_path: str, output_folder_name: str, prefix: str, suffix: str, size: int,
                                 quality: int,
                                 callback) -> None:
    """Entrypoint for the resize operation that accepts a folder path as input."""
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        callback("The specified folder does not exist or is not a directory.", 100)
        return

    callback(f"Starting resize operation for folder: {folder_path}", 0)
    list_of_file_names = os.listdir(folder_path)
    list_of_file_paths = [os.path.join(folder_path, file_name) for file_name in list_of_file_names
                          if
                          os.path.isfile(os.path.join(folder_path, file_name)) and file_name.lower().endswith('.jpg')]

    resize_list_of_file_paths_operation(list_of_file_paths, output_folder_name, prefix, suffix, size, quality, callback)


def resize_list_of_file_paths_operation(list_of_file_paths: list[str], output_folder_name: str, prefix: str,
                                        suffix: str, size: int, quality: int, callback) -> None:
    """Resize a list of file paths. Do it multithreaded. Report the progress via the callback."""
    total = len(list_of_file_paths)
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(resize_image, file_path, output_folder_name, prefix, suffix, size, quality)
            for file_path in list_of_file_paths
        ]
        i = 0
        for future in concurrent.futures.as_completed(futures):
            i += 1
            input_file_name, success = future.result()  # Get the result from the future
            if success:
                callback(f"Finished resizing: {input_file_name}", int((i / total) * 100))
            else:
                callback(f"FAILED to resize: {input_file_name}", int((i / total) * 100))

    callback("Finished!", 100)


def resize_image(file_path, output_folder_name, prefix, suffix, size, quality):
    """Save the resized image to output_folder with prefix/suffix and quality."""

    # compose the new file path
    folder_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    root, ext = os.path.splitext(file_name)
    if ext.lower() != '.jpg':
        return file_path, False
    new_folder_path = folder_path if output_folder_name == "." else os.path.join(folder_path, output_folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    new_file_name = root
    new_file_name = f"{prefix}{new_file_name}" if prefix != "none" else new_file_name
    new_file_name = f"{new_file_name}{suffix}" if suffix != "none" else new_file_name
    new_file_name += ".jpg"  # Ensure it has a valid extension
    new_file_path = os.path.join(new_folder_path, new_file_name)

    # resize the image so the longest side is equal to 'size' using pillow
    try:
        with Image.open(file_path) as img:
            if img.width > img.height:
                new_width = size
                new_height = int((size / img.width) * img.height)
            else:
                new_height = size
                new_width = int((size / img.height) * img.width)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img.save(new_file_path, "JPEG", quality=quality)
            return file_name, True
    except Exception as e:
        return file_path, False


if __name__ == "__main__":
    # Example usage
    def progress_callback(message, progress):
        print(f"{message} - Progress: {progress}%")


    resize_folder_path_operation(r"C:\Users\jorrit\Desktop\sandbox\test100",
                                 "resized_subfolder",
                                 "small_",
                                 "none",
                                 150,
                                 85,
                                 progress_callback)
