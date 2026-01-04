import os
import yt_dlp

def download_video(url, output_path, format='mp4'):
    """
    Downloads a video from the given URL to the output path.
    """
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': f'bestvideo[ext={format}]+bestaudio[ext=m4a]/best[ext={format}]/best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Download completed successfully."
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")
