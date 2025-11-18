// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const documentsInfo = document.getElementById('documentsInfo');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const chatMessages = document.getElementById('chatMessages');

// File selection handler
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        uploadBtn.disabled = false;
        uploadStatus.className = 'status-message';
        uploadStatus.textContent = `Selected: ${file.name}`;
        uploadStatus.classList.add('info');
    }
});

// Upload button handler
uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        showStatus('Please select a file first', 'error');
        return;
    }

    // Disable button during upload
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showStatus(data.message || 'Document uploaded successfully!', 'success');
            await checkDatabaseStatus();
            await loadUploadedFiles(); // Refresh file list
            // Clear file input
            fileInput.value = '';
            uploadBtn.disabled = true;
        } else {
            showStatus(data.detail || 'Error uploading file', 'error');
            uploadBtn.disabled = false;
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        uploadBtn.disabled = false;
    } finally {
        uploadBtn.textContent = 'Upload Document';
    }
});

// Ask question handler
askBtn.addEventListener('click', handleQuestion);
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleQuestion();
    }
});

async function handleQuestion() {
    const question = questionInput.value.trim();
    if (!question) {
        return;
    }

    // Clear input
    questionInput.value = '';

    // Remove welcome message if present
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    // Display user question first
    addMessage(question, 'question');
    
    // Scroll to show the question
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Show loading indicator
    const loadingId = addLoadingMessage();

    try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        // Remove loading indicator
        removeLoadingMessage(loadingId);

        if (response.ok) {
            // Display answer - answer should be at the top
            if (data.answer) {
                addMessage(data.answer, 'answer', data.sources);
            } else {
                addMessage('Received empty answer from server', 'error');
            }
        } else {
            // Show clean error message
            const errorMsg = data.detail || data.message || 'Failed to get answer';
            addMessage(`Error: ${errorMsg}`, 'error');
        }
    } catch (error) {
        removeLoadingMessage(loadingId);
        // Clean error message - remove HTML and extra characters
        let errorMsg = error.message || 'Unknown error occurred';
        errorMsg = errorMsg.replace(/<[^>]*>/g, ''); // Remove HTML tags
        errorMsg = errorMsg.replace(/\s+/g, ' ').trim(); // Clean whitespace
        addMessage(`Error: ${errorMsg}`, 'error');
    }
}

// Helper functions
function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `status-message ${type}`;
    setTimeout(() => {
        uploadStatus.className = 'status-message';
    }, 5000);
}

async function checkDatabaseStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        const data = await response.json();
        
        if (data.documents_in_db > 0) {
            documentsInfo.textContent = `✓ ${data.documents_in_db} document chunk(s) in database. You can now ask questions!`;
            documentsInfo.classList.add('show');
        } else {
            documentsInfo.classList.remove('show');
        }
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

function addMessage(content, type, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    if (type === 'question') {
        messageDiv.innerHTML = `
            <div class="question-bubble">${escapeHtml(content)}</div>
        `;
    } else if (type === 'answer') {
        // Clean the content - remove any HTML that might have leaked in
        let cleanContent = escapeHtml(content);
        
        // Remove any HTML tags that might have been included in error messages
        cleanContent = cleanContent.replace(/<[^>]*>/g, '');
        
        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            sourcesHtml = `
                <div class="sources-section">
                    <h4>📄 Document Excerpts Used:</h4>
                    ${sources.map((source, idx) => {
                        // Clean source text too
                        let cleanSource = escapeHtml(source);
                        cleanSource = cleanSource.replace(/<[^>]*>/g, '');
                        return `
                        <div class="source-item">
                            <strong>Excerpt ${idx + 1}:</strong><br>
                            ${cleanSource.substring(0, 300)}${cleanSource.length > 300 ? '...' : ''}
                        </div>
                    `;
                    }).join('')}
                </div>
            `;
        }
        messageDiv.innerHTML = `
            <div class="answer-bubble">
                <strong>🤖 Answer:</strong><br>
                ${cleanContent}
                ${sourcesHtml}
            </div>
        `;
    } else {
        // Error message - clean up any HTML that might have leaked in
        let cleanError = escapeHtml(content);
        // Remove any HTML tags that might have been included
        cleanError = cleanError.replace(/<[^>]*>/g, '');
        // Remove excessive whitespace
        cleanError = cleanError.replace(/\s+/g, ' ').trim();
        
        messageDiv.innerHTML = `
            <div class="answer-bubble" style="background: #f8d7da; color: #721c24;">
                <strong>❌ Error:</strong><br>
                ${cleanError}
            </div>
        `;
    }

    chatMessages.appendChild(messageDiv);
    // Scroll to bottom to show the latest message
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

function addLoadingMessage() {
    const loadingId = 'loading-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.id = loadingId;
    messageDiv.innerHTML = `
        <div class="answer-bubble">
            <div class="loading"></div> Thinking...
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingId;
}

function removeLoadingMessage(id) {
    const loadingMsg = document.getElementById(id);
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Check database status on page load
checkDatabaseStatus();
loadUploadedFiles();

// Load and display uploaded files
async function loadUploadedFiles() {
    try {
        const response = await fetch(`${API_BASE_URL}/files`);
        const data = await response.json();
        
        const filesList = document.getElementById('uploadedFilesList');
        const filesSection = document.getElementById('uploadedFilesSection');
        
        if (!response.ok || !data.files || data.files.length === 0) {
            filesList.innerHTML = '<p class="no-files">No files uploaded yet.</p>';
            return;
        }
        
        filesList.innerHTML = '';
        
        data.files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <div class="file-info">
                    <span class="file-icon">📄</span>
                    <span class="file-name">${escapeHtml(file.filename)}</span>
                    <span class="file-chunks">${file.chunks} chunk(s)</span>
                </div>
                <button class="btn-delete" onclick="deleteFile('${escapeHtml(file.filename)}')" title="Delete file">
                    🗑️
                </button>
            `;
            filesList.appendChild(fileItem);
        });
        
        filesSection.style.display = 'block';
    } catch (error) {
        console.error('Error loading files:', error);
    }
}

// Delete a file
async function deleteFile(filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/files/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus(data.message || 'File deleted successfully', 'success');
            await loadUploadedFiles();
            await checkDatabaseStatus();
        } else {
            showStatus(data.detail || 'Error deleting file', 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Make deleteFile available globally
window.deleteFile = deleteFile;

