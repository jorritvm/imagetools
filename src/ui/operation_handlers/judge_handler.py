"""
Judge is a pure UI operation.
As such all of the logic is contained in this module.
There is no separate operation module for the file system operations.
"""
import os
from dataclasses import dataclass
from enum import Enum

from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtGui import QImage, QPixmap, QGuiApplication, QPalette
from PyQt6.QtWidgets import QMessageBox, QDialog, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy, QApplication

from threaded_resizer.threaded_resizer import Supervisor, ImageResizeTask
from ui import constants


def handle_judge(main_window):
    folder_select = main_window.folder_select
    browser_selection: list[QFileInfo] = main_window.browser.get_selection()
    resize_supervisor = main_window.supervisor  # this module will use the same threaded resize as the browser
    if len(browser_selection) == 0:
        QMessageBox.warning(main_window, "No selection", "Create a selection first.")
    else:
        """create the dialog"""
        dlg = JudgeDialog(browser_selection, resize_supervisor)
        dlg.exec()
        folder_select.force_refresh()


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"


class Marker(Enum):
    A = "A selection"
    B = "B selection"
    T = "Trash"
    E = "Empty"


@dataclass
class JudgedImage:
    """
    A JudgedImage holds all information about an image that is being judged. All of its file info, the thumbnail,
    the destination folder where it will be moved to, and the resize ticket number.
    """
    file_info: QFileInfo
    resize_ticket_number: int = None  # this will be provided by the supervisor when the image is resized
    thumbnail: QImage = None
    marker: Marker = None  # this will be set when marking the image
    marker_color: Qt.GlobalColor = None  # color for the marker, will be set based on the marker type
    destination_folder: str = None  # subfolder in which to place the judged image, e.g. "sel_a", "sel_b", or "trash"

    def has_thumbnail(self) -> bool:
        return self.thumbnail is not None

    def set_marker(self, marker: Marker):
        """Set the marker for this image and set the destination folder based on the marker."""
        self.marker = marker
        if marker == Marker.A:
            self.destination_folder = constants.JUDGE_FOLDER_NAME_MARKER_A
            self.marker_color = constants.JUDGE_MARKER_A_COLOR
        elif marker == Marker.B:
            self.destination_folder = constants.JUDGE_FOLDER_NAME_MARKER_B
            self.marker_color = constants.JUDGE_MARKER_B_COLOR
        elif marker == Marker.T:
            self.destination_folder = constants.JUDGE_FOLDER_NAME_MARKER_T
            self.marker_color = constants.JUDGE_MARKER_T_COLOR
        elif marker == Marker.E:
            # erase any marker
            self.destination_folder = None
            self.marker_color = None
            self.marker = None
        else:
            raise ValueError("Invalid marker type.")


