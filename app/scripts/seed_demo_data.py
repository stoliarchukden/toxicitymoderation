from app.database import SessionLocal
from app.models.comment import Comment
from app.services.classifier import predict_toxicity
from app.services.explanation import explain_comment


demo_comments = [
    ("John", "Thank you for your help"),
    ("Alice", "This explanation was very useful"),
    ("Michael", "You are stupid and useless"),
    ("Emma", "This sounds strange and questionable"),
    ("David", "Great work on the project"),
    ("Sophia", "I hate this stupid discussion"),
    ("Robert", "I am not sure this is safe"),
    ("Olivia", "Your answer solved my problem"),
    ("Daniel", "You are an idiot"),
    ("Grace", "This may be problematic"),
    ("Andrew", "The interface looks clean and modern"),
    ("Kate", "Nobody wants you here"),
    ("William", "This comment feels borderline toxic"),
    ("Laura", "I appreciate the detailed explanation"),
    ("Thomas", "Your idea is terrible"),
    ("Mia", "The response may offend someone"),
    ("James", "Everything works perfectly"),
    ("Nora", "This wording is somewhat offensive"),
    ("Peter", "You are a moron"),
    ("Anna", "The instructions are easy to follow"),
]


def seed_demo_data():
    db = SessionLocal()

    try:
        for author_name, text in demo_comments:
            prediction = predict_toxicity(text)
            explanations = explain_comment(text)

            comment = Comment(
                author_name=author_name,
                text=text,
                model_label=prediction["label"],
                toxicity_score=prediction["score"],
                explanation_json=explanations,
                moderation_status="pending",
            )

            db.add(comment)

        db.commit()

        print("Demo data inserted successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()