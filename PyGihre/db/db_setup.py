import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "sqlite:///db/gihre.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'gihre.db')}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)






