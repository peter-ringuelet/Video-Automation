from moviepy.editor import VideoFileClip
import os

def ensure_result_directory(video_filename):
    result_path = f"Resultado/{video_filename}"
    if not os.path.exists(result_path):
        os.makedirs(result_path)

def calculate_segment_bounds(duration, video_count):
    if video_count == 1:
        start = 0
        end = 60
    else:
        start = (video_count - 1) * 58  # Adjusted to avoid overlap
        end = start + 60

    if end > duration:
        end = duration

    return start, end

def process_segment(video, start, end, video_filename, video_count):
    new_clip = video.subclip(start, end)
    new_filename = f"Resultado/{video_filename}/video{video_count}.mp4"
    new_clip.write_videofile(new_filename)

def split_video(filename, video_filename):
    if not os.path.exists("Resultado"):
        os.makedirs("Resultado")

    with VideoFileClip(filename) as video:
        duration = int(video.duration)
        video_count = 1

        ensure_result_directory(video_filename)

        for _ in range(0, duration, 60):
            start, end = calculate_segment_bounds(duration, video_count)
            process_segment(video, start, end, video_filename, video_count)
            video_count += 1

if __name__ == "__main__":
    video_path = "videos/"
    video_filename = input(f"Ingresa el nombre del video en la carpeta '{video_path}': ")
    split_video(f"videos/{video_filename}.mp4", video_filename)
