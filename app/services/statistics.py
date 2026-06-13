from sqlalchemy.orm import Session

from app.models.comment import Comment


def get_statistics(db: Session) -> dict:
    total_comments = db.query(Comment).count()

    non_toxic_count = (
        db.query(Comment)
        .filter(Comment.model_label == "non-toxic")
        .count()
    )

    suspicious_count = (
        db.query(Comment)
        .filter(Comment.model_label == "suspicious")
        .count()
    )

    toxic_count = (
        db.query(Comment)
        .filter(Comment.model_label == "toxic")
        .count()
    )

    pending_count = (
        db.query(Comment)
        .filter(Comment.moderation_status == "pending")
        .count()
    )

    approved_count = (
        db.query(Comment)
        .filter(Comment.moderation_status == "approved")
        .count()
    )

    rejected_count = (
        db.query(Comment)
        .filter(Comment.moderation_status == "rejected")
        .count()
    )

    toxic_percent = 0

    if total_comments > 0:
        toxic_percent = round((toxic_count / total_comments) * 100, 1)

    return {
        "total_comments": total_comments,
        "non_toxic_count": non_toxic_count,
        "suspicious_count": suspicious_count,
        "toxic_count": toxic_count,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "toxic_percent": toxic_percent,
    }