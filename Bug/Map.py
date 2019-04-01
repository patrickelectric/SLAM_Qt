from PySide2.QtCore import Qt, QRect, Property, Signal, QEventLoop, Slot, QPoint
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QImage, QPainter

import math
import random
import time

class Map(QQuickPaintedItem):

    def __init__(self, parent = None):
        super(Map, self).__init__(parent)

        self.viewport = None

        self.setAcceptedMouseButtons(Qt.AllButtons)
        self.generate()

    clicked = Signal(QPoint)

    @Slot()
    def generate(self):
        # QImage does not work with bits, only with bytes
        self.image = QImage(300, 300, QImage.Format_Grayscale8)
        self.oldImage = None
        self.generateMap()
        self._percentage = 0

        self._pressClick = QPoint()

    def pixel(self, x: int, y: int, image = None) -> bool:
        if not image:
            image = self.image

        # This solves:
        # QImage::pixelIndex: Not applicable for 8-bpp images (no palette)
        return image.bits()[int(x) + int(y) * image.bytesPerLine()] & 0xff

    def setPixel(self, x: int, y: int, value: int, image = None):
        if not image:
            image = self.image

        # This solves:
        # QImage::pixelIndex: Not applicable for 8-bpp images (no palette)
        image.bits()[int(x) + int(y) * image.bytesPerLine()] = value

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
        self.oldImage = self.image.copy()
        self.percentageChanged.emit()
        QEventLoop().processEvents()

    def generateMap(self):
        self.createRandomMap()
        self.update()
        self.oldImage = self.image.copy()

    def paint(self, painter):
        painter.drawImage(QRect(0, 0, self.width(), self.height()), self.image)
        self.viewport = painter.viewport()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            print('Update..')
            start = time.time()
            self.doStep()
            print('Took: %.2fs' % (time.time() - start))
        event.accept()

    def mousePressEvent(self, event):
        a, b = event.pos().x()*self.image.width()/self.width(), event.pos().y()*self.image.height()/self.height()
        self.clicked.emit(QPoint(a, b))

    def mouseMoveEvent(self, event):
        a, b = event.pos().x()*self.image.width()/self.width(), event.pos().y()*self.image.height()/self.height()
        self.clicked.emit(QPoint(a, b))

    def percentage(self):
        return self._percentage

    percentageChanged = Signal()
    percentage = Property(float, percentage, notify=percentageChanged)

    @Slot()
    def addVehicle(self):
        self.image = self.image.convertToFormat(QImage.Format_RGBA8888)
        painter = QPainter(self.image)
        painter.drawImage(QRect(50, 50, 13, 15), QImage("imgs/turtle.png"))
        painter.end()
        self.update()

    @Slot(str)
    def saveMap(self, path: str):
        # Check image encoder
        if(self.image.format() != QImage.Format_Grayscale8):
            print('Wrong map pixel format, create map without vehicle added.')
            return
        ok = self.image.save(path)
        if(not ok):
            print('It was not possible to save Map in:', path)

    @Slot(str)
    def loadMap(self, path: str):
        # Check image encoder
        image = QImage(path)
        if(image.format() != QImage.Format_Grayscale8):
            print('Wrong map pixel format, map should be Grayscale8.')
            return
        self.image = image
        self.oldImage = self.image.copy()
        self.update()