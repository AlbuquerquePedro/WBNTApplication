from flask import Flask, jsonify, request
from controllers import get_all_notes, get_note, create_note, update_note, delete_note
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def main_page():
    return "<h1>Welcome to the Notes App</h1>"

@app.route('/api/notes', methods=['GET'])
def api_get_all_notes():
    return jsonify(get_all_notes())

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def api_get_note(note_id):
    return jsonify(get_note(note_id))

@app.route('/api/notes', methods=['POST'])
def api_create_note():
    note_data = request.json
    return jsonify(create_note(note_data)), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def api_update_note(note_id):
    note |data = request.json
    return jsonify(update_note(note_id, note_data))

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def api_delete_note(note_id):
    return jsonify(delete_note(note_id))

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT', 5000))