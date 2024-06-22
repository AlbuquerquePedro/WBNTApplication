from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI)
SessionLocal = scoped_ipfs_session_factory(sessionmaker(autocommit=False, autoflush=False, bind=engine))