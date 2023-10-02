# Importamos las librerías necesarias
from pytube import YouTube
from moviepy.editor import VideoFileClip

# Función para descargar un video desde YouTube
def download_video(url):
    # Creamos un objeto YouTube con la URL proporcionada
    yt = YouTube(url)
    # Obtenemos el stream de la más alta resolución del video
    stream = yt.streams.get_highest_resolution()
    # Descargamos el video y guardamos el nombre del archivo descargado
    filename = stream.download()
    return filename

# Función para dividir el video en clips de 1 minuto
def split_video(filename):
    # Abrimos el archivo de video
    with VideoFileClip(filename) as video:
        # Obtenemos la duración total del video en segundos
        duration = int(video.duration)
        
        # Dividimos el video en clips de 1 minuto (60 segundos)
        for i in range(0, duration, 60):
            # Determinamos el punto de inicio del clip
            start = i
            # Determinamos el punto final del clip
            end = i + 60 if i + 60 < duration else duration
            # Creamos un nuevo clip con el rango definido
            new_clip = video.subclip(start, end)
            # Generamos un nombre para el nuevo archivo basado en los tiempos de inicio y fin
            new_filename = f"clip_{start}_{end}.mp4"
            # Guardamos el nuevo clip en un archivo
            new_clip.write_videofile(new_filename)

# Punto de entrada del script
if __name__ == "__main__":
    # Solicitamos al usuario ingresar la URL del video de YouTube
    url = input("Ingresa el link del video de YouTube: ")
    # Descargamos el video
    video_filename = download_video(url)
    # Dividimos el video en clips
    split_video(video_filename)
