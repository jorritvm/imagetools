'''
Created on 4-sep.-2013

@author: jorrit
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from threaded_resizer import *
import time

    
class a(QObject):
    def __init__(self, parent = None):
        QObject.__init__(self,parent)
        self.start = time.time()
        self.l = []                    
        sup = Supervisor(4, self)
        sup.newItemReady.connect(self.perform)

        q = []
        for i in range(1,57): #zorg dat jpg's 01 tot 56 in de folder staan voor TEST 
            q.append([QFileInfo('pics/' + str(i).zfill(2)  + '.jpg'), 300, True])
        print('ex: new piece of queue: ' + str(q))
        sup.add_items(q)
        sup.process_queue()
        
    def perform(self, ticket, img):
        print("ex: received & showing scaled item with ticket " + str(ticket))
        lb = QLabel()
        lb.setPixmap(QPixmap(img))
        #lb.show()
        self.l.append(lb)
        print("time passed: " + str(round(time.time() - self.start,2)) + "s")
    
if __name__ == "__main__":
    
    import sys
    app = QApplication(sys.argv)
    a = a()
   
    
    sys.exit(app.exec_())
        