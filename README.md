# AI News Voice Recognition

A Python application that fetches news articles and provides voice recognition and text-to-speech capabilities. Access news through CLI with voice commands or via a phone-friendly web interface with audio playback.

## 🌐 Quick Access - Browser-Based Q&A

**NEW!** Browser-based interface with **full voice interaction** (no Python installation needed):

### 🎤 Voice Features (NEW!)
- **Ask questions with your voice** - Click mic button and speak
- **Hear answers spoken back** - Enable voice mode for automatic TTS
- **Conversational AI** - Works just like talking to Copilot!
- **No installation needed** - All in browser using Web Speech API

### 📱 Access Online (After Deployment)
**Live URL**: https://ana-iulia.github.io/AI-news-voice-recognition/

### 💻 Access Locally
Open `index.html` in any modern browser - works immediately!

```bash
# Just open the file
open index.html              # macOS
start index.html             # Windows
xdg-open index.html          # Linux
```

**See [USAGE.md](USAGE.md) for complete usage instructions.**

## Features

✨ **Voice Recognition** - Search for news using your voice (no API key required)
🔊 **Text-to-Speech** - Listen to news articles read aloud
🎤 **Voice Q&A** - Ask questions with your voice and hear answers (NEW!)
💬 **Conversational Mode** - Talk naturally like with Copilot (NEW!)
📱 **Web Interface** - Mobile-friendly web UI with audio playback
💻 **CLI Mode** - Command-line interface with interactive voice mode
🔒 **Privacy-First** - All free libraries, no API keys required
🌐 **Offline Support** - Falls back to offline samples when network unavailable
🎯 **Browser Q&A** - Ask questions about fetched news articles

## Installation

### Prerequisites

- Python 3.7 or higher
- Microphone (for voice input in CLI mode)
- Audio output device

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Note for PyAudio installation issues:**
- **macOS**: `brew install portaudio && pip install pyaudio`
- **Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`
- **Windows**: Download pre-built wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

### Optional (for audio playback on Linux)

```bash
sudo apt-get install mpg123  # or ffmpeg
```

## Usage

### CLI Mode (Default)

#### Basic news fetch:
```bash
python news_voice_app.py
```

#### Search specific topic:
```bash
python news_voice_app.py --topic "artificial intelligence" --limit 10
```

#### With voice input:
```bash
python news_voice_app.py --voice
```

#### Read news aloud:
```bash
python news_voice_app.py --read-aloud --limit 3
```

#### Interactive voice mode:
```bash
python news_voice_app.py --voice --interactive
```

In interactive mode, use voice commands like:
- "search python programming"
- "read article 1"
- "exit"

### Web Server Mode

#### Start the web server:
```bash
python news_voice_app.py --mode server
```

Then open http://127.0.0.1:8000 in your browser.

#### Custom host and port:
```bash
python news_voice_app.py --mode server --host 0.0.0.0 --port 8080
```

## Web Interface

The web interface provides:
- Search news by topic
- Display articles with title, description, and source
- "Read Aloud" button for each article
- "Read All" to listen to all articles sequentially
- Mobile-friendly responsive design

## Command-Line Options

```
--mode {cli,server}      Run mode: cli or server (default: cli)
--topic TOPIC           News topic to search
--limit LIMIT           Number of articles (default: 5, max: 20)
--voice                 Enable voice input (CLI only)
--read-aloud            Read articles aloud (CLI only)
--interactive           Interactive voice mode (CLI only)
--host HOST             Server host (server mode, default: 127.0.0.1)
--port PORT             Server port (server mode, default: 8000)
```

## How It Works

### Voice Recognition
- Uses **SpeechRecognition** library with Google's free speech recognition service
- No API key required
- Works with any microphone

### Text-to-Speech
- **CLI Mode**: Uses `pyttsx3` (offline) for immediate playback
- **Web Mode**: Uses `gTTS` (online, free) to generate MP3 files
- Both options require no API keys

### News Source
- Fetches from Hacker News Algolia API (free, no key required)
- Falls back to offline samples if network unavailable
- Configurable topic and article limit

## Architecture

```
news_voice_app.py
├── NewsFetcher        - Fetch articles from Hacker News API
├── VoiceRecognizer    - Speech-to-text using SpeechRecognition
├── TextToSpeech       - Text-to-speech using pyttsx3/gTTS
├── SessionManager     - Manage web sessions
├── NewsHTTPHandler    - Web server request handler
├── run_cli()          - CLI interface with voice support
└── run_server()       - Web server interface
```

## API Endpoints (Web Mode)

- `GET /` - Web interface HTML
- `POST /api/session` - Create a new session
- `GET /api/news?session_id=...&topic=...&limit=...` - Fetch news articles
- `GET /api/audio?session_id=...&text=...` - Generate audio from text
- `GET /health` - Health check

## Examples

### Example 1: Quick news check
```bash
python news_voice_app.py --topic "cybersecurity" --limit 5
```

### Example 2: Voice-controlled news reader
```bash
python news_voice_app.py --voice --read-aloud --interactive
# Then say: "search machine learning"
# Then say: "read article 2"
```

### Example 3: Web server for mobile
```bash
python news_voice_app.py --mode server --host 0.0.0.0 --port 8080
# Access from phone: http://YOUR_IP:8080
```

## Troubleshooting

### Voice recognition not working
- Check microphone permissions
- Ensure PyAudio is properly installed
- Try adjusting microphone sensitivity

### Text-to-speech not working (CLI)
- **Offline (pyttsx3)**: May need platform-specific TTS engine
  - macOS: Built-in `say` command
  - Linux: Install `espeak`: `sudo apt-get install espeak`
  - Windows: Built-in SAPI5
- **Online (gTTS)**: Requires internet connection

### Web audio not playing
- Ensure `gTTS` is installed: `pip install gTTS`
- Check browser console for errors
- Some browsers may block autoplay

## Privacy & Security

- No external API keys required
- News fetched from public Hacker News API
- Google Speech Recognition used (free tier, no account needed)
- gTTS audio generation (free, no account needed)
- Session data stored in memory only (not persisted)
- Sessions expire after 1 hour of inactivity

## License

MIT License - Feel free to use and modify

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.

## Credits

- News data from [Hacker News Algolia API](https://hn.algolia.com/api)
- Speech recognition via [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- Text-to-speech via [pyttsx3](https://github.com/nateshmbhat/pyttsx3) and [gTTS](https://github.com/pndurette/gTTS)