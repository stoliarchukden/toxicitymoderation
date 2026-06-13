import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


df = pd.read_csv("app/ml/dataset.csv")

texts = df["text"]
labels = df["label"]


vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
)

X = vectorizer.fit_transform(texts)


model = LogisticRegression(
    max_iter=1000,
)

model.fit(X, labels)


joblib.dump(model, "app/ml/model.pkl")
joblib.dump(vectorizer, "app/ml/vectorizer.pkl")


print("Model trained successfully.")