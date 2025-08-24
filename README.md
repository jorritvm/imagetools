# Imagetools

A JPG photography workflow toolsuite.

<!-- TOC -->

* [Imagetools](#imagetools)
    * [Description](#description)
    * [Screenshot](#screenshot)
    * [Changelog](#changelog)
    * [Developer instructions (windows)](#developer-instructions-windows)
        * [Cloning the repository](#cloning-the-repository)
        * [Restoring the virtual environment](#restoring-the-virtual-environment)
            * [Installing using `uv` based on `pyproject.toml`](#installing-using-uv-based-on-pyprojecttoml)
            * [Installing using `pip` based on `requirements.txt`](#installing-using-pip-based-on-requirementstxt)
        * [Running all the unit tests](#running-all-the-unit-tests)
        * [Updating the dependencies (after adding new packages)](#updating-the-dependencies-after-adding-new-packages)
        * [Building the windows installer](#building-the-windows-installer)
    * [Installation instructions (windows)](#installation-instructions-windows)
    * [Usage instructions (windows)](#usage-instructions-windows)
        * [Running the CLI application](#running-the-cli-application)
        * [Running the UI application](#running-the-ui-application)
    * [Author](#author)

<!-- TOC -->

## Description

Imagetools helps you perform the necessary photography workflow operations to manage your library efficiently.  
Operations are accessible through either the UI or via their own CLI or both.

| Action           | Description                                                       | Supported in UI | Supported in CLI |
|------------------|-------------------------------------------------------------------|:---------------:|:----------------:|
| Auto Select      | Auto select new images from a directory based on previous imports |        ✅        |        ❌         |
| Import           | Import selected images from your SD card into your library        |        ✅        |        ❌         |
| Takeout          | Extract Google takeout archives and apply JSON metadata           |        ✅        |        ✅         |
| Heic to JPG      | Convert all .heic files in a folder into .jpg & keep EXIF         |        ✅        |        ✅         |
| Flat to Tree     | Convert a flat list of imagest to a date-based folder hierarchy   |        ✅        |        ✅         |
| Separate Media   | Separate images from video files                                  |        ✅        |        ✅         |
| Harvest Metadata | Overwrite downloaded Google photos with correct metadata          |       ⚠️        |       ⚠️ ️       |
| Created to Mod   | Overwrite append and modified times with created times            |        ✅        |        ✅         |
| Rename Auto      | Automatically rename files using a template string                |        ✅        |        ✅         |
| Rename Manual    | Manually rename files efficiently                                 |        ✅        |        ❌         |
| Judge            | Select the best images from a series                              |        ✅        |        ❌         |
| Resize           | Resize images uniformly                                           |        ✅        |        ✅         |
| Web Album        | Create a web album                                                |        ✅        |        ❌         |
| FTP upload       | Upload a folder to an FTP server                                  |        ✅        |        ✅         |
| Archive          | Archive image folders into .zip files                             |        ❌        |        ✅         |
| Google Seq       | Make files appear in alphabetical order on google photos.         |        ❌        |        ✅         |
| Cleanup          | Analyse and cleanup image folders                                 |        ❌        |        ❌         |

✅ Supported    
⚠️ Warning  
❌ Not supported

## Screenshot

[<img src="docs/screenshots/v4.0/main.png" width="300"/>](docs/screenshots/v4.0/main.png)

More screenshots can be found in the [docs/screenshots](docs/screenshots) folder.

## Changelog

[See NEWS.md](NEWS.md)

## Developer instructions (windows)

### Cloning the repository

```commandline
git clone https://github.com/jorritvm/imagetools.git
cd imagetools
```

### Restoring the virtual environment

The project comes with both a pyproject.toml and requirements.txt file.

#### Installing using `uv` based on `pyproject.toml`

Requires python 3.13.

```commandline
uv install --dev
```

#### Installing using `pip` based on `requirements.txt`

```commandline
python -m venv .venv
./bin/activate.bat
pip install -r requirements.txt
```

### Running all the unit tests

From the project root directory, run

```commandline
python -m pytest
```

### Updating the dependencies (after adding new packages)

Adding new dependencies to the `pyproject.toml` file can be done using:

```commandline
uv add <package_name>
```

However, to keep requirements.txt up to date, you must also use:

```commandline
uv pip freeze > requirements.txt
```

### Building the windows installer

```commandline
pyinstaller imagetools.spec
```

## Installation instructions (windows)

If you do not want to build the application yourself, you can install the precompiled version.
Download the windows binaries from the 'release' folder, all dependencies are included.
Unzip the folder and run `imagetools_gui.exe` or `imagetools_cli.exe`.

## Usage instructions (windows)

### Running the CLI application

```commandline
(.venv) python src/imagetools_cli.py
usage: imagetools_cli.py [-h] {takeout,heic_to_jpg,flat_to_tree,harvest_metadata,created_to_mod,rename_auto,separate_media,resize,ftp_upload,archive,google_seq} ...

```

Get an overview of all available commands:

```commandline
(.venv) python src/imagetools_cli.py -h 
usage: imagetools_cli.py [-h] {takeout,heic_to_jpg,flat_to_tree,harvest_metadata,created_to_mod,rename_auto,separate_media,resize,ftp_upload,archive,google_seq} ...

ImageTools CLI - run various image operations.

positional arguments:
  {takeout,heic_to_jpg,flat_to_tree,harvest_metadata,created_to_mod,rename_auto,separate_media,resize,ftp_upload,archive,google_seq}
    takeout             Run the takeout operation.
    heic_to_jpg         Run the heic_to_jpg operation.
    flat_to_tree        Run the flat_to_tree operation.
    harvest_metadata    Run the harvest_metadata operation.
    created_to_mod      Run the created_to_mod operation.
    rename_auto         Run the rename_auto operation.
    separate_media      Run the separate_media operation.
    resize              Run the resize operation.
    ftp_upload          Run the ftp_upload operation.
    archive             Run the archive operation.
    google_seq          Run the google_seq operation.

options:
  -h, --help            show this help message and exit
```

Get more details on the arguments for a specific command:

```commandline
(.venv) python src/imagetools_cli.py <command> -h

(imagetools) PS C:\dev\python\imagetools> python src/imagetools_cli.py resize -h     
usage: imagetools_cli.py resize [-h] folder_path output_folder_name prefix suffix size quality

positional arguments:
  folder_path         Folder for which to resize all .jpg files.
  output_folder_name  Name of the subfolder to store the resized images. Choose '.' to keep them in the original folder.
  prefix              Prefix string to give to the resized files. Use 'none' to skip.
  suffix              Suffix string to give to the resized files. Use 'none' to skip.
  size                Size of the longest side of the resized images.
  quality             Quality of the resized images (85 is a good default).

options:
  -h, --help          show this help message and exit
```

### Running the UI application

```commandline
(.venv) python src/imagetools_ui.py 
```

## Author

Jorrit Vander Mynsbrugge