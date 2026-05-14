#!/usr/bin/env python3
"""Fetch news for CLI or phone-friendly web usage with optional audio output."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import string
import sys
import time
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs
from uuid import uuid4

import requests

NEWS_API_URL = "https://hn.algolia.com/api/v1/search"
DEFAULT_TOPIC = "technology"
MIN_KEYWORD_LENGTH = 3
MAX_ARTICLES_LIMIT = 20
REQUEST_TIMEOUT_SECONDS = 20
MAX_SESSIONS = 200
SESSION_TTL_SECONDS = 3600
MAX_REQUEST_BODY_BYTES = 1024 * 1024
MAX_TOPIC_LENGTH = 100
MAX_QUESTION_LENGTH = 500


@dataclass
class Article:
    title: str
    description: str
    source: str
    url: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "description": self.description,
            "source": self.source,
            "url": self.url,
        }


class NewsFetcher:
    """Client for pulling articles from a public no-key news endpoint."""

    @staticmethod
    def _fallback_articles(topic: str, limit: int) -> List[Article]:
        samples = [
            Article(
                title="Open-source AI tools continue to expand",
                description="Developers are adopting open-source AI stacks for rapid prototyping.",
                source="Offline sample",
                url="",
            ),
            Article(
                title="Cybersecurity teams focus on supply-chain risks",
                description="Organizations increase dependency audits and automated checks.",
                source="Offline sample",
                url="",
            ),
            Article(
                title="Cloud costs drive renewed optimization efforts",
                description="Engineering teams revisit right-sizing and workload scheduling.",
                source="Offline sample",
                url="",
            ),
        ]
        topic_lower = topic.lower()
        filtered = [a for a in samples if topic_lower in f"{a.title} {a.description}".lower()]
        pool = filtered if filtered else samples
        return pool[: max(1, min(limit, MAX_ARTICLES_LIMIT))]

    def fetch_top_headlines(self, topic: str, limit: int) -> List[Article]:
        page_size = max(1, min(limit, MAX_ARTICLES_LIMIT))
        try:
            response = requests.get(
                NEWS_API_URL,
                params={
                    "query": topic,
                    "tags": "story",
                    "hitsPerPage": page_size,
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            print(
                f"Warning: could not reach live news feed ({exc.__class__.__name__}). "
                "Using offline sample headlines."
            )
            return self._fallback_articles(topic=topic, limit=page_size)
        payload = response.json()

        if not isinstance(payload.get("hits"), list):
            print("Warning: live news feed format changed. Using offline sample headlines.")
            return self._fallback_articles(topic=topic, limit=page_size)

        articles: List[Article] = []
        for item in payload.get("hits", []):
            title = (item.get("title") or "Untitled").strip()
            description = "No description available."
            source = "Hacker News"
            url = (item.get("url") or item.get("story_url") or "").strip()
            articles.append(Article(title=title, description=description, source=source, url=url))

        if not articles:
            print("Warning: no live headlines found. Using offline sample headlines.")
            return self._fallback_articles(topic=topic, limit=page_size)

        return articles


class VoiceRecognizer:
    """Handle voice input using free speech recognition."""

    def __init__(self):
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.available = True
        except ImportError:
            print("Warning: speech_recognition not installed. Voice input disabled.")
            self.available = False

    def listen_for_command(self, prompt: str = "Listening...") -> Optional[str]:
        """Listen to microphone and convert speech to text."""
        if not self.available:
            return None

        import speech_recognition as sr

        print(prompt)
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Speak now!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            # Try Google Speech Recognition (free, no API key needed)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand audio. Please try again.")
                return None
            except sr.RequestException as e:
                print(f"Could not request results; {e}")
                return None

        except Exception as e:
            print(f"Error accessing microphone: {e}")
            return None


class TextToSpeech:
    """Handle text-to-speech using free TTS engines."""

    def __init__(self, use_offline: bool = True):
        self.use_offline = use_offline
        self.offline_available = False
        self.online_available = False

        # Try to initialize offline TTS (pyttsx3)
        if use_offline:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)  # Speed of speech
                self.offline_available = True
            except Exception as e:
                print(f"Warning: pyttsx3 not available: {e}")

        # gTTS is available as fallback
        try:
            import gtts
            self.online_available = True
        except ImportError:
            pass

    def speak(self, text: str) -> bool:
        """Speak the given text using available TTS engine."""
        if self.use_offline and self.offline_available:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
                return True
            except Exception as e:
                print(f"Error with offline TTS: {e}")

        if self.online_available:
            try:
                from gtts import gTTS
                import tempfile
                import os

                # Create temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_path = fp.name

                # Generate speech
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(temp_path)

                # Play audio (platform-specific)
                if sys.platform == "darwin":  # macOS
                    os.system(f"afplay {temp_path}")
                elif sys.platform == "linux":  # Linux
                    os.system(f"mpg123 -q {temp_path} || ffplay -nodisp -autoexit -loglevel quiet {temp_path}")
                elif sys.platform == "win32":  # Windows
                    os.system(f"start {temp_path}")

                # Clean up
                time.sleep(0.5)
                try:
                    os.unlink(temp_path)
                except:
                    pass

                return True
            except Exception as e:
                print(f"Error with online TTS: {e}")

        return False

    def generate_audio_file(self, text: str, output_path: str) -> bool:
        """Generate an audio file from text (for web interface)."""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            return True
        except Exception as e:
            print(f"Error generating audio file: {e}")
            return False


class Session:
    """Represents a user session for the web interface."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.articles: List[Article] = []
        self.current_topic = DEFAULT_TOPIC

    def is_expired(self) -> bool:
        return time.time() - self.last_accessed > SESSION_TTL_SECONDS

    def touch(self):
        self.last_accessed = time.time()


