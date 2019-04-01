import QtQuick 2.0
import QtQuick.Window 2.1
import Qt.labs.settings 1.0

import Box2D 2.0

Window {
    id: screen
    width: 800
    height: 600
    visible: true

    Settings {
        property alias x: screen.x
        property alias y: screen.y
        property alias width: screen.width
        property alias height: screen.height
    }

    property var speed: 2
    property var v: Qt.point(0, 0)

    World {
        id: physicsWorld
        onStepped: {
            movableBox.step(physicsWorld)
            canvas.requestPaint()
            avoid()
        }
    }

    // Angle to the target and bubble rebound angle
    property var angle: 0
    property var angleR: 0

    // Avoid algorithm
    function avoid() {
        var finalPoint = Qt.point(screen.width, screen.height)
        var pos = movableBox.center
        var dist = Math.hypot(pos.x-finalPoint.x, pos.y-finalPoint.y)
        angle = Math.atan((pos.y-finalPoint.y)/(pos.x-finalPoint.x))
        //print('angle', angle, finalPoint, pos, dist)

        var lastIndex = movableBox.lidarOutput.length
        var alpha0 = 2*Math.PI/lastIndex
        var middleIndex = lastIndex*angle/(2*Math.PI)
        var maxIndex = Math.round(middleIndex + lastIndex/4)
        var minIndex = Math.round(middleIndex - lastIndex/4)
        var alphaRS = 0
        var alphaRI = 0
        //print('min max mid, ', minIndex, maxIndex, middleIndex, middleIndex*2*Math.PI/400)
        //print(180*alpha0*minIndex/Math.PI, 180*alpha0*maxIndex/Math.PI, 180*alpha0*middleIndex/Math.PI)
        for(var i = minIndex; i < maxIndex; i++) {
            var u = i
            if(i < 0) {
                u += lastIndex
            } else if (i >= lastIndex) {
                u -= lastIndex
            }
            var lidarDist = Math.abs(Math.hypot(pos.x-movableBox.lidarOutput[u].x, pos.y-movableBox.lidarOutput[u].y))
            alphaRS += (i+0.5)*alpha0*Math.pow(lidarDist, 100);
            alphaRI += Math.pow(lidarDist, 100);
        }
        angleR = alphaRS/alphaRI;
        //print('alphaR', angleR)
        movableBox.move(speed*Math.cos(angleR), speed*Math.sin(angleR));
    }

    // Obstacles
    Repeater {
        model: 50
        delegate: Obstacle {
            width: 20
            height: 20
            x: Math.max(width*2, Math.random() * screen.width - width);
            y: Math.max(height*2, Math.random() * screen.height - height);
            rotation: Math.random() * 90;
        }
    }

    // Our robot
    MovableBox {
        id: movableBox
        width: 10
        height: width
    }

    Canvas {
        id: canvas
        anchors.fill: parent

        // Draw small arrow
        function canvas_arrow(context, fromx, fromy, tox, toy, color){
            // https://stackoverflow.com/questions/808826/draw-arrow-on-canvas-tag
            var headlen = 2;   // length of head in pixels
            var angle = Math.atan2(toy-fromy,tox-fromx);
            context.beginPath();
            context.strokeStyle = color
            context.moveTo(fromx, fromy);
            context.lineTo(tox, toy);
            context.lineTo(tox-headlen*Math.cos(angle-Math.PI/6),toy-headlen*Math.sin(angle-Math.PI/6));
            context.moveTo(tox, toy);
            context.lineTo(tox-headlen*Math.cos(angle+Math.PI/6),toy-headlen*Math.sin(angle+Math.PI/6));
            context.stroke();
        }

        // Draw lidar
        onPaint: {
            var context = getContext("2d");
            context.reset();
            var lastIndex = movableBox.lidarOutput.length
            for(var i = 0; i < lastIndex - 1; i++) {
                context.beginPath();
                context.moveTo(movableBox.lidarOutput[i].x, movableBox.lidarOutput[i].y);
                context.lineTo(movableBox.lidarOutput[i+1].x, movableBox.lidarOutput[i+1].y);
                context.stroke();
            }
            context.beginPath();
            context.moveTo(movableBox.lidarOutput[lastIndex - 1].x, movableBox.lidarOutput[lastIndex - 1].y);
            context.lineTo(movableBox.lidarOutput[0].x, movableBox.lidarOutput[0].y);
            context.stroke();

            canvas_arrow(context, movableBox.center.x, movableBox.center.y, movableBox.center.x + 50*Math.cos(angle), movableBox.center.y + 50*Math.sin(angle), "#cc0000")
            canvas_arrow(context, movableBox.center.x, movableBox.center.y, movableBox.center.x + 50*Math.cos(angleR), movableBox.center.y + 50*Math.sin(angleR), "#0000cc")
        }
    }

    ScreenBoundaries {}
}
