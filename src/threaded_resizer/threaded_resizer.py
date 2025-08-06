# ===============================================================================
# information:
#
# Upon creation of a single supervisor it will create a fixed amount of workers.
# With add_items, you provide the supervisor with items to resize. It will put these
# in the queue, and immediately provide the client with tickets for every item.
# When processQueue is called, every time an item in the queue is ready the
# newItemReady signal is emited consisting of the ticket number and the resized
# QImage.
#
#
# usage:
#
# self.supervisor = Supervisor(self.settings['n_threads'], self)
# self.supervisor.newItemReady.connect(self.perform)
# q = []
# q.append('QFileInfo', size in int, True/False for priority])
# self.supervisor.addItems(q)
# self.supervisor.processQueue()
# ===============================================================================

from PyQt6.QtCore import *
from PyQt6.QtGui import *


class Supervisor(QObject):
    newItemReady = pyqtSignal(int, QImage)

    def __init__(self, n_threads, parent=None):
        QObject.__init__(self, parent)
        self.parent = parent
        self.queue = []  # lists [ [fileinfo, size, fast, ticket], ...]

        self.n_threads = n_threads
        self.threads = []
        self.create_threads()

        self.ticket_counter = 0

    def create_threads(self):
        for i in range(self.n_threads):
            x = Worker()
            x.resize_done.connect(self.process_result)
            self.threads.append(x)

    def add_items(self, new_images, prior=False):
        """
            new_images: [ [fileinfo, img_size, fast, ticket], ...]
            prior: true/false
        """
        for item in new_images:
            self.ticket_counter += 1
            item.append(self.ticket_counter)

        if prior:
            self.queue = new_images + self.queue
        else:
            self.queue = self.queue + new_images

        return new_images  # this time ticket has been added

    def clear_queue(self):
        self.queue = []

    def process_queue(self):
        for thread in self.threads:
            if not thread.isRunning() and len(self.queue) > 0:
                item = self.queue.pop(0)
                thread.set_image_to_convert(item)
                thread.start()

    def process_result(self, ticket, resized_image):
        self.newItemReady.emit(ticket, resized_image)  # emit to client
        self.process_queue()  # get on with the rest of the queue


class Worker(QThread):
    resize_done = pyqtSignal(int, QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.file_info = QFileInfo()
        self.size = 0
        self.speed = Qt.TransformationMode.SmoothTransformation
        self.ticket = 0  # value should be overwritten in initialize

    def set_image_to_convert(self, item):
        """ set an item for this worker """
        self.file_info = item[0]
        self.size = item[1]
        if item[2]:
            self.speed = Qt.TransformationMode.FastTransformation
        else:
            self.speed = Qt.TransformationMode.SmoothTransformation
        self.ticket = item[3]

    def run(self):
        """ do the work when thread.start() is called """
        img = QImage(self.file_info.absoluteFilePath())
        try:
            img = img.scaled(self.size, self.size, Qt.KeepAspectRatio, self.speed)
            self.resize_done.emit(self.ticket, img)
        finally:
            pass