class SessionManager:
    """Manage user sessions for the web interface."""

    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def create_session(self) -> str:
        # Clean up expired sessions
        self._cleanup_expired()

        # Limit total sessions
        if len(self.sessions) >= MAX_SESSIONS:
            oldest = min(self.sessions.values(), key=lambda s: s.last_accessed)
            del self.sessions[oldest.session_id]

        # Create new session
        session_id = str(uuid4())
        self.sessions[session_id] = Session(session_id)
        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        session = self.sessions.get(session_id)
        if session and not session.is_expired():
            session.touch()
            return session
        elif session:
            del self.sessions[session_id]
        return None

    def _cleanup_expired(self):
        expired = [sid for sid, sess in self.sessions.items() if sess.is_expired()]
        for sid in expired:
            del self.sessions[sid]


class NewsHTTPHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the web interface."""

    session_manager = SessionManager()
    news_fetcher = NewsFetcher()
    tts = TextToSpeech(use_offline=False)  # Use online for web interface

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/":
            self._serve_index()
        elif path == "/api/news":
            self._handle_get_news(params)
        elif path == "/api/audio":
            self._handle_audio(params)
        elif path == "/health":
            self._send_json({"status": "healthy"}, HTTPStatus.OK)
        else:
            self._send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/session":
            self._handle_create_session()
        elif path == "/api/search":
            self._handle_search()
        else:
            self._send_error(HTTPStatus.NOT_FOUND, "Not found")

    def _serve_index(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI News Voice Reader</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                .article { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .article h3 { margin-top: 0; color: #333; }
                button { padding: 10px 20px; margin: 5px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 5px; }
                button:hover { background: #0056b3; }
                input { padding: 10px; width: 300px; border: 1px solid #ddd; border-radius: 5px; }
                #status { margin: 10px 0; color: #666; }
            </style>
        </head>
        <body>
            <h1>AI News Voice Reader</h1>
            <div>
                <input type="text" id="topic" placeholder="Enter topic (e.g., AI, python)" value="technology">
                <button onclick="searchNews()">Search News</button>
                <button onclick="readAll()">Read All</button>
            </div>
            <div id="status"></div>
            <div id="articles"></div>

            <script>
                let sessionId = null;
                let articles = [];

                async function init() {
                    const response = await fetch('/api/session', { method: 'POST' });
                    const data = await response.json();
                    sessionId = data.session_id;
                    searchNews();
                }

                async function searchNews() {
                    const topic = document.getElementById('topic').value || 'technology';
                    document.getElementById('status').textContent = 'Fetching news...';

                    const response = await fetch(`/api/news?session_id=${sessionId}&topic=${encodeURIComponent(topic)}&limit=5`);
                    const data = await response.json();

                    if (data.articles) {
                        articles = data.articles;
                        displayArticles(articles);
                        document.getElementById('status').textContent = `Found ${articles.length} articles`;
                    }
                }

                function displayArticles(articles) {
                    const container = document.getElementById('articles');
                    container.innerHTML = articles.map((article, index) => `
                        <div class="article">
                            <h3>${article.title}</h3>
                            <p>${article.description}</p>
                            <p><small>Source: ${article.source}</small></p>
                            ${article.url ? `<a href="${article.url}" target="_blank">Read more</a>` : ''}
                            <button onclick="readArticle(${index})">Read Aloud</button>
                        </div>
                    `).join('');
                }

                async function readArticle(index) {
                    const article = articles[index];
                    const text = `${article.title}. ${article.description}`;
                    document.getElementById('status').textContent = 'Generating audio...';

                    const audio = new Audio(`/api/audio?session_id=${sessionId}&text=${encodeURIComponent(text)}`);
                    audio.play();
                    document.getElementById('status').textContent = 'Playing audio...';

                    audio.onended = () => {
                        document.getElementById('status').textContent = 'Ready';
                    };
                }

                async function readAll() {
                    for (let i = 0; i < articles.length; i++) {
                        await new Promise(resolve => {
                            const article = articles[i];
                            const text = `Article ${i + 1}. ${article.title}. ${article.description}`;
                            const audio = new Audio(`/api/audio?session_id=${sessionId}&text=${encodeURIComponent(text)}`);
                            audio.play();
                            document.getElementById('status').textContent = `Reading article ${i + 1} of ${articles.length}...`;
                            audio.onended = resolve;
                        });
                    }
                    document.getElementById('status').textContent = 'Finished reading all articles';
                }

                init();
            </script>
        </body>
        </html>
        """
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def _handle_create_session(self):
        session_id = self.session_manager.create_session()
        self._send_json({"session_id": session_id}, HTTPStatus.CREATED)

    def _handle_get_news(self, params):
        session_id = params.get("session_id", [None])[0]
        if not session_id:
            self._send_error(HTTPStatus.BAD_REQUEST, "Missing session_id")
            return

        session = self.session_manager.get_session(session_id)
        if not session:
            self._send_error(HTTPStatus.UNAUTHORIZED, "Invalid or expired session")
            return

        topic = params.get("topic", [DEFAULT_TOPIC])[0]
        limit = int(params.get("limit", [5])[0])

        # Validate inputs
        if len(topic) > MAX_TOPIC_LENGTH:
            self._send_error(HTTPStatus.BAD_REQUEST, "Topic too long")
            return

        articles = self.news_fetcher.fetch_top_headlines(topic, limit)
        session.articles = articles
        session.current_topic = topic

        self._send_json({
            "articles": [a.to_dict() for a in articles],
            "topic": topic,
            "count": len(articles)
        }, HTTPStatus.OK)

    def _handle_search(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > MAX_REQUEST_BODY_BYTES:
            self._send_error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "Request too large")
            return

        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON")
            return

        session_id = data.get("session_id")
        topic = data.get("topic", DEFAULT_TOPIC)

        if not session_id:
            self._send_error(HTTPStatus.BAD_REQUEST, "Missing session_id")
            return

        session = self.session_manager.get_session(session_id)
        if not session:
            self._send_error(HTTPStatus.UNAUTHORIZED, "Invalid or expired session")
            return

        articles = self.news_fetcher.fetch_top_headlines(topic, 5)
        session.articles = articles

        self._send_json({
            "articles": [a.to_dict() for a in articles],
            "count": len(articles)
        }, HTTPStatus.OK)

    def _handle_audio(self, params):
        session_id = params.get("session_id", [None])[0]
        text = params.get("text", [None])[0]

        if not session_id or not text:
            self._send_error(HTTPStatus.BAD_REQUEST, "Missing parameters")
            return

        session = self.session_manager.get_session(session_id)
        if not session:
            self._send_error(HTTPStatus.UNAUTHORIZED, "Invalid or expired session")
            return

        # Generate audio file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            audio_path = fp.name

        if self.tts.generate_audio_file(text[:500], audio_path):
            try:
                with open(audio_path, 'rb') as f:
                    audio_data = f.read()

                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(len(audio_data)))
                self.end_headers()
                self.wfile.write(audio_data)

                os.unlink(audio_path)
            except Exception as e:
                print(f"Error serving audio: {e}")
                self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Error generating audio")
        else:
            self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Error generating audio")

    def _send_json(self, data: dict, status: HTTPStatus):
        response = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def _send_error(self, status: HTTPStatus, message: str):
        self._send_json({"error": message}, status)

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_cli(args):
    """Run the CLI interface with voice support."""
    fetcher = NewsFetcher()
    voice = VoiceRecognizer()
    tts = TextToSpeech(use_offline=True)

    topic = args.topic or DEFAULT_TOPIC
    use_voice = args.voice and voice.available

    print(f"\n{'='*60}")
    print(f"AI News Voice Reader - CLI Mode")
    print(f"{'='*60}\n")

    # Get topic from voice or use default
    if use_voice and not args.topic:
        print("Would you like to search for a specific topic?")
        voice_topic = voice.listen_for_command("Say a topic or press Ctrl+C to skip...")
        if voice_topic:
            topic = voice_topic

    # Fetch news
    print(f"\nFetching top {args.limit} headlines about '{topic}'...\n")
    articles = fetcher.fetch_top_headlines(topic, args.limit)

    # Display articles
    for i, article in enumerate(articles, 1):
        print(f"\n[{i}] {article.title}")
        print(f"    {article.description}")
        print(f"    Source: {article.source}")
        if article.url:
            print(f"    URL: {article.url}")
        print("-" * 60)

    # Read aloud if requested
    if args.read_aloud and articles:
        print("\nReading articles aloud...")
        for i, article in enumerate(articles, 1):
            text = f"Article {i}. {article.title}. {article.description}"
            print(f"Reading: {article.title}")
            tts.speak(text)
            time.sleep(0.5)

    # Interactive mode
    if use_voice and args.interactive:
        print("\n" + "="*60)
        print("Interactive Voice Mode")
        print("Say 'search [topic]' to search, or 'read article [number]' to read")
        print("Press Ctrl+C to exit")
        print("="*60 + "\n")

        try:
            while True:
                command = voice.listen_for_command("Listening for command...")
                if not command:
                    continue

                command_lower = command.lower()

                if "search" in command_lower:
                    # Extract topic from command
                    parts = command_lower.split("search", 1)
                    if len(parts) > 1:
                        topic = parts[1].strip()
                        print(f"\nSearching for '{topic}'...")
                        articles = fetcher.fetch_top_headlines(topic, args.limit)

                        for i, article in enumerate(articles, 1):
                            print(f"[{i}] {article.title}")

                        tts.speak(f"Found {len(articles)} articles about {topic}")

                elif "read" in command_lower:
                    # Extract article number
                    import re
                    numbers = re.findall(r'\d+', command)
                    if numbers:
                        idx = int(numbers[0]) - 1
                        if 0 <= idx < len(articles):
                            article = articles[idx]
                            text = f"{article.title}. {article.description}"
                            tts.speak(text)
                        else:
                            tts.speak("Invalid article number")
                    else:
                        tts.speak("Please specify an article number")

                elif "exit" in command_lower or "quit" in command_lower:
                    tts.speak("Goodbye!")
                    break

        except KeyboardInterrupt:
            print("\n\nExiting...")


