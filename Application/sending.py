from flask import Flask, jsonify
import random
import time
from threading import Thread

app = Flask(__name__)

def generate_random_data():
    # Function to generate random water quality parameters
    water_quality_data = {
        'pH': round(random.uniform(6.5, 8.5), 2),
        'Turbidity': random.randint(1, 100),
        'Dissolved Oxygen': round(random.uniform(5.0, 12.0), 2),
        'Salinity': round(random.uniform(0.1, 5.0), 2),
        'Temperature': random.randint(18, 30),
        'Nitrate Concentration': round(random.uniform(0.0, 10.0), 2)
    }
    # Calculate WQI (Water Quality Index) as a random value for now
    wqi = round(random.uniform(50, 100), 2)
    
    return {**water_quality_data, 'WQI': wqi}

def send_data():
    while True:
        data = generate_random_data()
        print(f"Generated Data: {data}")  # Print the generated data for debugging
        # This could be updated with a mechanism to send the data (e.g., push to subscribers)
        time.sleep(30)  # Sleep for 30 seconds

@app.route('/get_water_quality', methods=['GET'])
def get_water_quality():
    data = generate_random_data()
    return jsonify(data)

if __name__ == "__main__":
    # Start the background thread to generate and print data at 30-second intervals
    data_thread = Thread(target=send_data)
    data_thread.daemon = True
    data_thread.start()

    app.run(debug=True, host="0.0.0.0", port=5000)
