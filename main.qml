import QtQuick 2.7
import QtQuick.Controls 2.4
import Qt.labs.platform 1.0 as QLP

import Bot 1.0
import Map 1.0

ApplicationWindow {
    width: 1024
    height: 768
    visible: true

    footer: Text {
        id: footerText
    }

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem {
                text: "Open..."
                onTriggered: loadMap.visible = true
            }
            MenuItem {
                text: "Save..."
                onTriggered: saveMap.visible = true
            }
        }

        Menu {
            title: "Map"
            MenuItem {
                text: "Generate"
                onTriggered: map.generate()
            }
            MenuItem {
                text: "Step"
                onTriggered: map.doStep(1)
            }
            MenuItem {
                text: "5 Steps"
                onTriggered: map.doStep(5)
            }
            MenuItem {
                text: "10 Steps"
                onTriggered: map.doStep(10)
            }
            MenuItem {
                text: "20 Steps"
                onTriggered: map.doStep(20)
            }
        }

        Menu {
            title: "Vehicle"
            MenuItem {
                text: "Add."
                onTriggered: map.addVehicle();
            }
        }

        Menu {
            title: "Lidar"
            MenuItem {
                text: "Draw Circle"
                onTriggered: map.drawCircle();
            }
        }
    }


    Bot {
        id: bot
        map: map
        anchors.fill: map
        z: map.z + 1
        visible: true
    }

    Map {
        id: map
        anchors.centerIn: parent
        anchors.fill: parent
        focus: true
        onPercentageChanged: {
            footerText.text = "Updating... " + (percentage*100).toFixed(2) + "%"
        }
    }

    SqtFileDialog {
        id: loadMap
        title: "Please choose a Map file"
        //folder: QLP.shortcuts.home
        nameFilters: ["Map files (*.png)"]
        fileMode: QLP.FileDialog.OpenFile
        onOutputChanged: {
            print('Load from >', output)
            map.loadMap(output)
        }
    }

    SqtFileDialog {
        id: saveMap
        title: "Please select a folder"
        //folder: QLP.shortcuts.home
        nameFilters: ["Map files (*.png)"]
        fileMode: QLP.FileDialog.SaveFile
        onOutputChanged: {
            print('Save in >', output)
            map.saveMap(output)
        }
    }
}