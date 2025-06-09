import os
from dotenv import load_dotenv

load_dotenv()

LIVEKIT_URL = os.getenv('LIVEKIT_URL')
LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
DEEPGRAM_MODEL = os.getenv('DEEPGRAM_MODEL')
DEEPGRAM_LANGUAGE = os.getenv('DEEPGRAM_LANGUAGE')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID')
TARGET_LATENCY = float(os.getenv('TARGET_LATENCY', 2.0))
METRICS_FILE = os.getenv('METRICS_FILE', './metrics/session_metrics.xlsx')
