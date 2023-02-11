import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ThumbnailBrowser(QWidget):
    def __init__(self, supervisor, path, image_size, parent=None):
        QWidget.__init__(self, parent)
        
        self.setup_ui()
        self.setup_slots()

        self.thumbs_view.icon_size_position = image_size
        self.thumbs_view.set_icon_size()

        self.supervisor = supervisor
        self.supervisor.newItemReady.connect(self.image_ready)
        
        self.root_folder = ""
        self.change_folder(path)

    def setup_ui(self):
        """create the custom listview that will show the thumbnails"""
        self.thumbs_view = ThumbnailListWidget()

        """create selectionbox buttons"""
        self.btn_add = QPushButton("Add")
        self.btn_remove = QPushButton("Remove")
        self.btn_add_all = QPushButton("Add All")
        self.btn_clear = QPushButton("Clear")

        list_buttons_selection = [self.btn_add, self.btn_remove, self.btn_add_all, self.btn_clear]
        group_selection = QGroupBox("Selection")
        layout_buttons_selection = QHBoxLayout(group_selection)
        for button in list_buttons_selection:
            layout_buttons_selection.addWidget(button)
        layout_buttons_selection.setContentsMargins(4, 4, 4, 4)
        layout_buttons_selection.setSpacing(4)

        """create browser buttons"""
        self.btn_thumb = QPushButton("T")
        self.btn_detail = QPushButton("D")
        self.btn_zoom_in = QPushButton("+")
        self.btn_zoom_out = QPushButton("-")

        # todo: remove when T and D view both exist
        self.btn_thumb.setDisabled(True)
        self.btn_detail.setDisabled(True)

        list_buttons_browser = [self.btn_thumb, self.btn_detail, self.btn_zoom_out, self.btn_zoom_in]
        group_browser = QGroupBox("Browser")
        layout_buttons_browser = QHBoxLayout(group_browser)
        for button in list_buttons_browser:
            button.setMaximumWidth(25)
            layout_buttons_browser.addWidget(button)
        layout_buttons_browser.setContentsMargins(4, 4, 4, 4)
        layout_buttons_browser.setSpacing(4)
        group_browser.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))
                             
        """combine all components into a vlayout"""
        layout_all_buttons = QHBoxLayout()
        layout_all_buttons.addWidget(group_selection)
        btnSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout_all_buttons.addItem(btnSpacer)
        layout_all_buttons.addWidget(group_browser)
        layout_thumbnail_browser = QVBoxLayout()
        layout_thumbnail_browser.addWidget(self.thumbs_view)
        layout_thumbnail_browser.addLayout(layout_all_buttons)
        layout_thumbnail_browser.setContentsMargins(4, 4, 4, 4)
        self.setLayout(layout_thumbnail_browser)

    def setup_slots(self):
        self.thumbs_view.itemDoubleClicked.connect(self.open_in_external_app)
        self.btn_add.pressed.connect(self.add_to_selection)
        self.btn_remove.pressed.connect(self.remove_from_selection)
        self.btn_add_all.pressed.connect(self.add_all_to_selection)
        self.btn_clear.pressed.connect(self.clear_selection)
        self.btn_zoom_in.pressed.connect(lambda: self.thumbs_view.adjustIconSize("+"))
        self.btn_zoom_out.pressed.connect(lambda: self.thumbs_view.adjustIconSize("-"))

    def open_in_external_app(self, item):
        fi = QFileInfo()
        fi.setFile(QDir(self.root_folder), item.text())
        link = fi.absoluteFilePath()
        os.startfile(link)

    def add_to_selection(self):
        items = self.thumbs_view.selectedItems()
        self.change_color(items, Qt.darkGray)

    def remove_from_selection(self):
        items = self.thumbs_view.selectedItems()
        self.change_color(items, Qt.white)

    def add_all_to_selection(self):
        items = [self.thumbs_view.item(x) for x in range(self.thumbs_view.count())]
        self.change_color(items, Qt.darkGray)

    def clear_selection(self):
        items = [self.thumbs_view.item(x) for x in range(self.thumbs_view.count())]
        self.change_color(items, Qt.white)

    def change_color(self, items, color):
        for item in items:
            item.setBackground(QColor(color))

    def change_folder(self, path):
        self.root_folder = path
        self.thumbs_view.clear()
        self.supervisor.clear_queue()

        """set a directory model with appropriate filters to get the image info"""
        dirModel = QDir(path)
        dirModel.setNameFilters(["*.jpg","*.jpeg","*.png","*.bmp"])

        """create the DATA the model will use"""
        images = dirModel.entryList()
        img_absolute_paths = list()
        for fileName in images:
            img_absolute_paths.append(dirModel.absoluteFilePath(fileName))
        
        q = []
        maximum_thumbnail_size = self.thumbs_view.iconSizes[-1]
        for file in img_absolute_paths:
            q.append([QFileInfo(file), maximum_thumbnail_size, False])  # not smooth
            px = QPixmap(maximum_thumbnail_size,maximum_thumbnail_size)  #take this dummy thumbnail large enough
            px.fill(QColor(255,255,255))  # makes sure it's white
            x = QListWidgetItem(QIcon(px), os.path.basename(file))
            self.thumbs_view.addItem(x)
            
        # pass the work to the supervisor and receive tickets for every image in return
        self.currentlyProcessing = self.supervisor.add_items(q, False)
        self.supervisor.process_queue()

    def image_ready(self, ticket, img): #img is in QImage format
        for item in self.currentlyProcessing:
            # match the QListViewItem to the QImage using the ticket the threaded resizer offers
            if item[3] == ticket:
                name = os.path.basename(item[0].absoluteFilePath())
                for i in range(self.thumbs_view.count()):
                    if self.thumbs_view.item(i).text() == name:
                        self.thumbs_view.item(i).setIcon(QIcon(QPixmap.fromImage(img)))

    def get_selection(self):
        """returns list of QFileInfo objetcs"""
        x = []
        view = self.thumbs_view
        for i in range(view.count()):
            item = view.item(i)
            if item.background() == QColor(Qt.darkGray):
                fi = QFileInfo()
                fi.setFile(QDir(self.root_folder), item.text())
                x.append(fi)
        return x

    def update_elements(self, changes):
        """update filenames of items in the thumbnailbrowser"""
        for old,new in changes.items():
            fi_old = QFileInfo(old)
            fi_new = QFileInfo(new)                       
            if self.root_folder == fi_old.absolutePath():
                view = self.thumbs_view
                for i in range(view.count()):
                    item = view.item(i)
                    if item.text() == fi_old.fileName():
                        item.setText(fi_new.fileName())


class ThumbnailListWidget(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self,parent)

        """change the viewmode to iconmode instead of listmode"""
        self.setViewMode(QListView.IconMode)

        """set the icon size"""
        self.iconSizes = list(range(50, 750, 50))
        self.icon_size_position = 2
        self.set_icon_size()

        """add some spacing around the elements"""
        self.setSpacing(10)

        """wrap the items when there are too many to layout horizontally"""
        self.setWrapping(True)

        """set the automatic resize to adjust instead of fixed"""
        self.setResizeMode(QListView.Adjust)

        """set the view to allow multiple selection"""
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def adjustIconSize(self, direction):
        if direction == "+":
            newPos = self.icon_size_position + 1
        elif direction == "-":
            newPos = self.icon_size_position - 1
        
        """make sure we don't try to go out of bounds of our sizes list"""
        if newPos < 0 or newPos > len(self.iconSizes)-1:
            newPos = self.icon_size_position

        self.icon_size_position = newPos
        self.set_icon_size()

    def set_icon_size(self):
        """here we really set the iconSize, the view will update automaticly"""
        size = self.iconSizes[self.icon_size_position]
        self.setIconSize(QSize(size,size*9/16))
        self.setGridSize(QSize(size+0,size*9/16+25))
        
