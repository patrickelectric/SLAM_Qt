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

    @Slot()
    def generate(self):
        # QImage does not work with bits, only with bytes
        self.image = QImage(300, 300, QImage.Format_Grayscale8)
        self.oldImage = None
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
        self.viewport = painter.viewport()

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
        if self.viewport:
            a, b = 2*event.pos().x()*self.image.width()/self.viewport.width(), 2*event.pos().y()*self.image.height()/self.viewport.height()
            #print('Mouse click in:', a, b)
            self.drawCircle(a, b)

    def mouseMoveEvent(self, event):
        if self.viewport:
            a, b = 2*event.pos().x()*self.image.width()/self.viewport.width(), 2*event.pos().y()*self.image.height()/self.viewport.height()
            #print('Mouse move:', a, b)
            self.drawCircle(a, b)

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

    @Slot()
    def drawCircle(self, a: int, b: int):
        angle_step_size = 64
        radius = 90
        initPoint = (None, None)
        finalPoint = (None, None)
        firstPoint = finalPoint
        if not self.oldImage:
            self.oldImage = self.image.copy()
        else:
            self.image = self.oldImage.copy()
        painter = QPainter(self.image)
        painter.setPen('#888888')
        for i in [-1, 0, 1]:
            for u in [-1, 0, -1]:
                self.setPixel(a + i, b + u, 0x88)
        for step in range(0, angle_step_size - 1):
            angle = 2*math.pi*step/angle_step_size
            initPoint = finalPoint
            for r in range(1, radius):
                x = a + r*math.cos(angle)
                y = b + r*math.sin(angle)
                finalPoint = (x, y)
                if(self.pixel(x, y)):
                    #self.setPixel(x, y, 0x88)
                    pass
                else:
                    break

            if initPoint[0] and initPoint[1]:
                painter.drawLine(initPoint[0], initPoint[1], finalPoint[0], finalPoint[1])
                #print(initPoint, finalPoint)
                pass
            else:
                firstPoint = finalPoint

        painter.drawLine(finalPoint[0], finalPoint[1], firstPoint[0], firstPoint[1], )
        #print(initPoint, finalPoint)
        painter.end()
        self.update()