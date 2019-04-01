#!/usr/bin/env python3

import sys

from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQml import qmlRegisterType

from Map import *
from Bot import *

def main():
    sys.argv += ['--style', 'material']
    app = QApplication(sys.argv)

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    qmlRegisterType(Map, 'Map', 1, 0, 'Map')
    qmlRegisterType(Bot, 'Bot', 1, 0, 'Bot')

    engine = QQmlApplicationEngine('main.qml')

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
