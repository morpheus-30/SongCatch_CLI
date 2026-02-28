import spotipy
from spotipy.oauth2 import SpotifyPKCE

# 🚨 SAFE TO HARDCODE: These are public-facing in the PKCE flow.
# Paste your actual Client ID here before uploading to GitHub!
SPOTIFY_CLIENT_ID = "a476951a69c841aca39f24eb09ed7bce"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8080"

def get_spotify_client():
    """Authenticates with Spotify using PKCE (No Secret Required)."""
    scope = "user-library-read user-library-modify"
    
    try:
        # SpotifyPKCE securely generates dynamic codes under the hood
        # completely eliminating the need for a static Client Secret.
        auth_manager = SpotifyPKCE(
            client_id=SPOTIFY_CLIENT_ID,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope,
            cache_path=".spotify_cache" 
        )
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        print(f"❌ Failed to authenticate with Spotify: {e}")
        return None

def search_track(sp, title, artist):
    """Searches Spotify for a specific track and returns its URI."""
    print(f"🔍 Searching Spotify for: '{title}' by '{artist}'...")
    query = f"track:{title} artist:{artist}"
    
    try:
        result = sp.search(q=query, type="track", limit=1)
        tracks = result.get('tracks', {}).get('items', [])
        
        if tracks:
            track_uri = tracks[0]['uri'] 
            track_name = tracks[0]['name']
            print(f"✅ Found on Spotify: {track_name}")
            return track_uri
        else:
            print(f"🤷 Could not find '{title}' on Spotify.")
            return None
    except Exception as e:
        print(f"❌ Error searching Spotify: {e}")
        return None

def add_to_liked_songs(sp, track_uri):
    """Adds a Spotify track directly to your Liked Songs using the API bypass."""
    print(f"💚 Saving track to your Liked Songs...")
    try:
        # Bypassing spotipy's broken method and hitting the API directly
        sp._put(f"me/library?uris={track_uri}") 
        print("🎉 SUCCESS! Track added to your Liked Songs.")
        return True
    except Exception as e:
        print(f"❌ Failed to save to Liked Songs: {e}")
        return False