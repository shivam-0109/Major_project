import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtCore import QObject, QVariant
from PyQt5.QtTest import QSignalSpy
import requests

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from your main application
from main import Backend

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()

    @patch('main.requests.post')
    def test_update_water_quality_success(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "input_data": {"turbidity": 1.2, "solids": 150},
            "prediction": {"status": "Safe", "suggestions": ["Good to drink"]}
        }
        mock_post.return_value = mock_response

        # Create signal spy
        spy = QSignalSpy(self.backend.waterQualityUpdated)

        # Call the method
        self.backend.updateWaterQuality()

        # Assertions
        self.assertEqual(len(spy), 1)
        emitted_data = spy[0][0]
        self.assertEqual(emitted_data["input_data"]["turbidity"], 1.2)
        self.assertEqual(emitted_data["prediction"]["status"], "Safe")

    # ... rest of your test methods ...



    @patch('main.requests.post')
    def test_update_water_quality_server_error(self, mock_post):
        # Setup mock response with error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        spy = QSignalSpy(self.backend.waterQualityUpdated)
        self.backend.updateWaterQuality()

        self.assertEqual(len(spy), 1)
        emitted_data = spy[0][0]
        self.assertTrue("error" in emitted_data)
        self.assertEqual(emitted_data["input_data"]["turbidity"], "N/A")

    @patch('main.requests.post')
    def test_update_water_quality_connection_error(self, mock_post):
        # Setup mock to raise connection error
        mock_post.side_effect = requests.exceptions.RequestException("Connection failed")

        spy = QSignalSpy(self.backend.waterQualityUpdated)
        self.backend.updateWaterQuality()

        self.assertEqual(len(spy), 1)
        emitted_data = spy[0][0]
        self.assertTrue("error" in emitted_data)
        self.assertIn("Connection error", emitted_data["error"])

    def test_request_water_quality_update(self):
        # Test that changing water type updates the selection
        self.backend.requestWaterQualityUpdate("Lake Water")
        self.assertEqual(self.backend.selectedWaterType, "Lake Water")

if __name__ == '__main__':
    unittest.main()