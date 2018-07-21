import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQml import qmlRegisterType

from Map import *

app = QApplication(sys.argv)

qmlRegisterType(Map, 'Map', 1, 0, 'Map')

engine = QQmlApplicationEngine('main.qml')

sys.exit(app.exec_())
