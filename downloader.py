import os
import sys
import yt_dlp
import instaloader

# Lokasi penyimpanan video/audio sesuai skripmu
SAVE_PATH = "/storage/emulated/0/Download/"  
os.makedirs(SAVE_PATH, exist_ok=True)

def download_video(url, audio_only=False):
    """Mengunduh video atau audio dari YouTube, TikTok, dan Facebook"""
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(SAVE_PATH, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if audio_only else []
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_instagram(url):
    """Mengunduh video dari Instagram"""
    try:
        loader = instaloader.Instaloader()
        # Mengatur folder download khusus untuk Instaloader
        loader.dirname_pattern = SAVE_PATH
        
        # Mengambil shortcode dari URL Instagram
        if "shopt/p/" in url or "/p/" in url or "/reel/" in url:
            shortcode = url.split("/")[-2]
            if not shortcode: # Antisipasi jika ada slash di ujung url
                shortcode = url.split("/")[-3]
        else:
            print("URL Instagram tidak valid.")
            return

        print(f"Mengunduh postingan Instagram dengan kode: {shortcode}...")
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=SAVE_PATH)
        print("Selesai mengunduh dari Instagram!")
    except Exception as e:
        print(f"Gagal mengunduh dari Instagram: {e}")

if __name__ == "__main__":
    # Menerima argumen dari skrip Bash
    if len(sys.argv) < 3:
        print("Argumen kurang.")
        sys.exit(1)
        
    tipe = sys.argv[1]
    link = sys.argv[2]
    
    if tipe == "yt_video":
        download_video(link, audio_only=False)
    elif tipe == "yt_audio":
        download_video(link, audio_only=True)
    elif tipe == "ig":
        download_instagram(link)
        