"""
Entry point for the ImageTools CLI application.
"""
import argparse

from operations import takeout


def process_cli(args):
    if args.command == "takeout":
        takeout.takeout_operation(
            args.takeout_zip_file,
            args.output_folder,
            callback=lambda msg, progress: print(f"({progress}%) {msg}")
        )


def main():
    # create the cli argument parser
    parser = argparse.ArgumentParser(
        description="ImageTools CLI - run various image operations."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- takeout command ---
    takeout_parser = subparsers.add_parser(
        "takeout", help="Run the takeout operation."
    )
    takeout_parser.add_argument("takeout_zip_file", help="Path to input takeout zip file, empty if already unzipped")
    takeout_parser.add_argument("output_folder", help="Path to output folder")

    args = parser.parse_args()
    print(args)
    process_cli(args)


if __name__ == "__main__":
    main()