def run_server(args):
    """Run the web server interface."""
    host = args.host
    port = args.port

    print(f"\n{'='*60}")
    print(f"AI News Voice Reader - Web Server Mode")
    print(f"{'='*60}")
    print(f"\nStarting server on http://{host}:{port}")
    print(f"Open this URL in your browser to use the web interface")
    print(f"Press Ctrl+C to stop the server\n")

    server = ThreadingHTTPServer((host, port), NewsHTTPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(
        description="AI News Voice Reader - Fetch and read news with voice support"
    )

    parser.add_argument(
        "--mode",
        choices=["cli", "server"],
        default="cli",
        help="Run mode: cli for command-line, server for web interface (default: cli)"
    )

    parser.add_argument(
        "--topic",
        type=str,
        help="News topic to search for (default: technology)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of articles to fetch (default: 5, max: 20)"
    )

    parser.add_argument(
        "--voice",
        action="store_true",
        help="Enable voice input (CLI mode only)"
    )

    parser.add_argument(
        "--read-aloud",
        action="store_true",
        help="Read articles aloud (CLI mode only)"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enable interactive voice mode (CLI mode only)"
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server host (server mode only, default: 127.0.0.1)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (server mode only, default: 8000)"
    )

    args = parser.parse_args()

    if args.mode == "cli":
        run_cli(args)
    else:
        run_server(args)


if __name__ == "__main__":
    main()
