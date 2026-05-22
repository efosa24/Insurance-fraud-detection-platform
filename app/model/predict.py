import joblib
import pandas as pd
import numpy as np

from app.utils.config import MODEL_PATH, PIPELINE_PATH

model = joblib.load(MODEL_PATH)
pipeline = joblib.load(PIPELINE_PATH)

expected_columns = list(pipeline.feature_names_in_)

class FraudPredictor:

    def predict(self, data):

        df = pd.DataFrame([data])

        # Ensure the input data includes every feature the pipeline was trained on.
        # Missing values are filled with pandas NA so the preprocessing pipeline
        # can impute them consistently.
        missing_columns = [col for col in expected_columns if col not in df.columns]
        for col in missing_columns:
            df[col] = np.nan

        df = df[expected_columns]

        transformed = pipeline.transform(df)

        prediction = model.predict(transformed)[0]
        probability = model.predict_proba(transformed)[0][1]

        return {
            "fraud_prediction": int(prediction),
            "fraud_probability": round(float(probability), 4)
        }