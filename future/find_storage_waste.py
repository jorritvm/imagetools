import os

DIGITAL_NEGATIVE_EXTENSIONS = {'.CR2', '.NEF', '.DNG'}
LARGE_JPG_FOLDERS = {'jpg_large', 'jpeg_large'}
SMALL_JPG_FOLDERS = {'jpg_small', 'jpeg_small'}
JPG_EXTENSIONS = {'.JPG', '.JPEG'}

parent_path = r"C:\pictures"
total_savings = 0

def count_files_with_extensions(directory, extensions):
    """Return list of files and their total size if extension matches."""
    files = []
    total_size = 0
    for entry in os.scandir(directory):
        if entry.is_file() and os.path.splitext(entry.name)[1].upper() in extensions:
            files.append(entry.path)
            total_size += entry.stat().st_size
    return files, total_size

def identify_storage_waste_from_trash_negatives(path):
    global total_savings
    for root, dirs, files in os.walk(path):
        # Only proceed if the folder is exactly named "path"
        if os.path.basename(root).lower() == "trash":
            neg_files, neg_size = count_files_with_extensions(root, DIGITAL_NEGATIVE_EXTENSIONS)
            X = len(neg_files)
            if X == 0:
                continue  # No digital negatives, skip

            has_large = has_small = False
            count_large = count_small = 0

            for subfolder in dirs:
                subfolder_lower = subfolder.lower()
                subfolder_path = os.path.join(root, subfolder)

                if subfolder_lower in LARGE_JPG_FOLDERS:
                    large_files, _ = count_files_with_extensions(subfolder_path, JPG_EXTENSIONS)
                    count_large = len(large_files)
                    if count_large == X:
                        has_large = True

                elif subfolder_lower in SMALL_JPG_FOLDERS:
                    small_files, _ = count_files_with_extensions(subfolder_path, JPG_EXTENSIONS)
                    count_small = len(small_files)
                    if count_small == X:
                        has_small = True

            total_savings = total_savings + neg_size

            if has_large and has_small:
                print(f"{root} -> already contains developed SMALL and LARGE jpgs - potential save space = {neg_size / (1024 ** 2):.2f} MB")
            elif has_large and not has_small:
                print(f"{root} -> contains LARGE jpgs but not SMALL - potential save space = {neg_size / (1024 ** 2):.2f} MB")
            elif not has_large and has_small:
                print(f"{root} -> contains SMALL jpgs but not LARGE - potential save space = {neg_size / (1024 ** 2):.2f} MB")
            else:
                print(f"{root} -> no jpgs found, consider redeveloping - potential save space = {neg_size / (1024 ** 2):.2f} MB")

    print(f"total savings could amount to: {total_savings / (1024 ** 2):.2f} MB")

if __name__ == "__main__":
    identify_storage_waste_from_trash_negatives(parent_path)