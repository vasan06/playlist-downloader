Spotify-Downloader: Automated Music Archive 🎵

This project is a "Zero-Manual-Search" tool. It takes Spotify tracks, playlists, or albums and automatically locates, downloads, and converts the highest-quality audio equivalent from YouTube, complete with metadata and album art.
🚀 Quick Start Guide
Step 1: Prerequisites

    Python 3.8+ installed.

    FFmpeg: Essential for converting high-quality video streams into .mp3 format.

    Spotify Developer Credentials: A Client ID and Secret (available for free at Spotify Dashboard).

Step 2: Automated Installation

Clone the repository and install the processing engine:
Bash

pip install -r requirements.txt

Step 3: Run the Engine

Launch the downloader script:
Bash

python main.py

⚡ What Happens Automatically

    Credential Validation: On startup, the script authenticates with the Spotify Web API to gain access to private and public playlist data.

    Metadata Extraction: The engine scans your Spotify link to extract track names, artists, album names, and high-resolution cover art.

    Smart Search & Matching: The system automatically queries YouTube for the most accurate audio match, filtering out low-quality "covers" or "live" versions.

    Post-Processing: Using FFmpeg, the script strips the video, converts the audio to 320kbps MP3, and embeds the original Spotify ID3 tags (artist, album, year).

💎 Unique Features
🎧 Intelligent Metadata Injection

Unlike basic recorders, this tool injects official metadata into the downloaded file. When you play the file on any device, it displays the official album art, genre, and track number as if purchased from a digital store.
📁 Dynamic Folder Organization

The downloader doesn't just dump files; it automatically creates a hierarchical folder structure:

    Downloads/Playlist_Name/Artist_Name - Track_Name.mp3 This keeps your local music library perfectly organized without manual sorting.

⚡ Batch Processing Engine

    Single Track: Instant download of one song.

    Full Album/Playlist: Paste one link, and the script will sequentially process hundreds of songs without intervention.

    Download Resume: If the connection breaks, the system skips already-downloaded tracks to save time and bandwidth.

📂 Technical Project Structure
Component	Responsibility
main.py	The Controller: Manages the user input and the overall download queue.
spotify_client.py	The Mapper: Interacts with Spotify API to fetch track details.
downloader.py	The Engine: Uses yt-dlp to fetch and convert audio streams.
ffmpeg	The Converter: Handles high-fidelity audio encoding and tag embedding.
