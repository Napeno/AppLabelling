from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QSizePolicy, QLayout, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF
from PyQt5.uic import loadUi

class painter:
    def __init__(self) -> None:
        painter = QPainter(self)
        painter.drawLine(50, 10, 200 ,400)
        painter.end()

    def paintEvent(self):
        if self.fname:  # Check if an image is loaded
            painter = QPainter(self.ScreenPic.pixmap())  # Create a QPainter object on the current pixmap
            # Perform drawing operations here
            painter.drawLine(50, 10, 200, 400)
            painter.end()  # End painting operations
            self.ScreenPic.update()
