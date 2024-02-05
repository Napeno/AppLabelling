from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QSizePolicy, QLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys
import os

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("main.ui", self)
        self.fname = ""
        self.directory = ""
        self.file_path = []
        self.count = 0
        self.actionOpen_File.triggered.connect(self.openFile)
        self.actionOpen_Folder.triggered.connect(self.openFolder)
        self.actionOpen_Recent.triggered.connect(self.openRecent)
        self.actionSave.triggered.connect(self.Save)
        self.actionSave_as.triggered.connect(self.saveAs)
        self.actionSave_Automatically.triggered.connect(self.saveAuto)
        self.actionChange_output_folder.triggered.connect(self.changeOutput)
        self.actionNext_Image.triggered.connect(self.nextImage)
        self.actionBack_Image.triggered.connect(self.backImage)
        self.actionClose.triggered.connect(self.Close)

    def showPic(self, fname):
        original_pixmap = QPixmap(fname)
        self.ScreenPic.setPixmap(original_pixmap.scaled(1591, 904, aspectRatioMode=Qt.KeepAspectRatio))

    def openFile(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C\\' ,'Image files (*.jpg *.png)')
        self.directory = os.path.dirname(self.fname)
        self.showPic(self.fname)      

    def openFolder(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Open Folder')
        print(self.directory)
        for filename in os.listdir(self.directory):
            if(filename.endswith('.jpg') or filename.endswith('.png')):
                self.file_path.append(os.path.join(self.directory, filename))
        self.showPic(self.file_path[0])

        

    def openRecent(self):
        print('Open Recent')

    def Save(self):
        print('Save')

    def saveAs(self):
        print('Save As')

    def saveAuto(self):
        print('Save Auto')
    
    def changeOutput(self):
        print('Change Output')

    def nextImage(self):
        if (self.count < len(self.file_path) - 1):
            self.count += 1
        else:
            self.count = 0
        
        self.showPic(self.file_path[self.count])
        

    def backImage(self):
        if (self.count >= 1):
            self.count -= 1
        else:
            self.count = len(self.file_path) - 1
        
        self.showPic(self.file_path[self.count])
    
    def Close(self):
        print('Close')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()