# 🎵 SongCatch CLI

**SongCatch** is a lightning-fast command-line tool that listens to your system audio, identifies the currently playing track using the Shazam API, and automatically saves it to your Spotify **Liked Songs**.

No switching tabs. No copy-pasting. Just run one command.

---

## ✨ Features

- ⚡ **One-Command Save** – Identify and like a track instantly.
- 🎧 **System Audio Capture** – Works with YouTube, Twitch, Spotify Web, movies, or any sound your system plays.
- 🔐 **Secure Spotify Login (PKCE)** – No client secrets stored.
- 🧠 **First-Run Setup** – Prompts for your API key once and remembers it.
- ❤️ **Auto-Likes** – Adds the recognized track directly to your Spotify library.

---

## 🛠️ Prerequisites

SongCatch requires **`ffmpeg`** for capturing and processing system audio.

Install it using:

### Ubuntu / Debian

```bash
sudo apt install ffmpeg
```

### Arch Linux

```bash
sudo pacman -S ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

---

## 📦 Installation

Install globally from GitHub:

```bash
pip install git+https://github.com/morpheus-30/SongCatch_CLI.git
```

After installation, you can run it from anywhere using:

```bash
songcatch
```

---

## 🚀 Usage

Whenever you hear a banger playing on your system:

```bash
songcatch
```

SongCatch will:

1. Record a short snippet of system audio
2. Identify the track via Shazam API
3. Search it on Spotify
4. Add it to your **Liked Songs**
5. Display the result in your terminal

Example output:

```
🎵 Found: Blinding Lights – The Weeknd
❤️ Added to your Spotify Liked Songs
```

---

## 🔑 First Run Setup

On first launch:

1. You’ll be prompted for a **Shazam API Key**
   Get one free from:
   [https://rapidapi.com/apidojo/api/shazam/](https://rapidapi.com/apidojo/api/shazam/)

2. Your browser will open for **Spotify authorization**
   Approve access to allow SongCatch to add tracks to your library.

After that, you're fully set up. No repeated logins.

---

## 🔒 Security

- Uses Spotify’s **PKCE OAuth Flow**
- No client secret stored locally
- Tokens are securely saved in your user directory
- API keys are only requested once

---

## 🧠 How It Works

```
System Audio → ffmpeg → Shazam API → Spotify Search → Add to Library
```

Clean. Fast. Automated.

---

## 💡 Why SongCatch?

Because great songs shouldn’t be lost.

If something hits your ears, it should hit your library too.
