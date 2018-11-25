from PySide2.QtCore import QObject, Slot, Property, QPoint, QRect, QTimer
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QImage, QPainter, QColor

from Map import Map

import math
import copy

class Bot(QQuickPaintedItem):

    def __init__(self, parent = None):
        super(Bot, self).__init__(parent)

        self._map = None
        self.image = QImage(300, 300, QImage.Format_RGBA8888)
        self.image.fill('#000000ff')
        self.timer = QTimer()
        self.position = QPoint()
        self.around = None
        self.angle = 0
        self.last_front = False
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
        self.image.fill('#000000ff')

    def getMap(self) -> Map:
        return self._map

    map = Property(Map, getMap, setMap)

    @Slot(QPoint)
    def handleClick(self, point: QPoint):
        self.position = point
        self.around = False
        self.drawCircle(point)
        self.timer.start(100)

    def mousePressEvent(self, event):
        a, b = event.pos().x()*self.image.width()/self.width(), event.pos().y()*self.image.height()/self.height()

    def mouseMoveEvent(self, event):
        a, b = event.pos().x()*self.image.width()/self.width(), event.pos().y()*self.image.height()/self.height()

    @Slot(QPoint)
    def drawCircle(self, point: QPoint):
        a = point.x()
        b = point.y()
        angle_step_size = 64
        radius = 90
        initPoint = QPoint(-1, -1)
        finalPoint = initPoint
        firstPoint = finalPoint
        self.image.fill('#000000ff')
        painter = QPainter(self.image)
        lidarPoints = []
        painter.setPen('#00ff00')
        painter.drawRect(point.x() - 1, point.y() - 1, 2, 2)
        front = QPoint(math.cos(self.angle), math.sin(self.angle))
        self.image.setPixelColor(point + front, QColor('#0000ff'))

        painter.setPen('#ff0000')
        for step in range(0, angle_step_size - 1):
            angle = 2*math.pi*step/angle_step_size + self.angle
            initPoint = finalPoint
            for r in range(1, radius):
                x = point.x() + r*math.cos(angle)
                y = point.y() + r*math.sin(angle)
                finalPoint = QPoint(x, y)
                if not self.map.pixel(x, y):
                    break
            if initPoint != QPoint(-1, -1):
                painter.drawLine(initPoint, finalPoint)
            else:
                firstPoint = finalPoint
            lidarPoints.append(finalPoint - point)

        painter.drawLine(finalPoint, firstPoint)
        painter.end()
        self.update()
        self.runObstacleAvoidance(point, lidarPoints)

    def runObstacleAvoidance(self, point, lidarPoints):
        # Calculate distance
        # Target 287, 293
        destiny = QPoint(287, 293)
        ao = destiny - point

        rcoli = 2
        # Get only the front, right, back and left values
        lpoints = [lidarPoints[int(i*(len(lidarPoints) + 1)/4)] for i in range(4)]
        dist = lambda d : (d.x()**2 + d.y()**2)**0.5
        dist2 = lambda d,d2 : ((d.x() - d2.x())**2 + (d.y() - d2.y())**2)**0.5
        dists = [ dist(p) for p in lpoints]

        # Calculate next point
        nextPoint = point
        if dists[0] < rcoli and not self.around:
            self.around_point = copy.copy(point)
        self.around = dists[0] < rcoli or self.around

        # Bug algorithm
        if not self.around:
            if abs(ao.x()) > abs(ao.y()):
                if ao.x() > 0:
                    nextPoint += QPoint(1, 0)
                    self.angle = 0
                else:
                    nextPoint += QPoint(-1, 0)
                    self.angle = math.pi
            else:
                if ao.y() > 0:
                    nextPoint += QPoint(0, 1)
                    self.angle = math.pi/2
                else:
                    nextPoint += QPoint(0, -1)
                    self.angle = 3*math.pi/2
        else:
            if dist2(self.around_point, point) + dist2(destiny, point) - dist2(destiny, self.around_point) < 3 and dist2(self.around_point, point) > 3:
                self.around = False
            elif dists[3] < rcoli:
                if dists[0] > rcoli:
                    self.position += QPoint(math.cos(self.angle), math.sin(self.angle))
                else:
                    self.angle += math.pi/2
            elif dists[0] < rcoli:
                self.position += QPoint(math.cos(self.angle), math.sin(self.angle))
                self.angle += math.pi/2
            elif dists[1] < rcoli:
                self.angle += math.pi
            else:
                self.position += QPoint(math.cos(self.angle - math.pi/2), math.sin(self.angle - math.pi/2))
                self.angle -= math.pi/2

