from sqlalchemy import Column, Integer, Text
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Text)
    issues = Column(Text)
    score = Column(Integer)
    ai_review = Column(Text)