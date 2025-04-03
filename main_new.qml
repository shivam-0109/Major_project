import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Water Quality Prediction"

    Image {
        source: "img3.jpg"
        anchors.fill: parent
        fillMode: Image.PreserveAspectCrop
    }

    property var jsonData: ({})
    property string selectedWaterType: "Drinking Water"  // Initialize with default value

    Connections {
        target: backend
        onWaterQualityUpdated: function(data) {
            jsonData = data;
        }
    }

    Label {
        text: "Water Quality Prediction"
        font.pixelSize: 36
        font.bold: true
        color: "black"
        x: 600
        y: 20
    }

    Label {
        id: timeLabel
        font.pixelSize: 36
        font.bold: true
        color: "black"
        x: 1100
        y: 20

        Timer {
            interval: 1000
            running: true
            repeat: true
            onTriggered: timeLabel.text = Qt.formatDateTime(new Date(), "dd/MM/yy, hh:mm:ss")
        }
    }

    Rectangle {
        width: 1600
        height: 2
        color: "black"
        x: 160
        y: 70
    }

    Column {
        id: parameterColumn
        spacing: 7.5
        x: 50
        y: 75

        Repeater {
            model: [
                { name: "ph", range: "6.5 - 8.5" },
                { name: "hardness", range: "0 - 300 mg/L" },
                { name: "sulfate", range: "0 - 250 mg/L" },
                { name: "conductivity", range: "50 - 500 µS/cm" },
                { name: "chloramines", range: "0 - 4 mg/L" },
                { name: "organicCarbon", range: "0 - 20 mg/L" }
            ]

            delegate: Rectangle {
                width: 400
                height: 150
                radius: 5
                color: "#80FFFFFF"
                border.color: "black"

                property string paramName: modelData.name
                property string paramRange: modelData.range

                Label {
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: parent.paramName
                    font.pixelSize: 18
                    color: "black"
                    font.bold: true
                }

                ComboBox {
                id: typeSelector
                width: 200
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                model: ["Drinking Water", "Tap Water", "Lake Water", "Ash/Mud", "Soap Water"]
                currentIndex: model.indexOf(selectedWaterType)

                onActivated: {
                    selectedWaterType = currentText
                    console.log("Selected water type:", selectedWaterType)
                    if (backend.requestWaterQualityUpdate) {
                        backend.requestWaterQualityUpdate(selectedWaterType)
                    } else {
                        console.error("backend.requestWaterQualityUpdate is not a function!")
                    }
                }
            }


                Label {
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "Selected: " + selectedWaterType + "\nRange: " + parent.paramRange
                    font.pixelSize: 16
                    color: "black"
                    wrapMode: Text.WordWrap
                }
            }
        }
    }

    Column {
        spacing: 15
        x: 1620
        y: 100

        Repeater {
            model: ["turbidity", "solids"]

            delegate: Rectangle {
                width: 250
                height: 200
                radius: 5
                color: "#80FFFFFF"
                border.color: "black"

                Label {
                    anchors.centerIn: parent
                    text: modelData + ": " + (jsonData.input_data ? jsonData.input_data[modelData] : "N/A")
                    font.pixelSize: 18
                    color: "black"
                    font.bold: true
                }
            }
        }
    }

    Rectangle {
        width: 800
        height: 450
        radius: 5
        color: "#80FFFFFF"
        border.color: "black"
        x: 600
        y: 200

        Label {
            id: statusLabel
            text: jsonData.prediction ? jsonData.prediction.status : "N/A"
            font.pixelSize: 48
            font.bold: true
            color: {
                if (!jsonData.prediction) return "black";
                return jsonData.prediction.status === "Safe" ? "green" : "red";
            }
            anchors.horizontalCenter: parent.horizontalCenter
            y: 50
        }

        Column {
            anchors.top: statusLabel.bottom
            anchors.topMargin: 50
            anchors.left: parent.left
            anchors.leftMargin: 40
            spacing: 20

            Repeater {
                model: jsonData.prediction ? jsonData.prediction.suggestions : []

                delegate: Label {
                    text: "• " + modelData
                    font.pixelSize: 18
                    color: "black"
                    font.bold: true
                    wrapMode: Text.WordWrap
                    width: parent.parent.width - 80
                }
            }
        }
    }
}