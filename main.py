from yt_dlp import YoutubeDL
import os
from urllib.parse import urlparse


def get_site_name(url):
    domain = urlparse(url).netloc
    if 'youtube' in domain or 'youtu.be' in domain:
        return 'YouTube'
    elif 'tiktok' in domain:
        return 'TikTok'
    return 'Unknown'


def download_video(url, save_path='downloads'):
    # Create downloads folder if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Basic options for video download
    options = {
        'format': 'best',
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True
    }

    # Add specific options based on the platform
    site = get_site_name(url)
    if site == 'YouTube':
        options.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        })

    try:
        with YoutubeDL(options) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            video_title = info['title']

            print(f"\nDownloading: {video_title}")
            print(f"From: {site}")

            # Download the video
            ydl.download([url])

            # Get the output path
            ext = 'mp4' if site == 'YouTube' else info['ext']
            final_path = os.path.join(save_path, f"{video_title}.{ext}")
            print(f"\nSaved to: {os.path.abspath(final_path)}")

    except Exception as e:
        print(f"\nError: Could not download video - {str(e)}")


def main():
    print("\n=== Video Downloader ===")
    while True:
        url = input("\nEnter video URL (or 'q' to quit): ").strip()

        if url.lower() == 'q':
            break

        save_path = input("Enter save path (press Enter for 'downloads'): ").strip()
        if not save_path:
            save_path = 'downloads'

        download_video(url, save_path)


if __name__ == "__main__":
    main()
    
