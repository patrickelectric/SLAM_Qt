import QtQuick 2.0

import Box2D 2.0

PhysicsItem {
    id: box

    sleepingAllowed: false
    bullet: true
    fixedRotation: true
    bodyType: Body.Dynamic
    gravityScale: 0
    property var center: Qt.point(x + width/2, y + height/2)
    property var lidarOutput: undefined
    property var lidars: []
    property var radius: 60

    function move(xv, yv) {
        body.linearVelocity.x = xv
        body.linearVelocity.y = yv
    }

    fixtures: Box {
        width: box.width
        height: box.height

        density: 1
        friction: 0.3
        restitution: 0.2
        groupIndex: 1
    }

    Rectangle {
        anchors.fill: parent
        color: "red"
    }
}
