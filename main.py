from app import app
from flask import render_template, request, jsonify
from flask_socketio import SocketIO, emit
import yt_dlp
from pathlib import Path
import os
import time

# Diretório de downloads do usuário no Windows
DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Downloads', 'Video_Downloads')
socketio = SocketIO(app)

# Variável para rastrear o início do download
download_start_time = None

def progress_hook(d):
    """Callback para enviar progresso via WebSocket"""
    global download_start_time
    
    if d['status'] == 'downloading':
        if download_start_time is None:
            download_start_time = time.time()
        
        percent = d.get('_percent_str', '0%').replace('%', '')
        try:
            percent = float(percent) * 0.5  # Download é 50% do progresso total
            socketio.emit('progress', {'percent': percent, 'message': 'Baixando vídeo e áudio...'})
            
            # Mensagem interativa baseada no tempo
            elapsed_time = time.time() - download_start_time
            if elapsed_time > 30 and percent < 40:
                socketio.emit('progress', {
                    'percent': percent,
                    'message': 'Está demorando mais que o normal, mas aguarde que já já vai ficar pronto!'
                })
        except ValueError:
            pass
    
    elif d['status'] == 'finished':
        socketio.emit('progress', {'percent': 50, 'message': 'Download concluído, mesclando vídeo e áudio...'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    global download_start_time
    url = request.json.get('url')
    if not url:
        return jsonify({'status': 'error', 'message': 'URL não fornecida'}), 400

    try:
        Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)
        download_start_time = None  # Reseta o tempo
        
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'ffmpeg_location': 'C:\\tmp\\Python\\ffmpeg\\bin\\ffmpeg.exe',  # Caminho atualizado
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
            },
            'progress_hooks': [progress_hook],
            'verbose': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            socketio.emit('progress', {'percent': 0, 'message': 'Iniciando download...'})
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Simula progresso da mesclagem
            socketio.emit('progress', {'percent': 75, 'message': 'Quase pronto, finalizando o arquivo...'})
            time.sleep(1)
            socketio.emit('progress', {'percent': 100, 'message': 'Arquivo pronto para reprodução!'})
        
        return jsonify({
            'status': 'success',
            'filename': os.path.basename(filename),
            'title': info.get('title', 'Video'),
            'path': filename
        })

    except Exception as e:
        socketio.emit('progress', {'error': str(e)})
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500    
@app.route('/open_folder', methods=['POST'])
def open_folder():
    folder = DOWNLOAD_DIR  # Usa o mesmo diretório definido globalmente
    try:
        os.startfile(folder)  # Abre a pasta no Windows Explorer
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)