from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./responses.db")

Base = declarative_base()


class UserResponses(Base):
    __tablename__ = "user_responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)
    education = Column(String, nullable=True)
    familiarity = Column(String, nullable=True)
    crt_q1_answer = Column(Float, nullable=True)
    crt_q1_correct = Column(Boolean, nullable=True)
    crt_q1_response_time = Column(Float, nullable=True)
    crt_q2_answer = Column(Float, nullable=True)
    crt_q2_correct = Column(Boolean, nullable=True)
    crt_q2_response_time = Column(Float, nullable=True)
    crt_q3_answer = Column(Float, nullable=True)
    crt_q3_correct = Column(Boolean, nullable=True)
    crt_q3_response_time = Column(Float, nullable=True)
    delay_choice = Column(String, nullable=True)
    delay_response_time = Column(Float, nullable=True)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user_responses(session_id, responses):
    db = next(get_db())
    user_responses = UserResponses(
        session_id=session_id,
        age=responses.get("demographics", {}).get("age"),
        education=responses.get("demographics", {}).get("education"),
        familiarity=responses.get("demographics", {}).get("familiarity"),
        crt_q1_answer=responses.get("crt", [{}])[0].get("user_answer"),
        crt_q1_correct=responses.get("crt", [{}])[0].get("is_correct"),
        crt_q1_response_time=responses.get("crt", [{}])[0].get("response_time"),
        crt_q2_answer=responses.get("crt", [{}])[1].get("user_answer"),
        crt_q2_correct=responses.get("crt", [{}])[1].get("is_correct"),
        crt_q2_response_time=responses.get("crt", [{}])[1].get("response_time"),
        crt_q3_answer=responses.get("crt", [{}])[2].get("user_answer"),
        crt_q3_correct=responses.get("crt", [{}])[2].get("is_correct"),
        crt_q3_response_time=responses.get("crt", [{}])[2].get("response_time"),
        delay_choice=responses.get("delay_discounting", [{}])[0].get("user_answer"),
        delay_response_time=responses.get("delay_discounting", [{}])[0].get(
            "response_time"
        ),
    )
    db.add(user_responses)
    db.commit()
    db.refresh(user_responses)
    return user_responses


from sqlalchemy.orm import Session


def fetch_all_responses(db: Session):
    return db.query(UserResponses).all()
