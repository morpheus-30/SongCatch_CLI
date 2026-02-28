import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    """Authenticates with Spotify and returns the client object."""
    scope = "user-library-read user-library-modify"
    
    try:
        auth_manager = SpotifyOAuth(
            scope=scope, 
            cache_path=".final_cache", 
            show_dialog=True
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
            track_uri = tracks[0]['uri']  # 🚨 Grabbing the URI specifically for our bypass
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
        # 🚨 THE FIX: Bypassing spotipy's broken method and hitting the API directly
        sp._put(f"me/library?uris={track_uri}") 
        print("🎉 SUCCESS! Track added to your Liked Songs.")
        return True
    except Exception as e:
        print(f"❌ Failed to save to Liked Songs: {e}")
        return False

# --- STANDALONE TEST BLOCK ---
if __name__ == "__main__":
    sp = get_spotify_client()
    
    if sp:
        # The ultimate test: The song we caught with Shazam!
        test_title = "A Thousand Bad Times"
        test_artist = "Post Malone"
        
        track_uri = search_track(sp, test_title, test_artist)
        
        if track_uri:
            add_to_liked_songs(sp, track_uri)