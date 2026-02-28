import time
from .audio import record_audio  # Adjust this import based on your audio.py function name
from .recognize import recognize_song
from .spotify import get_spotify_client, search_track, add_to_liked_songs
import os
from pathlib import Path
from dotenv import load_dotenv

# Load keys from the home directory before importing anything else
config_path = Path.home() / ".songcatch_env"
load_dotenv(config_path)

def run_songcatch():
    print("🚀 Firing up SongCatch...")
    audio_file = "capture.wav"
    
    # --- STEP 1: CAPTURE AUDIO ---
    print("\n[1/3] 🎙️  Listening to system audio...")
    # Assuming your audio.py has a function that records and saves to 'capture.wav'
    record_audio(filename=audio_file, duration=5) 
    
    # --- STEP 2: RECOGNIZE SONG ---
    print("\n[2/3] 🧠 Identifying track via Shazam...")
    song_info = recognize_song(filename=audio_file)
    
    if not song_info:
        print("❌ Could not identify the song. Exiting.")
        return

    title = song_info['title']
    artist = song_info['artist']
    print(f"🎵 Identified: {title} by {artist}")
    
    # --- STEP 3: SAVE TO SPOTIFY ---
    print("\n[3/3] 💚 Injecting into Spotify Liked Songs...")
    sp = get_spotify_client()
    if not sp:
        print("❌ Spotify authentication failed. Exiting.")
        return
        
    track_uri = search_track(sp, title, artist)
    
    if track_uri:
        success = add_to_liked_songs(sp, track_uri)
        if success:
            print(f"\n✅ BOOM. '{title}' is now in your Liked Songs.")
        else:
            print("\n❌ Failed to save the track.")
    else:
        print(f"\n🤷 Couldn't find the exact track on Spotify to save.")

if __name__ == "__main__":
    run_songcatch()