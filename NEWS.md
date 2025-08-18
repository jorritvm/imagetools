# future

- refactor everything
    - add type annotations everywhere
    - make sure style guide is followed
    - make sure autoformatter is applied to every document
    - add docstrings where needed (module/class/function doc)
    - add architecture document (diagram)
- build in a catalog = resizer cache / metadata manager
- add picture housekeeper modules
- maak een versie 4 van imagetools als alles af is
- performing heic to jpg does not update the ui, need to fix that using a subthread for the operation wrapper
- executing takeout does not update the ui, need to fix that using a subthread for the operation wrapper
- takeout operation crashes when a metadata.json file is present which is not a valid media metadata file

# imagetools v4.0

### NOTES

- removing IDE project folders (.idea / .vscode) from source control
- project changes from pip to uv for dependency management
- remove settings.bin from github & improve default settings handling
- upgrade to PyQt6
- adding style guide to the documentation folder + started applying it more rigorously
- adding architecture documentation: module_view and ADR to the documentation folder
- adding main window widget nesting diagram
- refactoring repo structure separating ui and backend code
- joining main window code but separating operation handler code
- refactoring all UI operation handlers into their own submodules
- refactoring folder_select, browser and threaded resizer code slightly for better maintainability

### NEW FEATURES

- now follows system color scheme
- hardcoded parameters of the UI application are now part of a constants file so you can easily change selection
  background color etc.
- mouse press on folder select now highlights the entire value making it easy to copy or overwrite
- added google takeout operation, cli interface, and ui dialog
- added heic to jpg operation, cli interface, and ui dialog
- added flat to tree operation, cli interface, and ui dialog
- added metadata harvester operation, cli interface - then realised the google api is no longer available
- added created to modified operation, cli interface, and ui dialog
- added rename auto operation, cli interface, and ui dialog
- added separate media operation, cli interface, and ui dialog
-

# imagetools v3.0

### NOTES

- abandonned MVC framework and recoded using simple widget
- refactored about half of the existing modules
- added ui build scripts
- increased maximum thumbnail size
- increased webalbum image thumbnail size
- bugfix where close action did not store latest settings
- added some tests (pytest)
- move from cx_freeze to pyinstaller for build process

### NEW FEATURES

- redesigned UI
- selections can be done in the thumbnail browser
- added backward/forward folder navigation
- opens folder in OS file explorer when one is double clicked
- opens image in OS default viewer when image is double clicked
- added about box
- added changelog box
- added settings panel
- remembers last directory etc..
- remembers and restores previous window size and position
- added ftp upload (nonblocking) + site manager
- improved resizer using multithreading which is used for both browser & resizer tool

# imagetools v2.0

### NOTES

- recode using PyQt MVC framework

### NEW FEATURES

- new UI
- added web album feature
- added a thumbnailviewer
- improved performance using multithreading

# imagetools v1.1

### NOTES

- fixed bugs in number section
- fixed 'no thumnbail bug' for windows users
- now comes with windows installer for dekstop integration

# imagetools v1.0

### NOTES

- self extraction archive for windows
- source tarbal for unix

### NEW FEATURES

- first release
- number files
- rename files quickly (prefixes, suffixes and human entries)
- resize files
