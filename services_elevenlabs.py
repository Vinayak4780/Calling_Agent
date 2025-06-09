from elevenlabs import ElevenLabs
from utils import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
import io

class ElevenLabsService:
    def __init__(self):
        self.client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
    def synthesize(self, text):
        try:
            # Generate audio using ElevenLabs text_to_speech
            audio = self.client.text_to_speech.convert(
                voice_id=ELEVENLABS_VOICE_ID,
                text=text,
                model_id="eleven_multilingual_v2"
            )
            
            # Convert generator to bytes
            audio_bytes = b"".join(audio)
            return audio_bytes
        except Exception as e:
            print(f"ElevenLabs synthesis error: {e}")
            return b""
    
    async def synthesize_async(self, text):
        # Async wrapper for synthesis
        return self.synthesize(text)
