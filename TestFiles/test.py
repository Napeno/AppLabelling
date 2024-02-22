from PyQt5.QtGui import QPainter, QPolygonF, QColor
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QPointF, QPoint
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 350, 200)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(255, 0, 0))
        points = QPolygonF([QPointF(50.11111, 50), QPointF(150, 50), QPointF(100, 150)])
        qp.drawPolygon(points)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())