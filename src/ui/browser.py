import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from threaded_resizer.threaded_resizer import ImageResizeTask
from ui import constants


class Browser(QWidget):
    def __init__(self, supervisor, path, image_size, parent=None):
        QWidget.__init__(self, parent)

        self.setup_ui()
        self.setup_slots()

        self.thumbnail_view.icon_size_index = image_size
        self.thumbnail_view.set_icon_size()

        self.supervisor = supervisor
        self.supervisor.newItemReady.connect(self.image_ready)

        self.root_folder = ""
        self.change_folder(path)

    def setup_ui(self) -> None:
        """create the custom listview that will show the thumbnails"""
        self.thumbnail_view = ThumbnailListWidget()

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
        self.btn_thumbnail_view = QPushButton("T")
        self.btn_details_view = QPushButton("D")
        self.btn_zoom_in = QPushButton("+")
        self.btn_zoom_out = QPushButton("-")

        list_buttons_browser = [self.btn_thumbnail_view, self.btn_details_view, self.btn_zoom_out, self.btn_zoom_in]
        group_browser = QGroupBox("Browser")
        layout_buttons_browser = QHBoxLayout(group_browser)
        for button in list_buttons_browser:
            button.setMaximumWidth(25)
            layout_buttons_browser.addWidget(button)
        layout_buttons_browser.setContentsMargins(4, 4, 4, 4)
        layout_buttons_browser.setSpacing(4)
        group_browser.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred))

        """combine all components into a vlayout"""
        layout_all_buttons = QHBoxLayout()
        layout_all_buttons.addWidget(group_selection)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout_all_buttons.addItem(spacer)
        layout_all_buttons.addWidget(group_browser)
        layout_thumbnail_browser = QVBoxLayout()
        layout_thumbnail_browser.addWidget(self.thumbnail_view)
        layout_thumbnail_browser.addLayout(layout_all_buttons)
        layout_thumbnail_browser.setContentsMargins(4, 4, 4, 4)
        self.setLayout(layout_thumbnail_browser)

    def setup_slots(self) -> None:
        self.thumbnail_view.itemDoubleClicked.connect(self.open_in_external_app)
        self.btn_add.pressed.connect(self.add_to_selection)
        self.btn_remove.pressed.connect(self.remove_from_selection)
        self.btn_add_all.pressed.connect(self.add_all_to_selection)
        self.btn_clear.pressed.connect(self.clear_selection)
        self.btn_zoom_in.pressed.connect(lambda: self.thumbnail_view.adjust_icon_size("+"))
        self.btn_zoom_out.pressed.connect(lambda: self.thumbnail_view.adjust_icon_size("-"))

    @pyqtSlot(QListWidgetItem)
    def open_in_external_app(self, item: QListWidgetItem) -> None:
        file_path = os.path.join(self.root_folder, item.text())
        link = os.path.abspath(file_path)
        os.startfile(link)

    @pyqtSlot()
    def add_to_selection(self) -> None:
        items = self.thumbnail_view.selectedItems()
        self.change_color(items, constants.THUMBNAIL_SELECTION_COLOR)

    @pyqtSlot()
    def remove_from_selection(self) -> None:
        items = self.thumbnail_view.selectedItems()
        self.change_color(items, Qt.GlobalColor.transparent)

    @pyqtSlot()
    def add_all_to_selection(self) -> None:
        items = [self.thumbnail_view.item(x) for x in range(self.thumbnail_view.count())]
        self.change_color(items, constants.THUMBNAIL_SELECTION_COLOR)

    @pyqtSlot()
    def clear_selection(self) -> None:
        items = [self.thumbnail_view.item(x) for x in range(self.thumbnail_view.count())]
        self.change_color(items, Qt.GlobalColor.transparent)

    def change_color(self, items: list[QListWidgetItem], color: Qt.GlobalColor) -> None:
        for item in items:
            item.setBackground(QColor(color))

    def change_folder(self, path: str) -> None:
        """
        change the folder to the given path and update the thumbnail view
        :param path: the absolute path to the folder to change to
        """
        self.root_folder = path
        self.thumbnail_view.clear()
        self.supervisor.clear_queue()

        """set a directory model with appropriate filters to get the image info"""
        folder = QDir(path)
        folder.setNameFilters(constants.IMAGE_FILTERS)

        """create the DATA the model will use"""
        images = folder.entryList()
        img_absolute_paths = list()
        for fileName in images:
            img_absolute_paths.append(folder.absoluteFilePath(fileName))

        # the threaded resizer will resize images to the maximum thumbnail size
        # another option would be to resize to the screen height (monitor)
        maximum_thumbnail_size = self.thumbnail_view.icon_sizes[-1]
        image_resize_tasks = []
        for file in img_absolute_paths:
            # creeate a n image resize task for every image
            image_resize_task = ImageResizeTask(QFileInfo(file),
                                                maximum_thumbnail_size,
                                                True)  # fast resize
            image_resize_tasks.append(image_resize_task)  # not smooth

            # create a dummy thumbnail for every image
            px = QPixmap(maximum_thumbnail_size, maximum_thumbnail_size)  # take this dummy thumbnail large enough
            px.fill(Qt.GlobalColor.transparent)
            # px.fill(QColor(255, 255, 255))  # makes sure it's white
            placeholder = QListWidgetItem(QIcon(px), os.path.basename(file))
            self.thumbnail_view.addItem(placeholder)

        # pass the work to the supervisor and receive tickets for every image in return
        self.ticketed_image_resize_tasks = self.supervisor.add_items(image_resize_tasks, False)
        self.supervisor.process_queue()

    @pyqtSlot(int, QImage)
    def image_ready(self, ticket: int, img: QImage) -> None:
        """
        update the thumbnail of an image by matching the QListViewItem to the QImage
        using the ticket the threaded resizer offers and the file name
        """
        for image_resize_tasks in self.ticketed_image_resize_tasks:
            if image_resize_tasks.ticket == ticket:
                name = image_resize_tasks.file_info.fileName()
                for i in range(self.thumbnail_view.count()):
                    if self.thumbnail_view.item(i).text() == name:
                        self.thumbnail_view.item(i).setIcon(QIcon(QPixmap.fromImage(img)))

    def get_selection(self) -> list[QFileInfo]:
        """
        return the current selection by matching on the background color of the items in the thumbnail view
        :return: list of QFileInfo objects of the selected items in the thumbnail view
        """
        selection = []
        view = self.thumbnail_view
        for i in range(view.count()):
            item = view.item(i)
            if item.background() == QColor(constants.THUMBNAIL_SELECTION_COLOR):
                file_info = QFileInfo()
                file_info.setFile(QDir(self.root_folder), item.text())
                selection.append(file_info)
        return selection

    def update_elements(self, changes):
        """update filenames of items in the thumbnailbrowser"""
        # todo: refactor when we see this being used for the first time
        for old, new in changes.items():
            file_old = QFileInfo(old)
            file_new = QFileInfo(new)
            if QFileInfo(self.root_folder).absoluteFilePath() == file_old.absolutePath():
                for i in range(self.thumbnail_view.count()):
                    item = self.thumbnail_view.item(i)
                    if item.text() == file_old.fileName():
                        item.setText(file_new.fileName())


