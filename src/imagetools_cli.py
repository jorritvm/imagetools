"""
Entry point for the ImageTools CLI application.
"""
import argparse

from operations import takeout, heic2jpg


def print_callback(msg, progress):
    print(f"({progress}%) {msg}")


def process_cli(args):
    if args.command == "takeout":
        takeout.takeout_operation(
            args.takeout_zip_file,
            args.output_folder,
            callback=print_callback)

    if args.command == "heic2jpg":
        heic2jpg.heic_to_jpg_operation(
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
    takeout_parser.add_argument("takeout_zip_file", help="Path to input takeout zip file, empty if already unzipped")
    takeout_parser.add_argument("output_folder", help="Path to output folder")

    # --- heic2jpg command ---
    heic2jpg_parser = subparsers.add_parser("heic2jpg", help="Run the heic2jpg operation.")
    heic2jpg_parser.add_argument("folder_path", help="Path to folder containing the HEIC files")

    args = parser.parse_args()
    print(args)
    process_cli(args)


if __name__ == "__main__":
    main()
