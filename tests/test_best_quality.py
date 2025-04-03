import unittest
import json
from unittest.mock import patch, mock_open
from flask import Flask
from best_quality import app, generate_water_data, WaterQualityPredictor

class TestWaterQualityAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("builtins.open", new_callable=mock_open, read_data='{"turbidity": 5.0, "tds": 100}')
    def test_sensor_data_update(self, mock_file):
        data = generate_water_data("Lake Water")
        self.assertGreaterEqual(data["turbidity"], 0)
        self.assertGreaterEqual(data["solids"], 0)
    
    def test_prediction_valid_input(self):
        test_data = {
            "water_type": "Drinking Water",
            "ph": 7.5,
            "hardness": 150,
            "solids": 45,
            "chloramines": 2,
            "sulfate": 125,
            "conductivity": 250,
            "organicCarbon": 5,
            "trihalomethanes": 50,
            "turbidity": 0.5
        }
        predictor = WaterQualityPredictor()
        result = predictor.predict(test_data)
        self.assertIn("status", result)
        self.assertIn("severity", result)
        self.assertIn("suggestions", result)

    def test_predict_endpoint_post(self):
        response = self.app.post("/predict", data=json.dumps({"water_type": "Lake Water"}),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("prediction", data)
        self.assertIn("input_data", data)

    def test_predict_endpoint_get(self):
        response = self.app.get("/predict?water_type=Lake Water")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("prediction", data)

    @patch("best_quality.generate_water_data", side_effect=Exception("Test Exception"))
    def test_predict_error_handling(self, mock_gen_data):
        response = self.app.post("/predict", data=json.dumps({"water_type": "Lake Water"}),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
