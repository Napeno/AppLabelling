import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

class TouchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 400)
        self.label = QLabel('Touch here to get coordinates.', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 400, 400)
        self.show()

    def mousePressEvent(self, event):
        self.label.setText(f'X: {event.x()}, Y: {event.y()}')
        self.forLoop()

    def forLoop(self):
        for i in range(0, 10):
            print(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TouchApp()
    sys.exit(app.exec_())
