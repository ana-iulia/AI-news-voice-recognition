# How to Use the News Audio Q&A Interface

## 🌐 Where to Access

### Option 1: GitHub Pages (Recommended - Live Online Access)

Once you merge this PR to the `main` branch, the site will automatically deploy to GitHub Pages at:

**https://ana-iulia.github.io/AI-news-voice-recognition/**

The GitHub Actions workflow will automatically:
1. Build and deploy when you push to `main`
2. Make it accessible from any device with a browser
3. Update automatically on every push to `main`

To enable GitHub Pages:
1. Go to your repository settings
2. Navigate to **Pages** section (left sidebar)
3. Under "Source", select **GitHub Actions**
4. The workflow will deploy automatically

### Option 2: Local File Access (Works Immediately)

You can open the file directly in your browser:

**File path**: `index.html`

#### On Windows:
```
# Double-click index.html or:
start index.html
```

#### On macOS:
```bash
open index.html
```

#### On Linux:
```bash
xdg-open index.html
# or
firefox index.html
# or
google-chrome index.html
```

### Option 3: Local Web Server

For testing or development, run a local server:

```bash
# Using Python 3
python3 -m http.server 8000

# Then open: http://localhost:8000/index.html
```

## 📱 How to Use the Interface

### Step 1: Start a Session

1. **Enter a Topic** (default: "technology")
   - Examples: "artificial intelligence", "python", "blockchain", "cybersecurity"
   - Any topic will fetch related news from Hacker News

2. **Set Number of Articles** (1-20, default: 5)
   - Choose how many articles you want to fetch
   - More articles = more content to ask questions about

3. **Click "Start Session"**
   - Fetches live news from Hacker News API
   - Falls back to offline samples if network unavailable
   - Articles will appear in the list below

### Step 2: Read the Articles

The fetched articles will display in a numbered list showing:
- Article titles
- Brief descriptions
- Source information

**Optional**: Click **"Read All Aloud"** button to have your browser read all articles using text-to-speech.

### Step 3: Ask Questions (3 Questions per Session)

You can ask questions about the fetched articles **using text OR voice**. The system supports:

#### 🎤 NEW: Voice Interaction Mode

**Enable Voice Mode** for a hands-free, conversational experience:

1. **Toggle Voice Mode ON** (switch at top of question section)
   - When enabled, answers will be automatically spoken aloud
   - Works just like talking to Copilot!

2. **Click the 🎤 Voice Button** to ask questions with your voice
   - The button will pulse red while listening
   - Speak your question clearly
   - Your question is automatically transcribed and submitted
   - The answer is spoken back to you (if voice mode is on)

3. **Grant Microphone Permission** when prompted by your browser
   - Required for voice input to work
   - Permission is saved for future visits

**Voice Interaction Example:**
```
1. Enable Voice Mode toggle ✓
2. Click 🎤 Voice button
3. Speak: "How many articles did you fetch?"
4. See question appear in text box
5. Hear answer: "I fetched 5 articles."
```

#### Question Types:

1. **Count Questions**
   - "How many articles did you fetch?"
   - "What's the count?"
   - **Returns**: The number of articles

2. **Title Questions**
   - "What are the titles?"
   - "List all titles"
   - "Show me the titles"
   - **Returns**: All article titles separated by semicolons

3. **Source Questions**
   - "What are the sources?"
   - "Where did these come from?"
   - "Show sources"
   - **Returns**: Unique sources (usually "Hacker News" or "Offline sample")

4. **Keyword Search Questions**
   - "Are there articles about Python?"
   - "Do any mention machine learning?"
   - "Which articles have the keyword security?"
   - **Returns**: Articles that contain your keyword in title or description

#### How to Ask:

1. Type your question in the **"Your Question"** input field
2. Click **"Submit"** button
3. The answer will appear in the **"Answer"** section below
4. You get **3 questions per session**
5. After 3 questions, start a new session to ask more

### Step 4: Start New Session (Optional)

To search a different topic or reset your questions:
1. Enter a new topic
2. Click **"Start Session"** again
3. Your question counter resets to 0/3

## 🎯 Example Usage Scenario

```
1. Topic: "artificial intelligence"
2. Number of Articles: 10
3. Click "Start Session"

Questions you could ask:
Q1: "How many articles?"
A1: "I fetched 10 articles."

Q2: "List the titles"
A2: "Here are the titles: AI breakthrough in healthcare; Machine learning..."

Q3: "Do any mention Python?"
A3: "2 article(s) mention 'python': Python ML Library Released; Python AI Tools"
```

## 🔊 Audio Features

### Browser Text-to-Speech
- Click **"Read All Aloud"** to hear all articles
- Uses your browser's built-in speech synthesis
- Works on most modern browsers (Chrome, Firefox, Safari, Edge)
- No internet required for speech synthesis
- Automatically queues all articles for reading

