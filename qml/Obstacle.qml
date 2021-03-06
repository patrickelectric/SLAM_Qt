import QtQuick 2.0
import Box2D 2.0

PhysicsItem {
    id: box

    width: 100
    height: 100
    sleepingAllowed: false

    fixtures: Box {
        property bool isBox: true

        width: box.width
        height: box.height

        density: 1
        friction: 0.3
        restitution: 0.5
    }

    Rectangle {
        anchors.fill: parent
        color: "black"
    }
}
