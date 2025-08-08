from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ui.designer.rename import *


class Rename(QDialog, Ui_Rename):

    def __init__(self, files, supervisor, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # dialog
        # self.buttonStartNumbering.clicked.connect(self.accept)
        # self.buttonStartNumbering.setDefault(True)

        self.files = files  # QFileInfo objects
        self.supervisor = supervisor  # threaded resizer

        self.trackChanges = dict()

        self.setupSlots()
        self.imageIndex = 0
        self.loadImage()

    def setupSlots(self):
        self.editNewName.textEdited.connect(self.adjustPreview)
        self.spinSkipLeft.valueChanged.connect(self.adjustPreview)
        self.buttonSaveNext.clicked.connect(self.saveNext)
        self.buttonSkipNext.clicked.connect(self.gotoNext)
        self.supervisor.newItemReady.connect(self.displayThumbnail)
        # self.editNewName.returnPressed.connect(self.saveNext) #this already works out of the box - weird...Is QDialog the reason?

    def loadImage(self):
        if len(self.files) > 0:
            fi = self.files[self.imageIndex]
            self.labelOldName.setText(fi.baseName())
            self.labelExtension.setText(fi.completeSuffix())
            self.editNewName.clear()
            self.editNewName.setFocus()  # todo: validate if this works
            path = fi.absoluteFilePath()
            self.showThumbnail(path)

    def showThumbnail(self, path):
        self.labelImagePreview.setText("creating preview...")
        request = [[QFileInfo(path), self.height(), True]]  # request = [qfileinfo, size, smooth]
        self.reply = self.supervisor.add_items(request,
                                               True)  # true for priorty - #reply [qfileinfo, size, smooth, *ticket*]
        self.supervisor.process_queue()

    def displayThumbnail(self, ticket, img):
        if self.reply[0][3] == ticket:  # onze resized file is hier
            self.labelImagePreview.setPixmap(QPixmap.fromImage(img))

    def adjustPreview(self):
        """we create the virtual new filename to show a preview"""
        leftKeep = self.spinSkipLeft.value()
        oldName = self.labelOldName.text()
        oldNameKeep = oldName[:leftKeep]
        newPart = self.editNewName.text()
        extension = "." + self.labelExtension.text()
        newName = oldNameKeep + newPart + extension
        self.labelPreview.setText(newName)

    def saveNext(self):
        """get new filename"""
        newName = self.labelPreview.text()

        if newName == '':
            QMessageBox.warning(self, "Invalid filename", "You need to enter a new filename first!")
        else:
            """create file object"""
            fileInfo = self.files[self.imageIndex]
            file = QFile(fileInfo.absoluteFilePath())

            oldName = fileInfo.absoluteFilePath()
            newName = fileInfo.absolutePath() + "/" + newName

            x = file.rename(newName)
            # print("-"+str(x))
            if x:
                """rename succesful -> let the program know"""
                self.trackChanges[oldName] = newName
                self.gotoNext()
            else:
                QMessageBox.warning(self, "Invalid filename", "Rename failed.")

    def gotoNext(self):
        newIndex = self.imageIndex + 1
        if newIndex >= len(self.files):
            QMessageBox.information(self, "End of selection", "End of selection reached.")
        else:
            self.imageIndex = newIndex
            self.loadImage()

    def getChanges(self):
        return self.trackChanges
