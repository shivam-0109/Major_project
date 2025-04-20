# import sys
# import pytest
# from unittest.mock import MagicMock, patch
# from PyQt5.QtCore import QVariant
# from PyQt5.QtGui import QGuiApplication
# import requests

# # Import your backend module
# from main import Backend, resource_path  # Replace with your actual module

# @pytest.fixture(scope="module")
# def qapp():
#     """Fixture to provide QApplication instance for the tests"""
#     app = QGuiApplication.instance()
#     if app is None:
#         app = QGuiApplication(sys.argv)
#     yield app
#     # Cleanup if needed

# @pytest.fixture
# def backend(qapp):
#     """Fixture to provide a Backend instance for testing"""
#     backend = Backend()
#     # Mock the timer to avoid actual timeouts during tests
#     backend.timer = MagicMock()
#     yield backend

# def test_resource_path():
#     """Test the resource_path function works in both dev and packaged modes"""
#     # Test development mode
#     path = resource_path("test.txt")
#     assert "test.txt" in path
    
#     # Test PyInstaller mode
#     with patch.object(sys, '_MEIPASS', '/fake/path', create=True):
#         path = resource_path("test.txt")
#         assert path == "/fake/path\\test.txt"

# def test_backend_initialization(backend):
#     """Test that the backend initializes correctly"""
#     assert backend.selectedWaterType == "Drinking Water"
#     assert backend.data_file == "data.json"
#     assert backend.timer is not None

# @patch('requests.post')
# def test_update_water_quality_success(mock_post, backend):
#     """Test successful water quality update"""
#     # Setup mock response
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {
#         "input_data": {"turbidity": 5, "solids": 10},
#         "prediction": {"status": "Good", "suggestions": []}
#     }
#     mock_post.return_value = mock_response
    
#     # Mock the signal emission
#     backend.waterQualityUpdated = MagicMock()
    
#     backend.updateWaterQuality()
    
#     # Verify the request was made correctly
#     mock_post.assert_called_once_with(
#         "http://127.0.0.1:5000/predict",
#         json={"water_type": "Drinking Water"},
#         headers={"Content-Type": "application/json"},
#         timeout=5
#     )
    
#     # Verify the signal was emitted with correct data
#     backend.waterQualityUpdated.emit.assert_called_once()
#     emitted_data = backend.waterQualityUpdated.emit.call_args[0][0]
#     assert isinstance(emitted_data, (dict, QVariant))
#     if isinstance(emitted_data, QVariant):
#         emitted_data = emitted_data.toPyObject()
#     assert emitted_data["input_data"]["turbidity"] == 5

# @patch('requests.post')
# def test_update_water_quality_server_error(mock_post, backend):
#     """Test server error response"""
#     mock_response = MagicMock()
#     mock_response.status_code = 500
#     mock_post.return_value = mock_response
    
#     backend.waterQualityUpdated = MagicMock()
#     backend.updateWaterQuality()
    
#     assert backend.waterQualityUpdated.emit.called
#     emitted_data = backend.waterQualityUpdated.emit.call_args[0][0]
#     if isinstance(emitted_data, QVariant):
#         emitted_data = emitted_data.toPyObject()
#     assert "error" in emitted_data
#     assert "Server error: 500" in emitted_data["error"]

# @patch('requests.post')
# def test_update_water_quality_connection_error(mock_post, backend):
#     """Test connection error handling"""
#     mock_post.side_effect = requests.exceptions.RequestException("Connection failed")
    
#     backend.waterQualityUpdated = MagicMock()
#     backend.updateWaterQuality()
    
#     assert backend.waterQualityUpdated.emit.called
#     emitted_data = backend.waterQualityUpdated.emit.call_args[0][0]
#     if isinstance(emitted_data, QVariant):
#         emitted_data = emitted_data.toPyObject()
#     assert "error" in emitted_data
#     assert "Connection error" in emitted_data["error"]

# def test_request_water_quality_update(backend):
#     """Test the manual update request slot"""
#     backend.updateWaterQuality = MagicMock()
#     backend.requestWaterQualityUpdate("River Water")
    
#     assert backend.selectedWaterType == "River Water"
#     backend.updateWaterQuality.assert_called_once()

# def test_emit_error(backend):
#     """Test the error emission helper"""
#     backend.waterQualityUpdated = MagicMock()
#     test_msg = "Test error message"
#     backend.emitError(test_msg)
    
#     assert backend.waterQualityUpdated.emit.called
#     emitted_data = backend.waterQualityUpdated.emit.call_args[0][0]
#     if isinstance(emitted_data, QVariant):
#         emitted_data = emitted_data.toPyObject()
#     assert emitted_data["error"] == test_msg
#     assert emitted_data["input_data"]["turbidity"] == "N/A"
#     assert emitted_data["prediction"]["status"] == "Error"