### Supported Browsers:
- ✅ Chrome/Chromium (Desktop & Mobile)
- ✅ Firefox (Desktop & Mobile)
- ✅ Safari (Desktop & Mobile)
- ✅ Edge (Desktop & Mobile)
- ⚠️ Older browsers may not support speech synthesis

## 🎨 Features

- 📱 **Mobile-Friendly**: Responsive design works on phones and tablets
- 🌙 **Clean UI**: Modern, easy-to-read interface with purple gradient
- 🔒 **Privacy-First**: No API keys needed, all free services
- 🌐 **Offline Support**: Falls back to sample articles if network fails
- 🎤 **Voice Input**: Ask questions using speech recognition (NEW!)
- 🔊 **Voice Output**: Automatic text-to-speech for answers (NEW!)
- 💬 **Conversational AI**: Talk to it like Copilot (NEW!)
- ⚡ **Fast Loading**: Single HTML file with no external dependencies
- 🔄 **Real-time News**: Fetches live articles from Hacker News

## 🛠️ Technical Details

### Architecture:
- **Single Page Application (SPA)**: Everything in one HTML file
- **No Backend Required**: Runs entirely in the browser
- **News Source**: Hacker News Algolia API (free, no auth)
- **Speech Recognition**: Web Speech API for voice input (NEW!)
- **Text-to-Speech**: Web Speech API for voice output (built into browsers)
- **Session Management**: In-browser state management

### API Used:
- **Hacker News API**: `https://hn.algolia.com/api/v1/search`
- No API key or authentication required
- Public and free to use

### Browser Requirements:
- Modern browser with JavaScript enabled
- Support for ES6+ JavaScript features
- Speech Synthesis API for audio features
- Speech Recognition API for voice input (Chrome, Edge, Safari)

### Voice Features:
- **Speech Recognition**: Uses browser's built-in Web Speech API
- **Text-to-Speech**: Automatic voice responses in voice mode
- **Microphone Permission**: Required for voice input
- **Best Experience**: Chrome or Edge for voice recognition
- **Privacy**: All voice processing happens in your browser

## 🚀 Deployment Status

After merging to `main`:
- ✅ Automatic deployment via GitHub Actions
- ✅ Available at: `https://ana-iulia.github.io/AI-news-voice-recognition/`
- ✅ Updates automatically on every push
- ✅ CDN-backed for fast global access

## 📞 Access from Your Phone

### After GitHub Pages Deployment:
1. Open your phone's browser (Chrome, Safari, Firefox)
2. Go to: `https://ana-iulia.github.io/AI-news-voice-recognition/`
3. Bookmark it for easy access
4. Works offline after first visit (browser caching)

### Using Local Network (Before Deployment):
1. Start local server: `python3 -m http.server 8000`
2. Find your computer's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. On phone, open: `http://YOUR_IP:8000/index.html`
4. Make sure phone and computer are on same WiFi

## 🎓 Tips

1. **Better Questions**: Be specific with keywords (use words longer than 3 letters)
2. **More Context**: Fetch more articles (10-20) for richer question responses
3. **Focused Topics**: Use specific topics for more relevant results
4. **Audio Control**: Pause audio by closing/refreshing the page
5. **Session Reset**: Start new session anytime to search different topics

## ❓ Troubleshooting

**Q: "Read All Aloud" button doesn't work?**
- Check if your browser supports Speech Synthesis
- Ensure browser audio isn't muted
- Try Chrome/Firefox if using older browser

**Q: Voice button (🎤) not working?**
- Grant microphone permission when prompted
- Speech recognition works best in Chrome, Edge, and Safari
- Firefox has limited support for speech recognition
- Check browser console for permission errors
- Try refreshing the page

**Q: Microphone permission denied?**
- Click the 🔒 or ⓘ icon in browser address bar
- Allow microphone access for this site
- Refresh the page after granting permission

**Q: Voice mode not speaking answers?**
- Enable the "Voice Mode" toggle switch first
- Check that browser audio isn't muted
- Ensure system volume is up
- Try clicking the toggle off and on again

**Q: Voice recognition hears wrong words?**
- Speak clearly and at normal pace
- Reduce background noise
- Move closer to microphone
- Try rephrasing your question

**Q: No articles loading?**
- Check internet connection
- System will automatically fall back to offline samples
- Try a different topic

**Q: Can't access from phone?**
- Wait for GitHub Pages deployment to complete (~2-5 minutes)
- Or use local network method with IP address

**Q: Questions not working?**
- Ensure you clicked "Start Session" first
- Check that you haven't used all 3 questions
- Rephrase using keywords: "count", "titles", "sources", or specific keywords

## 📄 Files

- `index.html` - Complete web interface (standalone, no dependencies)
- `.github/workflows/deploy.yml` - Automated GitHub Pages deployment

---

**🎉 Enjoy your AI-powered News Q&A experience!**
