from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QSizePolicy, QLayout, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath, QPolygon, QPolygonF
from PyQt5.QtCore import Qt, QPointF, QPoint
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
        self.count_label = 0
        self.x_coordinate = 0
        self.y_coordiante = 0

        self.fname = ""
        self.jfile = ""
        self.label_selected = ""
        self.label_loaded = False
        self.isFolder = False
        self.isJson = False

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
        self.actionNext_label.triggered.connect(self.nextLabel)
        self.actionBack_label.triggered.connect(self.backLabel)
        self.actionClose.triggered.connect(self.Close)

    def paintEvent(self, event):

        if not self.fname:
            return

        if (self.isFolder == True):
            painter = QPainter(self)
            original_pixmap = QPixmap(self.fname)
            scaled_pixmap = original_pixmap.scaled(1591, 904, aspectRatioMode=Qt.KeepAspectRatio)

            self.getCaculated_coordinates()

            painter.drawPixmap(QPointF(self.x_coordinate, self.y_coordiante), scaled_pixmap)
            
            if self.isJson:

                painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.SolidLine))
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

                if (self.label_loaded == True):
                    painter.setBrush(QColor(0, 255, 0, 120))
                    points2 = [QPointF(point[0], point[1]) for point in self.label_selected]
                    points = QPolygonF(points2)
                    painter.drawPolygon(points)

                # print("click")
            
            painter.end()

    def getCaculated_multiplier(self):
        original_pixmap = QPixmap(self.fname)
        return 904 / original_pixmap.height()
    
    def getCaculated_coordinates(self):
        original_pixmap = QPixmap(self.fname)
        scaled_pixmap = original_pixmap.scaled(1591, 904, aspectRatioMode=Qt.KeepAspectRatio)
        pixmap_rect = scaled_pixmap.rect()
        label_rect = self.ScreenPic.geometry()
        self.x_coordinate = label_rect.x() + (label_rect.width() - pixmap_rect.width()) / 2
        self.y_coordiante = label_rect.y() + (label_rect.height() - pixmap_rect.height()) / 2 + 26

    def loadJsonFile(self):
        f = open(self.jfile)
        data = json.load(f)

        self.saveJsonData(data)
        self.coordinates.clear()

        num = self.getCaculated_multiplier()
        
        self.getCaculated_coordinates()

        for label, points in self.points_with_labels:
            group_label = []
            for point in points:
                group_point = []
                group_point.append(point.x()*num + self.x_coordinate)
                group_point.append(point.y()*num + self.y_coordiante)
                group_label.append(group_point)
            self.coordinates.append(group_label)

        f.close()

    def openFile(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C\\' ,'Image files (*.jpg *.png)')
        self.directory = os.path.dirname(self.fname)
        # self.showPic()      

    def openFolder(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Open Folder')

        for filename in os.listdir(self.directory):
            if(filename.endswith('.jpg') or filename.endswith('.png')):
                self.file_path.append(os.path.join(self.directory, filename))

        self.fname = self.file_path[0]

        self.isFolder = True
        self.update()
        # self.showPic()

    def openJsonFiles(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Open Folder')
        for filename in os.listdir(self.directory):
            if(filename.endswith('.json')):
                self.json_path.append(os.path.join(self.directory, filename))

        self.jfile = self.json_path[0]

        self.loadJsonFile()
        self.isJson = True

        self.update()

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
        
        self.label_selected = []

        if (self.count < len(self.file_path) - 1):
            self.count += 1
        else:
            self.count = 0

        self.fname = self.file_path[self.count]

        if self.isJson:
            self.jfile = self.json_path[self.count]
            self.loadJsonFile()

        self.update()
        

    def backImage(self):

        self.label_selected = []

        if (self.count >= 1):
            self.count -= 1
        else:
            self.count = len(self.file_path) - 1

        self.ScreenPic.setPixmap(QtGui.QPixmap())

        self.fname = self.file_path[self.count]

        if self.isJson:
            self.jfile = self.json_path[self.count]
            self.loadJsonFile()
        
        self.update()

    def nextLabel(self):

        self.label_selected = []

        if (self.count_label < len(self.coordinates) - 1):
            self.count_label += 1
        else:
            self.count_label = 0

        self.label_selected = self.coordinates[self.count_label]
        
        
        self.label_loaded = True

        self.update()
    
    def backLabel(self):

        self.label_selected = []

        if (self.count_label >= 1):
            self.count_label -= 1
        else:
            self.count_label = len(self.coordinates) - 1

        self.label_selected = self.coordinates[self.count_label]

        self.label_loaded = True

        self.update()
    
    def Close(self):
        print('Close')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()