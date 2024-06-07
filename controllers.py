import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([{'id': note.id, 'content': note.content} for note in notes]), 200

@app.route('/note', methods=['POST'])
def create_note():
    data = request.get_json()
    new_note = Note(content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'id': new_note.id, 'content': new_note.content}), 201

@app.route('/note/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.get_json()
    note = Note.query.get_or_404(id)
    note.content = data['content']
    db.session.commit()
    return jsonify({'id': note.id, 'content': note.content}), 200

@app.route('/note/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.config.commit()
    return jsonify({'message': 'Note deleted successfully.'}), 200

if __name__ == '__main__':
    app.run(debug=True)