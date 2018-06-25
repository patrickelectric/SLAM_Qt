from PySide2.QtCore import Qt, QRect
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QImage

class MyPaint(QQuickPaintedItem):
    def __init__(self, parent = None):
        super(MyPaint, self).__init__(parent)
        # QImage does not work with bits, only with bytes
        self.image = QImage(40, 40, QImage.Format_Grayscale8)
        '''
        #self.image.loadFromData(str.encode('010101010101010101010101010101'))
        print(self.image.bits())
        bits = bytearray(self.image.bits())
        print(bits, len(bits))
        print(self.image.rect().width(), self.image.rect().height())
        print('Bytes per line', self.image.bytesPerLine(), '\tbits per line:', 8*self.image.bytesPerLine())
        print('total bytes', self.image.byteCount(), '\tbits:', 8*self.image.byteCount())
        '''

    def paint(self, painter):
        painter.save()
        painter.drawImage(QRect(0, 0, self.width(), self.height()), self.image)
        painter.restore()