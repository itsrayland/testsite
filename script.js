// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initStickyNotes();
    initChat();
});

// Sticky Notes functionality
let notes = JSON.parse(localStorage.getItem('stickyNotes')) || [];
let noteIdCounter = notes.length > 0 ? Math.max(...notes.map(n => n.id)) + 1 : 1;

function initStickyNotes() {
    const addNoteBtn = document.getElementById('addNoteBtn');
    const notesContainer = document.getElementById('notesContainer');
    
    addNoteBtn.addEventListener('click', createNewNote);
    renderNotes();
}

function createNewNote() {
    const note = {
        id: noteIdCounter++,
        content: '',
        color: 'yellow',
        timestamp: new Date().toISOString()
    };
    
    notes.push(note);
    saveNotes();
    renderNotes();
    
    // Focus on the new note
    setTimeout(() => {
        const noteElement = document.querySelector(`[data-note-id="${note.id}"] textarea`);
        if (noteElement) noteElement.focus();
    }, 100);
}

function renderNotes() {
    const notesContainer = document.getElementById('notesContainer');
    notesContainer.innerHTML = '';
    
    notes.forEach(note => {
        const noteElement = createNoteElement(note);
        notesContainer.appendChild(noteElement);
    });
}

function createNoteElement(note) {
    const noteDiv = document.createElement('div');
    noteDiv.className = `sticky-note color-${note.color}`;
    noteDiv.dataset.noteId = note.id;
    
    const timestamp = new Date(note.timestamp).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    noteDiv.innerHTML = `
        <div class="note-header">
            <span class="note-timestamp">${timestamp}</span>
            <div class="note-actions">
                <button class="note-btn color-btn" title="Change color">🎨</button>
                <button class="note-btn delete-btn" title="Delete note">✖</button>
            </div>
        </div>
        <div class="color-picker" style="display: none;">
            <div class="color-option" data-color="yellow" style="background: #fff3cd;"></div>
            <div class="color-option" data-color="pink" style="background: #f8d7da;"></div>
            <div class="color-option" data-color="blue" style="background: #d1ecf1;"></div>
            <div class="color-option" data-color="green" style="background: #d4edda;"></div>
        </div>
        <textarea class="note-input" placeholder="Type your note here...">${note.content}</textarea>
    `;
    
    // Add event listeners
    const textarea = noteDiv.querySelector('.note-input');
    const deleteBtn = noteDiv.querySelector('.delete-btn');
    const colorBtn = noteDiv.querySelector('.color-btn');
    const colorPicker = noteDiv.querySelector('.color-picker');
    const colorOptions = noteDiv.querySelectorAll('.color-option');
    
    textarea.addEventListener('input', (e) => updateNoteContent(note.id, e.target.value));
    deleteBtn.addEventListener('click', () => deleteNote(note.id));
    colorBtn.addEventListener('click', () => {
        colorPicker.style.display = colorPicker.style.display === 'none' ? 'flex' : 'none';
    });
    
    colorOptions.forEach(option => {
        option.addEventListener('click', () => {
            const color = option.dataset.color;
            updateNoteColor(note.id, color);
            colorPicker.style.display = 'none';
        });
    });
    
    return noteDiv;
}

function updateNoteContent(id, content) {
    const note = notes.find(n => n.id === id);
    if (note) {
        note.content = content;
        saveNotes();
    }
}

function updateNoteColor(id, color) {
    const note = notes.find(n => n.id === id);
    if (note) {
        note.color = color;
        saveNotes();
        renderNotes();
    }
}

function deleteNote(id) {
    notes = notes.filter(n => n.id !== id);
    saveNotes();
    renderNotes();
}

function saveNotes() {
    localStorage.setItem('stickyNotes', JSON.stringify(notes));
}

// Chat functionality
let messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
let username = localStorage.getItem('username') || generateUsername();

function initChat() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatMessages = document.getElementById('chatMessages');
    
    renderMessages();
    
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Simulate receiving messages (for demo purposes)
    simulateIncomingMessages();
    
    // Poll for new messages (simulating real-time)
    setInterval(checkForNewMessages, 2000);
}

function generateUsername() {
    const adjectives = ['Happy', 'Creative', 'Brilliant', 'Dynamic', 'Friendly'];
    const nouns = ['Developer', 'Designer', 'Manager', 'Analyst', 'Engineer'];
    const username = `${adjectives[Math.floor(Math.random() * adjectives.length)]}${nouns[Math.floor(Math.random() * nouns.length)]}${Math.floor(Math.random() * 100)}`;
    localStorage.setItem('username', username);
    return username;
}

function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const messageText = chatInput.value.trim();
    
    if (messageText) {
        const message = {
            id: Date.now(),
            text: messageText,
            sender: username,
            timestamp: new Date().toISOString(),
            type: 'sent'
        };
        
        messages.push(message);
        saveMessages();
        renderMessages();
        chatInput.value = '';
        
        // Scroll to bottom
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function renderMessages() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '';
    
    messages.forEach(message => {
        const messageElement = createMessageElement(message);
        chatMessages.appendChild(messageElement);
    });
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function createMessageElement(message) {
    const messageDiv = document.createElement('div');
    const isSent = message.sender === username;
    messageDiv.className = `chat-message ${isSent ? 'sent' : 'received'}`;
    
    const time = new Date(message.timestamp).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
    
    messageDiv.innerHTML = `
        ${!isSent ? `<div class="message-info">${message.sender} • ${time}</div>` : ''}
        <div class="message-text">${escapeHtml(message.text)}</div>
        ${isSent ? `<div class="message-info">${time}</div>` : ''}
    `;
    
    return messageDiv;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function saveMessages() {
    localStorage.setItem('chatMessages', JSON.stringify(messages));
}

function simulateIncomingMessages() {
    const botMessages = [
        "Welcome to the team chat! 👋",
        "How's everyone doing today?",
        "Don't forget about the meeting at 3 PM!",
        "Great work on the project everyone!",
        "Anyone up for coffee? ☕",
        "The new features look amazing!",
        "Let's sync up later this afternoon",
        "Has anyone seen the latest designs?"
    ];
    
    // Simulate a message every 10-30 seconds
    setInterval(() => {
        if (Math.random() > 0.7) { // 30% chance
            const botNames = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'];
            const randomBot = botNames[Math.floor(Math.random() * botNames.length)];
            const randomMessage = botMessages[Math.floor(Math.random() * botMessages.length)];
            
            const message = {
                id: Date.now(),
                text: randomMessage,
                sender: randomBot,
                timestamp: new Date().toISOString(),
                type: 'received'
            };
            
            messages.push(message);
            saveMessages();
            renderMessages();
        }
    }, 15000);
}

function checkForNewMessages() {
    // In a real app, this would check a server
    // For now, we just re-render to show any changes
    const storedMessages = JSON.parse(localStorage.getItem('chatMessages')) || [];
    if (storedMessages.length !== messages.length) {
        messages = storedMessages;
        renderMessages();
    }
}