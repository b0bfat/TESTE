from flask import Flask

app = Flask(__name__)

# Configurações adicionais podem ser adicionadas aqui
app.config['DOWNLOAD_DIR'] = './downloads'