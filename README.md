# Imagetools

A JPG photography workflow toolsuite.

## Description

When you take many pictures in JPG, Imagetools helps you perform the necessary workflow operations to get everything
cleaned up efficiently.

Supported operations:

* Import from your SD card
* Auto rotate based on EXIF information
* Select the best images from a series of similar ones
* Number and rename
* Resize
* Create a webalbum
* Upload it to an FTP webhost

## Screenshot

[<img src="doc/screenshots/v3.0/main_window.png" width="300"/>](doc/screenshots/v3.0/main_window.png)

## Changelog

See NEWS.md

## Windows user installation instructions

Download the installer from the 'release' folder, all dependencies are included.

## Windows developer instructions

The project comes with both a pyproject.toml and requirements.txt file.

### Installing using `uv` based on `pyproject.toml`

```commandline
uv install --dev
```

### Installing using `pip` based on `requirements.txt`

```commandline
python -m venv .venv
./bin/activate.bat
pip install -r requirements.txt
```

### Running the application

```commandline
(.venv) python src/imagetools.py 
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

## Author

Jorrit Vander Mynsbrugge