import asyncio
import sys
from utils import *
from services_livekit import LiveKitService
from services_deepgram import DeepgramService
from services_groq import GroqService
from services_elevenlabs import ElevenLabsService
from metrics import init_metrics_file
from pipeline import AgentSession

async def main():
    """Main entry point for the calling agent"""
    print("🤖 LiveKit AI Calling Agent")
    print("=" * 50)
    
    # Initialize metrics file
    init_metrics_file()
    
    # Initialize services
    print("Initializing services...")
    try:
        livekit = LiveKitService(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        deepgram = DeepgramService()
        groq = GroqService()
        elevenlabs = ElevenLabsService()
        print("✅ All services initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing services: {e}")
        return
    
    # Create and run session
    try:
        session = AgentSession(livekit, deepgram, groq, elevenlabs)
        await session.run()
    except KeyboardInterrupt:
        print("\n👋 Session terminated by user")
    except Exception as e:
        print(f"❌ Error running session: {e}")
    
    print("🏁 Agent session completed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
