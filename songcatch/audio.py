import subprocess
import os

def get_default_monitor():
    """Finds the active desktop audio output and returns its monitor name."""
    try:
        # Get the current default output sink (your speakers/headphones)
        result = subprocess.run(
            ['pactl', 'get-default-sink'], 
            capture_output=True, text=True, check=True
        )
        default_sink = result.stdout.strip()
        monitor_name = f"{default_sink}.monitor"
        
        print(f"🎯 Auto-detected system audio target: {monitor_name}")
        return monitor_name
        
    except Exception as e:
        print("⚠️  Warning: Couldn't auto-detect sink. Falling back to 'default'.")
        return "default"

def record_audio(filename="sample.wav", duration=5):
    """Captures system audio using ffmpeg."""
    
    device = get_default_monitor()
    print(f"🎧 Capturing {duration}s of audio...")
    
    command = [
        "ffmpeg",
        "-y",               # Overwrite file if it exists
        "-f", "pulse",      # Use PulseAudio / PipeWire
        "-i", device,       # Target the specific monitor device
        "-t", str(duration),# Duration
        filename
    ]
    
    # Run silently
    with open(os.devnull, 'w') as devnull:
        subprocess.run(command, stdout=devnull, stderr=devnull)
        
    print(f"✅ Saved capture to {filename}")
    return filename

# --- STANDALONE TEST BLOCK ---
if __name__ == "__main__":
    print("🎵 Go play a song on Spotify/YouTube right now...")
    
    # Capture 5 seconds of audio
    record_audio("test_capture.wav", duration=5)
    
    print("\n▶️  Test complete! Play 'test_capture.wav' to verify:")
    print("Run: aplay test_capture.wav   (or open it in your file manager)")