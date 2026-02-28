import os
import sys
from pathlib import Path
from dotenv import load_dotenv, set_key

# Define the config path
CONFIG_PATH = Path.home() / ".songcatch_env"

def check_and_request_keys():
    """Checks for API keys and prompts the user if they are missing."""
    # Ensure the file exists
    if not CONFIG_PATH.exists():
        CONFIG_PATH.touch()

    # Load existing keys
    load_dotenv(CONFIG_PATH)

    # Check for Shazam Key
    shazam_key = os.getenv("SHAZAM_API_KEY")
    if not shazam_key:
        print("\n👋 Welcome to SongCatch!")
        print("⚠️  It looks like this is your first time running the app.")
        print("👉 You need a free Shazam API key from RapidAPI to identify songs.")
        print("🔗 Get it here: https://rapidapi.com/apidojo/api/shazam/")
        
        # Prompt the user
        shazam_key = input("\n🔑 Paste your Shazam API Key here: ").strip()
        
        if shazam_key:
            # Save it permanently to the hidden file
            set_key(str(CONFIG_PATH), "SHAZAM_API_KEY", shazam_key)
            # Load it into the current session so the script doesn't crash
            os.environ["SHAZAM_API_KEY"] = shazam_key
            print("✅ Key saved securely! You won't be asked for this again.\n")
        else:
            print("❌ No key provided. SongCatch cannot run without it.")
            sys.exit(1)


# 🚨 Remember the dots for relative imports!
from .audio import record_audio 
from .recognize import recognize_song
from .spotify import get_spotify_client, search_track, add_to_liked_songs

def run_songcatch():
    # 1. Check for keys before doing anything else
    check_and_request_keys()
    
    print("🚀 Firing up SongCatch...")
    audio_file = "/tmp/songcatch_capture.wav" # Saving to /tmp so we don't clutter folders
    
    # --- STEP 1: CAPTURE AUDIO ---
    print("\n[1/3] 🎙️  Listening to system audio...")
    
    # 🚨 Catch the filename returned by the smart audio function
    audio_file = record_audio(filename="/tmp/songcatch_capture.wav", duration=5) 
    
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