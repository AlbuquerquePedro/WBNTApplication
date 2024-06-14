from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()
Base = declarative_base()
class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
new_note = Note(title='Sample Note', content='This is a sample note.')
session.add(new_note)
session.commit()
notes = session.query(Note).all()
for note in notes:
    print(f'{note.title}: {note.content} (created on {note.date_created})')