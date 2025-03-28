from flask import Flask
from flask_socketio import SocketIO
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
socketio = SocketIO(app)

# Configurar o diretório de downloads
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "Video_Downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Importar as rotas
from src.backend.routes import download_routes