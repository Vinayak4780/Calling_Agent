import asyncio
import sounddevice as sd
import soundfile as sf
import numpy as np
import io
import wave
from livekit import api, rtc
from utils import LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET

class LiveKitService:
    def __init__(self, url, api_key, api_secret):
        self.url = url
        self.api_key = api_key
        self.api_secret = api_secret
        self.room = None
        self.audio_queue = asyncio.Queue()
        self.is_recording = False
        
    async def connect(self):
        try:
            # For now, we'll use local audio recording instead of LiveKit
            # You can implement full LiveKit integration later
            print("Audio service initialized (using local audio)")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def start_recording(self, duration=5, sample_rate=16000):
        """Record audio from microphone"""
        try:
            print(f"Recording for {duration} seconds...")
            audio_data = sd.rec(int(duration * sample_rate), 
                              samplerate=sample_rate, 
                              channels=1, 
                              dtype='float32')
            sd.wait()  # Wait for recording to complete
            
            # Convert to bytes format for processing
            audio_bytes = self._audio_to_bytes(audio_data, sample_rate)
            return audio_bytes
        except Exception as e:
            print(f"Recording error: {e}")
            return b""
    
    def _audio_to_bytes(self, audio_data, sample_rate):
        """Convert numpy audio data to WAV bytes"""
        try:
            # Normalize audio data
            audio_data = np.clip(audio_data, -1.0, 1.0)
            
            # Convert to 16-bit PCM
            audio_int16 = (audio_data * 32767).astype(np.int16)
            
            # Create WAV file in memory
            buffer = io.BytesIO()
            with wave.open(buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_int16.tobytes())
            
            buffer.seek(0)
            return buffer.read()
        except Exception as e:
            print(f"Audio conversion error: {e}")
            return b""
    
    def play_audio(self, audio_data):
        """Play audio through speakers"""
        try:
            # Convert bytes back to audio data for playback
            if isinstance(audio_data, bytes):
                # Save to temporary file and play
                temp_file = "temp_response.wav"
                with open(temp_file, "wb") as f:
                    f.write(audio_data)
                
                # Play the audio file
                data, fs = sf.read(temp_file)
                sd.play(data, fs)
                sd.wait()  # Wait for playback to complete
                
                # Clean up temporary file
                import os
                os.remove(temp_file)
            else:
                print("Invalid audio data format")
        except Exception as e:
            print(f"Audio playback error: {e}")
    
    def receive_audio(self):
        """Simulate receiving audio - for now, record from microphone"""
        return self.start_recording()
    
    def send_audio(self, audio_data):
        """Simulate sending audio - for now, play through speakers"""
        self.play_audio(audio_data)
    
    async def disconnect(self):
        """Disconnect from the service"""
        print("Audio service disconnected")