class JudgeDialog(QDialog):
    """
    JudgeDialog is a dialog that allows the user to judge images by marking them with A, B, or T (trash).
    """

    def __init__(self, files: list[QFileInfo], supervisor: Supervisor, parent=None):
        """there is no designer UI file for this dialog, it is created programmatically"""
        QDialog.__init__(self, parent)
        self.judged_images: list[JudgedImage] = self.convert_files_to_judged_images(files)
        self.setup_ui()

        self.supervisor = supervisor
        self.supervisor.newItemReady.connect(self.process_next_resized_item)
        self.start_resize()

        self.current_judged_image_index: int = 0
        self.show_count = constants.INITIAL_IMAGES_COUNT_TO_JUDGE

        # self.file_handler = FileHandler()
        # self.file_handler.nextDone.connect(self.write_result)

    def setup_ui(self):
        """set up the dialog and make it as big as possible knowing the showMaximized() is bugged."""
        self.setModal(False)
        self.setWindowTitle("Judge: [1-9]: images shown, [A B T]: selections, [enter/escape]: confirm, cancel.")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        screen_geometry = QApplication.primaryScreen().geometry()
        w = screen_geometry.width() - 10
        h = screen_geometry.height() - 100
        x = 0
        y = 0
        self.setGeometry(x, y, w, h)

    def keyPressEvent(self, e):
        """Overwrite keypress handles"""
        if e.key() == Qt.Key.Key_1:
            self.adapt_count(1)
        if e.key() == Qt.Key.Key_2:
            self.adapt_count(2)
        if e.key() == Qt.Key.Key_3:
            self.adapt_count(3)
        if e.key() == Qt.Key.Key_4:
            self.adapt_count(4)
        if e.key() == Qt.Key.Key_5:
            self.adapt_count(5)
        if e.key() == Qt.Key.Key_6:
            self.adapt_count(6)
        if e.key() == Qt.Key.Key_7:
            self.adapt_count(7)
        if e.key() == Qt.Key.Key_8:
            self.adapt_count(8)
        if e.key() == Qt.Key.Key_9:
            self.adapt_count(9)
        if e.key() == Qt.Key.Key_Right:
            self.move(Direction.RIGHT)
        if e.key() == Qt.Key.Key_Left:
            self.move(Direction.LEFT)
        if e.key() == Qt.Key.Key_A:
            self.mark_image(Marker.A)
        if e.key() == Qt.Key.Key_B:
            self.mark_image(Marker.B)
        if e.key() == Qt.Key.Key_T:
            self.mark_image(Marker.T)
        if e.key() == Qt.Key.Key_E:
            self.mark_image(Marker.E)
        if e.key() == Qt.Key.Key_Enter or e.key() == Qt.Key.Key_Return:
            self.write_result()
        if e.key() == Qt.Key.Key_Escape:
            self.reject()

    def convert_files_to_judged_images(self, files: list[QFileInfo]) -> list[JudgedImage]:
        """Convert a list of QFileInfo objects to a list of JudgedImage objects."""
        judged_images = []
        for file_info in files:
            judged_image = JudgedImage(file_info=file_info)
            judged_images.append(judged_image)
        return judged_images

    def adapt_count(self, i):
        """Adapt the number of images shown simultaneously in the dialog."""
        self.show_count = i
        self.setup_judging()

    def move(self, direction: Direction):
        """Move to the next or previous image based on the pressed arrow key."""
        if direction == Direction.RIGHT:
            self.current_judged_image_index = min(len(self.judged_images) - 1, self.current_judged_image_index + 1)
        if direction == Direction.LEFT:
            self.current_judged_image_index = max(0, self.current_judged_image_index - 1)
        self.setup_judging()

    def mark_image(self, marker: Marker):
        judged_image = self.judged_images[self.current_judged_image_index]
        judged_image.set_marker(marker)
        self.move(Direction.RIGHT)  # move to the next image after marking

    def start_resize(self):
        """Build a resize jobqueue and send it to the supervisor."""
        job_queue = []
        for judged_image in self.judged_images:
            resize_task = ImageResizeTask(judged_image.file_info,
                                          QGuiApplication.primaryScreen().geometry().height(),
                                          True)  # smooth
            job_queue.append(resize_task)

        # store the ticket number in our judged_images
        parsed_job_queue = self.supervisor.add_items(job_queue, True)  # prior
        for ticketed_task in parsed_job_queue:
            for judged_image in self.judged_images:
                if judged_image.file_info == ticketed_task.file_info:
                    judged_image.resize_ticket_number = ticketed_task.ticket
                    break

        # kick of the resize process
        self.supervisor.process_queue()

    def process_next_resized_item(self, ticket, img):
        """
        Add the received thumbnail to the corresponding judged image based on the resize ticket number.
        This method is the connected slot for the supervisor's newItemReady signal.
        """
        for judged_image in self.judged_images:
            if judged_image.resize_ticket_number == ticket:
                # set the thumbnail for the judged image
                judged_image.thumbnail = img
                break
        self.setup_judging()

    def verify_if_ui_is_ready_for_judging(self) -> bool:
        """Check if the UI is ready to show all the thumbnails based on the current judging item and show count."""
        subset_of_judged_images = self.get_subset_of_judged_images()
        return all([judged_image.has_thumbnail() for judged_image in subset_of_judged_images])

    def setup_judging(self):
        """Set up the judging UI by showing the thumbnails of the images."""
        if self.verify_if_ui_is_ready_for_judging():
            self.wipe_layout()
            target_width = int(self.size().width() / self.show_count - 25)
            target_heigth = int(self.size().height() - 45)
            subset_of_judged_images = self.get_subset_of_judged_images()
            for judged_image in subset_of_judged_images:
                # create a filename label
                top_widget = QLabel()
                top_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
                top_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
                file_name = judged_image.file_info.fileName()
                if judged_image.marker:
                    top_widget.setText(file_name + " >> " + judged_image.destination_folder)
                    pal = top_widget.palette()
                    pal.setColor(QPalette.ColorRole.WindowText, judged_image.marker_color)  # change text color
                    top_widget.setPalette(pal)
                else:
                    top_widget.setText(file_name)
                # create a thumbnail label
                bottom_widget = QLabel("End of list...")
                pixmap = QPixmap.fromImage(judged_image.thumbnail)
                pixmap_scaled = pixmap.scaled(target_width, target_heigth, Qt.AspectRatioMode.KeepAspectRatio)
                bottom_widget.setPixmap(pixmap_scaled)
                # add both to the central layout
                vbox = QVBoxLayout()
                vbox.addWidget(top_widget)
                vbox.addWidget(bottom_widget)
                self.layout.addLayout(vbox)

    def get_subset_of_judged_images(self):
        """Returns only the judged images that should be shown on the UI."""
        start = self.current_judged_image_index
        end = min(start + self.show_count, len(self.judged_images))  # do not exceed the list length
        return self.judged_images[start:end]

    def wipe_layout(self, layout=None):
        """Clear layout by deleting all its items (widgets and sublayouts) recursively."""
        if layout == None:
            layout = self.layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout:
                    self.wipe_layout(sublayout)

    def write_result(self):
        """Move the marked images to their destination folders. Ask for user confirmation first!"""
        count_of_marked_images = len([img for img in self.judged_images if img.marker is not None])
        answer = QMessageBox.question(self, 'Judge Result',
                                      f'Are you ready to move {count_of_marked_images} marked images?', )
        if answer != QMessageBox.StandardButton.Yes:
            return
        else:
            for judged_image in self.judged_images:
                if judged_image.marker is not None:
                    # create the destination folder if it does not exist
                    old_folder_path = judged_image.file_info.absolutePath()
                    new_folder_path = old_folder_path + "/" + judged_image.destination_folder
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path, exist_ok=True)

                    # move the file to the destination folder
                    old_file_path = judged_image.file_info.absoluteFilePath()
                    new_file_path = new_folder_path + "/" + judged_image.file_info.fileName()
                    if not os.path.exists(new_file_path):
                        os.rename(old_file_path, new_file_path)
                    else:
                        QMessageBox.warning(self, "File exists",
                                            f"File {new_path} already exists, skipping move operation.")
            # finally close the dialog
            self.accept()
