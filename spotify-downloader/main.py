import spotipy
import os
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

# --- LOAD .env CONFIGURATION ---
# Ensure you have a .env file in the same folder as this script, containing:
# SPOTIPY_CLIENT_ID=your_client_id
# SPOTIPY_CLIENT_SECRET=your_client_secret

load_dotenv()  # Load environment variables from .env

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")


def ensure_spotify_credentials():
    """Ensure Spotify API credentials are available."""
    if SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET:
        return True

    print("\n❌ Missing Spotify credentials!")
    print("Please fix this by either:")
    print("  1️⃣ Creating a `.env` file with:")
    print("      SPOTIPY_CLIENT_ID=your_client_id")
    print("      SPOTIPY_CLIENT_SECRET=your_client_secret")
    print("  2️⃣ Or setting them directly in PowerShell:")
    print("      $env:SPOTIPY_CLIENT_ID='your_client_id'")
    print("      $env:SPOTIPY_CLIENT_SECRET='your_client_secret'")
    print("Visit https://developer.spotify.com/dashboard to get them.")
    return False


# --- STEP 1: Get User Inputs ---
def get_user_inputs():
    """Prompts the user for the playlist URL, save location, and desired quality."""
    playlist_url = input("Enter the Spotify Playlist URL: ").strip()

    # Ask for Save Location
    save_dir = input("Enter the path to save the songs (e.g., C:\\Music\\): ").strip()
    os.makedirs(save_dir, exist_ok=True)

    # Ask for Quality/Format
    print("\nSelect Download Format:")
    print("1. MP3 (Standard Quality)")
    print("2. MP3 (High Quality, larger size)")
    print("3. Original Audio (M4A/WebM - No conversion)")

    quality_choice = input("Enter choice (1/2/3): ").strip()

    if quality_choice == '1':
        postprocessor_args = ['-q:a', '4']  # Standard MP3 quality
    elif quality_choice == '2':
        postprocessor_args = ['-q:a', '0']  # High MP3 quality (~320kbps)
    else:
        postprocessor_args = None  # Keep original format

    return playlist_url, save_dir, postprocessor_args


# --- STEP 2: Extract Song Information from Spotify ---
def get_spotify_tracks(playlist_url):
    """Uses Spotipy to extract track titles and artists."""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET
        ))

        # Extract playlist ID from URL
        if "playlist/" in playlist_url:
            playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
        else:
            print("Invalid Spotify playlist URL format.")
            return []

        print(f"\n🎵 Fetching tracks from playlist ID: {playlist_id}...")

        results = sp.playlist_items(playlist_id)
        tracks = []
        for item in results['items']:
            track = item['track']
            if track:
                artist_names = ", ".join([artist['name'] for artist in track['artists']])
                track_name = f"{track['name']} {artist_names}"
                tracks.append(track_name)

        print(f"✅ Found {len(tracks)} tracks in playlist.")
        return tracks

    except Exception as e:
        print(f"\n⚠️ Error accessing Spotify API: {e}")
        print("Please ensure your .env file is correct and accessible.")
        return []


# --- STEP 3: Search YouTube and Download Audio ---
def download_track(search_query, save_dir, postprocessor_args):
    """Searches YouTube and downloads the best audio using yt-dlp."""
    print(f"\n🔍 Searching YouTube for: {search_query}")

    try:
        video_url = f"ytsearch1:{search_query}"

        # yt-dlp configuration
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
            'noprogress': True,
            'quiet': True,
            'logtostderr': False,
        }

        # Add MP3 conversion if requested
        if postprocessor_args:
            ydl_opts.update({
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': postprocessor_args[1],  # '0' or '4'
                }],
                'outtmpl': os.path.join(save_dir, '%(title)s.mp3'),
            })

        # Execute download
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            print("  ✅ Downloaded successfully.")

    except Exception as e:
        print(f"  ❌ Error downloading: {e}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if not ensure_spotify_credentials():
        sys.exit(1)

    url, directory, postprocessor_args = get_user_inputs()

    if not url or not directory:
        print("❌ Required input missing. Exiting.")
        sys.exit(1)

    songs = get_spotify_tracks(url)

    if songs:
        print(f"\n--- 🎧 Starting Download of {len(songs)} Tracks ---")
        for song in songs:
            download_track(song, directory, postprocessor_args)
        print("\n--- ✅ All Downloads Finished ---")
    else:
        print("\n⚠️ No songs found. Exiting.")
