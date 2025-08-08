from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ui.designer.number import *


class Number(QDialog, Ui_Number):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.btn_start_numbering.clicked.connect(self.accept)
        self.btn_start_numbering.setDefault(True)

    def get_settings(self):
        """returns the user input / settings of the dialog"""
        settings = dict()
        if self.radio_pre.isChecked():
            settings["position"] = "prefix"
        elif self.radio_suff.isChecked():
            settings["position"] = "suffix"
        settings["digits"] = self.spin_digits.value()
        settings["seperator"] = self.edit_separator.text()
        settings["keep_old_filename"] = self.check_keep_old_name.isChecked()

        return settings

    def rename_files(self, files, settings):
        """renames the files with the given settings"""
        track_changes = dict()

        for i in range(len(files)):
            """create the objects to manipulate the files"""
            fi = files[i]
            ext = fi.completeSuffix()

            # numbering is done with leading zeros
            new_name = str(i + 1).zfill(settings["digits"])

            if settings["position"] == "prefix":
                if settings["digits"]:
                    new_name += settings["seperator"]
                if settings["keep_old_filename"]:
                    new_name += fi.fileName()
                else:
                    new_name += "." + ext

            elif settings["position"] == "suffix":
                if settings["digits"]:
                    new_name = settings["seperator"] + new_name
                if settings["keep_old_filename"]:
                    new_name = fi.baseName() + new_name + "." + ext
                else:
                    new_name += "." + ext

            """rename the file to the new name"""
            file = QFile(fi.absoluteFilePath())
            absolute_new_name = fi.absolutePath() + "/" + new_name

            x = file.rename(absolute_new_name)
            if x:  # rename success
                track_changes[fi.absoluteFilePath()] = absolute_new_name
            else:
                pass

        return track_changes
