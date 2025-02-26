from flask import Flask, jsonify
import random
from water_quality_model import WaterQualityPredictor

app = Flask(__name__)
model = WaterQualityPredictor()

def generate_random_data():
    return {
        "ph": round(random.uniform(5, 9), 2),
        "hardness": round(random.uniform(100, 300), 2),
        "solids": round(random.uniform(500, 1500), 2),
        "chloramines": round(random.uniform(0, 10), 2),
        "sulfate": round(random.uniform(100, 500), 2),
        "conductivity": round(random.uniform(500, 3000), 2),
        "organicCarbon": round(random.uniform(1, 20), 2),
        "trihalomethanes": round(random.uniform(10, 100), 2),
        "turbidity": round(random.uniform(1, 15), 2)
    }

@app.route("/predict", methods=["GET"])
def predict():
    data = generate_random_data()
    result = model.predict(data)
    return jsonify({"input_data": data, "prediction": result})

if __name__ == "__main__":
    app.run(debug=True)
