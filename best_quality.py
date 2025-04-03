import json
import random
import time
from threading import Thread
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables to store current sensor data
current_sensor_data = {"turbidity": 0.0, "tds": 0.0}
sensor_data_lock = False

def sensor_data_updater():
    """Thread that continuously updates sensor data from data.json"""
    global current_sensor_data, sensor_data_lock
    while True:
        try:
            # Prevent reading while data is being used
            while sensor_data_lock:
                time.sleep(0.1)
                
            sensor_data_lock = True
            with open("data.json", "r") as file:
                new_data = json.load(file)
                current_sensor_data["turbidity"] = new_data.get("turbidity", 0.0)
                current_sensor_data["tds"] = new_data.get("tds", 0.0)
            sensor_data_lock = False
            
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            sensor_data_lock = False
            
        time.sleep(2)  # Update every 2 seconds

# Start the sensor data updater thread
sensor_thread = Thread(target=sensor_data_updater, daemon=True)
sensor_thread.start()

# Enhanced water quality profiles with expected ranges
WATER_PROFILES = {
    "Drinking Water": {
        "ph": 7.5, 
        "hardness": 150, 
        "sulfate": 125, 
        "conductivity": 250, 
        "chloramines": 2, 
        "organicCarbon": 5,
        "tds_range": (30, 50),
        "turbidity_range": (0, 1)
    },
    "Tap Water": {
        "ph": 7.0, 
        "hardness": 200, 
        "sulfate": 150, 
        "conductivity": 300, 
        "chloramines": 3, 
        "organicCarbon": 8,
        "tds_range": (40, 80),
        "turbidity_range": (0, 5)
    },
    "Lake Water": {
        "ph": 6.8, 
        "hardness": 250, 
        "sulfate": 200, 
        "conductivity": 400, 
        "chloramines": 1, 
        "organicCarbon": 15,
        "tds_range": (100, 300),
        "turbidity_range": (5, 50)
    },
    "Ash/Mud": {
        "ph": 7.2, 
        "hardness": 280, 
        "sulfate": 220, 
        "conductivity": 500, 
        "chloramines": 0.5, 
        "organicCarbon": 12,
        "tds_range": (600, 800),
        "turbidity_range": (100, 200)
    },
    "Soap Water": {
        "ph": 9.0, 
        "hardness": 300, 
        "sulfate": 250, 
        "conductivity": 3000, 
        "chloramines": 10, 
        "organicCarbon": 20,
        "tds_range": (400, 500),
        "turbidity_range": (10, 20)
    }
}

