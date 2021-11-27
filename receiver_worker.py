from PyQt5 import QtCore

import traceback
import sys
# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal 

class WorkerSignals(QtCore.QObject):
    logging = QtCore.pyqtSignal(str)

class ReceiverWorker(QtCore.QThread):
    def __init__(self, queue):
        super(ReceiverWorker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.queue = queue
        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            message = self.queue.get()
            self.signals.logging.emit(message)
