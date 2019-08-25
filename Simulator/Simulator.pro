TARGET = Simulator

CONFIG += \
    c++14

QT += gui qml quick widgets

INCLUDEPATH += $$PWD/lib/Box2D/

HEADERS +=
    lib/Box2D/Box2D/Box2D.h

SOURCES += \
    src/main.cpp

RESOURCES += \
    resources.qrc