class WaterQualityPredictor:
    def predict(self, input_data):
        water_type = input_data.get("water_type", "Drinking Water")
        tds = input_data.get("solids", 0)
        turbidity = input_data.get("turbidity", 0)
        profile = WATER_PROFILES.get(water_type, WATER_PROFILES["Drinking Water"])
        
        # Get expected ranges for this water type
        tds_min, tds_max = profile["tds_range"]
        turbidity_min, turbidity_max = profile["turbidity_range"]
        
        # Analyze parameters
        tds_status = self._analyze_parameter(tds, tds_min, tds_max, "TDS")
        turbidity_status = self._analyze_parameter(turbidity, turbidity_min, turbidity_max, "Turbidity")
        ph_status = self._analyze_parameter(input_data["ph"], 6.5, 8.5, "pH")
        
        # Determine overall status
        status, severity = self._determine_status(tds_status, turbidity_status, ph_status, water_type)
        
        # Generate detailed suggestions
        suggestions = self._generate_suggestions(
            tds_status, 
            turbidity_status, 
            ph_status,
            water_type,
            input_data
        )
        
        return {
            "status": status,
            "severity": severity,
            "suggestions": suggestions,
            "analysis": {
                "tds": tds_status,
                "turbidity": turbidity_status,
                "ph": ph_status
            }
        }
    
    def _analyze_parameter(self, value, min_val, max_val, param_name):
        if value < min_val * 0.7:
            return {"status": "Very Low", "value": value, "expected": f"{min_val}-{max_val}"}
        elif value > max_val * 1.3:
            return {"status": "Very High", "value": value, "expected": f"{min_val}-{max_val}"}
        elif value < min_val:
            return {"status": "Low", "value": value, "expected": f"{min_val}-{max_val}"}
        elif value > max_val:
            return {"status": "High", "value": value, "expected": f"{min_val}-{max_val}"}
        else:
            return {"status": "Normal", "value": value, "expected": f"{min_val}-{max_val}"}
    
    def _determine_status(self, tds_status, turbidity_status, ph_status, water_type):
        critical_count = sum(1 for s in [tds_status, turbidity_status, ph_status] 
                         if s["status"] in ["Very High", "Very Low"])
        warning_count = sum(1 for s in [tds_status, turbidity_status, ph_status] 
                        if s["status"] in ["High", "Low"])
        
        if water_type == "Soap Water":
            return "Not Drinkable", "Critical"
        elif critical_count > 0:
            return "Non-Drinkable", "Critical"
        elif warning_count > 0:
            return "Needs Treatment", "Warning"
        else:
            return "Drinkable", "Normal"
    
    def _generate_suggestions(self, tds_status, turbidity_status, ph_status, water_type, input_data):
        suggestions = []
        
        # Water type specific suggestions
        if water_type == "Drinking Water":
            suggestions.append("Suitable for direct consumption if parameters are normal")
        elif water_type == "Tap Water":
            suggestions.append("May need basic filtration before drinking")
        elif water_type == "Lake Water":
            suggestions.append("Requires thorough treatment - consider filtration and disinfection")
        elif water_type == "Ash/Mud":
            suggestions.append("Needs extensive treatment - professional purification recommended")
        elif water_type == "Soap Water":
            suggestions.append("Not suitable for drinking - can be used for cleaning purposes")
        
        # TDS suggestions
        if tds_status["status"] == "Very High":
            suggestions.append("Use reverse osmosis or distillation to reduce high TDS")
        elif tds_status["status"] == "High":
            suggestions.append("Consider using a water softener for elevated TDS levels")
        elif tds_status["status"] == "Low":
            suggestions.append("Add mineral supplements to increase low TDS")
        
        # Turbidity suggestions
        if turbidity_status["status"] == "Very High":
            suggestions.append("Use coagulation-flocculation followed by sand filtration for high turbidity")
        elif turbidity_status["status"] == "High":
            suggestions.append("Use cartridge filters or activated carbon for turbidity reduction")
        
        # pH suggestions
        if ph_status["status"] == "Very High":
            suggestions.append("Add citric acid or vinegar to lower extremely high pH")
        elif ph_status["status"] == "High":
            suggestions.append("Use pH reducers to adjust alkaline water")
        elif ph_status["status"] == "Low":
            suggestions.append("Add baking soda to raise low pH levels")
        elif ph_status["status"] == "Very Low":
            suggestions.append("Use professional pH correction systems for highly acidic water")
        
        # Additional chemical suggestions
        if input_data["chloramines"] > 4:
            suggestions.append("Use activated carbon filtration to remove excess chloramines")
        if input_data["organicCarbon"] > 10:
            suggestions.append("Consider advanced oxidation process for high organic carbon")
        
        if not suggestions:
            suggestions.append("Water quality is excellent - no treatment needed")
        
        return suggestions

def generate_water_data(water_type):
    """Generate input data using current sensor readings"""
    global current_sensor_data, sensor_data_lock
    
    # Wait for lock to be released
    while sensor_data_lock:
        time.sleep(0.1)
    
    sensor_data_lock = True
    turbidity = current_sensor_data["turbidity"]
    tds = current_sensor_data["tds"]
    sensor_data_lock = False

    profile = WATER_PROFILES.get(water_type, WATER_PROFILES["Drinking Water"])
    
    return {
        "ph": profile["ph"],
        "hardness": profile["hardness"],
        "solids": tds,
        "chloramines": profile["chloramines"],
        "sulfate": profile["sulfate"],
        "conductivity": profile["conductivity"],
        "organicCarbon": profile["organicCarbon"],
        "trihalomethanes": round(random.uniform(10, 100), 2),
        "turbidity": turbidity,
        "water_type": water_type
    }

@app.route("/predict", methods=["POST", "GET"])
def predict():
    try:
        if request.method == "POST":
            data = request.get_json()
        else:
            data = request.args
            
        water_type = data.get("water_type", "Drinking Water")
        print(f"Predicting for {water_type} with current sensor data")
        
        input_data = generate_water_data(water_type)
        result = WaterQualityPredictor().predict(input_data)
        
        return jsonify({
            "input_data": input_data,
            "prediction": result,
            "water_type": water_type
        })

    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)