from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base class for our classes definitions
Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)

# Establish database connection
engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(engine)

# Create a Session class which will be used as a factory for session objects
Session = sessionmaker(bind=engine)
session = Session()

# Create a new note
def create_note(title, content):
    new_note = Note(title=title, content=content)
    session.add(new_note)
    session.commit()
    return f'Note "{title}" created successfully.'

# Read all notes
def read_notes():
    notes = session.query(Note).all()
    return notes

# Update a note by ID
def update_note(id, title=None, content=None):
    note = session.query(Note).filter(Note.id == id).first()
    if note:
        if title:
            note.title = title
        if content:
            note.content = content
        session.commit()
        return f'Note ID {id} updated successfully.'
    else:
        return 'Note not found.'

# Delete a note by ID
def delete_note(id):
    note = session.query(Note).filter(Note.id == id).first()
    if note:
        session.delete(note)
        session.commit()
        return f'Note ID {id} deleted successfully.'
    else:
        return 'Note not found.'

# Example usage
if __name__ == '__main__':
    print(create_note('Sample Note', 'This is a sample note.'))
    
    # Display all notes
    notes = read_notes()
    for note in notes:
        print(f'{note.title}: {note.content} (created on {note.date_created})')

    # Update a note (Assuming ID 1 exists)
    print(update_note(1, title='Updated Sample Note', content='This note has been updated.'))

    # Delete a note (Assuming ID 1 exists and you wish to delete it)
    print(delete_note(1))