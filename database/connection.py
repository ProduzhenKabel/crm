# database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# TODO: Update with your MySQL credentials
DATABASE_URL = "mysql+mysqlconnector://root:Berberis!a@localhost:3306/crm?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()
