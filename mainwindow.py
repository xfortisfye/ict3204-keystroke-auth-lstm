import os
import sys
import shutil
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from train_model_worker import TrainModelWorker
from create_model import CreateModel
from receiver_worker import ReceiverWorker
from queue import Queue

ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))

class UiMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        # call the inherited classes __init__ method
        super(UiMainWindow, self).__init__()

        # launch mainwindow.ui file
        uic.loadUi(f"{ABSOLUTE_PATH}/mainwindow.ui", self)

        # set gui window size
        self.setMinimumSize(QtCore.QSize(1280, 820))
        self.setMaximumSize(QtCore.QSize(1280, 820))

        self.import_csv_button.clicked.connect(lambda: self.importCSVDialog())

        self.threadpool = QtCore.QThreadPool()
        self.train_model_thread = None
        self.receiver_thread = None
        
        # Create Queue and redirect sys.stdout to this queue
        self.queue = Queue()
        sys.stdout = WriteStream(self.queue)

    # launch QFileDialog to import APK for obfuscation
    def importCSVDialog(self):
        # generate dialog window to obtain apk url
        epoch_time = int(self.input_epoch.text())
        batch_size = int(self.input_batch.text())
        num_fold = int(self.input_fold.text())
        csvUrl, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv)")

        if csvUrl:
            self.train_model_thread = TrainModelWorker(csvUrl, epoch_time, batch_size, num_fold)
            self.train_model_thread.signals.accuracy.connect(self.print_acc)
            self.train_model_thread.signals.data.connect(self.print_data)
            self.train_model_thread.signals.console.connect(self.print_console)
            self.train_model_thread.start()
            
            # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
            self.receiver_thread = ReceiverWorker(self.queue)
            self.receiver_thread.signals.logging.connect(self.print_log)
            self.receiver_thread.start()
        else:
            pass
        #     self.printLogs(WARNING, "No APK has been imported to decompile.")

    def isSignalConnected(self, obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False
        
    def print_acc(self, message):
        self.acc_display.append(message)
    def print_data(self, message):
        self.data_display.append(message)
    def print_log(self, message):
        self.log_display.append(message)
    def print_console(self, message):
        self.console_display.append(message)

    # def printLogs(self, mode, logs):
    #     if mode == SYSTEM:
    #         self.display_logs.moveCursor(QtGui.QTextCursor.End)
    #         self.display_logs.setTextColor(QtCore.Qt.green)
    #         self.display_logs.setTextBackgroundColor(QtCore.Qt.black)
    #         self.display_logs.append(" SYSTEM :")
    #         self.display_logs.setTextColor(QtCore.Qt.black)
    #         self.display_logs.setTextBackgroundColor(QtCore.Qt.white)
    #         self.display_logs.insertPlainText(" " + logs)
    #         self.display_logs.ensureCursorVisible()
    #     elif mode == WARNING:
    #         self.display_logs.moveCursor(QtGui.QTextCursor.End)
    #         self.display_logs.setTextColor(QtCore.Qt.red)
    #         self.display_logs.setTextBackgroundColor(QtCore.Qt.black)
    #         self.display_logs.append("WARNING:")
    #         self.display_logs.setTextColor(QtCore.Qt.red)
    #         self.display_logs.setTextBackgroundColor(QtCore.Qt.white)
    #         self.display_logs.insertPlainText(" " + logs)
    #         self.display_logs.ensureCursorVisible()
    #     elif mode == LOADING:
    #         self.display_logs.moveCursor(QtGui.QTextCursor.End)
    #         self.display_logs.setTextColor(QtCore.Qt.yellow)
    #         self.display_logs.setTextBackgroundColor(QtCore.Qt.black)
    #         self.display_logs.append(" LOADING ")
    #         self.display_logs.ensureCursorVisible()
    #     elif mode == LOADER:
    #         self.display_logs.moveCursor(QtGui.QTextCursor.End)
    #         self.display_logs.setTextColor(QtCore.Qt.yellow)
    #         self.display_logs.setTextBackgroundColor(QtCore.Qt.black)
    #         self.display_logs.insertPlainText(logs)
    #         self.display_logs.ensureCursorVisible()
    #     elif mode == COMPLETED:
    #         self.display_logs.moveCursor(QtGui.QTextCursor.End)
    #         self.display_logs.setTextColor(QtCore.Qt.yellow)
    #         self.display_logs.setTextBackgroundColor(QtCore.Qt.black)
    #         self.display_logs.insertPlainText("COMPLETED.")
    #         self.display_logs.ensureCursorVisible()
    #     else:
    #         self.display_logs.moveCursor(QtGui.QTextCursor.End)
    #         self.display_logs.append(logs)
    #         self.display_logs.ensureCursorVisible()

    def thread_complete(self, url):
        # if function == "importApk":
        #     self.import_apk_button.setEnabled(True)
        #     self.obf_package_button.setEnabled(True)
        #     self.obf_smali_button.setEnabled(True)
        #     self.export_apk_button.setEnabled(True)
        #     self.display_ori_tree.setEnabled(True)
        #     self.display_obf_tree.setEnabled(True)
        #     self.obf_package_button.clicked.connect(lambda checked: self.importPackageDialog(None))
        #     self.obf_smali_button.clicked.connect(lambda checked: self.importSmaliDialog(None))
        #     self.export_apk_button.clicked.connect(lambda checked, name=name: self.exportApkDialog(name))
        #     self.displayTreeFiles(ORIGINAL_PATH, self.display_ori_tree, self.display_ori_text, ORIGINAL)
        #     self.displayTreeFiles(OBFUSCATE_PATH, self.display_obf_tree, self.display_obf_text, OBFUSCATED)
        #     self.timer.stop()
        #     self.printLogs(COMPLETED, "")
        #     self.printLogs(SYSTEM, "Decompiled completed.")
        #     self.printLogs(SYSTEM, "Please select package that you want to obfuscate.")
        # elif function == "importPackage":
        #     self.import_apk_button.setEnabled(True)
        #     self.obf_package_button.setEnabled(True)
        #     self.obf_smali_button.setEnabled(True)
        #     self.export_apk_button.setEnabled(True)
        #     self.display_ori_tree.setEnabled(True)
        #     self.display_obf_tree.setEnabled(True)
        #     self.timer.stop()
        #     self.printLogs(COMPLETED, "")
        #     self.printLogs(SYSTEM, name + " has been obfuscated.")
        # elif function == "importSmali":
        #     self.import_apk_button.setEnabled(True)
        #     self.obf_package_button.setEnabled(True)
        #     self.obf_smali_button.setEnabled(True)
        #     self.export_apk_button.setEnabled(True)
        #     self.display_ori_tree.setEnabled(True)
        #     self.display_obf_tree.setEnabled(True)
        #     self.timer.stop()
        #     self.printLogs(COMPLETED, "")
        #     self.printLogs(SYSTEM, name + " has been obfuscated.")
        # elif function == "exportApk":
        #     self.import_apk_button.setEnabled(True)
        #     self.obf_package_button.setEnabled(True)
        #     self.obf_smali_button.setEnabled(True)
        #     self.export_apk_button.setEnabled(True)
        #     self.display_ori_tree.setEnabled(True)
        #     self.display_obf_tree.setEnabled(True)
        #     self.timer.stop()
        #     self.printLogs(COMPLETED, "")
        #     self.printLogs(SYSTEM, "Exported Signed-APK: exported-apk/" + name)
        print("hey")

    @ staticmethod
    def clear():
        # Clear all the files
        if os.path.exists("__pycache__/"):
            shutil.rmtree("__pycache__/")


# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        pass