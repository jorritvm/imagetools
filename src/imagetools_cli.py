"""
Entry point for the ImageTools CLI application.
"""
import argparse

from operations import takeout, heic_to_jpg, flat_to_tree, harvest_metadata


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

    args = parser.parse_args()
    print(args)
    process_cli(args)


if __name__ == "__main__":
    main()
