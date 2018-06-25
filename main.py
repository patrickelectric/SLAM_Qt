from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl
from PySide2.QtQml import qmlRegisterType

from Map import *

app = QApplication([])

qmlRegisterType(Map, 'Map', 1, 0, 'Map')

view = QQuickView()
url = QUrl("main.qml")

view.setSource(url)
view.show()
app.exec_()
