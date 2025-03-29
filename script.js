document.addEventListener('DOMContentLoaded', () => {
    const BOT_AVATAR_URL = '/static/bot-avatar.png';
    const chatContainer = document.querySelector('.chat-container');
    const messageInput = document.querySelector('#message-input');
    const sendButton = document.querySelector('#send-button');

    let isTyping = false;

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        if (!isUser) {
            const avatar = document.createElement('img');
            avatar.src = BOT_AVATAR_URL;
            avatar.alt = 'Bot Avatar';
            avatar.className = 'bot-avatar';
            messageDiv.appendChild(avatar);
        }

        const textDiv = document.createElement('div');
        textDiv.className = 'message-content';
        textDiv.textContent = content;
        messageDiv.appendChild(textDiv);

        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function showTypingIndicator() {
        if (isTyping) return;
        isTyping = true;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing';
        typingDiv.id = 'typing-indicator';

        const avatar = document.createElement('img');
        avatar.src = BOT_AVATAR_URL;
        avatar.alt = 'Bot Avatar';
        avatar.className = 'bot-avatar';
        typingDiv.appendChild(avatar);

        const dots = document.createElement('div');
        dots.className = 'typing-dots';
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            dot.className = 'dot';
            dots.appendChild(dot);
        }
        typingDiv.appendChild(dots);

        chatContainer.appendChild(typingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        isTyping = false;
    }

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Clear input and add user message
        messageInput.value = '';
        addMessage(message, true);
        showTypingIndicator();

        try {
            const response = await fetch('/chat', methods=['POST'], {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })  // Changed from query to message to match backend
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            hideTypingIndicator();
            addMessage(data.response, false);
        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again.', false);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Initialize with a welcome message
    addMessage('Hello! I\'m your Police Procedure Assistant. How can I help you today?', false);
}); 