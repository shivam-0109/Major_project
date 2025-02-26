import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Water Quality Prediction"
    //icon: "OIP.jpg" // Change this path

    background: Rectangle {
        color: "#75BFEC"
    }

    // Store the received JSON data
    property var jsonData: ({})

    // Update JSON data when received from Python
    Connections {
        target: backend
        onWaterQualityUpdated: (data) => {
            jsonData = data; // Store JSON data in property variable
        }
    }

    // Header Section
    Label {
        text: "Water Quality Prediction"
        font.pixelSize: 36
        font.bold: true
        color: "black"
        x: 750
        y: 20
    }

    Label {
        id: timeLabel
        font.pixelSize: 36
        font.bold: true
        color: "black"
        x: 1250
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

    // Left Column (4 input values)
    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 50
        y: 100
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "ph: " + jsonData.input_data.ph : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }

    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 50
        y: 305
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "turbidity: " + jsonData.input_data.turbidity : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }

    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 50
        y: 510
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "hardness: " + jsonData.input_data.hardness : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }

    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 50
        y: 715
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "solids: " + jsonData.input_data.solids : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }

   // Center Prediction Section
    Rectangle {
        width: 800
        height: 450
        radius: 5
        color: "white"
        border.color: "black"
        x: 600
        y: 200

        // Prediction Status Label
        Label {
            text: jsonData.prediction ? jsonData.prediction.status : "N/A"
            font.pixelSize: 48
            font.bold: true
            color: "red"
            x: (parent.width - width) / 2 // Center horizontally
            y: 50 // Fixed vertical position
        }

        // Suggestion Labels
        Repeater {
            model: jsonData.prediction ? jsonData.prediction.suggestions : []
            delegate: Label {
                text: modelData
                font.pixelSize: 18
                color: "black"
                font.bold: true
                wrapMode: Text.WordWrap
                width: parent.width - 40 // Add some margin
                x: 120  // Fixed horizontal position
                y: 120 + (index * 30) // Dynamically position each suggestion below
            }
        }
    }


    // Right Column (4 input values)
    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 1620
        y: 100
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "sulfate: " + jsonData.input_data.sulfate : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }

    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 1620
        y: 305
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "conductivity: " + jsonData.input_data.conductivity : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }

    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 1620
        y: 510
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "chloramines: " + jsonData.input_data.chloramines : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }

    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 1620
        y: 715
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "organicCarbon: " + jsonData.input_data.organicCarbon : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }

    Rectangle {
        width: 250
        height: 200
        radius: 5
        color: "white"
        border.color: "black"
        x: 850
        y: 675
        Label {
            anchors.centerIn: parent
            text: jsonData.input_data ? "Trihalomethanes: " + jsonData.input_data.trihalomethanes : "N/A"
            font.pixelSize: 18
            color: "black"
            font.bold: true
        }
    }
}