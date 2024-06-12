const API_URL = process.env.REACT_APP_API_URL;

async function fetchNotes() {
  try {
    const response = await fetch(`${API_URL}/notes`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('There was a problem with your fetch operation:', error);
  }
}

function displayNotes(notes) {
  const notesElement = document.querySelector('#notes');
  notesElement.innerHTML = '';
  
  notes.forEach(note => {
    const noteElement = document.createElement('div');
    noteElement.classList.add('note');
    noteElement.innerHTML = `
      <h3>${note.title}</h3>
      <p>${note.content}</p>
    `;
    notesElement.appendChild(noteElement);
  });
}

async function initApp() {
  const notes = await fetchNotes();
  if (notes) {
    displayNotes(notes);
  }
}

document.addEventListener('DOMContentLoaded', initApp);