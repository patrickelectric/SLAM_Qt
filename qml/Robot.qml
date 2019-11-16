import QtQuick 2.12

Item {
    id: root
    x: movableBox.x
    y: movableBox.y
    property var center: Qt.point(x + width/2, y + height/2)
    property var speed: 2
    onXChanged: updateCenter()
    onYChanged: updateCenter()
    onWidthChanged: updateCenter()
    onHeightChanged: updateCenter()

    function updateCenter() {
        center = Qt.point(x + width/2, y + height/2)
    }

    // Our robot
    MovableBox {
        id: movableBox
        parent: root.parent
        width: 10
        height: width
    }

    Connections {
        target: physicsWorld
        onStepped: {
            avoid()
        }
    }

    Lidar {
        id: lidar
        center: movableBox.center
        anchors.centerIn: root
        width: 200
        height: 200
    }

    // Angle to the target and bubble rebound angle
    property var angle: 0
    property var angleR: 0

    // Avoid algorithm
    function avoid() {
        var finalPoint = Qt.point(screen.width, screen.height)
        var pos = root.center
        var dist = Math.hypot(pos.x-finalPoint.x, pos.y-finalPoint.y)
        angle = Math.atan((pos.y-finalPoint.y)/(pos.x-finalPoint.x))
        //print('angle', angle, finalPoint, pos, dist)

        var lastIndex = lidar.lidarOutput.length
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
            var lidarDist = Math.abs(Math.hypot(pos.x-lidar.lidarOutput[u].x, pos.y-lidar.lidarOutput[u].y))
            alphaRS += i*alpha0*Math.pow(lidarDist, 100);
            alphaRI += Math.pow(lidarDist, 100);
        }
        angleR = alphaRS/alphaRI;
        //print('alphaR', angleR)
        movableBox.move(speed*Math.cos(angleR), speed*Math.sin(angleR));
        canvas.requestPaint()
    }

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

    Canvas {
        id: canvas
        property var size: 100
        x: movableBox.width/2 - size/2
        y: movableBox.height/2 - size/2
        width: size
        height: width
        onPaint: {
            var context = getContext("2d");
            context.reset();
            canvas_arrow(context, size/2, size/2, size/2 + (size/2)*Math.cos(angle), size/2 + (size/2)*Math.sin(angle), "#cc0000")
            canvas_arrow(context, size/2, size/2, size/2 + (size/2)*Math.cos(angleR), size/2 + (size/2)*Math.sin(angleR), "#0000cc")
        }
    }
}
