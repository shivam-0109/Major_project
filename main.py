import sys
import requests
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QVariant
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine

from PyQt5.QtCore import pyqtSlot
import os
import json
from pathlib import Path

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class Backend(QObject):
    waterQualityUpdated = pyqtSignal(QVariant, arguments=['data'])
    
    def __init__(self):
        super().__init__()
        self.selectedWaterType = "Drinking Water"
        self.data_file = "data.json"
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateWaterQuality)
        self.timer.start(5000)
        self.updateWaterQuality()  # Initial call

    def updateWaterQuality(self):
        """Fetch water quality data from the Flask API"""
        try:
            # Ensure data.json exists with default values
            print(f"Requesting data for: {self.selectedWaterType}")
            response = requests.post(
                "http://127.0.0.1:5000/predict",
                json={"water_type": self.selectedWaterType},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Received data: {data}")
                self.waterQualityUpdated.emit(data)
            else:
                error_msg = f"Server error: {response.status_code}"
                print(error_msg)
                self.emitError(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {str(e)}"
            print(error_msg)
            self.emitError(error_msg)

    @pyqtSlot(str)  # Add this decorator to expose the method to QML
    def requestWaterQualityUpdate(self, water_type):
        """Handle manual updates from UI"""
        self.selectedWaterType = water_type
        self.updateWaterQuality()

    def emitError(self, message):
        """Helper to emit error state"""
        self.waterQualityUpdated.emit({
            "error": message,
            "input_data": {"turbidity": "N/A", "solids": "N/A"},
            "prediction": {
                "status": "Error",
                "suggestions": ["Failed to get data from server"]
            }
        })



if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Use resource_path for all file paths
    icon_path = resource_path("img3.jpg")
    qml_path = resource_path("main_new.qml")
    
    app.setWindowIcon(QIcon(icon_path))

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    # Load QML using the correct path
    engine.load(qml_path)

    if not engine.rootObjects():
        sys.exit(-1)

    

    sys.exit(app.exec_())