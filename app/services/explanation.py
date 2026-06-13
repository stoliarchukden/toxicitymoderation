import joblib


model = joblib.load("app/ml/model.pkl")
vectorizer = joblib.load("app/ml/vectorizer.pkl")


def explain_comment(text: str, top_n: int = 5) -> list:
    """
    Explain prediction using TF-IDF feature weights
    and Logistic Regression coefficients.
    """

    transformed_text = vectorizer.transform([text])

    predicted_label = model.predict(transformed_text)[0]

    class_index = list(model.classes_).index(predicted_label)

    feature_names = vectorizer.get_feature_names_out()

    coefficients = model.coef_[class_index]

    tfidf_values = transformed_text.toarray()[0]

    word_scores = []

    for index, value in enumerate(tfidf_values):
        if value > 0:
            weight = value * coefficients[index]

            if weight > 0:
                word_scores.append(
                    {
                        "word": feature_names[index],
                        "weight": round(float(weight), 4),
                    }
                )

    word_scores = sorted(
        word_scores,
        key=lambda item: item["weight"],
        reverse=True,
    )

    return word_scores[:top_n]