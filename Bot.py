from PySide2.QtCore import QObject, Slot, Property, QPoint, QRect, QTimer
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QImage, QPainter, QColor

from Map import Map

import math

class Bot(QQuickPaintedItem):

    def __init__(self, parent = None):
        super(Bot, self).__init__(parent)

        self._map = None
        self.image = QImage(300, 300, QImage.Format_RGBA8888)
        self.timer = QTimer()
        self.position = QPoint()
        self.timer.timeout.connect(lambda: self.drawCircle(self.position))

    def paint(self, painter):
        painter.drawImage(QRect(0, 0, self.width(), self.height()), self.image)

    def setMap(self, map: Map):
        if not map:
            return
        print('Map', map)
        self._map = map
        self._map.clicked.connect(self.handleClick)
        self.image = QImage(self.map.image.width(), self.map.image.height(), QImage.Format_RGBA8888)

    def getMap(self) -> Map:
        return self._map

    map = Property(Map, getMap, setMap)

    @Slot(QPoint)
    def handleClick(self, point: QPoint):
        self.position = point
        self.drawCircle(point)
        self.timer.start(100)

    def mousePressEvent(self, event):
        a, b = 2*event.pos().x()*self.image.width()/self.viewport.width(), 2*event.pos().y()*self.image.height()/self.viewport.height()
        #print(a,b)

    def mouseMoveEvent(self, event):
        a, b = 2*event.pos().x()*self.image.width()/self.viewport.width(), 2*event.pos().y()*self.image.height()/self.viewport.height()
        #print(a,b)

    @Slot(QPoint)
    def drawCircle(self, point: QPoint):
        a = point.x()
        b = point.y()
        angle_step_size = 64
        radius = 90
        initPoint = (None, None)
        finalPoint = (None, None)
        firstPoint = finalPoint
        self.image.fill('#000000ff')
        painter = QPainter(self.image)
        painter.setPen('#ff0000')
        for i in [-1, 0, 1]:
            for u in [-1, 0, -1]:
                self.image.setPixelColor(QPoint(a + i, b + u), QColor('#00ff00'))
        for step in range(0, angle_step_size - 1):
            angle = 2*math.pi*step/angle_step_size
            initPoint = finalPoint
            for r in range(1, radius):
                x = a + r*math.cos(angle)
                y = b + r*math.sin(angle)
                finalPoint = (x, y)
                if(self.map.pixel(x, y)):
                    #self.setPixel(x, y, 0x88)
                    pass
                else:
                    break

            if initPoint[0] != None and initPoint[1] != None:
                painter.drawLine(initPoint[0], initPoint[1], finalPoint[0], finalPoint[1])
                #print(initPoint, finalPoint)
                pass
            else:
                firstPoint = finalPoint

        painter.drawLine(finalPoint[0], finalPoint[1], firstPoint[0], firstPoint[1])
        #print(initPoint, finalPoint)
        painter.end()
        self.update()
        nextPoint = point + QPoint(1, 0)
        if self.map.pixel(nextPoint.x(), nextPoint.y()) != 0:
            self.position = nextPoint
