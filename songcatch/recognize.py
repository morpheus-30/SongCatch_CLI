import requests
import base64
import os
import io
from pydub import AudioSegment
from dotenv import load_dotenv
import sys

load_dotenv()

def recognize_song(filename="test_capture.wav"):
    print("🧠 Forcing audio into strict s16le format for Shazam...")
    
    try:
        # 1. Load the original capture
        audio = AudioSegment.from_file(filename)
        
        # 2. Force Shazam's exact requirements: Mono, 44100Hz, 16-bit
        audio = audio.set_channels(1).set_frame_rate(44100).set_sample_width(2)
        
        # 3. Take a 4-second slice (keeps it well under the 500KB limit)
        snippet = audio[:4000] 
        
        # 4. 🚨 CRITICAL STEP: Export strictly as signed 16-bit PCM little endian
        raw_buffer = io.BytesIO()
        snippet.export(raw_buffer, format="s16le")
        raw_data = raw_buffer.getvalue()
        
        # 5. Encode strictly to Base64 text
        base64_audio = base64.b64encode(raw_data).decode('utf-8')
        
    except Exception as e:
        print(f"❌ Audio Prep Error: {e}")
        return None

    # --- API Request Setup ---
    api_key = os.getenv("SHAZAM_API_KEY")
    if not api_key:
        print("⚠️ Error: SHAZAM_API_KEY not found. Run: export SHAZAM_API_KEY='your_key'")
        return None

    url = "https://shazam.p.rapidapi.com/songs/v3/detect"
    
    headers = {
        "content-type": "text/plain",
        "x-rapidapi-host": "shazam.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    try:
        print("📡 Firing payload to Shazam...")
        response = requests.post(url, data=base64_audio, headers=headers)
        
        if response.status_code == 204 or not response.text:
            print("❌ Shazam returned 204 No Content. Audio might be silent or format is rejected.")
            return None
            
        result = response.json()

        # 1. Check if the 'results' dict contains 'matches'
        matches = result.get('results', {}).get('matches')

        if matches:
            # 2. Grab the ID of the first match
            match_id = matches[0].get('id')
            
            # 3. Use that ID to look up the song details in 'resources' -> 'shazam-songs'
            song_data = result.get('resources', {}).get('shazam-songs', {}).get(match_id, {}).get('attributes', {})
            
            title = song_data.get('title')
            artist = song_data.get('artist')
            
            return {"title": title, "artist": artist, "track_id": None} # Shazam v3 rarely gives Spot IDs, so we default to None
        else:
            print("🤷 No match found. The format was accepted, but the song wasn't recognized.")
            return None

    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

# --- STANDALONE TEST BLOCK ---
if __name__ == "__main__":
    if not os.path.exists("test_capture.wav"):
        print("❌ 'test_capture.wav' not found. Make sure you recorded audio first!")
        sys.exit(1)
        
    print("🔍 Analyzing your audio capture...")
    song_info = recognize_song("test_capture.wav")
    
    if song_info:
        print("\n✅ MATCH FOUND!")
        print(f"🎵 Title:   {song_info['title']}")
        print(f"🎤 Artist:  {song_info['artist']}")
        if song_info['track_id']:
            print(f"🔗 Spot ID: {song_info['track_id']}")
        else:
            print("🔗 Spot ID: Not provided by Shazam (we might need to search Spotify for it later).")