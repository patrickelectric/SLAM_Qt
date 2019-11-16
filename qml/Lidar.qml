import QtQuick 2.12
import Box2D 2.0

Canvas {
    id: canvas

    property var center: Qt.point(width/2, height/2)
    property var lidarOutput: undefined
    property var lidars: []
    property var radius: 60

    Repeater {
        id: rayCastRepeater
        model: 400
        Item {
            // RayCast need a parent
            RayCast {
                id: potato
                property bool isRayCast: true
                property point point1: center
                property point point2: Qt.point(point1.x + radius*Math.cos(2*Math.PI*index/rayCastRepeater.count), point1.y + radius*Math.sin(2*Math.PI*index/rayCastRepeater.count))
                onFixtureReported: {
                    lidarOutput[index] = point
                }
            }
        }
    }

    // Do lidar logic
    function step(world) {
        lidarOutput = []
        for(var i = 0; i < rayCastRepeater.count; i++) {
            var sensor = rayCastRepeater.itemAt(i).data[0]
            if(!sensor.isRayCast) {
                continue
            }
            lidarOutput.push(sensor.point2)
            physicsWorld.rayCast(sensor, sensor.point1, sensor.point2)
        }
        canvas.requestPaint()
    }

    // Draw lidar
    onPaint: {
        var context = getContext("2d");
        context.reset();
        var lastIndex = lidarOutput.length
        var recCenter = Qt.point(canvas.width/2 + 5, canvas.height/2 + 5)
        for(var i = 0; i < lastIndex - 1; i++) {
            context.beginPath();
            context.moveTo(recCenter.x + (lidarOutput[i].x - center.x), recCenter.y - (center.y - lidarOutput[i].y));
            context.lineTo(recCenter.x + (lidarOutput[i+1].x - center.x), recCenter.y - (center.y - lidarOutput[i+1].y));
            context.stroke();
        }
        context.beginPath();
        context.moveTo(recCenter.x + (lidarOutput[lastIndex - 1].x - center.x), recCenter.y + (lidarOutput[lastIndex - 1].y - center.y));
        context.lineTo(recCenter.x + (lidarOutput[0].x - center.x), recCenter.y + (lidarOutput[0].y - center.y));
        context.stroke();
    }

    Connections {
        target: physicsWorld
        onStepped: {
            canvas.step(physicsWorld)
        }
    }
}
