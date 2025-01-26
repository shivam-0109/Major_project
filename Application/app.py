import sys
import random
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QColor, QPalette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Water Quality Index")
        self.setGeometry(0, 0, 1920, 1080)

        # Define opacity as a variable
        self.opacity_value = 0.4  # You can adjust this value to make the boxes more or less transparent

        # Set custom background color (#75BFEC)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#75BFEC"))
        self.setPalette(palette)

        # Main layout
        main_layout = QVBoxLayout()

        # Header for title and time/date combined
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignTop)  # Align header to top
        header_layout.setContentsMargins(0, 2, 0, 0)  # 2px margin from top

        # Combined label for title and time
        combined_label = QWidget()
        combined_layout = QHBoxLayout()
        combined_layout.setSpacing(2)

        self.header_label = QLabel("Water Quality Index")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 36px; color: black; font-weight: bold;")

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 36px; color: black; font-weight: bold;")
        self.update_time()

        combined_layout.addWidget(self.header_label)
        combined_layout.addSpacing(5)
        combined_layout.addWidget(self.time_label)
        combined_label.setLayout(combined_layout)

        # Timer to update the time every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        header_layout.addWidget(combined_label, alignment=Qt.AlignCenter)

        # Add a black full-width line below the header (2px height)
        black_line = QFrame()
        black_line.setFrameShape(QFrame.HLine)
        black_line.setFrameShadow(QFrame.Sunken)
        black_line.setStyleSheet("background-color: black; height: 2px;")
        header_layout.addWidget(black_line)

        # Squares layout
        squares_layout = QHBoxLayout()

        # Left side squares (3 equal boxes)
        self.left_squares = []
        left_squares = QVBoxLayout()
        for i in range(3):
            square = self.create_square()
            label = QLabel("Loading...")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 18px; color: black; font-weight: bold;")
            square_layout = QVBoxLayout()
            square_layout.addWidget(label)
            square.setLayout(square_layout)
            self.left_squares.append(label)
            left_squares.addWidget(square)

        # Right side squares (3 equal boxes)
        self.right_squares = []
        right_squares = QVBoxLayout()
        for i in range(3, 6):
            square = self.create_square()
            label = QLabel("Loading...")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 18px; color: black; font-weight: bold;")
            square_layout = QVBoxLayout()
            square_layout.addWidget(label)
            square.setLayout(square_layout)
            self.right_squares.append(label)
            right_squares.addWidget(square)

        # Center square (500x500 size) for WQI
        center_square = self.create_square(500, 500)
        self.wqi_label = QLabel("WQI Loading...")
        self.wqi_label.setAlignment(Qt.AlignCenter)
        self.wqi_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.wqi_label)
        center_square.setLayout(center_layout)

        squares_layout.addLayout(left_squares)
        squares_layout.addWidget(center_square, alignment=Qt.AlignCenter)
        squares_layout.addLayout(right_squares)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(squares_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Start the data fetching every 30 seconds
        self.fetch_data()

    def create_square(self, width=380, height=280):
        square = QFrame()
        square.setFixedSize(width, height)
        # Use the opacity variable in the background color
        square.setStyleSheet(f"""
            background-color: rgba(255, 255, 255, {self.opacity_value}); 
            border: 2px solid rgba(0, 0, 0, 0.2); 
            border-radius: 5px;
        """)
        return square

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("  dd/MM/yy, hh:mm:ss")
        self.time_label.setText(current_time)

    def fetch_data(self):
        try:
            # Fetch data from the Flask API
            response = requests.get('http://127.0.0.1:5000/get_water_quality')
            data = response.json()

            # Update the labels with the received data
            self.left_squares[0].setText(f"pH value: {data['pH']}")
            self.left_squares[1].setText(f"Turbidity: {data['Turbidity']} NTU")
            self.left_squares[2].setText(f"Dissolved Oxygen: {data['Dissolved_Oxygen']} mg/L")
            self.right_squares[0].setText(f"Salinity: {data['Salinity']} ppt")
            self.right_squares[1].setText(f"Temperature: {data['Temperature']} °C")
            self.right_squares[2].setText(f"Nitrate Concentration: {data['Nitrate_Concentration']} mg/L")
            self.wqi_label.setText(f"WQI: {data['WQI']}")

        except Exception as e:
            print(f"Error fetching data: {e}")

        # Call this method again after 30 seconds
        QTimer.singleShot(30000, self.fetch_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
