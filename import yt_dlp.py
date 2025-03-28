import yt_dlp

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # URL de teste
ydl_opts = {
    'outtmpl': 'test_video.%(ext)s',
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'merge_output_format': 'mp4',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }],
    'ffmpeg_location': 'C:\\tmp\\Python\\ffmpeg\\bin\\ffmpeg.exe',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
    },
    'verbose': True,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download concluído!")
except Exception as e:
    print(f"Erro: {str(e)}")