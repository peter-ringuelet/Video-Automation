from pytube import YouTube
from moviepy.editor import VideoFileClip

def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    filename = stream.download()
    return filename

def split_video(filename):
    with VideoFileClip(filename) as video:
        duration = int(video.duration)
        
        for i in range(0, duration, 60):
            start = i
            end = i + 60 if i + 60 < duration else duration
            new_clip = video.subclip(start, end)
            new_filename = f"clip_{start}_{end}.mp4"
            new_clip.write_videofile(new_filename)

if __name__ == "__main__":
    url = input("Ingresa el link del video de YouTube: ")
    video_filename = download_video(url)
    split_video(video_filename)
