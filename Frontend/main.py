import sys
import requests
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QVariant
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

class Backend(QObject):
    waterQualityUpdated = pyqtSignal(QVariant)  # Sends JSON data as a dictionary

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_water_quality_data)
        self.timer.start(10000)  # Fetch data every 10 seconds
        self.fetch_water_quality_data()  # Initial fetch

    def fetch_water_quality_data(self):
        try:
            response = requests.get("http://127.0.0.1:5000/predict")
            if response.status_code == 200:
                data = response.json()
                self.waterQualityUpdated.emit(data)  # Send JSON as dictionary
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Failed to fetch data: {e}")

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    app.setWindowIcon(QIcon("OIP.jpg"))

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.load("main_try.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
