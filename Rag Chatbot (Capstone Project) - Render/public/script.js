const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const langSelect = document.getElementById('language-select');
const audioToggle = document.getElementById('audio-toggle');

let isRecording = false;
let audioEnabled = true;

// Speech Recognition Setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
        sendMessage(transcript);
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        stopRecording();
    };

    recognition.onend = () => {
        stopRecording();
    };
} else {
    micBtn.style.display = 'none';
    console.warn("Speech Recognition not supported in this browser.");
}

// Event Listeners
sendBtn.addEventListener('click', () => sendMessage(chatInput.value.trim()));
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(chatInput.value.trim());
    }
});

const randomBtn = document.getElementById('random-btn');
randomBtn.addEventListener('click', () => {
    chatInput.value = '';
    sendMessage("Tell me about a random exoplanet");
});

micBtn.addEventListener('click', () => {
    if (!recognition) return;
    
    if (isRecording) {
        recognition.stop();
        stopRecording();
    } else {
        recognition.lang = langSelect.value;
        recognition.start();
        micBtn.classList.add('recording');
        isRecording = true;
    }
});

audioToggle.addEventListener('click', () => {
    audioEnabled = !audioEnabled;
    if (audioEnabled) {
        audioToggle.classList.add('active');
        audioToggle.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
    } else {
        audioToggle.classList.remove('active');
        audioToggle.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
        window.speechSynthesis.cancel();
    }
});

function stopRecording() {
    isRecording = false;
    micBtn.classList.remove('recording');
}

async function sendMessage(text) {
    if (!text) return;

    // Add user message to UI
    appendMessage('user', text);
    chatInput.value = '';
    
    // Show loading indicator
    const loadingId = addLoadingIndicator();

    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: text,
                language: langSelect.value
            })
        });

        const data = await response.json();
        
        // Remove loading
        document.getElementById(loadingId).remove();
        
        // Add bot response to UI
        appendMessage('bot', data.reply);
        
        // Text to Speech
        if (audioEnabled) {
            speakText(data.reply, langSelect.value);
        }
        
    } catch (error) {
        console.error("Error communicating with backend:", error);
        document.getElementById(loadingId).remove();
        appendMessage('bot', "Sorry, I encountered an anomaly while accessing the Exoplanet database. Please try again.");
    }
}

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    
    const icon = sender === 'bot' ? 'fa-user-astronaut' : 'fa-user';
    
    // Simple markdown parsing for bold text
    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid ${icon}"></i></div>
        <div class="content"><p>${formattedText}</p></div>
    `;
    
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addLoadingIndicator() {
    const id = 'loading-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.className = `message bot`;
    msgDiv.id = id;
    
    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-user-astronaut"></i></div>
        <div class="content">
            <div class="loading-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return id;
}

function speakText(text, lang) {
    if (!window.speechSynthesis) return;
    
    window.speechSynthesis.cancel(); // cancel any ongoing speech
    
    // Remove markdown symbols for speech
    const cleanText = text.replace(/[*_#]/g, '');
    
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = lang;
    
    // Try to find a good voice
    const voices = window.speechSynthesis.getVoices();
    const targetVoice = voices.find(v => v.lang.startsWith(lang.split('-')[0]));
    if (targetVoice) {
        utterance.voice = targetVoice;
    }
    
    window.speechSynthesis.speak(utterance);
}

// Initialize voices (Chrome requires this to be triggered sometimes)
window.speechSynthesis.onvoiceschanged = () => {
    window.speechSynthesis.getVoices();
};