class ThumbnailListWidget(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)

        """change the view mode to icon mode instead of list mode"""
        self.setViewMode(QListView.ViewMode.IconMode)

        """set the icon size"""
        self.icon_sizes = constants.BROWSER_THUMBNAIL_SIZES
        self.icon_size_index = constants.BROWSER_DEFAULT_THUMBNAIL_SIZE
        self.set_icon_size()

        """add spacing around and wrapping of the items. also set up for auto resize"""
        self.setSpacing(10)
        self.setWrapping(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)

        """set the view to allow multiple selection and disable drag and drop"""
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setDragEnabled(False)

    @pyqtSlot(str)
    def adjust_icon_size(self, direction):
        new_position = self.icon_size_index
        if direction == "+":
            new_position = self.icon_size_index + 1
        elif direction == "-":
            new_position = self.icon_size_index - 1

        """make sure we don't try to go out of bounds of our sizes list"""
        if new_position < 0 or new_position > len(self.icon_sizes) - 1:
            new_position = self.icon_size_index

        self.icon_size_index = new_position
        self.set_icon_size()

    def set_icon_size(self):
        """here we really set the iconSize, the view will update automatically"""
        size = self.icon_sizes[self.icon_size_index]
        self.setIconSize(QSize(size, size))
        self.setGridSize(QSize(size + 25, size + 25))
