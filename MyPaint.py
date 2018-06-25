from PySide2.QtCore import Qt, QRect
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QImage

class MyPaint(QQuickPaintedItem):
    def __init__(self, parent = None):
        super(MyPaint, self).__init__(parent)
        self.update()

    def paint(self, painter):
        painter.save()
        painter.setPen(Qt.red)
        painter.drawEllipse(QRect(0, 0, self.width(), self.height()))
        painter.restore()