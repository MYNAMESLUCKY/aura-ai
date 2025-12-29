# 🤖 Aura — Local AI Assistant with Persistent Memory

Aura is a privacy-first, local AI assistant powered by Ollama.
It features **persistent identity**, **long-term memory**, **semantic (RAG) recall**, 
**automated browser control**, and **optional live web search** — all stored locally on your machine.

---

## ✨ Key Features

- 🔐 **Persistent Identity**
  - One-time generated user ID
  - Memory survives restarts
  - Encrypted identity storage

- 🧠 **Hybrid Memory System**
  - Short-term chat memory
  - Long-term factual memory
  - Semantic vector memory (RAG)
  - Automatic memory summarization

- 🌐 **Smart Browser Automation**
  - Intelligent intent parsing with LLM
  - Automatic web search integration
  - Reliable URL extraction and opening
  - Multi-platform support (YouTube, Netflix, GitHub, etc.)
  - Comprehensive error handling

- 🔎 **Optional Web Search**
  - Uses Tavily Search API
  - Automatic fallback mechanisms
  - Disabled by default unless API key is set

- ⚙️ **Model Agnostic**
  - Uses Ollama for local inference
  - Switch models anytime
  - Works with any Ollama-compatible model

- 🩺 **Built-in Diagnostics**
  - Doctor command for system health checks
  - Config migration and validation
  - Model inspection and verification

---

## 📦 Installation

