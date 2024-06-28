from sqlalchemy import create_engine, Column, Integer, String, DateTime, or_
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker, exc
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    raise ValueError("No DATABASE_URL found. Set the DATABASE_URL environment variable.")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_note(title, content):
    try:
        new_note = Note(title=title, content=content)
        session.add(new_note)
        session.commit()
        return f'Note "{title}" created successfully.'
    except Exception as e:
        session.rollback()
        return f'Failed to create note. Error: {str(e)}'

def read_notes():
    try:
        notes = session.query(Note).all()
        return notes
    except Exception as e:
        return f'Failed to read notes. Error: {str(e)}'

def update_note(id, title=None, content=None):
    try:
        note = session.query(Note).filter(Note.id == id).one()
    except exc.NoResultFound:
        return 'Note not found.'
    except Exception as e:
        return f'Failed to update note. Error: {str(e)}'
    
    try:
        if title:
            note.title = title
        if content:
            note.content = content
        session.commit()
        return f'Note ID {id} updated successfully.'
    except Exception as e:
        session.rollback()
        return f'Failed to update note. Error: {str(e)}'

def delete_note(id):
    try:
        note = session.query(Note).filter(Note.id == id).one()
    except exc.NoResultFound:
        return 'Note not found.'
    
    try:
        session.delete(note)
        session.commit()
        return f'Note ID {id} deleted successfully.'
    except Exception as e:
        session.rollback()
        return f'Failed to delete note. Error: {str(e)}'

def search_notes(keyword):
    try:
        notes = session.query(Note).filter(
            or_(Note.title.like(f'%{keyword}%'), Note.content.like(f'%{keyword}%'))
        ).all()
        if notes:
            return notes
        else:
            return 'No notes found matching your search criteria.'
    except Exception as e:
        return f'Failed to search notes. Error: {str(e)}'

if __name__ == '__main__':
    print(create_note('Sample Note', 'This is a sample note.'))
    notes = read_notes()
    if isinstance(notes, str):
        print(notes)
    else:
        for note in notes:
            print(f'{note.title}: {note.content} (created on {note.date_created})')
    print(update_note(1, title='Updated Sample Note', content='This note has been updated.'))
    print(delete_note(1))
    print('Search result:')
    search_results = search_notes('sample')  # Example search
    if isinstance(search_results, str):
        print(search_results)
    else:
  for note in search_results:
            print(f'{note.title}: {note.content} (created on {note.date_created})')