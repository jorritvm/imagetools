from PyQt6.QtWidgets import QDialog, QMessageBox

from ui.designer.about import Ui_Dialog


class AboutDialog(QDialog, Ui_Dialog):

    def __init__(self, file_path: str, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                txt = file.read()
                self.textEdit.setMarkdown(txt)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

        self.resize(600, 600)
