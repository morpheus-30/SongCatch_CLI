import sys
import time
import wave
import subprocess,os

def record_audio(filename="/tmp/songcatch_capture.wav", duration=5):
    """Detects the OS and routes the audio capture accordingly."""
    print("🎙️  Initializing audio interface...")
    print(sys.platform)
    if sys.platform == "win32":
        print("🪟 Windows detected! Booting native WASAPI loopback...")
        # Fix Windows pathing since /tmp/ doesn't exist natively on Windows
        win_filename = "songcatch_capture.wav" 
        _record_windows(win_filename, duration)
        
        # If running on Windows, we need to return the new filename 
        # so main.py knows where to find it!
        return win_filename 
    else:
        print("🐧/🍏 Unix system detected! Using standard audio routing...")
        _record_unix(filename, duration)
        return filename

def _record_windows(filename, duration):
    """Windows-specific WASAPI loopback capture."""
    try:
        import pyaudiowpatch as pyaudio
    except ImportError:
        print("❌ Missing Windows audio driver. Run: pip install pyaudiowpatch")
        sys.exit(1)

    with pyaudio.PyAudio() as p:
        try:
            # 1. Ask Windows for the WASAPI driver info
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
            # 2. Find whatever the user's default speakers are
            default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
            
            # 3. Find the hidden "Loopback" version of those exact speakers
            if not default_speakers["isLoopbackDevice"]:
                for loopback in p.get_loopback_device_info_generator():
                    if default_speakers["name"] in loopback["name"]:
                        default_speakers = loopback
                        break
        except OSError:
            print("❌ WASAPI is not available on this system.")
            return

        # 4. Set up the audio file format
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(default_speakers["maxInputChannels"])
        wave_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(int(default_speakers["defaultSampleRate"]))

        # 5. The callback that writes audio data instantly as it plays
        def callback(in_data, frame_count, time_info, status):
            wave_file.writeframes(in_data)
            return (in_data, pyaudio.paContinue)

        # 6. Open the loopback stream and listen
        with p.open(format=pyaudio.paInt16,
                    channels=default_speakers["maxInputChannels"],
                    rate=int(default_speakers["defaultSampleRate"]),
                    frames_per_buffer=512,
                    input=True,
                    input_device_index=default_speakers["index"],
                    stream_callback=callback):
            time.sleep(duration)
            
        wave_file.close()

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

def  _record_unix(filename="sample.wav", duration=5):
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