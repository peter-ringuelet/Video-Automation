import tkinter as tk
from pytube import YouTube
import subprocess
from tkinter import ttk
from tkinter import filedialog


class YouTubeDownloaderCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader and Cutter")

        self.url_label = tk.Label(root, text="YouTube URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(root)
        self.url_entry.pack()
        self.url_entry.bind("<FocusOut>", self.update_options_and_metadata)

        self.start_label = tk.Label(root, text="Start Time (HH:MM:SS):")
        self.start_label.pack()

        self.start_entry = tk.Entry(root)
        self.start_entry.pack()

        self.end_label = tk.Label(root, text="End Time (HH:MM:SS):")
        self.end_label.pack()

        self.end_entry = tk.Entry(root)
        self.end_entry.pack()

        self.format_label = tk.Label(root, text="Select Format:")
        self.format_label.pack()

        self.format_var = tk.StringVar()
        self.format_menu = tk.OptionMenu(root, self.format_var, "")
        self.format_menu.pack()

        self.resolution_label = tk.Label(root, text="Select Resolution:")
        self.resolution_label.pack()

        self.resolution_var = tk.StringVar()
        self.resolution_menu = tk.OptionMenu(root, self.resolution_var, "")
        self.resolution_menu.pack()

        self.save_location_button = tk.Button(
            root, text="Select Save Location", command=self.select_save_location)
        self.save_location_button.pack()

        self.metadata_label = tk.Label(root, text="Video Metadata:")
        self.metadata_label.pack()

        self.metadata_text = tk.Text(root, height=10, width=40)
        self.metadata_text.pack()

        self.preview_button = tk.Button(
            root, text="Preview", command=self.preview_video)
        self.preview_button.pack()

        self.cut_button = tk.Button(
            root, text="Cut and Download", command=self.cut_and_download)
        self.cut_button.pack()

        self.progress = ttk.Progressbar(
            root, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack()
        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack()

        self.save_location = ""

    def select_save_location(self):
        self.save_location = filedialog.askdirectory()
        if self.save_location:
            self.progress_label.config(
                text=f"Save location selected: {self.save_location}")

    def update_options_and_metadata(self, event):
        youtube_link = self.url_entry.get()

        try:
            yt = YouTube(youtube_link)
            formats = [stream.mime_type.split(
                "/")[-1] for stream in yt.streams.filter(file_extension="mp4")]
            resolutions = [stream.resolution for stream in yt.streams.filter(
                file_extension="mp4", mime_type="video/mp4")]

            self.update_format_menu(formats)
            self.update_resolution_menu(resolutions)
            metadata = self.load_video_metadata(youtube_link)
            self.update_metadata_text(metadata)
        except:
            pass

    def load_video_metadata(self, youtube_link):
        yt = YouTube(youtube_link)
        metadata = f"Title: {yt.title}\nAuthor: {yt.author}\nLength: {yt.length} seconds"
        return metadata

    def update_format_menu(self, formats):
        self.format_menu['menu'].delete(0, 'end')
        for fmt in formats:
            self.format_menu['menu'].add_command(
                label=fmt, command=tk._setit(self.format_var, fmt))

    def update_resolution_menu(self, resolutions):
        self.resolution_menu['menu'].delete(0, 'end')
        for res in resolutions:
            self.resolution_menu['menu'].add_command(
                label=res, command=tk._setit(self.resolution_var, res))

    def update_metadata_text(self, metadata):
        self.metadata_text.delete("1.0", tk.END)
        self.metadata_text.insert(tk.END, metadata)

    def preview_video(self):
        youtube_link = self.url_entry.get()
        youtube_link = self.url_entry.get()
        video_format = self.format_var.get()
        resolution = self.resolution_var.get()

        try:
            yt = YouTube(youtube_link)
            video_stream = yt.streams.filter(
                file_extension=video_format, resolution=resolution).first()
            subprocess.run(['ffplay', video_stream.url])
        except Exception as e:
            print(f"An error occurred: {e}")

    def cut_and_download(self):
        if not self.save_location:
            self.progress_label.config(text="Select a save location first.")
            return

        youtube_link = self.url_entry.get()
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()
        video_format = self.format_var.get()
        resolution = self.resolution_var.get()

        try:
            yt = YouTube(youtube_link)
            video = yt.streams.filter(
                file_extension=video_format, resolution=resolution).first()
            self.progress['maximum'] = 100
            self.progress_label.config(text="Downloading...")
            video.download(output_path=self.save_location,
                           filename='original_video.mp4')

            self.progress_label.config(text="Cutting and downloading...")
            subprocess.run(['ffmpeg', '-i', f'{self.save_location}/original_video.{video_format}',
                            '-ss', start_time, '-to', end_time, f'{self.save_location}/cut_video.{video_format}'])
            self.progress_label.config(
                text="Video downloaded and cut successfully!")
        except Exception as e:
            self.progress_label.config(text=f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderCutterApp(root)
    root.mainloop()