from PyQt6.QtWidgets import *
from pyprojroot import here

from ui.designer.about import Ui_Dialog


class AboutDialog(QDialog, Ui_Dialog):

    def __init__(self, md, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        if here(md).exists():
            try:
                fcon = open(here(md), "r")
                txt = fcon.read()
                self.textEdit.setMarkdown(txt)
            finally:
                fcon.close()

        self.resize(600, 600)
