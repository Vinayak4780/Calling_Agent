#!/usr/bin/env python3
"""
Simple test script to verify all services are working
"""
import asyncio
import time
from utils import *
from services_deepgram import DeepgramService
from services_groq import GroqService
from services_elevenlabs import ElevenLabsService

async def test_services():
    print("🧪 Testing AI Services")
    print("=" * 50)
    
    # Test Groq LLM
    print("\n1. Testing Groq LLM...")
    try:
        groq = GroqService()
        response = groq.generate_response("Hello, how are you today?")
        print(f"✅ Groq Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ Groq Error: {e}")
    
    # Test ElevenLabs TTS
    print("\n2. Testing ElevenLabs TTS...")
    try:
        elevenlabs = ElevenLabsService()
        audio = elevenlabs.synthesize("Hello, this is a test of the text to speech system.")
        print(f"✅ ElevenLabs generated {len(audio)} bytes of audio")
    except Exception as e:
        print(f"❌ ElevenLabs Error: {e}")
    
    # Test Deepgram STT (with a simple test)
    print("\n3. Testing Deepgram STT...")
    try:
        deepgram = DeepgramService()
        # Create a small test audio file (silence)
        import wave
        import numpy as np
        
        # Generate 1 second of silence as test audio
        sample_rate = 16000
        duration = 1
        audio_data = np.zeros(sample_rate * duration, dtype=np.int16)
        
        # Convert to WAV bytes
        import io
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        buffer.seek(0)
        test_audio = buffer.read()
        
        transcript = await deepgram.transcribe(test_audio)
        print(f"✅ Deepgram processed audio (result: '{transcript}')")
    except Exception as e:
        print(f"❌ Deepgram Error: {e}")
    
    print("\n🎉 Service tests completed!")

if __name__ == "__main__":
    asyncio.run(test_services())
