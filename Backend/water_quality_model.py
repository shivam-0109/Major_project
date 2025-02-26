# water_quality_model.py
import joblib

class WaterQualityPredictor:
    def __init__(self, model_path="svm.pkl"):
        self.model = joblib.load(model_path)

    def predict(self, data: dict):
        features = [
            data["ph"], data["hardness"], data["solids"], data["chloramines"],
            data["sulfate"], data["conductivity"], data["organicCarbon"],
            data["trihalomethanes"], data["turbidity"]
        ]
        
        prediction = self.model.predict([features])[0]
        result = {"status": "Safe for Drinking"} if prediction == 1 else {"status": "Non-drinkable"}
        
        if prediction == 0:
            suggestions = []
            if not (6.5 <= data["ph"] <= 8.5):
                suggestions.append("Adjust pH level between 6.5 and 8.5 using appropriate chemicals.")
            if data["hardness"] > 200:
                suggestions.append("Use a water softener to reduce hardness.")
            if data["solids"] > 1000:
                suggestions.append("Consider filtration to reduce total dissolved solids.")
            if data["turbidity"] > 10:
                suggestions.append("Use sediment filters to lower turbidity.")
            if data["chloramines"] > 4:
                suggestions.append("Use activated carbon filters to remove excess chloramines.")
            if data["conductivity"] > 2000:
                suggestions.append("Reverse osmosis can help reduce high conductivity levels.")
            
            result["suggestions"] = suggestions if suggestions else ["No specific suggestions available."]
        
        return result