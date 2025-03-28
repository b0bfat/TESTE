from app import app
from flask import render_template, request, jsonify
from flask_socketio import SocketIO, emit
import yt_dlp
from pathlib import Path
import os
import time
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Diretório de downloads do usuário no Windows
DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Downloads', 'Video_Downloads')
socketio = SocketIO(app, async_mode='threading')

# Variável para rastrear o início do download
download_start_time = None

def progress_hook(d):
    """Callback para enviar progresso via WebSocket"""
    global download_start_time
    
    logger.info(f"Progress hook chamado: {d['status']}")
    if d['status'] == 'downloading':
        if download_start_time is None:
            download_start_time = time.time()
        
        percent = d.get('_percent_str', '0%').replace('%', '')
        try:
            percent = float(percent) * 0.5  # Download é 50% do progresso total
            socketio.emit('progress', {'percent': percent, 'message': 'Baixando vídeo e áudio...'})
            logger.info(f"Progresso de download: {percent}%")
            
            # Mensagem interativa baseada no tempo
            elapsed_time = time.time() - download_start_time
            if elapsed_time > 30 and percent < 40:
                socketio.emit('progress', {
                    'percent': percent,
                    'message': 'Está demorando mais que o normal, mas aguarde que já já vai ficar pronto!'
                })
        except ValueError as e:
            logger.error(f"Erro ao processar porcentagem: {e}")
            socketio.emit('progress', {'error': f"Erro ao processar progresso: {str(e)}"})
    
    elif d['status'] == 'finished':
        socketio.emit('progress', {'percent': 50, 'message': 'Download concluído!'})
        logger.info("Download concluído")

@app.route('/')
def index():
    logger.info("Carregando página inicial")
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    global download_start_time
    logger.info("Requisição /download recebida")
    
    url = request.json.get('url')
    if not url:
        logger.error("URL não fornecida")
        socketio.emit('progress', {'error': 'URL não fornecida'})
        return jsonify({'status': 'error', 'message': 'URL não fornecida'}), 400

    try:
        logger.info(f"Iniciando download para URL: {url}")
        Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)
        download_start_time = None
        
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'format': 'best[ext=mp4]',  # Simplificado: baixa um único fluxo com vídeo e áudio
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
            },
            'progress_hooks': [progress_hook],
            'verbose': True,
            'geo_bypass': True,
        }

        logger.info("Configurando yt_dlp...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            socketio.emit('progress', {'percent': 0, 'message': 'Iniciando download...'})
            logger.info("Extraindo informações do vídeo")
            info = ydl.extract_info(url, download=True)
            logger.info("Informações extraídas, preparando nome do arquivo")
            filename = ydl.prepare_filename(info)
            
            socketio.emit('progress', {'percent': 100, 'message': 'Arquivo pronto para reprodução!'})
            logger.info(f"Download concluído: {filename}")
        
        return jsonify({
            'status': 'success',
            'filename': os.path.basename(filename),
            'title': info.get('title', 'Video'),
            'path': filename
        })

    except yt_dlp.utils.DownloadError as de:
        logger.error(f"Erro do yt_dlp: {str(de)}")
        socketio.emit('progress', {'error': f"Erro ao baixar o vídeo (yt_dlp): {str(de)}"})
        return jsonify({'status': 'error', 'message': str(de)}), 500
    except Exception as e:
        logger.error(f"Erro inesperado durante o download: {str(e)}")
        socketio.emit('progress', {'error': f"Erro inesperado ao baixar o vídeo: {str(e)}"})
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/open_folder', methods=['POST'])
def open_folder():
    folder = DOWNLOAD_DIR
    try:
        os.startfile(folder)
        logger.info("Pasta de downloads aberta")
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Erro ao abrir pasta: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    logger.info("Iniciando o servidor...")
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)