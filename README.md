# Toxicity Moderation

Toxicity Moderation is a web service for moderating user comments with explainable toxicity classification.

The system allows a moderator to:

* add and review comments,
* classify them as **non-toxic**, **suspicious**, or **toxic**,
* view the model confidence score,
* see keyword-based explanations,
* approve or reject comments,
* track moderation actions,
* view basic statistics.

## Tech Stack

* FastAPI
* Jinja2
* Bootstrap 5
* SQLAlchemy
* PostgreSQL (Supabase)
* scikit-learn

## Run Locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with required variables:

   * `DATABASE_URL`
   * `SECRET_KEY`
   * `DEMO_USERNAME`
   * `DEMO_PASSWORD`

3. Start the app:

   ```bash
   uvicorn app.main:app --reload
   ```

## Main Features

* Moderator authentication
* Comment classification
* Explainable predictions
* Moderation workflow
* Moderation log
* Statistics dashboard
