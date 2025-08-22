"""
Entry point for the ImageTools CLI application.
"""
import argparse

from operations import ftp_upload, archive
from operations import separate_media, resize
from operations import takeout, heic_to_jpg, flat_to_tree, harvest_metadata, created_to_mod, rename_auto


def print_callback(msg, progress):
    print(f"({progress}%) {msg}")


def process_cli(args):
    if args.command == "takeout":
        takeout.takeout_operation(
            args.takeout_zip_file,
            args.output_folder,
            callback=print_callback)

    if args.command == "heic_to_jpg":
        heic_to_jpg.heic_to_jpg_operation(
            args.folder_path,
            callback=print_callback)

    if args.command == "flat_to_tree":
        flat_to_tree.flat_to_tree_operation(
            args.folder_path,
            callback=print_callback)

    if args.command == "harvest_metadata":
        harvest_metadata.harvest_metadata_for_folder_path_operation(
            args.folder_path,
            args.album_name,
            args.client_secret_json_file_path,
            callback=print_callback)

    if args.command == "created_to_mod":
        created_to_mod.created_to_mod_for_folder_path_operation(
            args.folder_path,
            callback=print_callback)

    if args.command == "rename_auto":
        rename_auto.rename_auto_for_folder_path_operation(
            args.folder_path,
            args.new_file_name_template,
            callback=print_callback)

    if args.command == "separate_media":
        separate_media.separate_media_operation(
            args.folder_path,
            args.separate_what,
            callback=print_callback)

    if args.command == "resize":
        resize.resize_folder_path_operation(
            args.folder_path,
            args.output_folder_name,
            args.prefix,
            args.suffix,
            args.size,
            args.quality,
            callback=print_callback)

    if args.command == "ftp_upload":
        ftp_upload.ftp_upload_operation(
            args.ip,
            args.port,
            args.user,
            args.password,
            args.destination_folder_name,
            args.source_folder_path,
            callback=print_callback
        )

    if args.command == "archive":
        archive.archive_operation(
            args.folder_path,
            callback=print_callback)


def main():
    # create the cli argument parser
    parser = argparse.ArgumentParser(
        description="ImageTools CLI - run various image operations."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- takeout command ---
    takeout_parser = subparsers.add_parser("takeout", help="Run the takeout operation.")
    takeout_parser.add_argument("takeout_zip_file", help="Path to input takeout zip file, empty if already unzipped.")
    takeout_parser.add_argument("output_folder", help="Path to output folder.")

    # --- heic_to_jpg command ---
    heic_to_jpg_parser = subparsers.add_parser("heic_to_jpg", help="Run the heic_to_jpg operation.")
    heic_to_jpg_parser.add_argument("folder_path", help="Path to folder containing the HEIC files.")

    # --- flat_to_tree command ---
    flat_to_tree_parser = subparsers.add_parser("flat_to_tree", help="Run the flat_to_tree operation.")
    flat_to_tree_parser.add_argument("folder_path", help="Path to folder with files to restructure into subfolders.")

    # --- harvest_metadata command ---
    harvest_metadata_parser = subparsers.add_parser("harvest_metadata", help="Run the harvest_metadata operation.")
    harvest_metadata_parser.add_argument("folder_path",
                                         help="Path to folder with files to overwrite with new metadata from google api.")
    harvest_metadata_parser.add_argument("album_name", help="Name of the matching album on google photos.")
    harvest_metadata_parser.add_argument("client_secret_json_file_path",
                                         help="Path to the client secret JSON file for Google Photos API.")

    # --- created_to_mod command ---
    created_to_mod_parser = subparsers.add_parser("created_to_mod", help="Run the created_to_mod operation.")
    created_to_mod_parser.add_argument("folder_path",
                                       help="Path to folder with files for which to overwrite atime and mtime with ctime.")

    # --- rename auto command ---
    rename_auto_parser = subparsers.add_parser("rename_auto", help="Run the rename_auto operation.")
    rename_auto_parser.add_argument("folder_path", help="Path to folder with files to rename.")
    rename_auto_parser.add_argument("new_file_name_template",
                                    help="Template for the new file names. Use tags like $name, $ext, $mtime_date, etc.")

    # --- separate_media command ---
    separate_media_parser = subparsers.add_parser("separate_media", help="Run the separate_media operation.")
    separate_media_parser.add_argument("folder_path", help="Root path to recurse to separate media by type.")
    separate_media_parser.add_argument("separate_what",
                                       help="Choose between 'images', 'movies', or 'both'.", )

    # --- resize command ---
    resize_parser = subparsers.add_parser("resize", help="Run the resize operation.")
    resize_parser.add_argument("folder_path", help="Folder for which to resize all .jpg files.")
    resize_parser.add_argument("output_folder_name", help="Name of the subfolder to store the resized images. "
                                                          "Choose '.' to keep them in the original folder.")
    resize_parser.add_argument("prefix", help="Prefix string to give to the resized files. Use 'none' to skip.")
    resize_parser.add_argument("suffix", help="Suffix string to give to the resized files. Use 'none' to skip.")
    resize_parser.add_argument("size", type=int, help="Size of the longest side of the resized images.")
    resize_parser.add_argument("quality", type=int, help="Quality of the resized images (85 is a good default).")

    # --- ftp_upload command ---
    ftp_upload_parser = subparsers.add_parser("ftp_upload", help="Run the ftp_upload operation.")
    ftp_upload_parser.add_argument("ip", help="IP address of the FTP server.")
    ftp_upload_parser.add_argument("port", type=int, help="Port number of the FTP server.")
    ftp_upload_parser.add_argument("user", help="Username for FTP login.")
    ftp_upload_parser.add_argument("password", help="Password for FTP login.")
    ftp_upload_parser.add_argument("destination_folder_name",
                                   help="Destination folder on the FTP server (will be created if it doesn't exist).")
    ftp_upload_parser.add_argument("source_folder_path", help="Local path to the folder contents to upload.")

    # --- archive command ---
    archive_parser = subparsers.add_parser("archive", help="Run the archive operation.")
    archive_parser.add_argument("folder_path", help="Folder containing the subfolders to zip one by one.")

    args = parser.parse_args()
    # print(args) # debug only
    process_cli(args)


if __name__ == "__main__":
    main()
