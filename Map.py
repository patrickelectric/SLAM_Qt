from PySide2.QtCore import Qt, QRect, Property, Signal, QEventLoop, Slot, QPoint
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QImage, QPainter

import random
import time

class Map(QQuickPaintedItem):

    def __init__(self, parent = None):
        super(Map, self).__init__(parent)

        self.setAcceptedMouseButtons(Qt.AllButtons)
        self.generate()

    @Slot()
    def generate(self):
        # QImage does not work with bits, only with bytes
        self.image = QImage(300, 300, QImage.Format_Grayscale8)
        self.generateMap()
        self._percentage = 0

        self._pressClick = QPoint()
        self._doMapMove = False
        self._scale = 1
        self._offset = QPoint()


    def pixel(self, x: int, y: int, image = None) -> bool:
        if not image:
            image = self.image

        # This solves:
        # QImage::pixelIndex: Not applicable for 8-bpp images (no palette)
        return image.bits()[x + y * image.bytesPerLine()] & 0xff

    def setPixel(self, x: int, y: int, value: int, image = None):
        if not image:
            image = self.image

        # This solves:
        # QImage::pixelIndex: Not applicable for 8-bpp images (no palette)
        image.bits()[x + y * image.bytesPerLine()] = value

    def createRandomMap(self):
        for i in range(self.image.byteCount()):
            if random.random() < 0.35:
                self.image.bits()[i] = 255
            else:
                self.image.bits()[i] = 0

    def countNeighbors(self, x: int, y: int, image = None, n = 1) -> int:
        if not image:
            image = self.image

        count = 0
        for i in range(-n , n + 1):
            for u in range(-n , n + 1):
                if not i and not u:
                    continue

                #TODO: pixel function is poor
                # need to use bits()
                if x + i < 0 or y + u < 0 or \
                    x + i >= image.width() or y + u >= image.height():
                    count += 1
                    continue

                if not self.pixel(x + i, y + u, image):
                    count += 1

        return count

    @Slot(int)
    def doStep(self, n = 1):
        if self.image.format() != QImage.Format_Grayscale8:
            print("Wrong file format, generate map again.")
            return

        deathLimit = 14
        self._percentage = 0
        for _ in range(n):
            _image = self.image.copy()
            for x in range(self.image.width()):
                self._percentage += 1.0/(self.image.width()*n)
                if x%10 == 0:
                    # Update percentage
                    self.percentageChanged.emit()
                    # processEvent is necessary
                    QEventLoop().processEvents()
                    # Update map
                    self.update()
                for y in range(self.image.height()):
                    if self.countNeighbors(x, y, _image, 2) > deathLimit or \
                        x == 0 or y == 0 or x == _image.width() - 1 or y == _image.height() - 1:
                        self.setPixel(x, y, 0)
                    else:
                        self.setPixel(x, y, 255)
        # Update percentage
        self.update()
        self.percentageChanged.emit()
        QEventLoop().processEvents()

    def generateMap(self):
        self.createRandomMap()
        self.update()

    def paint(self, painter):
        if self._scale > 1:
            self._offset = QPoint(
                    (self._scale - 1)*self.width()/2,
                    (self._scale - 1)*self.height()/2
                ) - self._pressClick
        else:
            self._pressClick = QPoint()
            self._offset = QPoint(
                    (self._scale - 1)*self.width()/2,
                    (self._scale - 1)*self.height()/2
                )
        painter.translate(-self._offset)
        painter.scale(self._scale, self._scale)
        painter.drawImage(QRect(0, 0, self.width(), self.height()), self.image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            print('Update..')
            start = time.time()
            self.doStep()
            print('Took: %.2fs' % (time.time() - start))
        event.accept()

    def wheelEvent(self, event):
        # Get zoom
        # delta is around +-120
        self._scale += event.delta()/(120*2)
        if self._scale < 1:
            self._scale = 1
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressClick += QPoint(self.width(), self.height())/2 - event.pos()
            self._doMapMove = True
            self.update()

    def getPercentage(self):
        return self._percentage

    percentageChanged = Signal()
    percentage = Property(float, getPercentage, notify=percentageChanged)

    @Slot()
    def addVehicle(self):
        self.image = self.image.convertToFormat(QImage.Format_RGBA8888)
        painter = QPainter(self.image)
        painter.drawImage(QRect(50, 50, 13, 15), QImage("imgs/turtle.png"))
        painter.end()
        #self.image = image.copy()
        self.update()
