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

    World {
        id: physicsWorld
    }

    Robot {
        id: robot
    }

    // Obstacles
    Repeater {
        model: 20
        delegate: Obstacle {
            width: 20
            height: 20
            x: Math.max(width*2, Math.random() * screen.width - width);
            y: Math.max(height*2, Math.random() * screen.height - height);
            rotation: Math.random() * 90;
        }
    }

    ScreenBoundaries {}
}