### 1. Prerequisites
- **Python 3.10+**
- **Ollama installed and running** (https://ollama.ai)
- A supported model pulled: `ollama pull deepseek-v3.1:671b-cloud`

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo>
cd cyber/aura

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 3. Configuration

Create `aura/config.yaml` with your settings:

```yaml
# LLM Configuration
model: "deepseek-v3.1:671b-cloud"  # Ollama model name
temperature: 0.7

# Memory Settings
memory_dir: "./memory"
vector_db_dir: "./db/vectors"

# Web Search (Optional)
tavily_api_key: ""  # Set your Tavily API key here
enable_web_search: false  # Enable with API key

# Identity
identity_dir: "./identity"
```

---

## 🚀 Running Aura

### Start the Agent

```bash
aura
```

### Check Ollama is Running

Before running Aura, ensure Ollama is running:

```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# Or pull a model if needed
ollama pull deepseek-v3.1:671b-cloud
```

### Basic Usage

```
You: "What is the capital of France?"
Aura: "The capital of France is Paris..."

You: "Open YouTube and play lo-fi music"
Aura: "🌐 Opened result: https://youtube.com/..."

You: "Search for GitHub repositories about AI"
Aura: "Based on web search..."
```

---

## 🌐 Browser Automation Features

### How It Works

Aura intelligently detects and executes browser-related requests:

1. **Intent Parsing** - LLM extracts structured browser intent as JSON
2. **Direct Execution** - Opens URL if directly provided
3. **Web Search Fallback** - Uses Tavily to find relevant URLs
4. **URL Extraction** - Regex extracts valid URLs from search results
5. **Error Handling** - Detailed logging for debugging

### Intent Schema

The browser intent follows this JSON schema:

```json
{
  "tool": "browser",
  "action": "open|search|play",
  "query": "<what should be opened or searched>"
}
```

### Supported Actions

- **`open`** - Open a website or search result
- **`search`** - Perform a web search
- **`play`** - Play media (YouTube, Spotify, etc.)

### Supported Platforms

- YouTube
- Netflix
- Spotify
- GitHub
- Wikipedia
- Google
- And any other website

### Example Usage in Code

```python
from aura.tools.browser.intent import parse_browser_intent
from aura.tools.browser.execute import execute_browser_intent
from langchain_ollama import ChatOllama

llm = ChatOllama(model='deepseek-v3.1:671b-cloud', temperature=0)

# Parse user input into browser intent
intent = parse_browser_intent(llm, 'open youtube and play lo-fi music')
print('INTENT:', intent)
# Output: {'tool': 'browser', 'action': 'open', 'query': 'lo-fi music'}

# Execute the intent
if intent:
    result = execute_browser_intent(intent)
    print(result)
    # Output: 🌐 Opened result: https://youtube.com/...
```

### Error Handling

The browser tool includes comprehensive error handling:

- ✅ Validates URLs before opening
- ✅ Catches web search failures
- ✅ Logs detailed error messages
- ✅ Provides fallback mechanisms
- ✅ Never fails silently

**Example Error Messages:**
```
⚠️ Browser intent parsing failed: <error details>
⚠️ Web search unavailable: <error details>
⚠️ Failed to open browser: <error details>
⚠️ Couldn't find a suitable link to open.
```

---

## 📁 Browser Tool Architecture

### File Structure

| File | Purpose |
|------|---------|
| `browser/intent.py` | Parse user input into structured browser intent |
| `browser/execute.py` | Execute browser intents with fallbacks |
| `browser/enrich.py` | Resolve intent to safe URLs using Tavily + LLM |
| `browser/open.py` | Launch browsers with URL normalization |
| `browser/detect.py` | Detect installed browsers on Windows |
| `intent.py` | Pre-filtering for browser vs non-browser requests |
| `registry.py` | Tool routing and orchestration |

### Execution Flow Diagram

```
User Input
    ↓
parse_browser_intent() [browser/intent.py]
    ↓ (LLM extracts structured intent)
execute_browser_intent() [browser/execute.py]
    ↓
[Has direct URL?] → Yes → webbrowser.open(url)
    ↓ No
run_web_search() [features/web_search.py]
    ↓ (Tavily search)
_URL_REGEX.findall() 
    ↓ (Extract URLs)
webbrowser.open(urls[0])
    ↓
Success Response / Error Logging
```

---

## 🏗️ Project Structure

```
aura/
├── src/
│   └── aura/
│       ├── __main__.py           # Entry point
│       ├── app.py                # Main application
│       ├── config.py             # Configuration management
│       ├── db.py                 # Database layer
│       ├── identity.py           # User identity management
│       ├── embeddings.py         # Vector embeddings
│       ├── migrator.py           # Data migration
│       ├── ollama_utils.py       # Ollama integration
│       ├── version.py            # Version info
│       ├── features/
│       │   ├── chat.py           # Chat interface
│       │   ├── memory.py         # Memory management
│       │   ├── vector_memory.py  # RAG vector storage
│       │   ├── user_memory.py    # User-specific memory
│       │   ├── summarizer.py     # Memory summarization
│       │   ├── web_search.py     # Tavily web search
│       │   └── tools.py          # Tool orchestration
│       └── tools/
│           ├── intent.py         # Intent detection
│           ├── registry.py       # Tool routing
│           └── browser/
│               ├── intent.py     # Browser intent parsing
│               ├── execute.py    # Browser execution
│               ├── enrich.py     # Intent enrichment
│               ├── open.py       # Browser launcher
│               └── detect.py     # Browser detection
├── config.yaml                   # Configuration file
└── identity/
    ├── user_id.txt              # User identifier
    └── private_key.enc          # Encrypted identity key
```

---

## 🔧 Development

### Running Tests

```bash
pytest tests/
```

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Adding New Tools

1. Create a new tool module in `src/aura/tools/`
2. Implement intent parsing and execution
3. Register in `tools/registry.py`

Example structure:

```python
# src/aura/tools/calculator.py
def parse_calculator_intent(llm, user_input: str) -> dict | None:
    """Extract mathematical intent from user input"""
    pass

def execute_calculator_intent(intent: dict) -> str:
    """Execute the calculation"""
    pass
```

---

## 🐛 Troubleshooting

### Browser Not Opening

**Issue**: Browser sometimes opens and sometimes doesn't

**Root Causes** (Fixed in v0.1.1):
- ~~Incorrect JSON schema validation~~ ✅ Fixed
- ~~Missing error handling~~ ✅ Fixed
- ~~Silent failures~~ ✅ Fixed with logging

**Current Solutions**:
1. Check Tavily API key is set (if using web search)
2. Ensure system default browser is configured
3. Check console output for error messages
4. Verify network connectivity for web search
5. Ensure Ollama is running on localhost:11434

### Memory Not Persisting

**Issue**: Memory is lost after restart

**Solutions**:
1. Verify `memory_dir` exists in config
2. Check file permissions on memory directory
3. Ensure database is properly initialized

### Ollama Connection Issues

**Issue**: "Failed to connect to Ollama"

**Solutions**:
1. Verify Ollama is running: `ollama list`
2. Check Ollama is on correct host/port in config (default: localhost:11434)
3. Ensure model is pulled: `ollama pull <model-name>`
4. Restart Ollama service

---

## 📋 Recent Updates (v0.1.1)

### Browser Tool Improvements ✨

- ✅ **Fixed Intent Validation** - Corrected JSON schema from `platform` to `action`
- ✅ **Comprehensive Error Handling** - All exceptions caught and logged
- ✅ **Web Search Integration** - Better error handling for Tavily failures
- ✅ **URL Extraction** - Improved regex-based URL extraction from search results
- ✅ **Logging & Debugging** - Detailed error messages for troubleshooting

### What Was Fixed

1. **Intent Parsing** - Was checking for non-existent `platform` field, now validates `action` field
2. **Execution** - Added try/except blocks with proper error messages
3. **Web Search** - No more silent failures, all errors are logged
4. **Platform Filtering** - Simplified to open first valid URL instead of platform-specific logic

### Platform Support

- ✅ YouTube playback
- ✅ Netflix navigation
- ✅ Spotify music
- ✅ GitHub repository browsing
- ✅ Wikipedia searches
- ✅ Generic website opening

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error logs/console output for detailed messages
3. Verify Ollama is running before reporting issues
4. Open an issue with reproduction steps
