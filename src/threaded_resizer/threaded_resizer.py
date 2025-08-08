"""
threaded_resizer.py

This module provides a supervisor-worker pattern for threaded image resizing using PyQt6.
It allows you to add new image resize tasks to the start or end of the queue.
The Supervisor manages a fixed number of worker threads. As long as the queue is filled, it sends new tasks to the workers.
The resize tasks are processed concurrently by worker threads. When these are ready with an image they emit a signal
which the supervisor handles sequentially thereby avoiding any race conditions on the queue.

Usage example:
    from threaded_resizer import Supervisor, ImageResizeTask
    from PyQt6.QtCore import QFileInfo

    supervisor = Supervisor(n_threads=4)
    tasks = [
        ImageResizeTask(QFileInfo("image1.jpg"), img_size=256, fast=False, ticket=0),
        ImageResizeTask(QFileInfo("image2.jpg"), img_size=128, fast=True, ticket=0)
    ]
    supervisor.add_items(tasks)
    supervisor.newItemReady.connect(handle_resized_image)
    supervisor.process_queue()
"""
from dataclasses import dataclass

from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, QThread, QFileInfo, Qt
from PyQt6.QtGui import QImage


@dataclass
class ImageResizeTask:
    file_info: QFileInfo
    img_size: int  # Size to resize the image to
    fast: bool  # If True, use fast transformation mode
    ticket: int


class Supervisor(QObject):
    """
    The Supervisor class manages a queue of image resize tasks and a fixed number of worker threads.
    """
    newItemReady = pyqtSignal(int, QImage)

    def __init__(self, n_threads, parent=None):
        QObject.__init__(self, parent)
        self.queue: list[ImageResizeTask] = []
        self.n_workers: int = n_threads
        self.workers: list[Worker] = []
        self.ticket_counter: int = 0
        self.create_threads()

    def create_threads(self) -> None:
        """
        Create a fixed number of worker threads and connect their signal to the process_result method.
        Because the results are processed sequentially, there is no race condition on the queue.
        """
        for i in range(self.n_workers):
            new_worker = Worker(self)
            new_worker.resize_done.connect(self.process_result)
            self.workers.append(new_worker)

    def clear_queue(self) -> None:
        self.queue = []

    def add_items(self, new_images: list[ImageResizeTask], prior: bool = False) -> list[ImageResizeTask]:
        """Add items to the queue. If prior is True, the new images will be added to the front of the queue."""
        for image_resize_task in new_images:
            self.ticket_counter += 1
            image_resize_task.ticket = self.ticket_counter

        if prior:
            self.queue = new_images + self.queue
        else:
            self.queue = self.queue + new_images

        return new_images  # this time ticket has been added

    def process_queue(self) -> None:
        """Process the queue by sending new jobs to workers that are not running as long as the queue is filled."""
        for worker in self.workers:
            if not worker.isRunning() and len(self.queue) > 0:
                item = self.queue.pop(0)
                worker.set_image_to_convert(item)
                worker.start()

    @pyqtSlot(int, QImage)
    def process_result(self, ticket, resized_image: QImage) -> None:
        self.newItemReady.emit(ticket, resized_image)
        self.process_queue()


class Worker(QThread):
    """
    Worker class that performs the image resizing in a separate thread.
    It emits a signal when the resizing is done, providing the ticket number and the resized QImage.
    This allows the Supervisor to handle the resized image without blocking the main thread.
    """
    resize_done = pyqtSignal(int, QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.image_resize_task: ImageResizeTask = None

    def set_image_to_convert(self, item: ImageResizeTask) -> None:
        self.image_resize_task = item

    def run(self) -> None:
        image_original = QImage(self.image_resize_task.file_info.absoluteFilePath())
        size = self.image_resize_task.img_size
        speed = Qt.TransformationMode.SmoothTransformation
        if self.image_resize_task.fast:
            speed = Qt.TransformationMode.FastTransformation
        image_resized = image_original.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, speed)
        self.resize_done.emit(self.ticket, image_resized)
