// Initialize Socket.IO connection
const socket = io();

// DOM Elements
const videoUrlInput = document.getElementById('videoUrl');
const downloadButton = document.getElementById('downloadButton');
const buttonIcon = document.getElementById('buttonIcon');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const progressPercentage = document.getElementById('progressPercentage');
const downloadStatus = document.getElementById('downloadStatus');
const successMessage = document.getElementById('successMessage');

// Loading icon SVG
const loadingIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" 
        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
        class="animate-spin">
        <path d="M12 2v4"/><path d="M12 18v4"/><path d="m4.93 4.93 2.83 2.83"/>
        <path d="m16.24 16.24 2.83 2.83"/><path d="M2 12h4"/><path d="M18 12h4"/>
        <path d="m4.93 19.07 2.83-2.83"/><path d="m16.24 7.76 2.83-2.83"/>
    </svg>`;

// Download icon SVG
const downloadIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" 
        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
    </svg>`;

// Function to handle download
async function downloadVideo() {
    const url = videoUrlInput.value.trim();
    
    if (!url) {
        alert('Por favor, insira uma URL válida');
        return;
    }

    try {
        // Update UI to loading state
        downloadButton.disabled = true;
        buttonIcon.innerHTML = loadingIcon;
        progressContainer.classList.remove('hidden');
        successMessage.classList.add('hidden');
        
        // Send download request to server
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        if (!response.ok) {
            throw new Error('Erro ao iniciar o download');
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        if (data.status === 'success') {
            // Abrir pasta de downloads
            await fetch('/open_folder', {
                method: 'POST',
            });
        }
    } catch (error) {
        alert(`Erro: ${error.message}`);
        resetUI();
    }
}

// Socket event listeners
socket.on('progress', (data) => {
    if (data.error) {
        alert(`Erro: ${data.error}`);
        resetUI();
        return;
    }

    const progress = data.percent || 0;
    progressBar.style.width = `${progress}%`;
    progressPercentage.textContent = `${Math.round(progress)}%`;
    downloadStatus.textContent = data.message || 'Baixando...';
    
    if (progress === 100) {
        downloadComplete();
    }
});

// Function to handle download completion
function downloadComplete() {
    downloadButton.disabled = false;
    buttonIcon.innerHTML = downloadIcon;
    progressContainer.classList.add('hidden');
    successMessage.classList.remove('hidden');
    videoUrlInput.value = '';
}

// Function to reset UI
function resetUI() {
    downloadButton.disabled = false;
    buttonIcon.innerHTML = downloadIcon;
    progressContainer.classList.add('hidden');
    successMessage.classList.add('hidden');
    progressBar.style.width = '0%';
    progressPercentage.textContent = '0%';
    downloadStatus.textContent = 'Baixando...';
}

// Event listener for Enter key
videoUrlInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        downloadVideo();
    }
});