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
def get_all_notes():
    try:
        notes_list = Note.query.all()
        return jsonify([{'id': note.id, 'content': note.content} for note in notes_list]), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/note', methods=['POST'])
def create_new_note():
    try:
        note_data = request.get_json()
        if not note_data or not note_data.get('content'):
            return jsonify({'message': 'No content provided'}), 400
        new_note = Note(content=note_data['content'])
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'id': new_note.id, 'content': new_note.content}), 201
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/note/<int:note_id>', methods=['PUT'])
def update_existing_note(note_id):
    try:
        update_data = request.get_json()
        note_to_update = Note.query.get_or_404(note_id)
        note_to_update.content = update_data['content']
        db.session.commit()
        return jsonify({'id': note_to_update.id, 'content': note_to_update.content}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/note/<int:note_id>', methods=['DELETE'])
def delete_specific_note(note_id):
    try:
        note_to_delete = Note.query.get_or_404(note_id)
        db.session.delete(note_to_delete)
        db.session.commit()
        return jsonify({'message': 'Note deleted successfully.'}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.errorhandler(404)
def handle_404_errors(error):
    return jsonify(error=str(error)), 404

@app.errorhandler(400)
def handle_400_errors(error):
    return jsonify(error=str(error)), 400

if __name__ == '__main__':
    app.run(debug=True)