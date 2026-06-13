from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy.sql import func
from sqlalchemy import JSON

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    author_name = Column(String, nullable=False)

    text = Column(Text, nullable=False)

    model_label = Column(String, nullable=False)

    toxicity_score = Column(Float, nullable=False)

    explanation_json = Column(
        JSON,
        nullable=True,
    )
    
    moderation_status = Column(
        String,
        default="pending",
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )   