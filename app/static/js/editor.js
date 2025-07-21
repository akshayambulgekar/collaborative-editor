// app/static/js/editor.js
document.addEventListener('DOMContentLoaded', () => {
    const editor = document.getElementById('editor');
    const suggestionsDiv = document.getElementById('suggestions');
    const form = document.getElementById('editor-form');
    const socket = io();

    // Join document room
    socket.emit('join', { doc_id: docId });

    // Real-time editing
    editor.addEventListener('input', () => {
        socket.emit('edit', { 
            doc_id: docId, 
            content: editor.value, 
            timestamp: new Date().toISOString()
        });

        // Fetch AI suggestions
        fetch('/doc/api/suggestions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: editor.value })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Suggestions received:', data.suggestions);
            suggestionsDiv.innerHTML = data.suggestions.length > 0 
                ? data.suggestions.map(s => `<p>${s.message} ${s.replacements.length > 0 ? '(Suggestions: ' + s.replacements.join(', ') + ')' : ''}</p>`).join('')
                : '<p>No suggestions available.</p>';
        })
        .catch(error => {
            console.error('Error fetching suggestions:', error);
            suggestionsDiv.innerHTML = '<p>Failed to load suggestions. Please try again.</p>';
        });
    });

    // Receive real-time updates
    socket.on('update', (data) => {
        if (editor.value !== data.content) {
            editor.value = data.content;
        }
    });

    // Handle conflicts
    socket.on('conflict', (data) => {
        alert(data.message);
    });

    // Autosave every 5 seconds
    let lastSavedContent = editor.value;
    const saveIndicator = document.getElementById('save-indicator');
    setInterval(() => {
        if (editor.value !== lastSavedContent) {
            saveIndicator.textContent = 'Saving...';
            fetch(`/doc/editor/${docId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `content=${encodeURIComponent(editor.value)}`
            })
            .then(response => {
                if (response.ok) {
                    lastSavedContent = editor.value;
                    saveIndicator.textContent = 'Saved';
                    setTimeout(() => { saveIndicator.textContent = ''; }, 2000);
                } else {
                    saveIndicator.textContent = 'Save failed';
                    console.error('Autosave failed:', response.status);
                }
            })
            .catch(error => {
                saveIndicator.textContent = 'Save failed';
                console.error('Autosave error:', error);
            });
        }
    }, 5000);
});