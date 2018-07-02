import QtQuick 2.7
import QtQuick.Controls 2.4
import Qt.labs.platform 1.0 as QLP

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
            MenuItem { text: "Generate" }
            MenuItem { text: "Step" }
            MenuItem { text: "5 Steps" }
        }
    }

    Map {
        id: map
        anchors.centerIn: parent
        anchors.fill: parent
        focus: true
        onPercentageChanged: {
            footerText.text = "Updating... " + percentage.toFixed(1)*100 + "%"
        }
    }

    SqtFileDialog {
        id: loadMap
        title: "Please choose a Map file"
        //folder: QLP.shortcuts.home
        nameFilters: ["Map files (*.png)"]
        fileMode: QLP.FileDialog.OpenFile
        onOutputChanged: {
            print('>', output)
        }
    }

    SqtFileDialog {
        id: saveMap
        title: "Please select a folder"
        //folder: QLP.shortcuts.home
        nameFilters: ["Map files (*.png)"]
        fileMode: QLP.FileDialog.SaveFile
        onOutputChanged: {
            print('>', output)
        }
    }
}