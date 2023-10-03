from moviepy.editor import VideoFileClip
import os

def split_video(filename, video_filename):
    # Asegurarse de que el directorio 'Resultado' exista, sino crearlo
    if not os.path.exists(f"Resultado/{video_filename}"):
        os.makedirs(f"Resultado/{video_filename}")
    
    with VideoFileClip(filename) as video:
        duration = int(video.duration)
        
        # Contador para los nombres de los videos
        video_count = 1
        
        for i in range(0, duration, 60):
            if i == 0:  # Primer segmento
                start = 0
                end = 60
            else:
                start = i - 2 * (video_count-1)
                end = start + 60

            if end > duration:
                end = duration
            
            new_clip = video.subclip(start, end)
            
            new_filename = f"Resultado/{video_filename}/video{video_count}.mp4"
            new_clip.write_videofile(new_filename)
            video_count += 1

if __name__ == "__main__":
    if not os.path.exists("Resultado"):
        os.makedirs("Resultado")
    
    video_path = "videos/"  # carpeta donde están ubicados los videos
    video_filename = input(f"Ingresa el nombre del video en la carpeta '{video_path}': ")
    split_video(f"videos/{video_filename}.mp4", video_filename)

    # start=0  end= 60          start=55   end=1:55             start 1:55