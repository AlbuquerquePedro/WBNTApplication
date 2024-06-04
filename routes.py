from flask import Flask, jsonify, request
from controllers import fetch_all_notes, fetch_note_by_id, create_new_note, update_existing_note, remove_note
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def homepage():
    return "<h1>Welcome to the Notes App</h1>"

@app.route('/api/notes', methods=['GET'])
def handle_get_all_notes():
    return jsonify(fetch_all_notes())

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def handle_get_single_note(note_id):
    return jsonify(fetch_note_by_id(note_id))

@app.route('/api/notes', methods=['POST'])
def handle_create_note():
    note_details = request.json
    return jsonify(create_new_note(note_details)), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def handle_update_note(note_id):
    updated_note_details = request.json
    return jsonify(update_existing_note(note_id, updated_note_details))

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def handle_delete_note(note_id):
    return jsonify(remove_note(note_id))

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT', 5000))