from PySide2 import QtCore
from PySide2.QtCore import Qt, QRect
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QImage

import random

class Map(QQuickPaintedItem):
    def __init__(self, parent = None):
        super(Map, self).__init__(parent)
        # QImage does not work with bits, only with bytes
        self.image = QImage(300, 300, QImage.Format_Grayscale8)
        self.generateMap()

    def pixel(self, x, y, image = None):
        if not image:
            image = self.image

        # This solves:
        # QImage::pixelIndex: Not applicable for 8-bpp images (no palette)
        return image.bits()[x + y * image.bytesPerLine()] & 0xff

    def setPixel(self, x, y, value, image = None):
        if not image:
            image = self.image

        # This solves:
        # QImage::pixelIndex: Not applicable for 8-bpp images (no palette)
        image.bits()[x + y * image.bytesPerLine()] = value

    def createRandomMap(self):
        for i in range(self.image.byteCount()):
            if random.random() < 0.4:
                self.image.bits()[i] = 255
            else:
                self.image.bits()[i] = 0

    def countNeighbours(self, x, y, image = None, n = 1):
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

    def doStep(self, n = 0):
        deathLimit = 15
        _image = self.image.copy()
        for x in range(self.image.width()):
            for y in range(self.image.height()):
                if self.countNeighbours(x, y, _image, 2) < deathLimit:
                    self.setPixel(x, y, 255)
                else:
                    self.setPixel(x, y, 0)

    def generateMap(self):
        self.createRandomMap()
        self.update()


    def paint(self, painter):
        painter.save()
        painter.drawImage(QRect(0, 0, self.width(), self.height()), self.image)
        painter.restore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.doStep()
            self.update()
        event.accept()