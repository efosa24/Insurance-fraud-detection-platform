import joblib
import pandas as pd

from app.utils.config import MODEL_PATH, PIPELINE_PATH

model = joblib.load(MODEL_PATH)
pipeline = joblib.load(PIPELINE_PATH)

class FraudPredictor:

    def predict(self, data):

        df = pd.DataFrame([data])

        transformed = pipeline.transform(df)

        prediction = model.predict(transformed)[0]
        probability = model.predict_proba(transformed)[0][1]

        return {
            "fraud_prediction": int(prediction),
            "fraud_probability": round(float(probability), 4)
        }