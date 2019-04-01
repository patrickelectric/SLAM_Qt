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

    // Do lidar logic
    function step(world) {
        center = Qt.point(x + width/2, y + height/2)
        lidarOutput = []
        for(var i = 0; i < rayCastRepeater.count; i++) {
            var sensor = rayCastRepeater.itemAt(i).data[0]
            if(!sensor.isRayCast) {
                continue
            }
            lidarOutput.push(sensor.point2)
            world.rayCast(sensor, sensor.point1, sensor.point2)
        }
    }

    function move(xv, yv) {
        body.linearVelocity.x = xv;
        body.linearVelocity.y = yv;
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

    // Lidar
    Repeater {
        id: rayCastRepeater
        model: 400
        Item {
            // RayCast need a parent
            RayCast {
                id: potato
                property bool isRayCast: true
                property point point1: Qt.point(center.x, center.y)
                property point point2: Qt.point(point1.x + radius*Math.cos(2*Math.PI*index/rayCastRepeater.count), center.y + radius*Math.sin(2*Math.PI*index/rayCastRepeater.count))
                onFixtureReported: {
                    lidarOutput[index] = point
                }
            }
        }
    }
}
