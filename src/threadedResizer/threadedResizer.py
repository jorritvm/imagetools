'''
Created on 4-sep.-2013

@author: jorrit
'''
#===============================================================================
# usage:
#===============================================================================         
# self.supervisor = Supervisor(self.settings['nThreads'], self)
# self.supervisor.newItemReady.connect(self.perform)
# q = []
# q.append('QFileInfo', size in int, True/false for priority])
# self.supervisor.addItems(q)
# self.supervisor.processQueue()
#===============================================================================

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from msilib.schema import SelfReg


class Supervisor(QObject):
    
    newItemReady = pyqtSignal(int, QImage)
    
    def __init__(self,  nThreads, parent=None):
        QObject.__init__(self,parent)
        self.parent = parent
        self.queue = [] # lists [ [fileinfo, size, fast, ticket], ...]
        self.createThreads(nThreads)
        self.ticketCounter = 0
        
        
    def createThreads(self, nThreads):
        self.nThreads = nThreads
        self.threads = []
        for i in range(self.nThreads):
                x =  Worker()
                x.resizeDone.connect(self.processResult) 
                self.threads.append(x)
        
    def addItems(self, newImages, prior = False): #argument 1: [ [fileinfo, size, fast, ticket], ...] argument 2: prior true/false
        for item in newImages:
            self.ticketCounter += 1
            item.append(self.ticketCounter)

        if prior:
            self.queue = newImages + self.queue
        else:
            self.queue = self.queue + newImages
      
        return newImages #this time ticket has been added
               
        
    def clearQueue(self):
        self.queue = []

            
    def processQueue(self):
        for thread in self.threads:
            if not thread.isRunning() and len(self.queue) > 0:
                item = self.queue.pop(0)
                thread.initialize(item)
                thread.start()
                    
    
    def processResult(self, ticket, resizedImage):
        #emitting it
        self.newItemReady.emit(ticket, resizedImage)
    
        #on to the next item
        self.processQueue()
        
    
    
class Worker(QThread):
    
    resizeDone = pyqtSignal(int, QImage)
    
    def __init__(self,  parent=None):
        QThread.__init__(self, parent)
        self.parent = parent

           
    def initialize(self, item):
        self.fileinfo = item[0]
        self.size = item[1]
        if item[2]:
            self.fast = Qt.FastTransformation
        else:
            self.fast = Qt.SmoothTransformation
        self.ticket = item[3]

    def run(self):
        img = QImage(self.fileinfo.absoluteFilePath())
        try:
            img = img.scaled(self.size, self.size, Qt.KeepAspectRatio, self.fast) 
            self.resizeDone.emit(self.ticket, img) 
        finally:
            pass
        