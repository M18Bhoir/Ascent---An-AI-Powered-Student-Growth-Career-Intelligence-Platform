from app.database import Base, engine
from app.models import (
    Achievement,
    BehaviorEvent,
    Department,
    Domain,
    Faculty,
    Project,
    Skill,
    Student,
    User,
)


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()