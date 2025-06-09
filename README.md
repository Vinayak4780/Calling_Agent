# 🤖 AI Calling Agent

A real-time AI-powered calling agent that uses speech-to-text (STT), large language models (LLM), and text-to-speech (TTS) to create natural voice conversations. The system captures comprehensive metrics and logs conversation summaries to Excel for analysis.

## 🎯 Features

- **Real-time Voice Conversation**: Continuous speech interaction with AI agent
- **Multi-Service Integration**: 
  - **Deepgram** for Speech-to-Text (STT)
  - **Groq** for Language Model responses (LLM)
  - **ElevenLabs** for Text-to-Speech (TTS)
  - **LiveKit** for audio handling (with local fallback)
- **Comprehensive Metrics**: Tracks E2E delay, TIFT, TTFB, total latency
- **Excel Logging**: Automatically logs session metrics and conversation summaries
- **Pipeline Architecture**: Modular design for easy maintenance and updates

## 📊 Metrics Captured

| Metric | Description |
|--------|-------------|
| **E2E Delay** | End-to-end response time from user speech to agent audio output |
| **TIFT** | Time in First Transcription (STT processing time) |
| **TTFB** | Time to First Byte (LLM response generation time) |
| **Total Latency** | Combined STT + LLM + TTS processing time |
| **Usage Summary** | Character counts for input/output |
| **Conversation Summary** | Summary of user-agent exchanges |

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- Windows OS (tested on Windows)
- Microphone and speakers/headphones
- API keys for Deepgram, Groq, and ElevenLabs

### 1. Clone and Setup

```bash
# Navigate to your project directory
cd "c:\Users\vinay\OneDrive\Desktop\New folder (2)"

# Create virtual environment
python -m venv myenv

# Activate virtual environment
myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root with your API keys:

```env
# LiveKit Configuration (optional for full LiveKit mode)
LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# Deepgram STT Configuration (REQUIRED)
DEEPGRAM_API_KEY=your_deepgram_api_key
DEEPGRAM_MODEL=nova-2-phonecall
DEEPGRAM_LANGUAGE=en-US

# Groq LLM Configuration (REQUIRED)
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-8b-8192

# ElevenLabs TTS Configuration (REQUIRED)
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id

# Agent Configuration
TARGET_LATENCY=2.0
METRICS_FILE=./metrics/session_metrics.xlsx
```

### 3. Get API Keys

- **Deepgram**: Sign up at [console.deepgram.com](https://console.deepgram.com/)
- **Groq**: Get API key from [console.groq.com](https://console.groq.com/keys)
- **ElevenLabs**: Register at [elevenlabs.io](https://elevenlabs.io/app/settings/api-keys)

## 🚀 Usage

### Quick Start

1. **Test Services**:
   ```bash
   python test_services.py
   ```

2. **Run the AI Agent**:
   ```bash
   python main.py
   ```

3. **Start Conversation**:
   - The agent will start recording automatically
   - Speak into your microphone (5-second recording windows)
   - Listen to the AI response
   - The conversation continues until you press `Ctrl+C`

### Example Conversation Flow

```
🤖 LiveKit AI Calling Agent
==================================================
Initializing services...
✅ All services initialized successfully
Starting Agent Session: a1b2c3d4-e5f6-7890-abcd-ef1234567890

--- Turn 1 ---
🎤 Recording... (5 seconds)
🔄 Transcribing...
👤 User: Hello, how are you today?
🧠 Generating response...
🤖 Agent: Hello! I'm doing great, thank you for asking. How can I help you today?
🔊 Synthesizing speech...
📢 Playing response...

📊 Metrics:
   E2E Delay: 8.45s
   TIFT: 1.23s
   TTFB: 0.87s
   Total Latency: 3.21s
✅ Metrics logged to ./metrics/session_metrics.xlsx
```

## 📁 Project Structure

```
calling-agent/
├── main.py                 # Main entry point
├── pipeline.py             # Agent session and conversation logic
├── utils.py                # Environment variables and configuration
├── metrics.py              # Excel logging functionality
├── test_services.py        # Service testing script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── README.md              # This file
├── services/
│   ├── services_deepgram.py   # Deepgram STT service
│   ├── services_groq.py       # Groq LLM service
│   ├── services_elevenlabs.py # ElevenLabs TTS service
│   └── services_livekit.py    # LiveKit/Audio service
└── metrics/
    └── session_metrics.xlsx   # Generated metrics file
```

## 🔧 Configuration

### Audio Settings

The system uses:
- **Sample Rate**: 16kHz
- **Channels**: Mono (1 channel)
- **Recording Duration**: 5 seconds per turn
- **Format**: WAV, 16-bit PCM

### Model Configuration

- **STT Model**: `nova-2-phonecall` (optimized for phone calls)
- **LLM Model**: `llama3-8b-8192` (fast inference)
- **TTS Model**: `eleven_multilingual_v2` (high quality)

## 📈 Metrics Analysis

The system generates an Excel file (`./metrics/session_metrics.xlsx`) with columns:

| Column | Description |
|--------|-------------|
| SessionID | Unique identifier for each conversation session |
| Timestamp | ISO timestamp of the interaction |
| E2E Delay | Total time from user speech to agent audio (seconds) |
| TIFT | Speech-to-text processing time (seconds) |
| TTFB | LLM response generation time (seconds) |
| Total Latency | Combined processing time (seconds) |
| Usage Summary | Input/output character counts |
| Conversation Summary | Truncated conversation history |

## 🔍 Troubleshooting

### Common Issues

1. **ImportError: No module named 'xxx'**
   ```bash
   # Ensure virtual environment is activated
   myenv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Audio not recording**
   - Check microphone permissions
   - Ensure microphone is not being used by other applications
   - Test with `python test_services.py`

3. **API Errors**
   - Verify API keys in `.env` file
   - Check API quotas and billing
   - Test individual services with `test_services.py`

4. **High Latency**
   - Check internet connection
   - Consider using faster models
   - Monitor API response times in metrics

### Debug Mode

Add debug prints by modifying the service files to include more verbose logging.

## 🚦 Testing

Run the test suite to verify all services:

```bash
python test_services.py
```

Expected output:
```
🧪 Testing AI Services
==================================================

1. Testing Groq LLM...
✅ Groq Response: Hello! I'm doing well, thank you for asking...

2. Testing ElevenLabs TTS...
✅ ElevenLabs generated 49782 bytes of audio

3. Testing Deepgram STT...
✅ Deepgram processed audio (result: '')

🎉 Service tests completed!
```

## 🛡️ Security

- Keep your `.env` file secure and never commit API keys to version control
- Add `.env` to your `.gitignore` file
- Regularly rotate API keys
- Monitor API usage and billing

## 📝 License

This project is for educational and development purposes. Please ensure compliance with the terms of service for all integrated APIs (Deepgram, Groq, ElevenLabs, LiveKit).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes with `python test_services.py`
4. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Run `python test_services.py` to isolate problems
3. Review API documentation for individual services
4. Check the metrics Excel file for performance insights

---

**Built with ❤️ using Python, Deepgram, Groq, and ElevenLabs**
#   C a l l i n g _ A g e n t 
 
 
