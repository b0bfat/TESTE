# Video Downloader.

Aplicação web para baixar vídeos da internet usando yt_dlp.

## Habilitar hambiente virtual.
1. python -m venv video (video é o nomer de hambiente, nomeie como quiser.)
2. \video\Scripts\activate

## Instalação.
1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Instale o FFmpeg no sistema
4. Execute: `python main.py`

## Uso.
- Acesse http://localhost:5000
- Insira a URL do vídeo
- Clique em "Baixar"

## Estrutura Projeto.
video_downloader/
├── app/
│   ├── static/              # Arquivos estáticos como CSS, JS, imagens
│   │   ├── css/
│   │   │   └── style.css    # Estilos personalizados
│   │   └── js/
│   │       └── script.js    # Scripts JavaScript
│   ├── templates/           # Templates HTML
│   │   └── index.html       # Página principal
│   └── __init__.py          # Arquivo de inicialização do app Flask
├── downloads/               # Diretório para vídeos baixados
├── main.py                  # Arquivo principal da aplicação
├── requirements.txt         # Lista de dependências
└── README.md                # Documentação do projeto

## FFmpeg.

1. Instalar o FFmpeg no Windows
Baixe o FFmpeg:
Acesse o site oficial: https://ffmpeg.org/download.html
Ou use uma build confiável como a do Gyan: https://www.gyan.dev/ffmpeg/builds/
Recomendo baixar o arquivo ffmpeg-git-full.zip (versão completa).

2. Extraia o Arquivo:
Descompacte o arquivo ZIP em uma pasta, por exemplo: C:\ffmpeg.

3. Adicione ao PATH:
Abra o Painel de Controle > Sistema > Configurações avançadas do sistema > Variáveis de Ambiente.
Na seção "Variáveis de sistema", encontre a variável Path, clique em "Editar" e adicione o caminho C:\ffmpeg\bin.
Clique em "OK" para salvar.

## Ajuste FFmpeg direto do diretorio.
Se você não quer ou não pode adicionar o FFmpeg ao PATH (Como variavel de sistema). 
podemos especificar o caminho diretamente no código. Substitua 'ffmpeg_location': 'ffmpeg' pelo caminho completo do executável ffmpeg.exe. Por exemplo, se você extraiu em C:\ffmpeg, use 'ffmpeg_location': 'C:\\ffmpeg\\bin\\ffmpeg.exe' na linha 47 do arquivo main.py.