# goal of the file: convert the project's UI files into PY files

import os
from pathlib import Path

from pyprojroot import here

pyuic = here("./.venv/Scripts/pyuic6.exe")
ui_path_from = here("./src/resources/uixml")
ui_path_to = here("./src/resources/uipy")

print("Converting .xml UI designer files into python files...")
for uifile in sorted(ui_path_from.glob('*.ui')):
    pyfile = Path.joinpath(ui_path_to, uifile.stem + ".py")
    cmd = f'{pyuic} "{uifile}" -o "{pyfile}"'
    print(cmd)
    os.system(cmd)
print("Done.")
