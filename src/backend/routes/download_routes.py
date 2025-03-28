from src.backend.app import app, socketio, DOWNLOAD_FOLDER
from flask import render_template, request, jsonify
import yt_dlp
import os
import logging

@app.route('/')
def index():
    logging.info("Carregando página inicial")
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    logging.info(f"Requisição /download recebida para URL: {url}")

    if not url:
        return jsonify({'status': 'error', 'message': 'URL não fornecida'})

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: progress_hook(d, socketio)],
    }

    try:
        logging.info(f"Iniciando download para URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return jsonify({
                'status': 'success',
                'message': 'Download concluído',
                'title': info.get('title', 'Desconhecido'),
                'filename': os.path.basename(filename)
            })
    except Exception as e:
        logging.error(f"Erro ao baixar vídeo: {str(e)}")
        socketio.emit('progress', {'error': str(e)})
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/open_folder', methods=['POST'])
def open_folder():
    try:
        os.startfile(DOWNLOAD_FOLDER)  # Abre o diretório de downloads no Windows
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def progress_hook(d, socketio):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        logging.info(f"Progress hook chamado: {percent:.2f}%")
        socketio.emit('progress', {'percent': percent, 'message': f"Baixando: {percent:.2f}%"})
    elif d['status'] == 'finished':
        socketio.emit('progress', {'percent': 100, 'message': "Download concluído!"})