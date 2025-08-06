# imagetools v4.0

### NOTES

- project changes from pip to uv for dependency management

### NEW FEATURES

- ...

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
