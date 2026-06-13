import joblib
import numpy as np


model = joblib.load("app/ml/model.pkl")

vectorizer = joblib.load("app/ml/vectorizer.pkl")


def predict_toxicity(text: str) -> dict:
    """
    Predict toxicity using trained ML model.
    """

    transformed_text = vectorizer.transform([text])

    prediction = model.predict(transformed_text)[0]

    probabilities = model.predict_proba(transformed_text)[0]

    max_probability = float(np.max(probabilities))

    return {
        "label": prediction,
        "score": round(max_probability, 2),
    }