import QtQuick 2.0

import MyPaint 1.0

Rectangle {
    width: 200
    height: 200
    color: "green"
    anchors.fill: parent

    Text {
        text: "Hello World"
        anchors.centerIn: parent
    }

    MyPaint {
        anchors.centerIn: parent
        anchors.fill: parent
    }
}
