from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLineEdit, QDialog, QPushButton, QListWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QPolygonF, QIcon
from PyQt5.QtCore import Qt, QPointF
from PyQt5.uic import loadUi                                                            
import sys
import numpy as np
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
        self.data = ""
        self.label_loaded = False
        self.isFolder = False
        self.isJson = False
        self.doneEdit = True

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
        self.actionEdit_Label.triggered.connect(self.editLabel)
        self.actionClose.triggered.connect(self.Close)
        
        #Widgets
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.hide()

        # self.doneButton = QPushButton('Done' ,self.centralwidget)
        # self.doneButton.hide()

        # self.cancleButton = QPushButton('Cancle', self.centralwidget)
        # self.cancleButton.setText('Cancle')
        # self.cancleButton.hide()

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
    
    # def getLineEdit_location(self):

    def loadJsonFile(self):
        f = open(self.jfile)

        self.data = json.load(f)

        self.saveJsonData(self.data)
        print(self.text)
        self.coordinates.clear()

        num = self.getCaculated_multiplier()
        
        self.getCaculated_coordinates()

        for label, points in self.points_with_labels:
            group_label = []
            for point in points:
                group_point = []
                group_point.append(point.x()*num + self.x_coordinate)
                group_point.append(point.y()*num + self.y_coordiante)
                # group_point.append(point.x())
                # group_point.append(point.y())
                group_label.append(group_point)
            self.coordinates.append(group_label)

        f.close()

    def openFile(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C\\' ,'Image files (*.jpg *.png)')
        self.directory = os.path.dirname(self.fname)
        # self.showPic()      

    def openFolder(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if self.directory == '':
            return
        for filename in os.listdir(self.directory):
            if(filename.endswith('.jpg') or filename.endswith('.png')):
                self.file_path.append(os.path.join(self.directory, filename))

        self.fname = self.file_path[0]

        self.isFolder = True
        self.update()
        # self.showPic()

    def openJsonFiles(self):
        self.directory = QFileDialog.getExistingDirectory(self, 'Open Folder')

        if self.directory == '':
            return

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
        if self.isFolder:
            self.label_selected = []

            self.count_label = 0

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
        if self.isFolder:
            self.label_selected = []

            self.count_label = 0

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
        if self.isJson:
            self.label_selected = []

            if (self.count_label < len(self.coordinates) - 1):
                self.count_label += 1
            else:
                self.count_label = 0

            self.label_selected = self.coordinates[self.count_label]

            self.label_loaded = True

            self.update()
    
    def backLabel(self):
        if self.isJson:
            self.label_selected = []

            if (self.count_label >= 1):
                self.count_label -= 1
            else:
                self.count_label = len(self.coordinates) - 1

            self.label_selected = self.coordinates[self.count_label]

            self.label_loaded = True

            self.update()

    def editLabel(self):
        max_x_value = max(self.label_selected, key=lambda x: x[0])
        # min_x_value = min(self.label_selected, key=lambda x: x[0])
        min_y_value = min(self.label_selected, key=lambda y: y[1])
        
        left_coordinate = (max_x_value[0]) + 10
        top_coordinate = min_y_value[1]

        self.text = []

        # for shape in self.shapes:
        for shape in self.data['shapes']:
            if(int(self.count_label + 1) == int(shape["label"])):
                self.text = shape["text"]

        pop = Popup(int(left_coordinate), int(top_coordinate), self.count_label + 1, self.text, self.jfile, self)
        pop.show()

    def Close(self):
        print('Close')

class Popup(QDialog):
    def __init__(self, a, b, labelIndex, texts, jfile, parent):
        super().__init__(parent)
        self.exit_edit = False
        self.setWindowTitle("Label " + str(labelIndex))
        self.setGeometry(a, b, 300, 240)

        self.labelIndex = labelIndex
        self.jfile = jfile
        self.countLabel = 0
        self.checkUpdate = False
        self.clicked_text = ""
        self.clicked_index = 0
        self.textStored = []

        # Text
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(10, 10, 280, 30)
        self.lineEdit.show()

        # Add New Label Button
        self.newButton = QPushButton(self, default = False, autoDefault = False)
        self.newButton.setObjectName(u"newButton")
        self.newButton.setIcon(QIcon('./icons/add.png'))
        self.newButton.setGeometry(50, 45, 30, 30)
        self.newButton.clicked.connect(self.newLabel)

        # Delete Label Button
        self.deleteButton = QPushButton(self, default = False, autoDefault = False)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setIcon(QIcon('./icons/delete.png'))
        self.deleteButton.setGeometry(85, 45, 30, 30)
        self.deleteButton.clicked.connect(self.deleteLabel)

        # Finish Edit Button
        self.doneButton = QPushButton(self, default = False, autoDefault = False)
        self.doneButton.setObjectName(u"doneButton")
        self.doneButton.setText('Done')
        self.doneButton.setGeometry(120, 45, 80, 30)
        self.doneButton.clicked.connect(self.doneButtonEvent)
    
        # Cancle Button
        self.cancleButton = QPushButton(self, default = False, autoDefault = False)
        self.cancleButton.setObjectName(u"cancleButton")
        self.cancleButton.setText('Cancle')
        self.cancleButton.setGeometry(205, 45, 80, 30)
        self.cancleButton.clicked.connect(self.cancleButtonEvent)

        # List View Items
        self.list_widget = QListWidget(self)
        self.list_widget.setObjectName(u"list_widget")
        self.list_widget.setGeometry(10, 80, 280, 140)
        self.list_widget.clicked.connect(self.itemClicked)

        # Load texts to list view
        self.loadText(texts)


    def keyPressEvent(self, e):
        if e.key() == 16777220 and not e.modifiers():
            self.handleAction()
        if e.key() == 16777219 and  e.modifiers() & Qt.ControlModifier:
            self.cancleButtonEvent()
        if e.key() == 16777220 and e.modifiers() & Qt.ControlModifier:
            self.doneButtonEvent()
        else:
            super().keyPressEvent(e)

    def doneButtonEvent(self):
        # print('Button Done pushed')

        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            self.textStored.append(item.text())

        self.write_json(self.textStored, self.jfile)

        Popup.hide(self)

    def cancleButtonEvent(self):
        # print('Cancle Button pushed')
        Popup.hide(self)

    def write_json(self, texts, filename):
        with open(filename, 'r') as file:
            file_data = json.load(file)
            for shape in file_data["shapes"]:
                if (int(shape["label"]) == int(self.labelIndex)):
                    for text in texts:
                        if text not in shape['text']:
                            shape["text"].append(text)
        with open(filename, 'w') as file:
            json.dump(file_data, file, indent=2)
    
    def handleAction(self):
        if (self.checkUpdate):
            self.updateLabel(self.clicked_index, self.lineEdit.text())
        else:
            self.insertLabel(self.lineEdit.text())
        self.lineEdit.clear()

    def newLabel(self):
        self.lineEdit.clear()
        self.lineEdit.setFocus()
        self.list_widget.clearSelection()
        self.checkUpdate = False
    
    def deleteLabel(self):
        self.lineEdit.clear()
        self.lineEdit.clearFocus()
        row = self.clicked_index.row()
        self.list_widget.model().removeRow(row)

    def insertLabel(self, item):
        self.list_widget.insertItem(self.countLabel, item)
        self.countLabel += 1

    def updateLabel(self, pos, item):
        row = pos.row()
        self.list_widget.item(row).setText(item)
        self.list_widget.clearSelection()
        self.checkUpdate = False
    
    def loadText(self, texts):
        for i in range(0, len(texts) - 1):
            self.list_widget.insertItem(i, texts[i])

    def itemClicked(self):
        self.clicked_text = self.list_widget.currentItem()
        self.clicked_index = self.list_widget.currentIndex()

        self.lineEdit.setText(self.clicked_text.text())
        self.lineEdit.setFocus()
        self.checkUpdate = True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()