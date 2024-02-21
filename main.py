from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QSizePolicy, QLayout, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF
from PyQt5.uic import loadUi                                                            
import sys
import os
import json

class Main(QMainWindow, QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("main.ui", self)

        # Diretory
        self.fname = ""
        self.directory = ""
        self.file_path = []
        self.json_path = []
        self.count = 0

        self.fname = ""
        self.jfile = ""
        self.json_loaded = False

        # Shapes inside Json data
        self.shapes = []
        self.label = []
        self.text = []
        self.points = []
        self.group_id = []
        self.shape_type = []
        self.flags = []
        # self.x_coordinates = []
        # self.y_coordinates = []
        # self.group_label =[]
        self.group_point = []
        self.points_with_labels = []
        self.coordinates = []

        self.actionOpen_File.triggered.connect(self.openFile)
        self.actionOpen_Folder.triggered.connect(self.openFolder)
        self.actionOpen_Recent.triggered.connect(self.openRecent)
        self.actionSave.triggered.connect(self.Save)
        self.actionSave_as.triggered.connect(self.saveAs)
        self.actionSave_Automatically.triggered.connect(self.saveAuto)
        self.actionChange_output_folder.triggered.connect(self.openJsonFiles)
        self.actionNext_Image.triggered.connect(self.nextImage)
        self.actionBack_Image.triggered.connect(self.backImage)
        self.actionClose.triggered.connect(self.Close)

    def paintEvent(self, event):
        if not self.fname:
            return

        painter = QPainter(self.ScreenPic.pixmap())

        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        
        for group_label in self.coordinates:
            j = 0
            while (j < len(group_label) - 1):
                p1 = QPointF(group_label[j][0], group_label[j][1])
                p2 = QPointF(group_label[j+1][0], group_label[j+1][1])
                painter.drawLine(p1, p2)
                j += 1
            p1 = QPointF(group_label[0][0], group_label[0][1])
            p2 = QPointF(group_label[len(group_label) - 1][0], group_label[len(group_label) - 1][1])
            painter.drawLine(p1, p2)
        

        painter.end()

    def showPic(self):
        original_pixmap = QPixmap(self.fname)
        # print(original_pixmap.width())
        # print(original_pixmap.height())
        self.ScreenPic.setPixmap(original_pixmap.scaled(1591, 904, aspectRatioMode=Qt.KeepAspectRatio))
        self.ScreenPic.update()

    def getCaculated_coordinates(self):
        original_pixmap = QPixmap(self.fname)
        return 904 / original_pixmap.height()


    def loadJsonFile(self):
        f = open(self.jfile)
        data = json.load(f)

        self.saveJsonData(data)
        self.coordinates.clear()

        num = self.getCaculated_coordinates()

        for label, points in self.points_with_labels:
            group_label = []
            for point in points:
                group_point = []
                group_point.append(point.x()*num)
                group_point.append(point.y()*num)
                group_label.append(group_point)
            self.coordinates.append(group_label)

        f.close()


    def openFile(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C\\' ,'Image files (*.jpg *.png)')
        self.directory = os.path.dirname(self.fname)
        self.showPic()      

    def openFolder(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Open Folder')
        for filename in os.listdir(self.directory):
            if(filename.endswith('.jpg') or filename.endswith('.png')):
                self.file_path.append(os.path.join(self.directory, filename))
        self.fname = self.file_path[0]
        self.showPic()

    def openJsonFiles(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Open Folder')
        for filename in os.listdir(self.directory):
            if(filename.endswith('.json')):
                self.json_path.append(os.path.join(self.directory, filename))

        self.jfile = self.json_path[0]

        self.loadJsonFile()
            
        # print(self.coordinates)

        # for shape_points in self.points:
        #     for point in shape_points:
        #         self.x_coordinates.append(point.x()*2.71)
        #         self.y_coordinates.append(point.y()*2.71)

    def saveJsonData(self, data):

        self.points_with_labels.clear()
        self.points_with_labels = []

        for shape in data['shapes']:
            label = shape['label']
            points = [QPointF(point[0], point[1]) for point in shape['points']]
            self.points_with_labels.append((label, points))

        for self.shapes in data['shapes']:
            self.label.append(self.shapes['label'])
            self.text.append(self.shapes['text'])
            # self.points.append([QPointF(point[0], point[1]) for point in self.shapes['points']])
            self.group_id.append(self.shapes['group_id'])
            self.shape_type.append(self.shapes['shape_type'])
            self.flags.append(self.shapes['flags'])

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
        
        self.ScreenPic.setPixmap(QtGui.QPixmap())

        self.fname = self.file_path[self.count]
        self.jfile = self.json_path[self.count]

        
        self.showPic()
        self.loadJsonFile()
        

    def backImage(self):
        if (self.count >= 1):
            self.count -= 1
        else:
            self.count = len(self.file_path) - 1

        self.ScreenPic.setPixmap(QtGui.QPixmap())

        self.fname = self.file_path[self.count]
        self.jfile = self.json_path[self.count]

        self.ScreenPic.setPixmap(QtGui.QPixmap())
        
        self.showPic()
        self.loadJsonFile()
    
    def Close(self):
        print('Close')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()