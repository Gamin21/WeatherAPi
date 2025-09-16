import sys
import requests
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Weather App')
        self.layout = QVBoxLayout()

        # Input field for city name
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText('Enter city name (e.g., Dhaka or Dhaka,BD)')
        self.layout.addWidget(self.city_input)

        # Button to fetch weather
        self.get_weather_btn = QPushButton('Get Weather', self)
        self.get_weather_btn.clicked.connect(self.fetch_weather)
        self.layout.addWidget(self.get_weather_btn)

        # Label to display results
        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)
        self.resize(350, 200)

    def fetch_weather(self):
        city = self.city_input.text().strip()
        if city:
            api_key = '84d90302884f86fc2c2a1ec93191c52b'  # Your API key
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

            try:
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    temp = data['main']['temp']
                    description = data['weather'][0]['description']
                    self.result_label.setText(f'Temperature: {temp}°C\nDescription: {description}')
                else:
                    # Show API error message
                    self.result_label.setText(f"Error: {data.get('message', 'City not found')}")
            except requests.exceptions.RequestException:
                self.result_label.setText('Network error. Check your connection.')
        else:
            self.result_label.setText('Please enter a city name.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
